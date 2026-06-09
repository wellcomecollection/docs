# RFC XXX: IIIF Metrics for efficiency, insight and bot defence

blah blah

https://docs.google.com/document/d/1bRmGMMo4gM2JiUW5Zx-MRlHLi6ZVNg-HWfxQi5Hi9tw/edit?tab=t.0


**Last modified:**  2026-06-01T17:00+00:00

## Context

What DLCS does now

Outline our strategies

Lustre problems

bots

insight

Flow - decisions

CF, Orchestrator, thumbs, specialserver, imageserver

Special streams from S3
for full region but maybe also for non-tile regions?

Aim is not necessarily to provide fastest possible response to all callers
Infra costs money. We are not your cache.

Aim is to provide a reasonable service to human and bot consumers
 - for reasonable cost to Wellcome (otherwise have everything on 100TB of Lustre and infintly sclaing image servers)
And to deter bots when they start acting unreasonably, all the way up to blocking them
Our aim is not to block reasonable automated use of the Image API


But how do we block... what does orchestrator have access to?

as well as auth decision, orchestrator can make a bot decision
block - throttle - allow
How do you efficiently throttle an HTTP request in Orchestrator - without overwhelming the server?
Throttled: 100ms header

requests for different images from same source that are not thumb requests
"please use a value from the sizes array for bulk requesting"


## Proposal

![DLCS Metrics Diagram](images/dlcs-metrics.png)

### Metrics store

What is is? Postgres?
How long does stuff stay in it? Forever?
How long do we need stuff to stay in it?
Do we archive it?

What do we want to capture?

Scope to image requests only

timestamp


asset id

raw path

region

region type:
full | calculated tile | OSD sub-tile | other
char f, t, s, o
Algorithm for computing this
 - simple: Is it square, power of two or from edge if not square?
 - informed: Is it a valid tile from the image's info.json?

Store info.json in image table?
Does OSD still do this

size

size type:
max | tile | OSD sub tile | other
char m, t, s, o

rotation (store null for 0?)

quality
char d, b, g, etc

format
char j, p, w etc

(and/or quality.format?)

User agent

ip address

Did *this* request trigger orchestration?

How served
CF cache / thumb / resize thumb / specialserver / orchestrated img server
(is this gathered from CF)


Join to Images table for
 - size
 - location(s) (nas?)
 - open/not open (affects cloudfront cache)


## bots

If gathered from CF the data is post-request

How do we identify a bot?

 - retrospectively, from metrics
 - As it's happening

What do we do if we do identiy one?

fair use
throttle

What general-purpose services from WAF, Cloudflare, F6 Firewalls etc help us?
What can't they do because it's specific to IIIF traffic, especially image traffic?

IIIF Presentation
 - doesn't bother us so much at Wellcome but is still a magnet for bots

Fail-fast on requests that can't serve a response, e.g., Canvas `id`, Range `id` - don't waste resources on them (pattern match at Cloudfront?)

## Scavenger

Decision to evict is based on:
 - performance for human users
 - cost

As the disk nears a threshold, we need to start deleting orchestrated files

Example bad case
 - a very large artwork that is viewed intermittently. But often enough that it keeps getting re-orchestrated just after it's been scavenged

Conversely a very small jp2 that won't free up much space and is occasionally viewed



## Alternatives Considered

## Impact

(incl risks)

## Next Steps

A list of next steps for implementing the proposed solution, including any dependencies or prerequisites.