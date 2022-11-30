# RFC 053: Logging in Lambdas

In [RFC 022](https://github.com/wellcomecollection/docs/tree/main/rfcs/022-logging), we identified that our application logs - which were then stored in Cloudwatch - were costing us money, were hard to query, and were inconsistent. We proposed (and went on to implement) an architecture in which ECS services contained a logging sidecar container that used Fluent Bit to stream logs directly to an Elasticsearch cluster. This continues to serve us well.

However, we've now got a non-trivial number of production applications that are run as AWS Lambdas, rather than as Docker containers in ECS: namely, the [Identity APIs](https://github.com/wellcomecollection/identity) and the [concepts pipeline services](https://github.com/wellcomecollection/concepts-pipeline). To have better visibility over these applications, as well as for consistency, we now want to get our Lambda logs into the logging cluster in the same format as we have our other application logs.

## Two possible approaches

We want a flexible approach that doesn't require extra application configuration: it should be language-agnostic and it should capture stdout/stderr rather than providing an API for logs. We should be able to have the same schema for logs as we do for our ECS applications.

**1. Streaming from Cloudwatch**

This is the simplest approach: we would still use Cloudfront, but we wouldn't retain the logs and we would instead use a Lambda to stream them to Elasticsearch. This approach has been used successfully elsewhere: for example [at the BBC](https://medium.com/bbc-product-technology/lambda-logs-in-elk-e4d924757249).

Furthermore, Elastic provide a CloudFormation template for a ["serverless forwarder"](https://github.com/elastic/elastic-serverless-forwarder/blob/main/docs/README-AWS.md) to do this job for us. If this proves insufficient, we can implement our own transformer/streamer quite easily.

We would need to provide a Terraform module (as we do with the existing ECS logging solution) to ensure that a subscription is created automagically for each application. 

Optionally, we might choose to send the logs via a Kinesis stream which could be processed by a Lambda (rather than direct to a Lambda). While this introduces complexity and cost, it offers resilience in case of Elasticsearch downtime, Lambda issues or connection failures, and also makes [cross-account streaming](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CrossAccountSubscriptions-Kinesis.html) quite straightforward. Lambda invocations would also operate on batches of log lines.

We would need to pay for:

- CloudWatch ingest ($0.57/GB)
- Lambda invocation (duration assumed trivial, $0.20/million log lines)
- Kinesis (optional): ($0.04/hr + \$0.12/GB)
- Network egress (approximately constant)

![architecture for streaming from cloudwatch](https://user-images.githubusercontent.com/4429247/203840497-cb313e4e-7fb1-4b0e-bf01-e8c81dd6c432.png)

**2. Lambda extensions**

[Lambda extensions](https://docs.aws.amazon.com/lambda/latest/dg/runtimes-extensions-api.html) allow code to be integrated into the Lambda execution environment, hooking into the Lambda lifecycle and allowing access to logs and other telemetry. Streaming logs elsewhere is exactly their intended use case - there are already [3rd party extensions](https://docs.datadoghq.com/serverless/libraries_integrations/extension/) for doing this (unfortunately, not for Elasticsearch).

If we built our own Lambda extension, we would expose a Terraform module for provisioning Lambdas that included the extension and necessary config, IAM roles etc etc. We could write it in a language of our choice and use it with any native (ie non-Docker lambda). 

It could potentially use fluent bit for streaming the logs, instead of implementing that manually, although it looks like [others](https://github.com/aws-samples/aws-lambda-extensions/pull/42) have struggled with losing logs for short-lived invocations (probably due to buffering, and possibly resolveable with use of Lambda lifecycle hooks).

**There is a caveat with this option** - it doesn't work transparently for containerised (ie non-native) Lambdas. Instead, the packaged extension has to be [added to the container image](https://docs.aws.amazon.com/lambda/latest/dg/extensions-configuration.html). 

We use containerised Lambdas in the concepts pipeline: we would either have to switch to using native Java  runtimes, or provide our own base images which include the extension code.

There would be no additional cost associated with using a Lambda extension, other than the necessary network egress.

![Native lambda extensions architecture](https://user-images.githubusercontent.com/4429247/203977301-cb6c2cdb-685e-4b62-9ef1-5396fc349b12.png)

## A pragmatic path forward

*Option (1) does not preclude option (2) as further work*: we would already be providing a Terraform module for consumers, and if the Elastic Serverless Forwarder proved insufficient, we would already have written a module to stream the correct format of logs to Elasticsearch. 

This fact clarifies that option (1) - streaming of logs from CloudWatch - is the better starting point. If it proves insufficient or impractical, the work we will have done already will mostly still be useful for option (2).

The work plan might look something like this:

- Provision an Elastic serverless forwarder
- Create a log group subscription and verify that the forwarder works
- Create a Terraform module for Lambdas with log groups that subscribe to the forwarder
- Roll this out across our Lambdas - if we don't use a cross-account Kinesis stream, we'll want to have a log-streaming Lambda per account, like we have with Slack alerts.

## Caveats and questions

- We've seen CloudWatch logs for Lambdas go missing before - is this a risk? We believe this might be due to (mis)configuration of log retention periods and/or IAM permissions, but we're not sure. Using a consistent Terraform module across our Lambdas will hopefully resolve these issues.
- Should we use Kinesis or not? Some reasons for using it are given above: I think it would be a good idea.
- What index should Lambda logs go into? The ECS logs go into `firelens-<yyyy.mm.dd>` indices - we probably shouldn't do the same for these, as they aren't using firelens and may have a different schema. On the other hand, we would like all of our logs to fall under the same index pattern.
