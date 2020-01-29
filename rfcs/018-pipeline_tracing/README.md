## Pipeline Tracing

**Status:** :building_construction: Draft :construction:

**Last updated:** 2020/01/28

### Overview / background

When things go wrong in the pipeline, debugging them involves a confusing and slow mix of checking DLQs and reading through the logs of several separate services in order to figure out what went wrong, for which documents, and where. This slows down development across the catalogue and makes it harder to catch bugs.

As well as more comprehensive, structured logging in the constituent services of the pipeline, it would be beneficial to track the flow of data through it, from the adapters right through to ingest.

### Proposed solution

The [OpenTracing](https://opentracing.io/) project defines a common API and methodology for distributed tracing: tracing requests through multiple services whilst propagating and accumulating context throughout, enabling profiling and monitoring of the whole application.

Whilst tracing is typically used in a request/response context where traces/spans stack hierarchically, it can also be used for monitoring unidirectional data flow: ie, for a pipeline.

Even with no further tracing within a service, a top-level trace can tell us which data is in which service, and when. This would be a great starting point for knowing where to focus debugging efforts.

We currently use Elastic APM for performance monitoring of the catalogue API, and it contains an [OpenTracing compatibility layer](https://www.elastic.co/guide/en/apm/agent/java/current/opentracing-bridge.html). Using this, rather than the unwrapped Elastic APM public API, means the tracing can be augmented or swapped out as we wish.

An example of a distributed trace in Elastic APM:

![a distributed trace in elastic APM](https://user-images.githubusercontent.com/4429247/73259713-44adf980-41c0-11ea-8ddb-1e1c4e5ff631.png)

### Implementation details

[This example](https://github.com/bvader/pipelineapmexample) is a useful reference, 

- Tracing context to be propagated in SNS/SQS messages in their `attributes`.  `maxMessageSize` in `big_messaging` may need to be slightly decreased in order to account for the size overhead of this.
- Spans to be opened on message receipt, mapped onto the Akka `Source`, and to be closed either on error or on message ACK, at the `Sink`. 
- Spans to be annotated with the source identifiers and (post-minter) the minted identifiers.
- At this stage, no further tracing to be implemented within services, and auto-instrumentation + transaction "activation" to be disabled due to the multithreading problems that we know these can cause.

### Potential drawbacks

There are few-to-no drawbacks to adding tracing to the pipeline. However, the lack of auto-instrumentation provided by Elastic APM for our specific stack will make adding further tracing (ie, outside the scope of this RFC) more arduous than it would be if we were using Spring/Java, for example. This is partially addressed in the following section.

### Alternatives

There are a handful of Scala-specific tracing tools which could potentially be easier to integrate and provide better auto-instrumentation than Elastic APM: for example, [Kamon](kamon.io), [Zipkin](https://zipkin.io/) (including [akka-tracing](https://github.com/levkhomich/akka-tracing)), and [Lightbend Telemetry](https://developer.lightbend.com/docs/telemetry/current/home.html).
However, most of these are (a) paid and (b) even where they can send data to Elasticsearch, they don't work with Elastic APM, which we get for free and are already using with the catalogue API.

If, when we come to add more detailed tracing, we encounter more problems of the sort we dealt with [here](https://github.com/wellcometrust/catalogue/pull/307), we may wish to bring in one of these libraries. Hopefully, due to the aforementioned use of the OpenTracing standard, we could do this without having to rip out Elastic APM tracing.
