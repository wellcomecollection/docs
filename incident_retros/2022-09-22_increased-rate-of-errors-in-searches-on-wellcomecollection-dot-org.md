# Incident retro - increased rate of errors in searches on wellcomecollection.org

**Incident from:** 2022-09-22

**Incident until:** 2022-09-23

**Retro held:** 2022-09-26

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

22 September 2022

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1663849437942949 

13.00 AC triggers an upgrade of the API Elastic cluster from 8.4.1 to 8.4.2 by applying the Terraform in the pipeline stack

13:23 AC starts investigating the issues, identifies the “totalTermFreq must be at least docFreq” error coming from Elasticsearch. Unclear at this point if it might have been caused by the upgrade process.
Other debugging at this stage:
- Nothing obvious in Google/Twitter/GitHub to suggest other people have similar issues
- No significant activity in the pipeline that might be stressing the cluster

13:41 AC disables the catalogue pipeline entirely, to avoid further changes to the affected cluster.

14.00 AC and PB identify a minimal query that reproduces the error.

14.02 AC triggers an in-cluster reindex to try to rebuild the index; this has the same issue.

14:42: The in-cluster reindex fails; AC and PB agree to kick off a pipeline reindex.

15:17 AC kicks off a clean reindex.

18:46 Reindex completes, AC deploys the new index to prod. The issues persist.

19:55 AC opens a ticket on Elasticsearch core with a reproducible test case. Elastic engineers confirm the regression is in 8.4.2 a few minutes later. https://github.com/elastic/elasticsearch/issues/90275 

Thursday eve: AC kicks off a new reindex into an 8.3 index to run overnight.

23 September 2022

Morning AC promotes the 8.3 index to prod, which seems to resolve the issues.


## Analysis of causes
Upgrade of the API Elastic cluster from 8.4.1 to 8.4.2 which has “totalTermFreq must be at least docFreq” error 

## Actions

**Alex**
- Document why we don’t auto-upgrade in the pipeline clusters
- API logs out a query that gives a 500 error

**Mel**
- Create ticket to investigate if (something like) depandabot would be helpful

**All**
- For future use: reindex first before upgrading / check the version you’re upgrading to first
- Be more deliberate about upgrading manually rather than accepting it via Terraform
- Use cross fields less: be more explicit about how we want to query the data
