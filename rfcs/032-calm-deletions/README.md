# RFC 032: Calm deletion watcher

**Status:** Draft

**Last updated:** 28/01/2021

## Background

We've realised that the pipeline does not pick up deleted Calm records - once they're deleted there is no trace of them in the Calm API, but they remain in the source VHS tables. Especially because a cleanup project at the end of last year was responsible for a very large number of deletions, this needs to be resolved.

So far as we can tell, there is no way to find deleted records other than checking for their absence. This means that our solution needs to take some sort of polling-based approach: going through the source table and checking for the continued presence of each record in the Calm API.

## Proposal

The deletion watcher will consist of:

- A worker task in the calm adapter cluster
- A lambda
- The existing reindexer

The lambda will place a message on the reindexer queue requesting a "reindex" of Calm records to be sent to the worker. It will be triggered by a scheduled Cloudwatch event or manually. By default it will request the full source scan but in the case of a manual trigger it will be possible to request specific IDs, which will be useful in the case of expediting known deletions.

The worker will consume records and check for their existence in the Calm API. If the record has been deleted (is no longer present) then it will update the VHS entry to flag the deletion. 

The calm transformer will check for the presence of the deletion flag in the source data and create `Deleted` works as appropriate.

This architecture is illustrated below (arrows indicate the direction of data flow):

![image](https://user-images.githubusercontent.com/4429247/106171539-8da8dd00-6189-11eb-9aca-2577f1ab6ed7.png)

## Questions & potential issues

- Are we really 100% sure that polling for deletions is the only way to detect them?
- Might we want to be continually checking (more like crawling) for deletions rather than doing it all at once?

