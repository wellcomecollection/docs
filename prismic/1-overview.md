# 1. Overview

Prismic is a third party content management system. Users can log into the Prismic UI and create content based off underlying 'Content Types'. These 'Content Types' are based on Prismic Models, and they model the expected fields that a Content Type should have. We can call the Prismic API to query this content, parse/transform it and render it where we want it to go on weco.org.

The core of the Prismic setup is available in [this repo](https://github.com/wellcomecollection/wellcomecollection.org/tree/main/content/webapp/services/prismic), and the models are in [here](https://github.com/wellcomecollection/wellcomecollection.org/tree/main/prismic-model).
When you visit the [Prismic Rest API](https://wellcomecollection.cdn.prismic.io/api/v2) you will see a summary of our Prismic instance, including all available content types which are pulled from the models.

In `content/webapp`, where weco.org content lives, we fetch data, transform it and pass it to the relevant pages on the content webapp to serve on weco.org. We fetch content using a number of methods, mainly graphQuery, fetchlinks/predicates. We recently implemented use of the GraphQL endpoint from the Prismic API at `catalogue/webapp`, so that we can best query content types for search of stories, events and exhibitions.

The `types` object within that REST API response looks like this:
```
"types": {
    "webcomic-series": "[Deprecated] Webcomic series",
    "teams": "Team",
    "people": "Person",
    "popup-dialog": "Popup dialog",
    "project-formats": "Project format",
    "page-formats": "Page format",
    "global-alert": "Global alert",
    "interpretation-types": "Interpretation type",
    "exhibition-resources": "Exhibition resource",
    "exhibition-formats": "Exhibition format",
    "guide-formats": "Guide format",
    "labels": "Label",
    "collection-venue": "Collection venue",
    "card": "Card",
    "editorial-contributor-roles": "Contributor role",
    "event-policies": "Event policy",
    "event-formats": "Event format",
    "article-formats": "Story format",
    "audiences": "Audience",
    "background-textures": "Background texture",
    "organisations": "Organisation",
    "exhibition-guides": "Exhibition guide",
    "stories-landing": "Stories landing",
    "articles": "Story",
    "webcomics": "Webcomic",
    "exhibitions": "Exhibition",
    "books": "Book",
    "guides": "Guide",
    "seasons": "Season",
    "places": "Place",
    "events": "Event",
    "pages": "Page",
    "projects": "Project",
    "event-series": "Event series",
    "series": "Story series"
  },
```

*Interesting to know: You'll notice that our content types are often given plural names e.g. articles, this means they are mapped to the Prismic GraphQL schema as `allArticless`.*