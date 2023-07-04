# Incident retro - Images search down

**Incident from:** 2023-06-26

**Incident until:** 2023-06-26

**Retro held:** 2023-06-27

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

See [https://wellcome.slack.com/archives/C01FBFSDLUA/p1686565392141259](https://wellcome.slack.com/archives/C01FBFSDLUA/p1687798519681599 ) 

26 June 2023

17.07 AG mmmh there doesn't seem to be much in the indexes I'm going to scale down for the night and look at it tomorrow

>> Incident actually starts here, when AG runs terraform to scale down the services tasked with ingesting and indexing the catalogue into the newly created pipeline-2023-06-26 (so as not to pay for the extra resources overnight since full reindex would only be run 27 june)

However, running the command without targeting the specific pipeline-2023-06-26 applied some config to the live pipeline-2023-06-09 that was only intended for the pipeline-2023-06-26, rendering the index basically “unqueryable”

AG [colour vectors] Perform reindex (actually catalogue-pipeline) [#664](https://github.com/wellcomecollection/catalogue-api/issues/664)

17.23 Updown down alerts for 
API: Images: Image

See https://wellcome.slack.com/archives/CQ720BG02/p1687796574334019
Realising the index mapping is wrong for pipeline-2023-06-09 AG runs terraform cmd to put it back the way it should be

17.55 AG Image search is down at the moment because of some tangle I got myself into

17.57 JP OK - it looks like (guessing) when Terraform is asked to do a non-additive mapping change it destroys and recreates the index<br>
As a GET images-indexed-2023-06-09/_count is giving me 39 images<br>
Obviously that’s not ideal<br>
However I think the number in images-augmented looks correct

18.05 JP ran the reingest for display script that only ingested the 39 documents that were in the API index.

18.09 JP started ingesting all the documents from the previous stage of the images pipeline

18.39 Up
API: Images: Image

19.25 Up
Experience: Works: Images (origin)
Experience: Works: Images (cached)

20.30 reingestion completed


## Analysis of causes
- (PB) When I wrote the new way of creating indices, I didn’t sufficiently poka-yoke [mistake-proof] it. There wasn’t a safeguard against destroy-and-replace on existing indices.
- (PB) pipeline/terraform/modules/pipeline_indices/main.tf has the config dates in it.
- Terraform plan output is too long to be comprehensible


## Actions

**Paul**
- pipeline/terraform/modules/pipeline_indices/main.tf config dates are hard coded but should be a variable
- Investigate prevent destroy for the indexes

**Alex/Jamie**
- RFC for having separate stacks per pipeline [#2393](https://github.com/wellcomecollection/catalogue-pipeline/issues/2393)
