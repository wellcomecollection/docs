# Incident retro - story page appearing then replaced by a 404

**Incident from:** 2022-09-09

**Incident until:** 2022-09-09

**Retro held:** 2022-09-16

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

See https://wellcome.slack.com/archives/C8X9YKM5X/p1662729661355199

**14.21 DB identifies the initial issue**

14.21 DB this is an odd one, via digital@. this page
https://wellcomecollection.org/articles/YdQ6AhAAAJMQ5mEg 
(a story page, from 2022) is appearing, and then disappearing, to be replaced by a 404

14.31 AC made an initial guess at the fix, created PR #8434 Remember to serialise API results using superjson 

14.55 PR is reviewed and being deployed

15.14 AC may need to do a CloudFront invalidation (JP said they would do it)

**15.14 Initial fix is deployed and on staging + prod; similar issue identified**

16.11 DB still seeing the error on a different page; this time an [exhibition page](https://wellcomecollection.org/exhibitions/YjiSFxEAACIAcqpb)

16.13 JP patch needs to be applied to exhibitions too

16.15 JP confirms he’s run the CloudFront invalidation

16.22 AC I think the bug is somewhere in the interaction between fetchExhibitionRelatedContentClientSide in https://github.com/wellcomecollection/wellcomecollection.org/blob/main/content/webapp/services/prismic/fetch/exhibitions.ts and the API<br>
In particular I think we want to be using superjson to parse the response

16.31 AC The specific bug here is in the client-side fetchers we have for getting related content, eg the list of “read more” on an article<br>
That gets fetched asynchronously so as not to block the main page load, which means it doesn't go through getServerSideProps<br>
If the value includes a Date which gets serialised as a string, it may break the downstream components when they try to call date related methods on it<br>
We've fixed this in getServerSideProps with our superjson plugin, which knows how to serialise/deserialise Dates properly<br>
And when that was working, I removed all the casting of Date values to Date, because I thought it was redundant<br>
Thus exposing these API endpoints as a place where it wasn't being handled correctly

16.35 AC One thing we should capture as a result if this bug (next week!) is a list of URLs where these api endpoints return non-empty lists
There’s been a comment for a while that says “I think this might be broken”, but lack of known examples made it hard to test 

**16.35 Issues deploying to prod because of failing e2e tests, due to a bug in the initial fix**

16.39 JP pushed PR to prod

16.43 JP e2e failing
still a JSON error; this is not as bad as the page disappearing so going to override e2e tests and push to prod<br>
fyi - the URL checker is noticing this error because it is uncaught; the other one is “helpfully” caught by Next.js and turned into a readable error message

**16.45 Better fix opened that will fix e2e tests**

16.45 AC identified error: superjson expects text, not an already-parsed JSON object [#8436](https://github.com/wellcomecollection/wellcomecollection.org/pull/8436)

This is an error in the original patch

16.47 JP oh my god, weco-deploy erroring locally<br>
“Expected maxsize to be an integer or None”

16.48 AC weco-deploy bug needs a newer Python

**16.48 Better fix is merged and enters deployment process**

16.48 JP merges the second PR #8436, which starts rolling out to stage

16.59 PR #8436 is deployed and fixed in stage
17.03 prod deployment of #8436 is happening

17.07 JP Also fixed for me

**17.07 Incident done**


Tuesday 13 September
https://wellcome.slack.com/archives/C01FBFSDLUA/p1663075909007449
Enquirer reported they were having the same “Not the Wellcome you were expecting” error page. JP saw the same using Safari v 13. MR web site working in Safari v14; RC working in v15.

15.48 JP reported fixed


## Analysis of causes

Bug in datetime handling logic, and not caught by tests.

We don’t have good visibility on client side errors.

## Actions

**Alex**
- Look at how to have more resilience around related content? API failure is handled correctly
- Have a way for e2e tests to run and a person can override them for deployment

**Alex and Danny**
- Make a note of example pages where related content appears so we can do manual testing

**Gareth**
- Investigate an approach for client side errors
