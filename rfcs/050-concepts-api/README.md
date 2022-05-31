# RFC 050: Design considerations for the concepts API

This RFC collects some initial thinking on how we might represent concepts in the catalogue API.
It's a starting point for discussions; not a final design.



## Goals

*   We want to be able to create per-person and per-subject pages on the website.
    The data on these pages should come from the new concepts API.

*   These pages should contain enough context to distinguish two people/subjects (e.g. whether "Charles Darwin" is the famous naturalist, his uncle, his son, or his grandson).

*   We're not trying to replicate Wikidata -- the APIs shouldn't return large amounts of information we aren't going to use on wellcomecollection.org.

*   Any new APIs should be similar to the existing works and images APIs.
    We'll use the same conventions for filters, aggregations, including optional fields, and so on.



## Endpoint #1: retrieve a single concept

This is the single concept endpoint, which is used to render a page for an individual subject or person:

```
GET /concepts/azxzhnuh
{
  "id": "azxzhnuh",
  "identifiers": [
    {
      "identifierType": "lc-names",
      "value": "n12345678",
      "type": "Identifier"
    },
    ...
  ],

  "label": "Florence Nightingale",
  "alternativeLabels": [
    "The Lady with the Lamp",
  ]

  "type": "Person|Subject|Organisation|Place"

  // Everything above here is stuff I'm pretty sure we'll need;
  // everything below it is more nebulous and more likely to change
  // in the final API.

  "description": "Florence Nightingale was an English social reformer, statistician and the founder of modern nursing. Nightingale came to prominence while serving as a manager and trainer of nurses during the Crimean War, in which she organised care for wounded soldiers at Constantinople.",

  // not locations
  "urls": [
    "https://en.wikipedia.org/wiki/Florence_Nightingale"
  ],

  // cf productionEvent?
  "dates": [ { date, meaning } ]
  "places": [ { place, meaning } ]
  "birthDate/place"
  "deathDate/place"

  "thumbnail": { … },

  "connectedConcepts": [
    {
      "id": "asoiham1",
      "label": "Crimea",
      "type": "Place"
    }
  ]
}
```

Notes:

-   The `id` and `identifiers` fields are the same as on existing works/images.

-   The `label` and `alternativeLabels` fields are named analogously to `title` and `alternativeTitles` on works.

-   The `type` will be an enumeration that includes Person, Organisation, Meeting, Subject.
    For the initial implementation we'll likely have a few subtypes of Person but not of Subject.

    The alternative is to have `type: Concept` and do subtypes through something similar to workType/format, but I'm not sure that adds anything.

    This is a value users would be able to filter on (if we provide an endpoint for listing/searching concepts).

    Although conceptually we know that Person/Organisation/Meeting are subtypes of Agent, the API doesn't.
    For example, if you wanted to present a list of agent-like things, you'd use a filter `type=Person,Organisation,Meeting` rather than `type=Agent`.

-   The `description` should provide enough context to help users distinguish subjects/people with the same label but different meaning.
    This will likely be drawn from LCSH or Wikidata initially, but at some point we might write our own content here.

    Q: Is `description` the best name for this field, or should it be called something different?

-   The `urls` list points to this subject/person elsewhere.
    We aren't trying to replicate LCSH/MESH/Wikidata; if somebody wants to read more in-depth about a given concept, we should link them to an external entry.

    In works we use digital locations in `work.items.locations` to link to external resources.
    We don't want to reuse that structure, which is more complicated than we need here.

    Q: Aside from the URL, what other values do we want for these links?
    e.g. link label

    Q: Do we need these values at all?
    If we put the Wikidata ID in the list of identifiers, do we leave clients to construct a URL, or do we provide it in the API?

-   The `date`/`place` information is somewhat speculative.

    We think we might include birth/death information on per-person pages; we could also link to significant dates and places and use that as a way to link between concepts.
    This is similar to production events on works.

    We can start with a `birthDate/birthPlace/deathDate/deathPlace` field on the initial version of the API, and decide if we want to put this information on per-person pages.
    If yes, we can think about how to model this properly.
    If no, we can scrap all of these fields.

-   The `thumbnail` field uses the same model as the works API; whether we add it depends on the designs we use.
    If we want a thumbnail on (1) the per-concept pages or (2) the snippet that links to per-concept pages, we'll use this field.
    If not, we won't add it.

-   The `connectedConcepts` field lets us link between concept pages.
    It contains a simplified subset of a Concept's fields; enough to render a link but nothing more.

    We want the connections between concepts to be discoverable from a single concept endpoint, but behind an include.

    We don't want to describe how two concepts are connected yet; this is significantly more complicated.
    When we do, we'll put them in different properties (similar to `partOf` and `parts` in the works API).

    Connectedness/relatedness is not symmetric.
    e.g. many things might link to a large, generic subject like "London", but it won't back-link to them in return.



## Endpoint #2: Concepts in the works API

We'll simplify how concepts appear in the works API.
We'll provide enough information to render a link to the per-person or per-subject page, but nothing more -- for detailed information, use the concepts API.

For example:

```
GET /works?contributors.agent=azxzhnuh
{
  …,
  "contributors": [
    {
      "agent": {
        "id": "azxzhnuh",
        "label": "Florence Nightingale",
        "type": "Person"
      },
      "roles": [
        {
          "label": "Author",
          "type": "ContributionRole"
        }
        ...
      ]
    }
  ]
}
```



## Endpoint #3: Listing and searching concepts

This will look similar to the works and images endpoints:

```
GET /concepts
{
  "type": "ResultList",
  "results": [...]
}
```

The `results` list would contain the same objects as returned from endpoint #1.

This API would only return concepts that are used somewhere in our catalogue.

Q: If you find a concept in this API, you know it's somewhere in the works catalogue.
Is there any way to know whether you should be filtering by subjects/contributors to find a matching work?

Filtering, querying, aggregations, and so on, would follow the same patterns as the works and images APIs.
We don't need to decide the details of this yet.

We'll add this endpoint because it's consistent with works and images, and even if we won't use it, other people may use it to do other interesting things.



## Next steps: building a prototype

*   We could build a minimal version of endpoint #1 pretty quickly, using our existing indexes (id, identifiers, label, alternativeLabels).

    We'd need to index the ID on subjects, but then you could build an endpoint by:

    *   Filtering the index for `subject.id=<id>`
    *   Extracting the subject from the first Work in the results
    *   Adapting that into the shape of the new API response

    That would allow us to start using that API in prototype subject pages.

*   We'd need to pull in LCSH/MESH/Wikidata data to populate the other fields, but we could hard-code information in the API without building a full pipeline to flesh out the API and do more testing of concept pages.

    In turn, this might inform which fields we want to prioritise pulling through properly.
