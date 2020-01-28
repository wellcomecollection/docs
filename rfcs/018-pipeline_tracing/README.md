## Pipeline Tracing

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