# Reliability

In order that we can be confident that what we deploy will behave as we expect we should look at:

## Pipeline reliability

In order to verify that pipeline deployments will behave and are behaving as expected we should:

* Test pipeline changes that require re-indexes before new indexes are promoted into production view.
* Test the pipeline is performing as expected when updates flow through it.

### Pipeline reindexing

In order that we can quickly test the behaviour of the catalogue pipeline, we should:

* Reduce reindex costs
* Reduce reindex time
* Couple reindexes with pipeline deployments \(specifically model changes\).  

## Front-end reliability

In order to prevent regressions and errors in production we should:

* Provide acceptance tests that run before release to production.
* Provide component tests for individual UI components.

