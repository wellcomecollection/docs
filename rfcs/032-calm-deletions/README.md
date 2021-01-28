# RFC 032: Calm deletion watcher

**Status:** Draft

**Last updated:** 28/01/2021

## Background

We've realised that the pipeline does not pick up deleted Calm records - once they're deleted there is no trace of them in the Calm API, but they remain in the source VHS tables. Especially because a cleanup project at the end of last year was responsible for a very large number of deletions, this needs to be resolved.

So far as we can tell, there is no way to find deleted records other than checking for their absence. This means that our solution needs to take some sort of polling-based approach: going through the source table and checking for the continued presence of each record in the Calm API.

## Proposal

- The deletion watcher will be an ECS task within the existing calm adapter cluster.
- It will run as a scheduled task at a frequency to be agreed with the collections information team.
- It will also be possible to run the task manually via the `RunTask` API. A script will be provided for this.
- The task will scan the source data VHS table and check for the existence of each record in the Calm API. If the record has been deleted (is no longer present) then it will update the VHS entry to flag the deletion. 
- The calm transformer will check for the presence of the deletion flag in the source data and create `Deleted` works as appropriate.

This architecture is illustrated below (arrows indicate the direction of data flow):

![image](https://user-images.githubusercontent.com/4429247/106134857-08103780-615f-11eb-845f-112109ead907.png)

## Questions & potential issues

- Are we really 100% sure that polling for deletions is the only way to detect them?
- Can we reuse any existing things for this (eg the reindexer)?
- Might we want to be continually checking (more like crawling) for deletions rather than doing it all at once?

