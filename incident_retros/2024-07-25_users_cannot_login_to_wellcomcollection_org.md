# Incident retro - users cannot login to their accounts on wellcomecollection.org

**Incident from:** 2024-07-25

**Incident until:** 2024-07-25

**Retro held:** 2024-07-26


- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

### Thursday 25 July
Wellcome firewall migration

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1721903759248609 

10.00 NP mentioned Sierra and CALM issues in stand up, that users couldn’t log in to the desktop apps. But didn’t think it would affect our teams

10.14 Email to various library staff from Collections Systems Support (CSS) to restart laptops/refresh VPN connection if you have problems accessing Sierra and CALM

11.14 #wc-plaform-alerts:<br/>
platform-lambda-error-alarm: sierra-adapter-20200604-sierra-reader-orders<br/>
platform-lambda-error-alarm: sierra-adapter-20200604-sierra-reader-holdings<br/>
platform-lambda-error-alarm: sierra-adapter-20200604-sierra-reader-items<br/>
platform-lambda-error-alarm: sierra-adapter-20200604-sierra-reader-bibs

11.15 #wc-plaform-alerts: Catalogue API errors

11.19 #wc-plaform-alerts: identity-api-prod-5xx-alarm

11.20 #wc-plaform-alerts: Catalogue API errors<br/>
11.22 #wc-plaform-alerts: Catalogue API errors until last at 12.17

Failed login errors until last at 12.11

11.24 CSS email saying still working on Sierra desktop client issue but users can log in to the browser version

11.33 RC reported users couldn’t login on the web site

11.36 RC @weco_devs starting a chat here; Logging in is down, and we're having issues with the Catalogue API

11.37 RC It is, in turn, what fails our e2es so we can not worry about that for now. I reverted the FE code back a few days and it seems to behave the same + the code passed without problem locally, in the e2e env, as well as in staging.<br/>
If we find out it is causing issue though, we can always revert.

11.40 NP reported to CSS users can’t login

11.41 NP It looked like it was just an issue with accessing the Sierra desktop app (people have been logging in to the Sierra web app). I've asked for more info on Sierra now.

11.42 RC reverted last PR in case it affected API errors

11.44 SB We're working on fixing the logging issue, it's probably caused by the logging cluster running out of storage.<br/>
Not sure if the logging issue is related to the issues with the Catalogue API, but I can't see how those two would be connected

11.45 RC so there is the logging issue (kibana) and the log in issue (logging into the website), which I'm wondering if it's related to Sierra's issues.

11.45 NP opened statuspage incident

12.03 NP confirmed there’s no status page for Sierra and we have to hear from CSS for updates<br/>
RC suggested a banner on the site to tell users of no requesting. NP confirmed on-site users know of the issue from library staff

12.06 RC debugging out loud<br/>
https://api.wellcomecollection.org/catalogue/v2/works/xswz3swa/items <br/>
is it a valid url to query in the first place?<br/>
it's getting
```
{
"errorType": "http",
"httpStatus": 403,
"label": "Invalid API key",
"description": "Forbidden",
"type": "Error"
}
```
12.09 AG this is fine for the same work/item https://wellcomecollection.org/works/xswz3swa/items <br/>
The url you're trying to hit needs an API key to access, so can't be done freely through the browser

12.10 RC We're getting similar ones repeatedly at the moment. The page is accessible https://wellcomecollection.org/works/xswz3swa/items 

12.12 GE my understanding is that Auth0 needs to talk to Sierra

12.13 RC On the identity/aut0 page, we currently ask people to email the Library email when there's a problem with them logging in, that's interesting.

12.18 CSS report also having an issue with Sentry/Sierra so web site isn’t the only Sierra client with an issue. CSS have a call open with Sierra’s supplier

12.18 AG reported logging into library account.<br/>
NP confirmed and could make a successful request.

12.20 RC The last [API] alerts errors were fewer

12.22 AG I checked a few of the works that are throwing cloudfront errors, they're all findable/accessible online so could it just be some bots that are trying to go straight to api.wellcomecollection.org and failing for lack of api key (as they should!)

12.24 AG the /items endpoint does involve Sierra but I thought we were only making the call if the user was logged in

12.25 RC I'm relaunching my e2es and they pass, so I'll un-revert my PR.

12.37 CSS report the API issue appears to be resolved

12.39 NP closed statuspage incident

13.06 SB Logging cluster is back up and running. It's still deleting lots of documents in the background so it might be slower than usual, but I'm able to log in and use it normally now


## Analysis of causes
### What happened that we didn’t anticipate?

Sierra issue (via CSS): “D&T Networks team made a change on the network earlier this morning to resolve another issue, and it appears that III needed to restart the API junction to pick up the change.” and “apparently a knock-on from a Wellcome firewall migration yesterday.” i.e. Thursday 25 July

### Why didn't our safeguards catch this?

We did get alerts re Sierra adapter and the catalogue API - but not until much later than the incident starting 

Logging not available for looking at the issue - we were already aware of this and working to restore access.

Banner alert to tell site users that requesting/logging in wasn’t available
- Who decides when to do it? LE&E managers? Us?
- Who puts it up? Editorial? Us?
- LE&E managers unclear that Editorial can/should put up the alert


## Actions

**LB**
- Review current and desired behaviour for requestable items
- Review for optimisation of code/calls to Sierra

**SB**
- Investigate Slack alerts/dashboard for the logging cluster becoming unhealthy
- Document in GitBook how to address logging issues using the web-based console

**AG**
- Check logs (if they exist)
- What was wrong with Sierra and when - talk to Collections Systems Support
  
**NP**
- Talk to Digital Content Manager and LE&E manager re putting up banners on the site for incidents
- Create incident reference page in Notion e.g. Prismic or non-Prismic banner (for if NP is not around/so everyone can see what to do)
