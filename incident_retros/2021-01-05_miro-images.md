# Incident retro - Miro images 

**Incident from:** 2021-01-08

**Incident till:** 2021-01-08

**Retro held:** 2021-01-08

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1610103089000200

8 January 2021

10.43 Alex: Should I be able to view images from Miro? I was just looking at some image search results: https://wellcomecollection.org/images?query=nydjbrr7 but any time I click "View image" I get taken to an error page: “We are working to make this item available.”
(in #wc-platform-feedback)

10.48 James calls this an incident

10.51 Jamie moves discussion to wc-incident-response

10.51 Jamie: item page data being fetched when using the View button: should be image page data; identifies branch with problem

10.55 Jamie creates PR

11.17 James: The change was made on the 2 Dec [2020], and probably deployed around then.

11.31 James: reports that fix seems to be working on stage; asks others to confirm

11.44 Fix deployed to prod but not showing up.

11.54 James confirms problem resolved after cache busting


## Analysis of causes

Item page data was being fetched when using the View button: should have been fetching the  image page data

## Actions

JG:
- Find out how many images were affected, and how many users were affected

- Find out actual date of deployment

- Go through the broken example to improve understanding (with JP)
