# Incident retro - concept pages not available

**Incident from:** 2022-11-03

**Incident until:** 2022-11-03

**Retro held:** 2022-10-04

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

3 November 2022

See https://wellcome.slack.com/archives/CQ720BG02/p1667487956149609 and  https://wellcome.slack.com/archives/C01FBFSDLUA/p1667488779997449 

14.44 AC doing the 2022-03-11 reindex to:
- Fix the snapshot reporter
- Flush out some pipeline issues
- 
I’m going to kick off by deleting the 2022-10-14 pipeline, which seems like it was never used

AC thought it was never used based on https://api.wellcomecollection.org/catalogue/v2/_elasticConfig 

15.05 AC Was concepts looking at the 2022-10-14 index?<br>
yes<br>
gonna roll it back

15.19 AC FYI the concepts pages are broken, because the concepts API is broken<br>
For some reason we had a mixture of API indices:
- /works in prod = 2022-10-03
- /concepts in prod = 2022-10-14
- /works in stage = 2022-10-14

15:20 So I thought it was safe to delete 2022-10-14 and spin up 11-03, turns out that was wrong<br>
I’m rolling everything back to 10-03, and preparing 11-03 for rolling forward

15.24 JP suggests something went wrong with deployment?

AC yeah

errr https://buildkite.com/wellcomecollection/catalogue-api-deploy-prod/builds/373#0183e5ce-fcaa-487a-9d99-7c32ff37c073 

service | old image | new image | Git commit
--- | --- | --- | ---
concepts | ae604a2 | - | -
items | ------- | No image found! |
search | ------- | No image found! |
snapshot_generator | ------- | No image found! |

I’m having to deploy locally with weco-deploy, because Buildkite is unhappy at the missing secrets

It wants to see 2022-10-14 because that’s what the staging API has, but I’ve deleted that

I’m deploying the latest images to staging

I wonder if something between our build short-circuiting and weco-deploy has gone wrong, e.g. there is no image tagged ae604a2 because it was only a change to the concepts API

15.34 AC seems to be okay, deploying to prod

15.43 AC Should be back up now



## Analysis of causes
Thought same index was being used in works and concepts API

Something went wrong with the deployment of the 2022-10-14 index - bug in we-co deploy?


## Actions

- If queue crosses e.g 1.5 mill messages, stop the ingestor and send a message to Slack (check SQS metrics to determine the threshold). Discussed but decided not to do.

**Alex**
- Remove all the “clever” build logic from all the scala repos [#5626](https://github.com/wellcomecollection/platform/issues/5626)
- Simplify the deployment logic in weco deploy so it always deploys a complete set of images
