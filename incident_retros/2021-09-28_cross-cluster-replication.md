# Incident retro - search not available

**Incident from:** 2021-09-28

**Incident until:** 2021-09-28

**Retro held:** 2021-09-28

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

28 September 2021

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1632815554058100 

08.33 AC (in #wc-platform): I’ve set up CCR between the clusters, waiting for that to happen
[Started via Kibana, not a script.]

08.52 
Updown alerts:
Works API Search
Works API Single Work
 
AC: Okay, so it looks like the catalogue-api cluster is unhappy
Presumably because we’ve just tried to set up CCR for four new indices
Works search will be broken [Broken search not seen during this by NP]
Only one of the three nodes is borked, so try again and you’ll likely hit one of the other nodes
 
08.53
Recovery:
Works API Search
Works API Single Work
 
AC: I think Updown hit a node that’s up
 
08.56 AC: I’ve just deleted six indexes from July which we’re no longer using, to alleviate pressure on the cluster
 
08.59 AC: I think we have to wait for the cross-cluster replication of the new images index to complete
 
09.04 AC: My best guess is that trying to configure CCR for the new indexes used too much memory and starting knocking nodes over
Last I checked, three of the four indexes had completed their initial replication
 
09.07 JG: We’ve lost our master node, meaning we might have lost data, do we have a plan to get it back up?
Have we paused CCR?
AC couldn’t get into Kibana to check fourth index
JG: Elasticsearch is down
 
09.08 JG: Biggy is getting elasticsearch up and running again.
AC: I’ve already deleted a handful of old indexes we aren’t using
 
09.09 AC: To my eye it looks like we’re bouncing
I see an instance with high JVM memory pressure, then I reload and it’s gone, then I reload and it’s back to high pressure, [followed by normal pressure]
 
09.10 JG suggest to kill a CCR
AC: possible but can’t get into that part of Kibana. Can get into dev tools but CCR UI is in Stack management and don’t know how to use CCR API
 
09.13 AC deleting a few more unwanted indices
Unable to issue index management commands through dev tools presumably because there’s no master
 
09.14 Updown alert
Front End Works Search (Origin)
 
09.15 Recovery
Front End Works Search (Origin)

09.16 Got master back [intermittently]
 
09.17 JG couldn’t disable [Elasticsearch] snapshots as all APIs are down
AC lost master node again

09.18 Updown alert
Images API Search
 
AC/JG discussing:
- Restart ES and ElasticCloud - might be risky
- Spin up another catalogue-api cluster to start serving requests
 
09.20 Agreed to temporarily increase memory on the cluster -> would restart it and trigger a rolling restart which gives more headroom
 
09.21 Couldn’t restart by applying Elasticsearch change; chose to not report to Elastic support
 
09.25 AC: so I have another idea for a short-term fix
and possibly a long-term fix
the snapshot generator already bypasses the API cluster and reads from the relevant pipeline cluster
What if we configure the API to do the same, and bypass the unhealthy cluster?
(I am cheating here by suggesting the code solution I think we want long-term)
But we can deploy a new API as fast as Buildkite will let us
 
09.25 AC I’ve managed to get into the CCR console and unfollow the images-indexed-2021-09-27 index
Which is the one index that hadn’t completed initial replication
 
09.28 Looked like it was working again but AC reported master unhealthy
 
09.29 Recovery
Images API Search

AC: I’m unfollowing all the 2021-09-27 indexes
JG: I’d like to talk about it being the long term solution, but for now it solves the short term one.
Assuming what we need to do is update the secrets and flip the services?
JG tried rolling restart

09.30 AC: we are only doing CCR for the indexes we’re currently serving as prod
that blocks us from deploying anything new

09.34 JG: I have set the [Elasticsearch] snapshots to not run till saturday while we debug this (note to set it back)

I think the restart might have done it [recovery] but we are now in hypothetical land.

09.38 AC we’re receiving updates to prod indices
And I don’t think we can roll forward to newer indices [because it might replicate the problem]

## Analysis of causes

Set up CCR for four new indices. These are larger as they now include TEI.

Poor understanding of ES search and characteristics, including CCR specifically

## Actions

**AC/AFC**
- Change how the API behaves, spin up a new cluster, and do the CCR into the new cluster
- Make a small change to the API to tell it to read from the new cluster dynamically

**JG**
- Plan for getting better profiling for ES to find where the bottlenecks are to take to product
