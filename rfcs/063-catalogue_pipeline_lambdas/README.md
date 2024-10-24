# Catalogue Pipeline services from ECS to Lambda 

## Context

Catalogue-pipeline services run on ECS. The infrastructure includes scaling to account for resource needs during a reindex (scale up) or day-to-day running of the pipeline (scale down). Scaling is achieved using ECS auto scaling rules driven from CloudWatch metrics on queue depth.  

ECS services 

---

## Background

Why we want to make the change

1. Reduction in infra complexity by chucking scaling

Scaling the pipeline up or down is achieved in several ways:  
-> a manual step is performed to terraform the pipeline into "reindexing_state" by setting a bunch of variables to `true` [here](pipeline/terraform/2024-08-15/main.tf). Search for `reindexing_state` in the catalogue-pipeline repo to find all the ways these variables are used.  
-> every service also has a high/low message count alarm on its input queue. By [default](pipeline/terraform/modules/stack/variables.tf) services scale up to 12 instances as long as there are messages on the queue, and will scale down when the queue is clear. However some services (eg. ingestors) have specially configured `max_capacity` usually to account for data stores' read/write limits.

2. Reduction in app complexity by chucking akka/pekko batching

Several (SQS driven) pipeline services implement “SQSStream” (see https://github.com/wellcomecollection/scala-libs/blob/main/messaging/src/main/scala/weco/messaging/sqs/SQSStream.scala ) that batches SQS messages so that they can be processed in bulk. This logic lives inside the service and makes it difficult (impossible?) to run locally.  
This model means the messaging and business/processing logic part of the services are entangled in sometimes confusing ways, and we're losing queue management features of AWS SQS (eg. having to keep track of success and failure to delete or retry messaging accordingly).  
This change is also an opportunity to reassess and possibly refactor out some error handling that may be too particular, over-optimising for performance at the expense of clarity. 

3. Potential reductions in cost 
 
It is worth noting that the ECSs are configured to scale down to 0 (effectively shutting down) when the input is low, which means we are not, in fact, paying for continously-running tasks. One the other hand, this often means starting a task and stopping it repeatedly as messages trickle down the pipeline.  
Costs for 2023-10-01 to 2024-09-30:  
EC2 instances: $3,266.79  
EC2 - Other: $6,639.06

4. Potential increase in speed (deployment and processing)

Given that our services shut down when not in use, lambda would probably provide faster processing. Even accounting for cold starts lambda would be ready to process requests much faster than a EC2 service can. Using provisioned concurrency would further increase processing speed, but is likely not necessary, at least for most services. 

5. Align with concepts pipeline deployment  

The concepts-pipeline was designed and built around lambdas.  
It packages 2 different versions of the aggregator and recorder services, one for each use case for the pipeline: bulk, for complete concepts reindex and SQS, which handles low-volume works updates published to `<live_catalogue_pipeline>_ingestor_works_output` SNS topic. The ingestor service only runs when needed, eg. when we want to refresh the `authoritative-concepts` index.  
This allows for most efficient use of the infrastructure/resources and avoids one of the oft-cited complexity/downside in the catalogue-pipeline, namely that the application tries to handle two quite different use cases.  
The different versions of the aggregator and recorder are also configured for their purpose, thus making the infrastructure code easier to read and understand.



## Suggested solution

Incrementally refactor the catalogue-pipeline services to use lambdas instead of ECS.
1. Lambda has built-in scaling capabilities which will allow us to simplify the infrastructure by removing scaling configurations and Cloudwatch alarms on the queues. We would still use the `reindexing_state` to adjust data store provisioning. We could also leverage SQS lambda features to protect the data stores (eg. elasticsearch index at the ingestor stage) from overloading by setting a maximum concurrency on the event source. 
2. Leverage SQS event source and lambda features to batch up to 10000 messages before invoking the function (useful in the context of the batcher service). This will make it possible to remove the batching mechanism that exists inside the services, making it easier to run them locally using a [lambda runtime emulator](https://github.com/aws/aws-lambda-runtime-interface-emulator). Error handling could use [Partial batch responses](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html#services-sqs-batchfailurereporting) 
3. Lambda is generally considered to be cost-effective for workloads with intermittent or unpredictable traffic patterns.  
1ms for a 1024MB: $0.0000000167
4. Processing speed would be somewhat slowed down by lambda cold starts but this can be optimised by provisioning concurrency. 
4. The concepts-pipeline as demonstrated the value of using lambdas in a data pipeline

In terms of transition from ECS to lambdas, we would update the deployments to deploy both ECS and lambda

## Potential issues

BatchSize: The maximum number of records in each batch that Lambda pulls from your stream or queue and sends to your function. Lambda passes all of the records in the batch to the function in a single call, up to the payload limit for synchronous invocation (6 MB). The maximum batchsize for lambda is 10 000. This is far less than the batch size that the batcher is currently able to process (up to 120000 `collectionPath`). This could mean fewer nodes are being matched in a batch, reducing the beneficial effect of the batcher on the relation_embedder load. 

As of 2024-10-23 there are 271791 documents with a collectionPath in the merged index, ie. as many messages that the batcher needs to process as part of a full reindex

## Future improvements 

Is the router even needed?  

Could the relation_embedder itself decide which works actually need their relations embedded (ie. works that have a collection path) 

Given that the path_concatenator only processes Sierra record trees, would it be better for this to happen earlier in the pipeline? Could be just after the Sierra transformer business, which removes the need for the router to route the relevant works to have their paths concatenated.  

If we were to wait at the matcher/merger stage for every work to be processed, could we then do without the batcher? We would be able to scan the store populated by the matcher/merger and send all members of a tree together to have their relations embedded, removing the need for a mechanism that limits the “explosion” we have now that is caused by only sending partial trees to the relation_embedder.  

Look into SNS feature that allows conditional subscription based on the message body as a replacement for the router. 

Consider replacing intermediate indices with S3.  We don’t search them; they are acting as a simple JSON stores. 