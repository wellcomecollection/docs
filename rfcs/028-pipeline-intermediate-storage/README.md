# RFC 027: Pipeline Intermediate Storage

## Background

Whilst on the whole we aim to make to make the inner workings of pipeline as stateless as possible (receiving transformable input at the source and writing works to an index at the sink), there are a number of places where the business logic requires us to store work data in an intermediate state. Namely the matcher and merger require the ability to lookup unmerged works by ID from the `recorder` store, and the upcoming enricher requires an additional intermediate store of merged works in order to perform denormalisation consistently.

The current storage uses VHS (versioned hybrid store), a custom storage solution using a DynamoDB table that links IDs into locations in an S3 bucket where the works in question are actually stored (the reason for not storing works directly in DynamoDB is that not all our works fit within the 400KB storage limits for items).

Although not really a data store from the point of the view of our application, another place we use S3 is with our `big_messaging` module to get round the 256KB limit on the size of SQS messages. Here we write the payload of the message to S3 if it exceeds the maximum size, defaulting to including the payload within the message otherwise.

## Problem

There are a number of issues with the usage of VHS as intermediate storage:

* Perhaps most importantly, the current solution of using DynamoDB and S3 is very costly, and it is likely other methods will work out much cheaper.

* There is very little visibility into the intermediate stored data, and it is a pain to have to look up the DynamoDB ID followed by an S3 location to see a single item.

* Clean up of S3 buckets is not always performed, with stray data often persisting after tearing down a particular pipeline (not necessarily a problem with VHS itself, but worth bearing in mind for future solutions).

* There will be a performance penalty to making two sequential read or write requests to DynamoDB and S3 which other stores will not suffer from. Other databases will also make use of a cache to improve read performance, whilst the DynamoDB component of VHS will not be able to cache the data itself.

* Although the VHS is used throughout our code and has proven very reliable, it still feels like a workaround to the limitations of DynamoDB which would not be present in other stores.

There has already been some discussion about usage of a different store to VHS, and due to the work on the enricher requiring a new intermediate store we have an opportunity to try out an alternative. If we can improve on these issues above, in the future we could potentially backport this to other parts of the pipeline.

## Requirements for Intermediate Store

