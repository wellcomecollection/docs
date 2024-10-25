# Catalogue Pipeline services from ECS to Lambda 

## Context

Catalogue-pipeline services run on [Elastic Container Service (ECS)](https://aws.amazon.com/ecs/). The infrastructure includes scaling to account for resource needs during a reindex (scale up) or day-to-day running of the pipeline (scale down). Scaling is achieved using ECS auto scaling rules driven from CloudWatch metrics on queue depth. Other newer projects leverage AWS Lambda to run similar tasks, and there is an opportunity to remove complexity in the catalogue pipeline and align with newer projects.

## Background

The following points cover in more detail the reasoning behind moving from ECS based compute to AWS Lamdba:

- **Reduction in infra complexity by removing ECS auto-scaling logic:**

   Scaling the pipeline up or down is achieved in several ways:
   
   - A manual step is performed to terraform the pipeline into "reindexing_state" by setting a bunch of variables to `true` [here](pipeline/terraform/2024-08-15/main.tf). Search for `reindexing_state` in the catalogue-pipeline repo to find all the 
     ways these variables are used.  
   - Every service also has a high/low message count alarm on its input queue. By [default](pipeline/terraform/modules/stack/variables.tf) services scale up to 12 instances as long as there are messages on the queue, and will scale down when the queue 
     is clear. However some services (eg. ingestors) have specially configured `max_capacity` usually to account for data stores' read/write limits.

   This change aims to remove the need for this scaling logic.

- **Reduction in app complexity by removing akka/pekko batching:**

   Several (SQS driven) pipeline services implement “SQSStream” (see https://github.com/wellcomecollection/scala-libs/blob/main/messaging/src/main/scala/weco/messaging/sqs/SQSStream.scala ) that batches SQS messages so that they can be processed in 
   bulk. This logic lives inside the service and makes it difficult (impossible?) to run locally.  

   This model means the messaging and business/processing logic part of the services are entangled in sometimes confusing ways, and we're losing queue management features of AWS SQS (eg. having to keep track of success and failure to delete or retry 
   messaging accordingly).  
 
   This change is also an opportunity to reassess and possibly refactor out some error handling that may be too particular, over-optimising for performance at the expense of clarity. 

- **Potential reductions in cost:**
 
   ECS services are configured to scale down to 0 when the input is low, which means we are not paying for continously-running tasks, but this results in startinf and stopping tasks repeatedly as messages trickle down the pipeline.  

- **Potential increase in speed (deployment and processing):**

   ECS services take a few minutes to start tasks as the auto-scaling rules rely on reported CloudWatch metrics, whereas Lambda invocations are [much faster](https://docs.aws.amazon.com/lambda/latest/operatorguide/execution-environments.html#cold-start-latency). Using [provisioned concurrency](https://docs.aws.amazon.com/lambda/latest/dg/provisioned-concurrency.html) may further increase processing speed, but is likely not necessary, at least for most services.

  Service deployment at present relies on the ECS deployment APIs which take some time to determine that a service is "stable", there is no such process for AWS Lambda and deployments are almost instant.

- **Align with concepts pipeline deployment:**  

   The concepts-pipeline was designed and built around lambdas. It packages 2 different versions of the aggregator and recorder services, one for each use case for the pipeline: bulk, for complete concepts reindex and SQS, which handles low-volume 
   works updates published to `<live_catalogue_pipeline>_ingestor_works_output` SNS topic. The ingestor service only runs when needed, eg. when we want to refresh the `authoritative-concepts` index.  

   This allows for most efficient use of the infrastructure/resources and avoids one of the oft-cited complexity/downside in the catalogue-pipeline, namely that the application tries to handle two quite different use cases.  

   The different versions of the aggregator and recorder are also configured for their purpose, thus making the infrastructure code easier to read and understand.

## Suggested solution

We could incrementally refactor the catalogue-pipeline services to use lambdas instead of ECS. Some considerations are:

 - We currently build container images to package our code for deployment, we may wish to continue doing so for simplicity. See the documentation around [packaging and deploying container based Java Lambdas](https://docs.aws.amazon.com/lambda/latest/dg/java-image.html) that we would need to use to achieve this.

- Lambda has built-in scaling capabilities which will allow us to simplify the infrastructure by removing scaling configurations and Cloudwatch alarms on the queues. We would still use the `reindexing_state` to adjust data store provisioning. We 
  could also leverage SQS lambda features to protect the data stores (eg. elasticsearch index at the ingestor stage) from overloading by setting a maximum concurrency on the event source.
   
- We can leverage SQS event source and lambda features to batch up to 10000 messages before invoking the function (useful in the context of the batcher service). This will make it possible to remove the batching mechanism that exists inside the 
  services, making it easier to run them locally using a [lambda runtime emulator](https://github.com/aws/aws-lambda-runtime-interface-emulator).

  Error handling could use [Partial batch responses](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html#services-sqs-batchfailurereporting).
  
- Lambda is generally considered to be cost-effective for workloads with intermittent or unpredictable traffic patterns (1ms for 1024MB: $0.0000000167).

- Processing speed could be slowed down by [AWS Lambda cold starts](https://aws.amazon.com/blogs/compute/operating-lambda-performance-optimization-part-1/) but this can be optimised by provisioning concurrency.
  
- The concepts-pipeline has demonstrated the value of using AWS Lambdas in a data pipeline.


### Transition from ECS to Lambda

In terms of transition from ECS to lambdas to prevent downtime and allow a smooth transition:

- Update deployment to allow deployment of existing container images to both ECS & Lambda runtime environments.
- Move services over one at a time, testing that a new Lambda service works by dual-running it alongside its ECS counterpart without publishing messages downstream.
- When satisfied AWS Lambda behaviour for a service has reached parity we can remove the ECS service and infrastructure.

## Potential issues

AWS Lambda has a different execution model than ECS, with SQS messages causing Lambda invocations triggered by an AWS Lambda Trigger (managed invocations) and configuration options to dictate how many messages a Lambda invocation handles, how many Lambdas can run at once, and how long any single Lambda can run for. In ECS, tasks are launched by autoscaling rules, those tasks then poll SQS for messages processing and deleting them as they are received. In ECS when there is no more work to do tasks are terminated based on autoscaling rules.

Potential issues may arise around this change in exectution model, specifically:

### Concurrency

With ECS concurrency can be limited by the number of running tasks which provides a _rough_ restriction on the number of messages processed at once. With AWS Lambda concurrency can be specified exactly with ["reserved concurrency"](https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html), and in combination with [batch size](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html#sqs-polling-behavior) can tightly control the number of messages a Lambda processes.

As we are moving from one model to another, we will need to calibrate concurrency for each service by estimation and experiment. 

Concurrency is of particular concern where we are making network requests to external services that may not be configured to meet demand, for example Elasticsearch or RDS databases.

### Batching

Batching describes the number of messages handed to a Lambda to process in one invocation. For the catalogue pipeline we will be invoking Lambdas from non-FIFO SQS messages, and this has [specific restrictions around batch size](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html). 

Batch size is dictated by a combination of:

- Configured maximum batch size, up to [a maximum of 10,000 for non-FIFO queues](https://repost.aws/knowledge-center/lambda-sqs-scaling)
- Maximum payload size, up to [128kb for asynchronous invocation](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)
- Length of batch window, (how long to wait before passing on a batch), [up to 5 minutes](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html).

Along with concurrency batching dictates how much work is processed at one time. 

A specific concern around batch size: 

> The maximum number of records in each batch that Lambda pulls from your stream or queue and sends to your function. Lambda passes all of the records in the batch to the function in a single call, up to the payload limit for synchronous invocation 
  (6 MB). The maximum batchsize for lambda is 10 000. This is far less than the batch size that the batcher is currently able to process (up to 120000 `collectionPath`). This could mean fewer nodes are being matched in a batch, reducing the 
  beneficial effect of the batcher on the relation_embedder load. As of 2024-10-23 there are 271791 documents with a collectionPath in the merged index, ie. as many messages that the batcher needs to process as part of a full reindex

When deciding on batching configutation, maximum execution time must be considered in order that we do not attempt to process work that exceeds that limit.

While running on ECS batch size was less of a concern as there is no upper execution time, and messages are received by polling SQS for more messages while a task is executing.

### Execution time

AWS Lambda has a [maximum execution time of 15 minute](https://docs.aws.amazon.com/lambda/latest/dg/configuration-timeout.html), which cannot be extended. If a function execution exceeded the maximum execution time it will be terminated.

We must ensure that in the usual case we do not attempt to perform work that will take longer than the maximum execution time in a single invocation. The amount of work a function needs to perform should be tunable by changing batching configuration  to limit the number of messages processed in an invocation. If longer execution time is needed, computation should be split into further distinct steps handled by other Lambdas, or by services using a different paradigm. 

It is very unlikely that a single message in the current implementation should ever take longer than 15 minutes to process.

## Future improvements 

Some suggestions for future improvements that could be looked at as part of this project, more discussion may warrant further RFCs:

- Can we avoid using the router service in future by moving its functionality into another service?
  Could the relation_embedder itself decide which works actually need their relations embedded (ie. works that have a collection path)?

- Can we simplify batcher service processing logic?

- Given that the path_concatenator only processes Sierra record trees, would it be better for this to happen earlier in the pipeline? Could be just after the Sierra transformer business, which removes the need for the router to route the relevant works to have their paths concatenated.  

- If we were to wait at the matcher/merger stage for every work to be processed, could we then do without the batcher? We would be able to scan the store populated by the matcher/merger and send all members of a tree together to have their relations embedded, removing the need for a mechanism that limits the “explosion” we have now that is caused by only sending partial trees to the relation_embedder.  

- Should we look into SNS features that allows conditional subscription based on the message body as a replacement for the router?

- Can we consider replacing intermediate indices with S3? We don’t search them; they are acting as a simple JSON stores. 
