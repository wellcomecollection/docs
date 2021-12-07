# Incident retro - home page and stories page not available

**Incident from:** 2021-12-06

**Incident until:** 2021-12-06

**Retro held:** 2021-12-07

- [Timeline](#timeline)
- [Analysis of causes](#analysis-of-causes)
- [Actions](#actions)

## Timeline

6 December 2021

See https://wellcome.slack.com/archives/C01FBFSDLUA/p1638805397000300

15.42 updown alerts for
Experience: Content: Stories (origin)
Experience: Content: Stories (cached)
Experience: Content: Homepage (cached)
Experience: Content: Homepage (origin)

15.43 JP last deploy was 4 hours ago. Anyone terraforming?

15.44 JG Might be that we aren’t catering for certain prismic shapes, turns out there’s some oddities in the Prismic types

15.45 JP Lots of 400s from Prismic

15.46 JG confirmed it was a model change … It’s a grapQL thing https://wellcomecollection.cdn.prismic.io/api/v2/documents/search?page=1&pageSize=20&ordering[…]D%5Bnot(document.tags%2C%20%5B%22delist%22%5D)%5D%5D 
The application is asking for excerpt but we removed it. So a deploy should fix it.

15.47 JP why is stage working? Suggested rolling forward.

15.48 AC did the prod deploy succeed?
JP yes
JG It’s looking for the excerpt field. That doesn’t exist. Normally that’s not an issue using fetchLinks, apparently it is using `GraphQL`, which the homepage uses.

15.49 JP I’m going to deploy stage -> prod unless anyone objects

15.51 JG  way to have avoided this would be:
- remove the query for excerpts
- Deploy
- Remove the prop from the model
- Deploy to prismic

15.53 updown recovery for
Experience: Content: Stories (origin)
Experience: Content: Homepage (cached)
Experience: Content: Homepage (origin)
Experience: Content: Stories (cached)

15.54 Home and stories page back and stable 

## Analysis of causes

The application is asking for the excerpt field. That doesn’t exist. Normally that’s not an issue using fetchLinks, apparently it is using `GraphQL`, which the homepage uses.

Also, deploy to prod that AC asked about didn’t happen.

It is possible for an application that’s running to become inconsistent if the model is updated.
Model has to be updated first, then the app has to be updated.

## Actions

**Gareth E**
- Document correct order of steps for updating the Prismic model so we don’t break the site.
