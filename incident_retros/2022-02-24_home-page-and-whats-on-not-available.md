# Incident retro - home page and what's on not available

**Incident from:** 2022-02-24

**Incident until:** 2022-02-24

**Retro held:** 2022-03-01

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

23 February 2022<br>
PR merged Remove place from event (Prismic model and app types) [#7697 ](https://github.com/wellcomecollection/wellcomecollection.org/pull/7697)

The model change happened at about 17:00 on the 23rd Feb

24 February 2022

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1645692506693739 

08.47 Alert down for: 
- Experience: Content: Homepage (cached)
- Experience: Content: Homepage (origin)
- Experience: Content: What’s on (cached)
- Experience: Content: What’s on (origin)

08.48 AC I reckon this is probably @dmc’s change to the Prismic model – the deployed code is still looking for “place”, but it can’t find it because we’ve removed it
And deploying the front-end is blocked because it’s broken in a different way
I believe this fix will get the deployment unblocked: https://github.com/wellcomecollection/wellcomecollection.org/pull/7704 

08.50 AC I’m going to merge #7704 by fiat and we can review it later, to unblock the deployment and get the homepage working again<br>
Specifically: we check a set of URLs for 200'ing as part of the deployment process, which you can see here: https://buildkite.com/wellcomecollection/experience-deployment/builds/657#9cf35e09-cf96-467b-becf-2fdaf1125598 <br>
One of those URLs is 500'ing, which means we shouldn’t be allowed to deploy… but it’s not as bad as the prod front-end, which is totally broken

08.52 Statuspage update created for home page and events not available

09.06 AC: still broken https://buildkite.com/wellcomecollection/experience-deployment/builds/658#7e887723-5ecf-4ac7-8a1b-8bba6add23c4 

DMc but I’m wondering if putting `place` back into the Prismic model would make sense<br>
09.10 AC depends how long it would take to propagate<br>
I suspect the issue is that Prismic has only just propagated the model change you applied yesterday

09.23 DMc PR: [#7705 Stop 500ing](https://github.com/wellcomecollection/wellcomecollection.org/pull/7705)

09.25 PB Is it relevant that place is mentioned in this graphQuery?

09.26 DMc I think this is another possible issue https://github.com/wellcomecollection/wellcomecollection.org/pull/7705/files#diff-0d61a4c2769aa8f2991eec03d5ea6[…]ff8cd8a6b02a6def9ff904185f3befR221 

I had thought that putting place back on the Prismic model would be fairly instant, but perhaps Alex was right about propagation<br>
in any event, this change brings the site back up locally for me<br>
PB’s review of the above isn’t powerful enough

09.32 DMc couldn’t add PB to https://github.com/orgs/wellcomecollection/teams/js-ts-reviewers 

09.37 DMc couldn’t force the PR or push to main

09.38 Then I suppose we must wait for @Gareth Estchild or for the interviews to finish 

09.40 PB asked JT to add him to https://github.com/orgs/wellcomecollection/teams/js-ts-reviewers / done at 09.44

09.49 PB While we wait for that to go through - Is the underlying cause of this down to the delay in Prismic propagation?
i.e. that this all seemed fine and smoke tested perfectly because Prismic was still using the old model, so the queries using the deleted fields completed successfully, but then once it was deployed, and Prismic updated, it all went a bit wrong

10.07 Recovery for:<br>
- Experience: Content: What’s on (origin)
- Experience: Content: What’s on (cached)
- Experience: Content: Homepage (cached)
- Experience: Content: Homepage (origin)

10.11 Statuspage update: resolved


## Analysis of causes
Is the underlying cause of this down to the delay in Prismic propagation?
i.e. that this all seemed fine and smoke tested perfectly because Prismic was still using the old model, so the queries using the deleted fields completed successfully, but then once it was deployed, and Prismic updated, it all went a bit wrong

Reading between the lines in the Prismic docs and an old Prismic support thread, coupled with the timing of content being published and the site going down (see below). It looks like the model updates are only reflected in the API response once a piece of content has been published.

N.B. The model change happened at about 17:00 on the 23rd Feb

We need to remember to publish something, when we change the model.

A quicker fix in this type of scenario therefore, would be to change the model back to its previous state and publish something, to see those changes in the API.


PB couldn’t approve DMcs PR

DM couldn’t add PB to https://github.com/orgs/wellcomecollection/teams/js-ts-reviewers 

DMc couldn’t force the PR


## Actions

**Alex**
- Make the e2e tests go faster: If they were faster, we'd be able to recover from broken builds a lot faster. [#7706](https://github.com/wellcomecollection/wellcomecollection.org/issues/7706)
- All developers should be able to merge pull requests
- Add dev permissions to onboarding/leaving checklist
- Investigate splitting out the experience build
- Make the monitoring lambdas vend a prefilled link to the logging cluster

**David**
- Think about having a staging version of Prismic ([development environment for Prismic](https://prismic.io/docs/core-concepts/environments)) and talk to other developers about what has been found out

**Gareth**
- Document how to re-add deleted fields in Prismic, and update a piece of content arbitrarily.
- Add a message to the diff tools script re updating content after field deletion from the model.
- Make a ticket: Investigate all uses of graph query, and make sure we’re only using it where needed
