# Incident retro - slow web site
**Incident from:** 2026-02-04

**Incident until:** 2026-02-04

**Retro held:** 2026-02-05


- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

4 February 2026

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1770206278034739 

#wc-platform-alerts: <br>
11.50 LogicMonitor critical Alert - LMS2852 critical - WC - What's On  <br>
11.51 LogicMonitor critical Alert - LMS2672 critical - WC - Exhibition <br>
CLEARED critical - WC - What's On <br>
11.52 CLEARED critical - WC - Exhibition <br>
11.54 critical - WC - Exhibition <br>
CLEARED critical - WC - Exhibition  <br>
11.56 critical - WC - What's On <br>
11.57 critical - WC - Exhibition <br>
CLEARED critical - WC - What's On <br>
CLEARED critical - WC - Exhibition <br>
critical - WC - Exhibition <br>
CLEARED critical - WC - Exhibition <br>

11.57 RC Pages fed by our APIs render quickly, not so much the Prismic ones? But their status is green.

11.58 SB Yeah, I don't think it's a catalogue API issue, this page load instantly: https://api.wellcomecollection.org/catalogue/v2/works

12.00 RC It's not slow locally.... Anything with AWS?

12:04 RC We've identified a faulty experience content deployment, Štěpán is kick starting a fresh one

12.07 RC Staging is also affected

12.09 SB Spike of requests coming from Vietnam. I temporarily extended the rate limiting rule to cover Vietnam

12.13 RC We think it's under control now but we'll have to talk about how many countries we're limiting…

12.23 SB the number of allowed requests is back to normal

## Analysis of causes

What happened that we didn’t anticipate?

Why didn’t our safeguards catch this?

Blanket rate limit (2500 in 5 min window)


## Actions

**GE (/RK supporting)**
- Add Vietnam to rate limiting rules (not the Captcha)
- Add staging rules (UK/US/IE only) to code, to be first in the order of rules


**JC - to think about for an OKR**
- Investigate rate limiting/caching by areas of the site (works/items/images)

**NP**
- Add to Experience planning doc: find a way to ask Google not to index stage without impacting SEO
