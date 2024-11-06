# Content API: Functional content search

[Background information](#background-information)
[Proposal](#proposal)

## Background information

The goal with the Content API has always included some level of functional content search being possible. We define "Functional content" as "Visitor Information Content", which represents an array of content types in Prismic. In this RFC, we'll attempt to define which ones they are, how they will be indexed, and which methods we will use to search across them using one endpoint.

It is important to understand the distinction between the "All" search, and the "Functional content search", to ensure we are using the same language.

The "All" search relates to the `/search` page, where you can use a keyword query to search across Content and Collections. The "Functional content search" relates to a sub-selection of Prismic content types which we want to expose in the search but that don't warrant their own search page, unlike, for example, Stories, which have `/search/stories`.

Now let's discuss those content types:

### Affected content types
- Pages
- Visual stories
- Exhibition text
- Exhibition highlight tour
- Books
- Projects
- Seasons

To note: so far, only Visual Stories and Books have the potential to require this endpoint for listing pages. Otherwise, this will only be used in `/search` ("All"), in conjunction with our other API endpoints.

## Proposal