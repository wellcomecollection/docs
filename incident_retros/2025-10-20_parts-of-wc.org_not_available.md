# Incident retro - parts of wc.org not available

**Incident from:** 2025-10-20

**Incident until:** 2025-10-20

**Retro held:** 2025-10-23


- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

20 October 2025

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1760951167805789

09.03 [First alarm on Slack](https://wellcome.slack.com/archives/CQ720BG02/p1760947383226629) <br>
Home page, what’s on and exhibitions showing an internal error message. Other parts of the site were available including search.

9.03 onwards AG and RK debugging and identifying issue<br>
RC suggesting banner, all agree

9:42 RC struggling with putting the non-Prismic banner up because of Cloudfront(?) . It did deploy to S3 okay but took c. 25 mins to display via the toggle

9:57 RC tried to display banner by modifying code and deployed, but realised tests (which relied on Prismic content) would block it, so new things couldn’t be passed to production

10:0…? RK tries to do it manually (?)<br>
Toggles finally kick in so we leave it as is. Toggles are read through Cloudfront. Refreshing the CF cache took some time but eventually did refresh.

10:30 homepage available, still showing error for some users due to caching

10:35 PB - invalidate cache, finished ca. 1115

11:25 RK: Looks ok now. Prismic status has gone green, AWS have said they "continue to see resolution"
Plan is to give it till 12:30 and if we don't see any further issues to remove the banner and declare things OK again.

12:33 Banner removed because Prismic’s status was showing it was okay again 


## Analysis of causes

What happened that we didn't anticipate?
- Increased error rates and latencies for multiple AWS services in the US-EAST-1 Region ([AWS dashboard](https://health.aws.amazon.com/health/status?eventID=arn:aws:health:us-east-1::event/MULTIPLE_SERVICES/AWS_MULTIPLE_SERVICES_OPERATIONAL_ISSUE/AWS_MULTIPLE_SERVICES_OPERATIONAL_ISSUE_BA540_514A652BE1A)), breaking a lot of the services we use, such as Prismic.<br>
https://status.prismic.io/incidents/01K808EM0TEWWX74VG0T6J9WHA 
- We have a banner we can put up when Prismic is down, but it relies on our Toggles, which rely on AWS services (S3/Cloudfront). It eventually worked but took longer than usual to display. 
- In the meantime, we tried to display the banner by deploying changes to the codebase, but Content tests and “Diff Prismic Linting” failed as they rely on the Prismic API, blocking the deployment.
- Statuspage not available for updating: emailed instead
- Are correct people listed for comms?

Why didn’t our safeguards catch this?
- Updown and Logic Monitor also affected by the AWS outage

## Actions

**NP**
- Email comms head to check who are the correct people for the comms list - done and list updated in Statuspage and Notion 20/10/25

**RC**
- Ask Prismic if they are looking at how to improve their response/ask in their forum - done: 'Can't find anything on the forums aside for more "we'll be updating our status page"'

**For sprint planning**

**GE/RK**
- Document how to bypass CI process with a local script

**RC/RK**
- Figure out a range of how to avoid this in future e.g.
    - Static site generation
    - Caching eg display a good copy if you get a 500 from the origin https://aws.amazon.com/about-aws/whats-new/2023/05/amazon-cloudfront-stale-while-revalidate-stale-if-error-cache-control-directives/
    - Cache in the application

**RC**
- Write ticket to look into test content for what it fetches fresh from Prismic - can these be mocks? - done [#12414](https://github.com/wellcomecollection/wellcomecollection.org/issues/12414)


**DM**
- Diff custom types test - how to run this only when it’s useful
