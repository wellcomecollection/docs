# Incident retro - Internal model &lt;=&gt; Elastic index sync question

**Incident from:** 2020-01-07

**Incident till:** 2020-01-07

**Retro held:** 2020-01-15

* [Summary](2020-01-15_app-index-sync.md#summary)
* [Timeline](2020-01-15_app-index-sync.md#timeline)
* [Analysis of causes](2020-01-15_app-index-sync.md#analysis-of-causes)

## Summary

And application \(the API in this case\) was deployed with an internal model that was incompatible with the index that the application's environment was pointing to.

e.g.

```text
env: index = v2-20191115
app: model = v2
↓
deploy new app version with release tool
↓
env: index = v2-20191115
app: model = v3
```

Where the `v2-20191115` JSON cannot be deserialised into `model v3`.

This lead the API to start returning 500s. It was particularly tricky as the piece of the model that changed wasn't present in many documents, so only errored when a work with the offending data in was surfaced as a result and the app attempted to deserialise it.

[This was the change to the model for context](https://github.com/wellcometrust/catalogue/pull/328/files#diff-4bc08710478ccfb8e2ea57802292a290).

This error also flagged up a number of other parts of the system that are not currently working to the level that we need them to.

Namely:

* [The Model-Index-Sync question](2020-01-15_app-index-sync.md#the-model-index-sync-question)
* [Error reporting](2020-01-15_app-index-sync.md#error-reporting)
* [Error logging](2020-01-15_app-index-sync.md#error-reporting)
* [Deployment transparency and rollback](2020-01-15_app-index-sync.md#deployment-transparency-and-rollback)

### Timeline

Tue 7 Jan 2020

* Change merged that added licences, changed one licence \(the change couldn't be parsed\)

Wed 8 Jan 2020 Day

* Fix for relevancy deployed
* Checks went through and seemed fine

23.20

* Try to search “dinosaurs” on /works, and get an error page back.
* Go to Slack, and check \#wc-platform, \#wc-data, \#wc-experience and \#wc-platform-alerts. No messages or alerts that would indicate an error.
* Try to find the logs in the platform account. I can’t find the API at all.
* Log into Elastic Cloud at cloud.elastic.co. Click on the logging cluster, try to launch Kibana … boom, no logs for me!
* Realise the API is in the catalogue account now, go to terraform to hunt issues.
* Get into the catalogue account, search the logs. Search for “500”, see a lot of 500 errors accumulating in the API Gateway logs and nginx.
* Check the ECS tasks. Oh look, it got redeployed when the bugs started.
* Write this all up in Slack and a GitHub ticket.

Thu 9 Jan 2020

* Went through the above, tried rollback to potentially previously working version
* Guessed that it may be the modl breaking, pointed app to staging index which fixed it
* Put into code and committed

## Analysis of causes

### The Model-Index-Sync question

Currently we index into a new index when we start up a new pipeline, which is often triggered by a transformer or model change.

When then need to remember that any new changes to the API will have to reference this new model as it will be using the new model.

This has caused issues by going out of sync in the past.

### Error reporting

CloudWatch alarms were triggered in the Catalogue AWS account from API gateway.

These then tried to post to a topic in the Platform AWS account, to which it had no permissions. The topic has the lambda subscribed to it that then posts to Slack.

This never happened due to the permission issue.

**Thoughts**

* Should we decrease the amount of steps from Cloudwatch -&gt; Us. This is currently
  * CloudWatch
  * Topic
  * Lambda
  * Slack

### Error logging

The logs were non-descriptive and held in multiple places. This made it hard to to work out what the problem was.

**Thoughts**

* The logs should describe the error, especially if we know that this error can occur
* We should have the logs reporting into the Elastic search logging cluster

### Deployment transparency and rollback

When looking to rollback it was not clear as to where to log back to. This information is available in the release tool infrastructure \(Dynamo\). When releases are made we also know through ECS events that they are occuring, as @alexwlchan did to debug this problem.

## Actions

* [Create RFC](https://github.com/wellcomecollection/docs/pull/9)

