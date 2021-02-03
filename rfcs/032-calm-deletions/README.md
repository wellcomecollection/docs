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

The worker will consume records, filter out those that are already flagged as deleted, and check for the existence of the rest in the Calm API. If the record has been deleted (is no longer present) then it will update the VHS entry to flag the deletion. The deletion flag will live in the DynamoDB record so that the flag can be checked without fetching the object from S3. After updating a record, the worker will notify the transformer topic.

The calm transformer will check for the presence of the deletion flag in the source data and create `Deleted` works as appropriate.

This architecture is illustrated below (arrows indicate the direction of data flow):

![image](https://user-images.githubusercontent.com/4429247/106171539-8da8dd00-6189-11eb-9aca-2577f1ab6ed7.png)

### Minimising Calm API queries

Checking for the existence of the records can be done naïvely by performing a search (the only relevant action available to us in the current API version) for a given record ID and confirming that the returned `SearchResult` number is equal to 1. Obviously, this requires 1 request per record.

We can, however, do better than this. Consider that we have a large population of records with a fairly low prevalence of deletions. In one query, we can search for a set of `N` records, and know that the difference between `N` and the number of results is the number of deleted records in that set. If there is no difference, we can move on immediately.

At this point we could iterate through either the results or the record IDs to find which are missing, or we could find the missing records via binary search - but the former means that we only reduce the number of queries if there are _no_ records missing among the set, and the latter requires both that the resultant queries are made sequentially (not in parallel), and more significantly binary search is very poorly suited for finding multiple occurences.

Perhaps unsurprisingly, this is a problem that has been considered [at length](https://arxiv.org/pdf/1902.06002.pdf) in the literature and indeed is particularly relevant at the moment - for example, in October [Mutesa et al (2020)](https://www.nature.com/articles/s41586-020-2885-5) described a strategy for finding positive SARS-CoV-2 tests in individuals by pooled testing across a population. Our testing tool (a SOAP API rather than a PCR test) can tell us how many deleted items there are in a given set, so we can use a simple algorithm by [Hwang (1972)](https://www.jstor.org/stable/pdf/2284447.pdf?casa_token=d7hvCvhjYyQAAAAA:zr0BQ_BVfaBPezuV5P1RlFyDO1Uo1ZMLgMGi9fXCddGcrjj8GPxc9M2jn6CBzs1fV8GT8Nbjfwj_w68RV8imdWN8SchyMahjxBwF8qDM_j90sSedVg) to find the deleted works in fewer requests provided that the number of deleted works is less than `(N + 2)/2`.

Note: I have verified that the Calm API is happy to take requests for batches of IDs up to (and probably beyond) a size of 1000.

## Questions & potential issues

- Are we really 100% sure that polling for deletions is the only way to detect them?
- Might we want to be continually checking (more like crawling) for deletions rather than doing it all at once?

