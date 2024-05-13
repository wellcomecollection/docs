# Incident retro - search not available

**Incident from:** 2024-05-07

**Incident until:** 2024-05-10

**Retro held:** 2024-05-13


- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

Site was checked against Prismic staging

### Thursday 2 May
Decision to not to make changes ahead of a bank holiday weekend

### Tuesday 7 May 
[10.41](https://wellcome.slack.com/archives/C3N7J05TK/p1715074901944649) DM: Pushed Slice Machine types to prod and migrated content after checking with Editorial<br>
Told editorial about changes to Quote slices and Image gallery slices<br>

[11:53](https://wellcome.slack.com/archives/CQ720BG02/p1715079221400849): 1st There was an error in the content-pipeline-2023-03-24 Lambda alert in #wc-platform-alert channel <br>
	Cloudwatch logs indicate the issue is around fetching the data from the Prismic API<br>

```Error: Unable to parse fetch query Invalid fetch parsing Exception.",
        "",
        "A shared slice can only contains  `variation`."
```

[14.15](https://wellcome.slack.com/archives/CUA669WHH/p1715087740894799) AG: could it be possible that the slice machine changes are affecting the way we're fetching prismic articles and events to write them into the content index? We're seeing errors in the content pipeline where it's trying to fetch prismic docs. Articles weren’t modified yet

14:30ish: DM, RC, RK and AG get together to debug. The issue is identified as the content-api’s articles graph query being incompatible with the new Prismic data model. The graph query is modified to work with the new Prismic data model.

(15:00-16:00 break for review meeting)

16:00: Fix is being implemented and tested locally. PR open for review

16:39: Last alert pop in #wc-platform-alert 

16:50: Fix is approved, merged and deployed. Content-pipeline-2023-03-24 alerts stop 

### Wednesday 8 May
[07.58](https://wellcome.slack.com/archives/CUA669WHH/p1715151527461929) DM
Things I’ve noticed after remapping content:
1. Promo images aren’t always using the 16:9 version
2. ‘In Pictures’ articles aren’t showing all images by default
3. Old ‘webcomics’ (Body Squabbles) are rendering as image galleries with one image
4. One article from 2017 was somehow listed as the most recently published thing
I have delisted the old article. 

I’ve got a PR on the way that deals with 2. and 3.<br>
impact of 1 is that images aren’t all the same aspect ratio in cards currently (don’t think this is a huge deal?)<br>
[aspect ratio via contentUrlSuffix didn’t get taken over in the migration. Reported to Prismic as a bug with migrating assets] 
Change expected URL for meta image #10859

[13.15](https://wellcome.slack.com/archives/C3N7J05TK/p1715170506286159) Removed Bodies of Knowledge symposium to help with a bug fix<br>
Draft articles not migrated in the same way as published articles, and not easy to find

[14.39](https://wellcome.slack.com/archives/C3N7J05TK/p1715175594855709?thread_ts=1715170506.286159&cid=C3N7J05TK) DM you should be good to add/edit in Prismic now, but there are still old events that you won’t currently be able to see the body content for

17.07 Email reported that the [Opening times page](https://wellcomecollection.org/pages/WwQHTSAAANBfDYXU) was missing the location in the building - collection venues weren’t migrated (Collection venues weight/label needs to be added [#10856](https://github.com/wellcomecollection/wellcomecollection.org/issues/10856) )

[18.30](https://wellcome.slack.com/archives/CUA669WHH/p1715189433159889) RK: Am I right in thinking if we'd been using the content API to front all prismic content we'd have avoided this migration issue? The pipeline would have broken but we'd have maintained user facing content.<br>
RC: Hmmm that's a good question. We still would have had to migrate the content in order for it to render in the CMS editing side?

[18.36](https://wellcome.slack.com/archives/CUA669WHH/p1715182562668069) [Images] RC: It looks like just the width is now getting passed and anything else is ignored, which explains the difference in height.<br>
I feel like it has to do with missing contentUrlSuffix. They should probably contain w=, h= and rect= for crops and they're just empty strings?

DM: I’ve just removed and re-added a promo image for one of the cards on the /stories page and it appears to have fixed it for that one
so I think it might be a case of doing that for the ones on landing pages
I think this is something we can report to Prismic as a bug with migrating assets



### Thursday 9 May
Fix for [#10856](https://github.com/wellcomecollection/wellcomecollection.org/issues/10856) opening times page deployed<br>
[Migrated](https://wellcome.slack.com/archives/C3N7J05TK/p1715248398510779?thread_ts=1715242441.065249&cid=C3N7J05TK) content for draft event publishing this afternoon (JWM perspective tour and workshop)<br>
Fix for change expected URL for meta image [#10859](https://github.com/wellcomecollection/wellcomecollection.org/pull/10859)

### Friday 10 May
Add publishDate to articles graphQuery [#128](https://github.com/wellcomecollection/content-api/pull/128) deployed; reindex run Monday 13 May [fixed issue with old article that had to be delisted] Override date bug already existed but wasn’t known about - that date wasn’t fetched by the content API






## Analysis of causes
- High load caused the search service to get into a bad state, and our health-checks are not good enough to recognise that this last task needed booting
- Three tasks serving search. Two were restarted after a load balancer health check but third didn’t (it was healthy enough to look as if it was alright).
- Related to: Elasticsearch timeout can be fatal to the ingestor. [#2268](https://github.com/wellcomecollection/catalogue-pipeline/issues/2268) ?


## Actions

**Robert**
- Investigate why bot traffic is still reaching our service

**Natalie**
- Take to planning: Extend load balancer health checks or search API to fail if it can’t connect to ES (including Investigate Elasticsearch timeout can be fatal to the ingestor. #2268)

**Agnes**
- Check if updown checks the catalogue API and reports that in Slack
