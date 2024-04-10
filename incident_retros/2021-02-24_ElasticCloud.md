# Incident retro - Elastic Cloud 

**Incident from:** 2021-02-24

**Incident till:** 2021-02-24

**Retro held:** 2021-02-25

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

24 February January 2021

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1614165343000300

11.13 First alerts from updown in wc-platform / wc-experience
Front End Single Work Page
Images API Search
Front End Works Search
Images API Single Image
Works API Search 
Works API Single Work
Wellcome Images Redirect
https://wellcome.slack.com/archives/C3TQSF63C/p1614165226063400 

11.15 JP suggested moving to #wc-incident-response
11.15 AC: logging.wellcomecollection.org isn’t loading; AC: The fact that logging.wc.org is busted makes me think this might be an Elastic Cloud issue

11.15 JP: nothing here yet https://status.elastic.co/ 

11.16 Is something broken in the catalogue and hammering the logging cluster?

11.17 Doesn’t look like anything was deployed
11.17 JP restarting one of the catalogue API tasks to see if that helps
11.17 AC: all our clusters are unhealthy

11.18 JP confirmed the issue was search and work pages are down

11.19 RK suggests an elastic cloud issue

11.20 JP: nothing on their status page yet
11.20 AC manually turned staging API down to 0 tasks
11.20 Cloud console couldn’t give any useful metrics

11.22 JG emailed Laura, elastic account manager

11.25 Showing recovery; recovery messages from updown in wc-platform / wc-experience

11.29 From Laura (for future) Please send a support ticket is support@elastic.co as a severity-1 and they will look into it for you.

11.33 JG sent email and RK raised support ticket in the console

11.28 11.28 The other thing I had a concern about was a security issue (someone with access to the cloud console, with malicious intent) - but I think we can rule that out.cause I can still sign in!

11.59 RK expected to see emails to wellcomedigitalplatform@wellcome.ac.uk - which did eventually appear in RK’s spam

12.23 https://cloud-status.elastic.co/incidents/hnm8zyj41mmr - Elastic say they’ve recovered from whatever it was


## Analysis of causes

Some problem at Elastic with a proxy layer in a single region

## Actions

**Robert** Turn on 2FA for Elastic as root password is quite widely available? Robert to look at how to use SSO for logging into Elastic

**Alex** Investigate possibility of caching API responses for individual works

Have snapshots of ES clusters? Not needed as Elastic has been reliable enough so far.

**Natalie** to cc digital@wellcomecollection.org on emails letting other staff know what’s happening / tell wc-incident-response

