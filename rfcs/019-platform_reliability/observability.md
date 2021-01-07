# Observability

## Logging

In order that application issues are quickly found and diagnosed logs should be easily searchable & discoverable. We should accumulate logs in a single service, with a consistent format.

We should:

* Send all logs to the `logging.wellcomecollection.org` ELK \(Elasticsearch, Logstash, Kibana\) stack.
* Log in a consistent format to make the timestamp, originating service and environment easily searchable.
* Remove all CloudWatch logging.

## Tracing

In order that application issues are quickly found and diagnosed we should be able to follow work occurring across multiple services.

We should:

* Implement a tracing solution in our piplelines that allow us to visualise the flow of work through our services.

## Metrics

In order that application issues are quickly found and diagnosed we should be able to view metrics from our applications easily.

We should:

* Decide on appropriate metric collectors for each of our products.
* Decide on appropriate platforms for visualising application metrics across our products.

## Alerting

In order that we can quickly react to application issues we should be notified when issues requiring our attention arise.

We should:

* Be able to track out response to alerts and actions taken to resolve them.
* Decide on what constitutes a critical issue \(i.e. one that requires immediate action\) and provide a separate channel to deliver critical alerts.

