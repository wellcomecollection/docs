# Incident retro - web site not available

**Incident from:** 2023-09-02

**Incident until:** 2023-10-03

**Retro held:** 2023-09-11

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

[Saturday 2 September](#saturday-2-september-2023)
[Monday 4 September](#monday-4-september-2023)
[Tuesday 5 September](#tuesday-5-september-2023)
[Wednesday 6 September](#wednesday-6-september-2023)
[Thursday 7 September]()
[Friday 8 September]()
[Saturday 2 September]()

See [https://wellcome.slack.com/archives/C01FBFSDLUA/p1686565392141259 ](https://wellcome.slack.com/archives/C01FBFSDLUA/p1693813577323909)

NB notes in italics are the info sent out about this incident to give a rough idea of where we were at what point

### Saturday 2 September 2023

Updown alerts began at 16.50 for<br>
Experience: Content:What’s on (origin)<br>
Experience: Content: Exhibition (cached)<br>
Experience: Content: What's on (cached)<br>
Experience: Content: Event (origin)<br>
Experience: Content: Event (cached)<br>
and other content<br>

It continued to bounce down and up until the morning of Monday 4 September

### Monday 4 September 2023

08.46 NP messages @weco_devs in #wc-incident-response: Web site's gone AWOL (see wc-platform alerts) - can you please look at this as a priority.

Various colleagues reported the site was working for them, or that it was intermittently slow in various places.

*09.12 The web site is available now but we're aware that search is slower than normal. We're still investigating what has happened.*

9.27 PB checked and confirmed APIs were responding promptly

9.43 JP Throughput is normal but latency is spiking

9.51 JP posted graphs showing the CPU for the front end service spiked from Fri 1 September

9.52 JP It seems like we've killed the catalogue service for prod as well as e2e - don't know if this was intentional<br>
In the absence of an understanding of why that might happen I'm going to try bumping the task sizes<br>
Ah, that's going to be hard if the terraform changes are in-branch or local<br>
I'll do it in ECS console rather than TF<br>
Yeah these tasks are cycling<br>

09.57 We've identified what is causing the problem. We're now working to mitigate this which should make the web site more stable for everyone.

10.00 JP OK, that's done now - I expect it to help in the short term but if we look at the graphs above it almost looks like a memory leak sort of thing to me as the tasks started to fall over a day or so after they were started<br>
This behaviour might just be to do with caches getting stale though<br>
So I don't know if it's a proper fix<br>

10.25 JP OK, why has the event page gone down again?<br>
Latency started climbing again about 15-20 mins after the deploy

10.32 GE when did the content app take over traffic that was being served by the catalogue app? is that the heart of the problem?<br>
Looking at the cpu and memory utilisation graphs, they seemed to start climbing from Friday morning.<br>
The last deploy of the apps to prod was Thursday morning so I don't think it's the apps causing the issue<br>

10.33 JP Yeah I think that must be it<br>
Agreed, I think that it must've been changed in prod while this was being worked on: Remove the catalogue app from the infrastructure [#10169 ](https://github.com/wellcomecollection/wellcomecollection.org/pull/10169)<br>
That said - if quadrupling the resources doesn't work, it seems reasonable to infer that something in the merging of the apps causes something akin to a memory leak or thread starvation or something that causes this delayed latency problem<br>
Like something that only presents when traffic is going to both "sides" of the app<br>
Doesn't sound very plausible does it

10.42 AC I’d deployed into the e2e and staging environments and they both looked fine, all the routes were working, so I assumed it was good to go to prod<br>
JP it's a fair assumption and I expect this would've happened anyway<br>
probably not an assumption to test on a Friday afternoon though<br>
AC In other “not fantastically smart decisions” made on this PR: why oh why did I delete the ECR repo as part of it, and not save that for a separate patch<br>

10.53 JP What I said in standup about it being difficult to be 100% confident for perhaps a day - partly due to the poor resolution of ECS task resource metrics - does still stand though 

10.55 AC A thought from glancing at the ECS console: is it possible that the app container isn’t the thing being starved here?<br>
The nginx/log_router containers both have a memory reservation of 0.5GB each, which was 25% of the original task’s memory allocation

10.59 JP Yeah OK latency is going back up<br>
This isn't resolved

11.00 AC I’ve recreated the ECR repository, and I’ll kick off a deploy of the web app

11.01 AC interestingly the staging tasks seem unaffected<br>
JP again points to something like starvation or memory leak etc<br>
staging tasks don't get traffic<br>

11.03 AC ECR repo recreated, image published, tasks recreated<br>
Ah, and I need to run the publish script in ECR<br>
11:05 AC ECR image tags set<br>
Looks like catalogue tasks are coming up (edited) <br>
11:08 AC okay, I think we’re fully rolled back (aside from the content app being bigger than usual + having extra secrets)

11.09 AC So interestingly I am becoming less sure that HTTP 499 is a symptom of issues<br>
This is searching for an HTTP 499 in the catalogue app<br>
Gap when the catalogue app wasn’t logging anything<br>
JP Interesting - however 7 second average latency is definitely a symptom<br>

11.22 JP the 499s are presumably a proxy for latency<br>
and we know there is a long tail of request latencies for the catalogue app in particular<br>
so I am not surprised to see them intermittently<br>
and I am not surprised to see them in clusters either<br>

11.26 JP latencies back up<br>
AC And there goes the catalogue app<br>
 
11.29 JP catalogue CPU use is v high but that latency is for the content app although it seems to have reduced again

11.30 AC Looks like the catalogue app is really struggling making requests to iiif.wc.org, which seems fine AFAICT 
Also api.wc.org, is it just struggling to make outbound requests for some reason?

You can see lots of FetchErrors, e.g.
FetchError: request to https://api.wellcomecollection.org/catalogue/v2/works/ktdwkx2u?include=identifiers%2Cimages%2Citems%2Csubjects%2Cgenres%2Ccontributors%2Cproduction%2Cnotes%2CformerFrequency%2Cdesignation%2Cparts%2CpartOf%2CprecededBy%2CsucceededBy%2Clanguages%2Choldings failed, reason: socket hang up 
So the catalogue app should be as it was before I started mucking with Terraform on Friday

The content app has (1) increased resources and (2) a couple of extra ECS secrets

11.33 JP And the routing is definitely back to how it was?<br>
AC I think so, I just applied catalogue terraform in main<br>
And it looks right in the load balancer console

11.35 JP I don't know if you might expect to see those socket hangups from an app that's swamped

AC I wonder if the Terraform is a red herring, could this patch be anything to do with it? https://github.com/wellcomecollection/wellcomecollection.org/commit/3a61e41489aed2ccbdba00e882b02b8081d50c38#diff-9ed266619dda5[…]67be99c87f1R74-R78<br>
Promises feel like the sort of place you might get memory leaks …which is a great theory right until I realise that change never went to prod [confusion around the deployment task in Buildkit]

11.38 AC Just to satisfy another theory in my head: this is the chart of CloudFront requests over the last week. I have no idea what the massive spike on Saturday was, but it doesn’t look like we’re serving more requests than we normally do

11.52 AC Prismic model diff is failing<br>
12.00 GE because of this: rename and add fields [#10170 ](https://github.com/wellcomecollection/wellcomecollection.org/pull/10170)<br>
I can revert those changes for now in Prismic I mean - then the diffs should be good <br>
AC thanks super, prismic diff is now passed and deploying new images

12.03 JP did you do anything to the content app? the latency spiked and then just sort of resolved itself looks only to be a catalogue issue now
 
12.04 AC if Gareth has just rolled back his Prismic changes … could they be related somehow?<br>
JP it resolved about 11.52<br>
so I think probably not

12.12 AC redeploying catalogue app in prod with rolled back image

12.17 AC right, catalogue app is redeployed

12.28 AC nope, still seeing socket hang-ups in the catalogue app and ECS metrics are unhappy <br>
what gives??? and that sound was the works page falling over again

12.31 JP when the merged apps were deployed, is it possible that an old (non-merged) catalogue app actually kept running and then it was only with recent changes that the merged pseudo-app actually got deployed? ie should we roll back further

Nothing broke when this was merged: Merging catalogue into content [#9991 ](https://github.com/wellcomecollection/wellcomecollection.org/pull/9991)<br>
What if that was because the changes weren't fully deployed?

12.34 AC I see what looks like a deployment of the catalogue app here, on Thursday afternoon: https://buildkite.com/wellcomecollection/wc-dot-org-deployment/builds/2679#018a27d7-013b-45d6-8efa-573f48529bc4 

12.36 AC Let’s recap:
- the content app is running an image built from 3fd5f5b – it went down when it was serving catalogue traffic, but now seems healthy
- the catalogue app is running an image built from 3fd5f5b – it still seems unhappy
- We rolled back to before the weekend for application images

GE and the catalogue app happily ran an image built from 3fd5f5b for about 24 hours from Thursday morning before it was removed? so could there be something about the previous catalogue app infra that we didn't replicate in content when it was running both and haven't replicated for the new catalogue app? <br>
AC possibly? but all the infra was in Terraform

12.37 AC do we have an ignore_changes somewhere for CPU/memory on our ECS services?. Jamie manually increased the resources available to the content app. But if I go to main and I run terraform plan, it doesn’t want to roll those changes back. <br>
I was gonna wonder if the catalogue app is somehow under-provisioned<br>
If we’d maybe bumped its resources in the past and not committed that to Terraform, so when I recreated the service in Terraform it rolled back to a lower number of resources<br>
But that doesn’t seem to be the case, task definition 16 (Jan 31) and and 17 (today) both have 1 vCPU / 2GB   https://eu-west-1.console.aws.amazon.com/ecs/v2/task-definitions/catalogue-17092020-prod/16/containers?region=eu-west-1
in fact, the v16 and v17 task definitions have identical JSON<br>
doubling resources<br>
done, waiting for deployment<br>
JP https://content.wellcomecollection.org/works/a9zyrnjr (504)<br>
shouldn't that be catalogue.wc.org<br>
works.wellcomecollection.org I think<br>
AC now switched over to new tasks with 2x resources<br>
ooh, max CPU is dropping<br>
although I don’t feel good about this, because if it follows the pre-unmerging content app, it’ll soon climb back up

13.03 AC okay, so here’s a new theory: what if it’s nothing to do with a change we’ve made, and instead an external change? <br>
this is a search for the phrase “No data for page” in the app logs over the last 3 weeks, and it seems to have gone way up in the last few days<br>
If we were repeatedly calling up very large page props, would that cause the sort of memory-leak like behaviour we’re seeing?<br>
e.g. https://api.wellcomecollection.org/catalogue/v2/works/h43zp699?include=identifiers,items,h[…]guages,notes,images,parts,partOf,precededBy,succeededBy

13.18 AC I’m about to go to lunch; here’s a quick summary of where I think we are:
- The site was flapping all weekend, which started around the time the content app started serving the entire site (i.e. the merged content/catalogue app). Latency went way up; the apps were CPU and memory starved; everything unhappy.
- There’s nothing obviously abnormal about the site traffic over the weekend, e.g. we didn’t get 10x the usual number of requests.
- Rolling back all the changes on Friday to before the merge only partially fixed the issue (content app came back up after a bit, catalogue app was still struggling).
- Doubling the resources for the catalogue app seem to have stabilised things… for now.

13.24 AC My current theory is that we’re serving unusually large values in our Next.js props, and this is causing headaches in the catalogue app. I can see a couple of bits of low-hanging fruit, which I’m going to pop in a PR.

13.59 AC Here are a few bits of low-hanging fruit that I think will reduce the memory footprint of the catalogue routes: [#10174](https://github.com/wellcomecollection/wellcomecollection.org/pull/10174) Pick some low-hanging fruit to reduce the size of our Next.js props

14.33 AC That PR is green and passing e2es without the catalogue routes, so I’m going to merge it to main and remove the catalogue routes from the staging env.
 
14.50 AC Running e2es in staging now

14:53 e2es passing in stage, deploying to prod

15.00 AC e2es running in prod

15:01 removing the catalogue routes from the prod env

15:03 Okay, that’s merged and deployed, so now we have:
- All traffic going to the content app, which has some fixes to reduce the page weight
- e2es passing in staging and running now in prod<br>
I’m gonna keep an eye on latency in Kibana and ECS task health to see what happens next.

15.10 AC I’m seeing way less warnings about “data for page is too large”, which is good

ECS metrics are climbing but not redlining yet

15.35 AC I think tentatively looks okay

Do we want to turn the task size down before we call this good?

15.36 JP yes but not all the way<br>
2 vCPU seems reasonable for the merged app

15.39 We've deployed a fix that makes the web site stable again. Everyone should now be able to see and use the web site as usual.

15.45 AC Tweak the content apps – add the items API key, increase the task sizes [#10175](https://github.com/wellcomecollection/wellcomecollection.org/pull/10175)
That’s already deployed; I’d give it another half an hour to be safe?

16.12 AC thought was fixed but JP noticed a problem

16.22 AC suggested a memory leak; JP thread starvation

16.24 AC I was able to find another place where we can squeeze the JSON size a bit: [#10176](https://github.com/wellcomecollection/wellcomecollection.org/pull/10176) We only need to send a WorkBasic on download pages

16.42 Agreed to keep monitoring the web site into Tuesday 5 September until we know what happened or we don’t see any further issues.

19.42 AC I see a bunch of out-of-memory errors in the API logs starting exactly when the API fell over:<br>
java.lang.OutOfMemoryError: Java heap space<br>
It seems like CloudFront is maybe keeping it up but new queries aren’t working<br>
I have no idea what’s up, but I’m going to kick off a task redeployment to hopefully bring the API back up and then leave it for the night

### Tuesday 5 September 2023
Search not working. Rest of the web site looks okay.

*09.25 We are aware that search is not working this morning and we are continuing to work on resolving this issue.*

10.22 AC this is the logging link I'm starting with today: https://logging.wellcomecollection.org/app/discover#/?_g=(filters:!(),refreshInterval:(pause:!t,va[…]transaction*%22'),sort:!(!('@timestamp',desc))) <br>
It excludes all the HTTP traffic and just shows the rest of the logs<br>
You can see the OutOfMemoryError: Java heap space at 18:49 last night, but I can't see any corresponding errors this morning<br>
Looking in ECR, the API code hasn't changed in nearly a fortnight<br>
And ECS metrics for prod-search-api don't look unreasonable<br>
Looks like all the tasks were restarted correctly last night<br>
There's nothing abnormal in the Elastic console<br>
Latency of the content app was largely flat overnight; a brief spike when the API ran out of memory yesterday and then climbing this morning as the API struggles again<br>
CloudFront metrics look normal; we don't seem to be serving an abnormally high proportion of traffic

10.49 AC looking at the logs I see us serving a lot of search requests from the API which look like query spam

10.55 AC So I am tempted to introduce a new spam heuristic by expanding the range of characters we consider "unusual": [#10177](https://github.com/wellcomecollection/wellcomecollection.org/pull/10177) Expand the range of characters we consider 'unusual' for spam purposes

11.49 AC I've deployed my spam detection heuristic to prod, will keep an eye on latency. I see latency climbing again

12.16 AC I feel like there are clues pointing towards a renewed spam issue<br>
I've grabbed the CloudFront logs for the past 36 hours (half of today, all of yesterday)<br>
Yesterday we served 141,473 search pages on the website<br>
Today we've already served 113,208 search pages which weren't rejected as spam<br>
Very sus
 
15.04 AC [#10178](https://github.com/wellcomecollection/wellcomecollection.org/pull/10178) Add a toggle for disabling aggregations in search

15.51 AC disables aggregations in front end search (formats, locations, subjects, types/techniques, contributors, languages)

*17.00 Work has been done to get us to the place where we think search is working and more stable now. *

Tuesday summary:
- The website seems to be somewhat stable, but it's not fully back yet.
- We're fairly confident that the issue is not caused by a bug in our code – we can't find any recent change that might have caused the problems we're seeing.
- We can see the issue is caused by excessive load on the Elasticsearch cluster from searches, but it's unclear why the current search traffic is causing more issues than it used to.
- As a temporary fix, we've disabled aggregations (i.e. filters) on the website. Aggregations are the most expensive part of the query, and so far these seem to have stopped the site falling over repeatedly.
- We have a reindexed pipeline ready to go, in case the issue is something to do with the data in the Elasticsearch
- cluster. We're going to try deploying that tomorrow and see what happens.

Tomorrow:
- Switch over to the new index in the API
- Re-enable aggregations on the front end
- Monitor the site and see what happens

If we're still having issues, we'll raise a support ticket with Elastic.

### Wednesday 6 September 2023

08.37 AC the new API seems to be missing a handful of works<br>
I’m going to deploy it anyway, roll forward onto a hopefully-good index<br>
And I’ve got time to roll back if it breaks before I leave for the office

08.56 AC why is the what’s on page down<br>
PrismicError: An invalid API response was returned

NP checked just after 09.00 and What’s On was available

10.22 AC I haven't seen any issues since I rolled forward, hmm

11.54 AC [#696](https://github.com/wellcomecollection/catalogue-api/issues/696) API returns a 500 error when regex-like characters sneak into the search templates
 
12.43 AC [#10179](https://github.com/wellcomecollection/wellcomecollection.org/pull/10179) Allow toggling individual aggregations

13.24 AC re-enabling aggregations in search

13:25 I will start off with:<br>
:white_tick: genres, availabilities, workType<br>
:x: subjects, contributors, languages<br>
This ran for 25 minutes with no spikes in latency or anything, so assuming it's all okay

13.49 AC Flipping it round:<br>
:white_tick: subjects, contributors, languages<br>
:x: genres, availabilities, workType<br>
And within seconds those are spiking resources on the cluster. 

13.55 AC I'm going to disable those aggregations, let it cool back to zero, and then start re-enabling them

14.51 AC Now everything is back to the baseline, I'm going to re-enable a single aggregation<br>
:white_tick: contributors<br>
:x: genres, availabilities, workType, subjects, languages

15.07 AC This has caused a bunch of 500 errors, which seem to be caused by the workType filter being missing. I'm not sure why this didn't manifest before, but I'm going to change the experiment slightly:<br>
:white_tick: contributors, workType<br>
:x: genres, availabilities, subjects, languages

*15.08 We're making improvements to search as the day progresses, and will update you again later today.*

15.29 AC That last variant seems to be more stable, so I'm going to swap contributors and subjects:<br>
:white_tick: subjects, workType<br>
:x: genres, availabilities, contributors, languages

15.38 AC And now swapping out again, that previous variant seems stable:<br>
:white_tick: languages, workType<br>
:x: genres, availabilities, contributors, subjects

15.42 AC Again no issues, but we think it might be something to do with the interaction between aggregations, so we're going to try what we think are the two most expensive ones:<br>
:white_tick: subjects, contributors, workType<br>
:x: genres, availabilities, languages
 
15.56 AC Argh, it's still borked.<br>
:white_tick: subjects, contributors, workType, languages<br>
:x: genres, availabilities<br>

I've shoved in a query AWLC TURNING ON ALL THREE FILTERS so we can find the approximate timestamp in the logs

16.11 AC Elastic is stumbling again, languages agg is off

16.38 AC [#10181](https://github.com/wellcomecollection/wellcomecollection.org/pull/10181) Make our spam detection more aggressive

*16.54 We've stabilised search although not all of the filters are currently available.*

Wednesday summary:

Today:
- Jamie has identified a group of ~800 catalogue API requests which, if made at speed, will cause a latency spike in the Elastic cluster (see script above). This gives us a reproducible test case for exploring this further.
- We've also deployed a more aggressive spam detection heuristic which should cut some of the spam queries (which return a lot of results and might be causing more expensive aggregations).

Tomorrow:
- Get the raw Elastic queries for those API requests, cutting out the catalogue API. We can then feed them into
- Elasticsearch and profile the queries, e.g. removing certain clauses to see if they're the issue in aggregate.
- Re-enable some of the filters and see if the more aggressive spam detection has reduced the issue to manageable levels.


### Thursday 7 September 2023

### Friday 8 September 2023

### Monday 11 September 2023

### Tuesday 12 September 2023

### Friday 15 September 2023

### Monday 18 September 2023

*09.15 The web site performed normally over the weekend. We have re-enabled the filters and will continue to monitor.*

### Wednesday 20 September 2023

02.41-06.46 Updown down and up alerts for:<br>
What’s on cached and origin (https://wellcomecollection.org/whats-on )<br>
Content: Event cached and origin  (https://wellcomecollection.org/events/W4VKXR4AAB4AeXU7 )<br>
Content: Exhibition cached and origin (https://content.wellcomecollection.org/exhibitions/WZwh4ioAAJ3usf86 )<br>


### Tuesday 3 October 2023

*11.53 Resolved - We're closing this incident after extended monitoring. We believe we have effectively mitigated the effects of the requests that were causing issues and no longer believe there is an increased risk of downtime. Thank you for your patience.*

## Analysis of causes
- 

## Actions

**who**
- 
