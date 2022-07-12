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

2.  On per-concept pages, there's a link to a filtered search for the identified concept, directly below the sample results.

3.  On work pages, the list of subjects/contributors/genres link to:

    -   a concept page if the subject/contributor is identified (new behaviour)
    -   a filtered search by label if the subject/contributor/genre is unidentified (existing behaviour)

4.  In the works API, there are filters and aggregations for subject/contributor/genre that support (3).

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
How do we handle this in the front-end?

Consider the following flows in the front-end:

1.  A user lands on the concept page for "mental health".

    This includes a list of works with that identified concept.
    When they click to see the full list of works, they should see filtered search results.

    This filtered search must use ID filtering, because there may be concepts with similar/identical labels but which refer to different things.
    e.g. two members of the same family.

    Q: How do we distinguish this in the UI from a label search for "mental health"?

    Q: Should a user be able to discover this filter through the search UI?
    If they remove the filter, can they re-add it without going via the concepts page?

2.  A user is on a search page.
    They want to filter by subject.
    They click the dropdown to see a list of available subject filters, and pick one.

    Q: Is the list of available subjects based on ID or label?
    Is it a mixture of both?

    Q: How do we distinguish between a filter for the label "mental health" and the identified concept?

    Q: How do we distinguish between two identified concepts with the same label?

Questions:

*   Are the requirements as stated correct?
    Are there any missing or unnecessary requirements?

*   How many identified/unidentified concepts are there in the catalogue?

*   How do we want to approach this filtering?

## See also

*   [RFC 008](../008-api-filtering): API Filtering
*   [RFC 037](../037-api-faceting-principles): API faceting principles & expectations
