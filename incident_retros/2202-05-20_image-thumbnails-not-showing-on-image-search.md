# Incident retro -  requests not showing in account

**Incident from:** 2022-05-20

**Incident until:** 2022-05-20

**Retro held:** 2022-05-23

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

20 May 2022

See https://wellcome.slack.com/archives/C8X9YKM5X/p1653041045796299 and https://wellcome.slack.com/archives/C01FBFSDLUA/p1653041289304239   

10.30 Bug deployed convert-image-uri helper PR [#7987](https://github.com/wellcomecollection/wellcomecollection.org/pull/7987)

11.04 PB It looks like the preview images on the search images tab are all referencing the JSON description of the image rather than the image itself.

11.06 JP noted AC made changes on 19 May [that were deployed at 10.30 on 20 May]

11.08 JP Tidy up the convert-image-uri helper PR [#7987](https://github.com/wellcomecollection/wellcomecollection.org/pull/7987)  looks sus

11.11 JP  think a roll forward would look very similar to reverting that patch<br>
It makes the Image component assume it’s receiving prismic images<br>
When in fact it’s generic<br>
Going to revert: PR Revert “Tidy up the convert-image-uri helper” [#7998](https://github.com/wellcomecollection/wellcomecollection.org/pull/7998)

11.19 JP I’m going to say it’s about 12-15 minutes until we see this fix on prod (all being well)

11.21 JP Retro will be useful next week when Alex is back but a very obvious action we can start on already is adding a check for image rendering to some of our automated tests

11.23 JP idea to change from using a script that checks that URLs return 200s using cURLto use a headless browser which would also make sure there were no errors in the page

11.24 GE stage is working again

11.33 JP fixed


## Analysis of causes
PR #7987 made assumption about where things were being used (made them specific when they were still being used generically).


## Actions

**Jamie**
- change from using a script that checks that URLs return 200s using cURLto use a headless browser which would also make sure there were no errors in the page

**Alex**
- Add unit test to the affected component

**Gareth**
- Get related images back onto the image modal
