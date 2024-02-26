# Incident retro - search not available

**Incident from:** 2024-02-25

**Incident until:** 2024-02-26

**Retro held:** 2024-02-26


- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1708937288732099

### 25 February 2024

17.11 Updown alert down: What’s on, Exhibition, Concept<br>
17.12 Up: What’s on, Exhibition, Concept<br>
22.09 Updown alert down: What’s on<br>
Up: What’s on<br>
plus numerous CloudFront 5xx errors detected

### 26 February

08.48 RK Getting 50x for the collection search, and there are lots of errors in the alerts channel. [confirmed by DM and NP]

08.51 RK Lots of load on the api this morning. These are log events only, so that might just be the errors edit: it is - not especially high load - just a lot of errors starting around 1am.

08.59 RK Lots of errors all look like they are coming from the same container id: `58877c4d38434478a490e29e745f360b`. I'm going to kill the bad task and see if that clear things up<br>
A bit suspicious that the task that all the errors are coming from is 4 days old and the other 7 hours old.

09.03 RK Also worth repeating that bytespider traffic is back somehow. This is a search for the user-agent across all services but the logs are all from frontend-prod

09.07 RK I killed the task that was throwing errors and it looks like that may have resolved the problem <br>
NP/JC confirm no errors when searching.

09.08 RK Events from the search-api service, you can see 2 of the 3 tasks throwing errors duck at about 1 am to be replaced by healthy tasks, and me killing the last one just one.

09.10 RK Working hypothesis is that high load caused the search service to get into a bad state, and our health-checks are not good enough to recognise that this last task needed booting (though I suspect recent changes made them better).

09.17 RK To recap - over the weekend there were updown notifications at ~5pm and 10pm (see the alerts channel) yesterday that are in line with the increased traffic from the bytespider bot.<br>
Then from approximately 1:30am we start seeing errors in the search API.<br>
And at about 2am 2/3 of the tasks associated with the search service restarted.

09.26 RK Digging into the errors on the troubled task<br>
```com.sksamuel.elastic4s.http.JavaClientExceptionWrapper: java.util.concurrent.CancellationException: Request execution cancelled```

looks like an issue talking to ES


## Analysis of causes
- High load caused the search service to get into a bad state, and our health-checks are not good enough to recognise that this last task needed booting
- Three tasks serving search. Two were restarted after a load balancer health check but third didn’t (it was healthy enough to look as if it was alright).
- Related to: Elasticsearch timeout can be fatal to the ingestor. [#2268](https://github.com/wellcomecollection/catalogue-pipeline/issues/2268) ?


## Actions

**Robert**
- Investigate why bot traffic is still reaching our service

**Natalie**
- Take to planning: Extend load balancer health checks or search API to fail if it can’t connect to ES (including Investigate Elasticsearch timeout can be fatal to the ingestor. #2268)

**Agnes**
- Check if updown checks the catalogue API and reports that in Slack
