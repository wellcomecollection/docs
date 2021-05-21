# Incident retro - ingestors 

**Incident from:** 2021-05-20

**Incident till:** 2021-05-20

**Retro held:** 2021-05-21

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

20 May 2021

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1621515479023400 

Morning: bulk update of licences for 100,000 MIRO works

13.41 DOWN alerts for
Works API Search

13.41 AC anybody mind if I tear down the 2021-05-05 pipeline?
13.42 AC it’ll be getting all these Miro updates 
RK posted [screenshot](https://wellcome.slack.com/archives/C3TQSF63C/p1621514765052000?thread_ts=1621514558.051400&cid=C3TQSF63C) of CPU usage, search response times, index response times
FWIW, I think the alerts are a bit jumpy (whenever I actually try and look at the API it’s fine)

13.43 Recovery:
Works API search

Down:
Front End Works Search (Origin)
Images API Search

Then these alerts up and down:
Works API search
Front End Works Search (Origin)
Images API Search
Front End Works Search (Cached)
Images API Single Image [degraded, not down]

13.57 AC Debugging the API yo-yoing in here
13:58 We are sending moderate ingestor traffic at the API, but not loads
13:59 We’re capped at 3 image ingestors and 3 work ingestors a piece
Precisely to stop this sort of thing when we’re not in the middle of a reindex
I’ve just trimmed the unused API indexes, which usually reduces the load a bit

14.00 AC/RK advised on message to send out; NP sent message

14.01 AC temporarily clamped the number of work ingestors at 1

14.08 AC: no, it seems to have scaled back up again
dang it, I reapplied the terraform
I’m tearing down the 2021-05-05 cluster, and it didn’t clean up the first time
14:09 reclamping at 1 ingestor
14:09 :crossed_fingers: the old pipeline goes away

14.11 AC I will turn ingestor-images down, yes
14:12 The heavy volume of image indexing is probably the issue here

14.14 AC Quick recap: I’ve triggered a reindex of ~100k Miro images as I update their licenses.
RK posted [screenshot of ingestions](https://wellcome.slack.com/archives/C01FBFSDLUA/p1621516466035900)
AC It looks like this is putting the catalogue cluster under heavy load and causing it to intermittently drop requests

14.15 RK suggested turning it down to 0
14.16 AC Done

14.17 AC: I’m a bit suspicious of the size of the works ingestor queue, and I wonder if something is up
I could believe I sent a few updates twice, but how does 100k licence changes manifest as more than 200k messages on the queue?

14.20 This is the only change to the index config between the 2021-05-05 and 05-17 pipelines: https://github.com/wellcomecollection/catalogue-pipeline/commit/74711f7cd458f89de3a84b70069ccfcc4d554fd7 

14.20 RK turning off the ingestors has solved this - lets have a retro and talk about causes / mitigation. i’d like to look at scaling things whatever the root cause, because we’re always going to have intermittent high load during reindexes.

14.22 AC okay, so it’s just adding a pair of date fields that changed in the most recent pipeline

14.24 AC I’d like to see the CPU drop on the catalogue cluster before we call this done

14.25 RK the performance metrics in the elastic cloud dash are terrible - can we get better metrics over a longer period? That might help us identify if this has been a building issue or has a traceable trigger.

Discussion around:
Pipelines/reindex
Miro updates topic
c.15.30 snapshot generator started

15.35 DOWN alert
Images API Search
Front End Works Search (Origin)

15.38 Recovery
Front End Works Search (Origin)
Images API Search

15.36 JP seems like it can’t handle the images ingestor
15:37 I have turned them down to 0
15:39 going to turn works down too
15.41 yeah just realised I did it wrong
should be fixed now

15.42 NP emailed/put message in Slack to say search was slow again; then that it was fixed but no new updates will be coming through until we resolve the underlying problem.

Evening: AC turned ingestor back on at 1, no problems seen after that

## Analysis of causes

More bigger works being reindexed at the same time; fewer sparse works to spread out the load

Complexity of images mapping?


## Actions

**Team**
Investigate
- cross-cluster read replication
- testing reindexing away from production to look further into the root cause whilst simultaneously load testing an API pointed at it 
- autoscaling for ES
 
 **Robert**
- Turn on monitoring for production Elastic cluster
- Update Tom - DONE

**Natalie**
- Tell people that changes are coming through again (as of Thu evening) - DONE

 
 