Taking into account the business logic of our services, and given the issues with the current VHS highlighted in [Problem](#problem), there are a number of requirements and desirable features for any alternative store:

1. The ability to insert items into the store with some unique string ID and some specific integer version (set externally to the pipeline from our adapters), with a method to only store data when the version given is greater or equal to what is currently in the store.

2. The ability to retrieve data from the store, where the latest data is always retrieved and the version is returned with the data.

3. Happily stores data in our current range of around 8GB, and scaling beyond this for future proofing. Also has per item limit beyond the 400KB of DynamoDB.

4. Some form of disk persistence so that we do not need to perform a reindex from scratch in the case of the database going down.

5. Cheaper overall cost than currently, including read / write requests, associated networks costs, and storage costs.

6. Ideally improved performance.

7. Ideally better visibility into the data.

## Store Options

There are a number of different options to use as an intermediate store that I have considered, outlined below.

### Elasticsearch

Pros:

* Used elsewhere in the pipeline so general familiarity with it.

* Kibana would provide a level of visibility into the output at different stages unlike anything else available, and the ability to perform complex queries on our data would likely be an asset to debugging.

* Can access via AWS network address to reduce NAT gateway costs (see [here](https://www.elastic.co/guide/en/cloud/current/ec-getting-started-private.html)).

* Back of the envelope calculations show likely to be much cheaper than current solution.

* Horizontal scalability means quite capable of supporting data at sizes much beyond what we have now.

Cons:

* Requires use of external cloud platform or maintenance of our own Elasticsearch cluster, rather than being a service within AWS.

* Terraform does not control the creation and removal of Elasticsearch indices so might require manual clean up after removing a pipeline.

* No transactions which might prove useful for certain use cases.

Questions:

* Elasticsearch supports [versioning](https://www.elastic.co/blog/elasticsearch-versioning-support), including the ability to index with our own external version numbers. However when using external versioning it only indexes data when the version number is greater than currently stored, whereas our business logic currently expects updates to be processed when versions are greater or equal. Some thought will need to be given whether this might work for us, and if not we would need to implement our own system on top of the Elasticsearch APIs (which may not be particularly resilient to race conditions due to lack of transactions). EDIT: it turns out there is a [external_gte](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html#index-version-types) version type which would be suitable.

* Eventual consistency is probably sufficient for our purposes, but may need some investigation. The [refresh interval](#https://www.elastic.co/guide/en/elasticsearch/reference/current/tune-for-indexing-speed.html#_unset_or_increase_the_refresh_interval) where written data is made available is 1 second by default, which should be enough that downstream services see the latest data, but it might be worth being more aggressive than this.

### Redis

Pros:

* In memory so likely to be fastest reads / writes out of all the options.

* AWS offers it via ElastiCache.

* Improved visibility over VHS.

Cons:

* Requires an instance with enough memory to store all the data, so whilst certainly possible with our current sizes of data the point at which it becomes infeasible will be reached much quicker than other solutions.

* No inbuilt versioning so would have to implement something manually within our applications.

* Visibility nothing like Kibana, and not particularly queryable.

Questions:

* Redis offers some persistence, either via regular snapshots or by logging individual create / update / delete operations to disk with the ability to reconstruct the store via playback. Would need further investigation.

* Pricing is unknown, likely would need some pretty large reserved EC2 instances but expect it to be cheaper than DynamoDB / S3 combination.

### AWS RDS / PostgreSQL

Pros:

* The most reliable and predictable option due to being the only solution which is completely ACID compliant.

* Can support our versioning needs (this could be achieved e.g. within our application logic using transactions, or within a more complex single query using clauses).

* Available as a service on AWS.

* Improved visibility over VHS, and ability to query data.

* Replicas can help with scalability when large number of reads.

* Transaction support might be useful for some of our current logic or future use cases.

Cons:

* Performance may not match other options due to stronger consistency guarantees (though likely to be much better than VHS due to only hitting a single system and making use of a cache).

* Writing raw SQL is not fun, and I have not really been satisfied with any of the Scala wrappers I have tried.

* Visibility nothing like Kibana (there are some web interfaces available which attempt to do similar things, but would require more manual setup and maybe not as polished).

Questions:

* Costs?

* Will not scale as well to mega large data sets: probably not an issue with the sizes of data we are likely to deal with, but worth considering.

## Implementation

Orthogonal to the choice of store, the way we write data into the store for usage later in the pipeline has two main possibilities.

### Service

The current `recorder` service is a wrapper round VHS which stores items received at its input, emitting a message contained the ID of the stored item for downstream pipeline stages to use themselves for access in future.

 We could mirror this design using a different store to VHS for upcoming intermediate storage needs. As the behaviour would be essentially the same regardless of what state the works were in (unmerged, merged, enriched etc) the exact same service can be inserted in different parts of the pipeline differing only in configuration of what store the service has access to.

### Module

An alternative to using a separate service would be to have the services performing the data transformation writing to the store directly themselves, such as through a common module (`scala-storage` may already serve this purpose sufficiently). This would clearly result in less infrastructure, and so would reduce costs and possibly maintenance burden.

The main issue with this approach is that there is potentially less delineation of concerns, with stages of the pipeline performing work additional to solely data transformation. Any failures during the storage would result in the whole incoming message being marked as a failure, with any previous work on transforming the data having to be redone. Having a separate service solely for storage thus means the point of failure for a particular message making its way through the pipeline is more granular.

However, it is worth mentioning that the waters are muddied somewhat due to the fact that the ability to receive whole works as input to some service requires the use of `big_messaging`. In the case of works over 256KB these works will be stored twice, once in S3 and subsequently in the intermediate store itself. Beyond just reducing costs related to this repeated storage, it may make the whole architecture more easily understandable and improve visibility if we just used intermediate stores and the passing of keys between services, rather than requiring both systems.
