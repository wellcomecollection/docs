# RFC 053: Filtering by contributor, genre, and subject

For per-subject and per-person pages, we want to filter for images and works that match a given subject/person.
For example:

*   Works by Florence Nightingale
*   Works about Charles Darwin
*   Images about mental health

This turns out to be non-trivial, so this RFC describes how we'll get there.

Strictly speaking we only need subjects and contributors for this work, but genres are so similar we should treat them in the same way.

## Requirements

1.  On per-concept pages, there's a sample of matching images/works.

2.  On per-concept pages, there's a link to a filtered search for the given concept, directly below the sample results.

3.  On work pages, the list of subjects/contributors/genres to link to filtered searches for each subject.

4.  In the works API, there are filters and aggregations for subject/contributor/genre.

5.  Given a single work in the works API, there should be an obvious way to construct a filter URL for works with the same subjects/contributors/genres as this work.

6.  The catalogues are the source of truth for subject identifiers.
    We can find equivalent identifiers, but we can't pick them from scratch.

    e.g. If a Sierra record has a subject tagged with an LCSH identifier, we can find the Wikidata subject with that identifier.
    If a Sierra record has a subject with no identifier, we can't choose an identifier, even if we could find a Wikidata subject with a matching label.

## Current behaviour

We have filters and aggregations for *label*, not ID.

## Considerations for future behaviour

If we add filtering/aggregations for subjects by ID, we already know how they'll be named: `subjects` and `source.subjects` for works and images, respectively.
This is consistent with our existing API design.

But do we add filtering/aggregations for subjects by ID?
We find ourselves in a dilemma:

*   We can't rely on filtering by label, because there may be concepts with similar/identical labels but which refer to different things.
    e.g. two members of the same family.

*   We can't rely on filtering by ID, because not all subjects/genres/contributors are identified.

From an API perspective, we could easily support both, but it's more complicated in the front-end.
How do we choose which filter mechanism to use?
How does an API client choose which filter mechanism to use?

Questions:

*   Are the requirements as stated correct?
    Are there any missing or unnecessary requirements?

*   How many identified/unidentified concepts are there in the catalogue?

*   How do we want to approach this filtering?

## An idea

We create synthetic source identifiers for unidentified subjects, which uses the label as the value, e.g.

```json
{
  "identifierType": {
    "id": "wellcome-catalogue-label",
    "label": "Wellcome catalogue label",
    "type": "IdentifierType"
  },
  "value": "Mental health",
  "type": "Identifier"
}
```

This would allow these subjects to get canonical IDs within the platform, but we don't want to put synthetic identifiers in public API responses.

Instead, we suppress them in the API response but keep the canonical ID, so you'd get subjects like:

```json
"subjects": [
  {
    "id": "axbum98n",
    "identifiers": [],
    "label": "Mental health",
    "concepts": [],
    "type": "Subject"
  }
]
```

This means every subject can be filtered by identifier, and API clients (including the front-end) can find the filter URL.

It adds some complexity to the pipeline, because we have to ensure these synthetic identifiers get scrubbed.

## See also

*   [RFC 008](../008-api-filtering): API Filtering
*   [RFC 037](../037-api-faceting-principles): API faceting principles & expectations
