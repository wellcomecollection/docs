# Incident retro -  works search errors

**Incident from:** 2022-05-24

**Incident until:** 2022-05-24

**Retro held:** 2022-05-26

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

24 May 2022

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1653408854658319

15.03 alerts for errors in the catalogue API, followed by a continuous stream of alerts for cloudfront 

15.15 (approx) CCR of works index started from pipeline cluster into rank cluster

16.00 (approx) HP noticed 500 and asked if search was broken in #wc-incident-response, later deleted that message as reran search and it worked as expected

17.14 AC https://wellcomecollection.org/works?page=1&query=conosceva 
looks like the API is unhappy

Saw api was flaky

Cleared index caches which didn’t help

Suggested check refresh interval seen in previous issues - wasn’t that

A rolling restart did fix the issue

PB That link works for me in production but not if I switch my toggle to staging api

17.43 AC We seem to have fixed the issue



## Analysis of causes
Combination of different factors:
- CCR was the trigger which depleted some resource
- Increased document size was a contributing factor
- Not being able to clear out the circuit breakers


## Actions

**Harrison**
- Add notes to rank documentation as reminders for:
    - Increase cluster size when doing a CCR as that is memory intensive and remember to turn down the size afterwards
    - More communication with colleagues when you’re about to use CCR
    - CCR works and images separately


**Alex**
- Improve alerts in Slack so it’s easier to triage and spot new errors - DONE

**Team**
- Fix known errors in Slack as they arise
