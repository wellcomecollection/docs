# Incident retro - slow search due to 900k messages on the ingestor queue

**Incident from:** 2022-10-04

**Incident until:** 2022-10-04

**Retro held:** 2022-10-04

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

4 October 2022

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1664871483404409 

~02.00 900k messages on the ingestor queue

09.00 User reported issue with search and posted an internal server error image. Very slow search confirmed by NP.

09.25 AC cluster claims healthy, but I’d guess it’s under sustained load somehow

09.36 AC issue found
the issue is that the works ingestor is hammering the cluster

009:38 AC okay, think I've applied a fix<br>
the basic issue is that there are 900k messages on the ingestor queue<br>
the ingestor is the app that populates the API index<br>
if we send too many writes to Elasticsearch, the cluster will struggle to respond to incoming requests (aka users)<br>
and it's been saturated since ~2am this morning, which is when a Calm ~> Sierra record harvest occurs (this is to allow items catalogued in Calm to be ordered through Sierra)<br>
most of those are a no-up change for us, the only update is the "last synced from Calm" field which we don't expose on the front-end, so we filter out the errors<br>
but this tiny change will have caused everything to get re-sent: https://github.com/wellcomecollection/catalogue-pipeline/pull/2212 <br>
#2212 MeSH, not MESH<br>
If you look at the NLM website, it's a lowercase 'e':

09:42 AC API seems to be back for me

09.44 NP confirmed that search is running fast again


## Analysis of causes
Unexpected load from the overnight Sierra harvest, which in turn caused:<br>
the basic issue is that there are 900k messages on the ingestor queue<br>
the ingestor is the app that populates the API index<br>
if we send too many writes to Elasticsearch, the cluster will struggle to respond to incoming requests (aka users)


## Actions

- If queue crosses e.g 1.5 mill messages, stop the ingestor and send a message to Slack (check SQS metrics to determine the threshold). Discussed but decided not to do.

**Alex**
- Investigate why a label change caused this problem

**Paul**
- Investigate the retention time on the queues when not reindexing
