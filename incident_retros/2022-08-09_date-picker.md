# Incident retro -  date picker

**Incident from:** 2022-08-08

**Incident until:** 2022-08-08

**Retro held:** 2022-08-09

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

8 August 2022

See from https://wellcome.slack.com/archives/CUA669WHH/p1659961075741759 

9.07 branch merged to remove the toggle for the date picker [#8249](https://github.com/wellcomecollection/wellcomecollection.org/issues/8249)

13.14 Email to digital@wc.org:
I just noticed that there is no drop down menu for readers to select the date for their requests at the moment. Can this be reinstated please?

13.17 AC: Email to digital@ about the missing date picker – could this be to do with the toggle removal?

13.18 DMC: sounds like a likely candidate
I’ll take a look

13.25 DMC: I think possibly the result of me having merged my branch which will have automatically removed the toggle from the json, but I haven’t deployed this morning so the code still bailing out if the toggle isn’t present (which it won’t be

13.36 date picker back on prod

## Analysis of causes

Qn: how do we (I) ensure that we don’t remove toggles until after the code that uses them is deployed?

There is only one toggles environment for stage and prod.

Merging a branch with updates to toggles updates the singular toggles environment.

Toggles turned on for the public can be turned off very quickly.


## Actions

**Jamie, David & Raphaëlle**
- Stop deploying toggles universally on merge
