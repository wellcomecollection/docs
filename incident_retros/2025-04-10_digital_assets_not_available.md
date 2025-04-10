# Incident retro - digital assets not available

**Incident from:** 2025-04-10

**Incident until:** 2025-04-10

**Retro held:** 2025-04-10


- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

10 April 2025

See https://wellcome.slack.com/archives/C02ANCYL90E/p1744276895179669 

10.21 JC reported this work is showing an internal server error, this is a TEI record: https://wellcomecollection.org/works/axqp36b6  (MS Sinhalese 326). Similar issue reported by an enquirer by email on 10 April at 9.55

10.44 SB it looks like it's not an issue with the catalogue API — the response looks as expected:<br>
https://api.wellcomecollection.org/catalogue/v2/works/axqp36b6 <br>
https://api.wellcomecollection.org/catalogue/v2/works/bekbcf63 <br>

10.46 AG Looks like it's happening with anything that has digital asset. Could it be the IIIF cloudfront changes applied this morning?

The catalogue API is fine <br>
https://api.wellcomecollection.org/catalogue/v2/works/a22qnrb4 <br>
for this work that is not fine https://wellcomecollection.org/works/a22qnrb4 

10.49 AG messaged Digirati 

Digirati checked logs but couldn’t see anything because the block occurred before the logging. Recommended reverting.

11.02 AG 
[10/Apr/2025:10:00:00 +0000] "GET /works/a22ndzm4 HTTP/1.1" 500 90095 "-" "Amazon CloudFront"
But
[10/Apr/2025:09:55:51 +0000] "GET /api/works/items/a22ndzm4 HTTP/1.1" 200 849 "-" "Amazon CloudFront" <br>
So it's intermittent

11.08 AG I'm checking out the commit on main just before the WAF changes
https://github.com/wellcomecollection/platform-infrastructure/commits/main/55180b77af92d388dc97fad5c0990ab271490a6d 
and running terraform from there [to reform the terraform changes to see whether it gets things back to normal]

11.10 AG Plan gives us
Plan: 0 to add, 7 to change, 6 to destroy.
Which matches what was changed/created this morning

11.15 AG Apply in progress

11.35 SB It looks like it recovered after the terraform apply. (I think that some pages might still return 500 for a while due to caching)

12.11 incident closed

## Analysis of causes

weco.org firewall block was applied to IIIF firewall and Digirati added to the blocks


## Actions

**Digirati via AG**
- IIIF WAF count rather than block to see how many there are
- Ask Digirati if they have load monitoring

**SB**
- Give Digirati info on IIIF WAF rules

Following answers from above:
- set alam on CF if blocking more than x% requests to the site
- extend CF alerting to IIIF instances
