# Incident retro - home page with json 

**Incident from:** 2021-06-05-08

**Incident until:** 2021-06-08

**Retro held:** 2021-06-10

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

See https://wellcome.slack.com/archives/C294K7D5M/p1623163112057800 and 
https://wellcome.slack.com/archives/C01FBFSDLUA/p1623163293054600 

7 June 2021

18.21 This PR with the issue went in https://github.com/wellcomecollection/wellcomecollection.org/pull/6583

8 June 2021

14.44 https://buildkite.com/wellcomecollection/experience-deploy-prod/builds/110 build

15.38 Tom Scott reported home page borked. It was showing lots of json
 
15.40 JG asked experience devs to look at what’s been released, JG to look at rolling back

15.41 GE: I released but quite a few things went out

15.42 JG any chance to roll back as stage has the same problem

15.43 Danny Birchall suggested it might be because he’d republished On Happiness; JG confirmed it was fine, so this was a red herring

15.44 GE: rolling back

15.45 JG: rolling back

15.49 DB: /stories page also broken [ie had json on it]

15.51 GE confirmed it’s good on preview, clearing cache and live should be good too

15.55 JG cleared cache for /stories

15.52 JG putting in this fix for the bug 

15.56 JG: we’ve rolled back and are working on a fix

16:16 JG: TL;DR
We released a bug
We rolled back quickly

There’s a PR in waiting for tests to pass

9 June 2021
PR released 9:59


## Analysis of causes

- PR was about Cardigan
- Wouldn’t have thought it would touch the content apps
- json was quite low down the page so wouldn't have scrolled down that far to check
- Pull request was giant
- Deployment to prod included other changes (but might not have seen the issue even without that)
- Wasn’t deployed via Buildkite because Cardigan deploys go via main (build step only pertains to content and catalogue app, anything else is deployed automatically)
- Dummy data (json object) accidentally got deployed instead of being removed before deployment


## Actions

**DMc**
- Investigate a way to programmatically prevent json stringify from being deployed in a tsx file

**GE**
- Change the QA script for a person to check the deployment: scroll through a few top level pages including home page - DONE in [#6598](https://github.com/wellcomecollection/wellcomecollection.org/pull/6598)




