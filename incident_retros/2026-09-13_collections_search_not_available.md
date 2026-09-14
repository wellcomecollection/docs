# Incident retro - collections search not available
**Incident from:** 2026-09-13

**Incident until:** 2026-09-13

**Retro held:** 2026-09-14


- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

See [https://wellcome.slack.com/archives/C01FBFSDLUA/p1789313297275609 ](https://wellcome.slack.com/archives/C01FBFSDLUA/p1789313297275609)

Sunday 13 September 2026

From 13:07 to 18:59 UTC, roughly 60% of requests to the prod catalogue API's works and images endpoints returned HTTP 500. The website's search and work pages failed for the same period. 

16.28 JC created a Statuspage alert to notify that collections search was not available

20.14 RK Some ECS tasks on the API got stuck, out of memory issues, didn't get properly evicted. Not sure of root cause.

I have restarted the stuck tasks, things are back healthy again.

Will weigh in with an RCA (root cause analysis) Monday.

Claude is running an analysis as we speak, looks like an interesting one. (edited) 

This may reoccur, if the same pattern of behaviour happens that caused it. Remediation is pretty easy though.

14 September 2026

06.50 RK No reoccurrence, I think this can be closed

08.00 RK posted this summary https://gist.github.com/kenoir/57a687fb97bb1ea1169e32e6193b34e7 

## Analysis of causes

From 13:07 to 18:59 UTC, roughly 60% of requests to the prod catalogue API's works and images endpoints returned HTTP 500. The website's search and work pages failed for the same period.
A distributed scraper (ImgSearch/0.2, 57 Azure IPs) began paging /catalogue/v2/images?pageSize=100 at about 12:52. Every image search asks Elasticsearch for vectorValues.features, a 4096-float vector per image, so each 100-image page is a multi-megabyte Elasticsearch response even though the API returns about 140 KB to the client. The three prod-search-api tasks, each running a JVM with a 512 MB heap (the JVM default of 25% of the 2 GB task, measured by running the image under the same limit), went into a GC storm within three minutes and started throwing OutOfMemoryError on the Elasticsearch client's I/O threads at 13:18.
1. A scraper made /images?pageSize=100 requests at 40 times the normal rate
2. Each of those requests is a multi-megabyte Elasticsearch response
3. The heap is small and there is no headroom configuration
4. An OOM on the client's I/O thread leaves the task alive but unable to reach Elasticsearch
5. Nobody saw the alarm for five hours, as this happened on a Sunday and therefore outside of normal working hours.


## Actions

- Issue tracking long term remediation: Search API: image scraper can exhaust the JVM heap and leave tasks serving 500s indefinitely [#547](https://github.com/wellcomecollection/platform-infrastructure/issues/547) - DONE
