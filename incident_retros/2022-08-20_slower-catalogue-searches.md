# Incident retro -  requests not showing in account

**Incident from:** 2022-08-02

**Incident until:** 2022-08-02

**Retro held:** 2022-08-04

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

1 August 2022

[Identifying the unidentified #2149](https://github.com/wellcomecollection/catalogue-pipeline/pull/2149) merged

2 August 2022

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1659430616459229 

c. 2.00 Increase in requests to ES cluster

c. 7.00 Further increase in latency

9.56 JP catalogue API latency is currently averaging >1.5s, p95 is about 10s
imo this is a degradation of service sufficient to be an incident
the cluster is having a bad time from a huuuuge load of requests
I’m going to bump the cluster size temporarily to give it more CPU credits
Then I will investigate where those requests came from and what we should do about it
(I don’t think those came via the catalogue API)

9.58 JP this started at about 2am and got quite a lot worse at about 7

9.59 NP message to users sent out

10.05 AC doubled the Elastic cluster size
Latency got worse

10.13 NP update to users sent out re identifying cause as high number of searches

AC turned off relation embedder

c. 10.30 latency improved due to relation embedder turned off and increase in Elastic cluster size 

12.24 AC looks like the incident has indeed resolved, but now we're not getting any pipeline updates


## Analysis of causes

Increase in requests to ES cluster, caused by…

Overnight updates from Sierra.
https://github.com/wellcomecollection/catalogue-pipeline/pull/2149
Meant all Sierra documents harvested from CALM were now different, so had to go through the whole pipeline (c 900,000).

This created a need for a proper reindex but the cluster was underpowered, and the batching behaviour impacted it.

If a change to the transformer will change the documents from CALM we need to reindex before an overnight harvest from CALM to Sierra

Turn down transformers

Change batching behaviour if this happens a few more times


## Actions

**Alex & Paul**
- Transformers: if more than e.g.10k messages on the queue, turn off the transformer and alert about it
- Tidy Slack alert for more focussed information, and have it post to #wc-search, not #wc-platform
