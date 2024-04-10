# Incident retro - Prismic model changes

**Incident from:** 2023-06-12

**Incident until:** 2023-06-12

**Retro held:** 2023-06-14

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1686565392141259 

12 June 2023

11.18 RC deployed Prismic model

11.21 Someone on Content team published new content

11.23 Updown alerts for
Homepage (origin)
Homepage (cached)
Stories (origin)
Stories (cached)

JP Home page down
Cannot find slice of type soundcloudEmbed
Cannot find slice of type vimeoVideoEmbed
Cannot find slice of type instagramEmbed
Cannot find slice of type twitterEmbed
Cannot find slice of type youtubeVideoEmbed

11.23 RC I've just changed the model to remove those
I wasn't sure which order was required

11.24 AC “WARNING: If you are removing fields from a custom type, you must remove any queries for those fields from the content app and deploy the changes to the content app first, before deploying the changes to Prismic.”
https://github.com/wellcomecollection/wellcomecollection.org/tree/main/prismic-model  

We’ve been bitten by this before, I should have remembered when I reviewed the PR

RC It's deploying as we speak, I'll have it go to prod asap

[Rolling forward; est 13-15 mins until back up]

11.26 AC Note: you can fix immediately by checking out a version of prismic-model prior to your change
And deploying the custom types to put those queried fields back
So the currently-executing queries will start working again

RC yeah it's all of them though. or can you update them all in one go?

AC: I don’t think so. it’s a bit fiddly, but I think worth doing?

11.30 still 500ing although RC thought it should be back up; needed a new instance of Prismic content

11.34 AC I’ve published a change in Prismic (fixing a lint error) and now prod is back up

11.35 RC triggering prod deploy now

11.35 Updown up alerts for restored
Stories (cached)
Homepage (cached)
Homepage (origin)
Stories (origin)

11.42 AC so now prod is deployed, I think you should be safe to re-deploy the custom Prismic types

11.43 RC yeah was just waiting for e2es, in case will deploy asap

11.46 RC re-ran the type deploys and republished a random page in prismic, still up

## Analysis of causes
- We had an outage that started about half an hour ago, caused jointly by [1] deploying some changes to a custom model at ~11:15 and [2] somebody making a change in Prismic at 11:21 (when the site went down)
- We identified the issue quickly in the logs, rolled back the changes to the Prismic model, and published another change at 11:34 to bring the site back up
- Once we’d rolled forward the front-end apps, we redeployed the changes to the Prismic model

Unsafe deployment of changes to the model

## Actions

**Alex & Raphaëlle**
- Put a warning in the deploy tool to warn when deleting fields, including a prompt to publish
- Change the deploy tool to update all types in one go

**Raphaëlle & David**
- Improve readme documentation about how to remove fields
