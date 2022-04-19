# RFC 047: Changing the structure of the Catalogue API index

We use the Elasticsearch index for the catalogue API for several purposes:

*   To serialise the public API responses
*   To index and search documents
*   To help debug the API and the pipeline

Currently the documents in this index are a serialisation of the "internal model", which has to support all of these uses.
This causes a number of problems:
When the API returns a response, it converts the internal model into a display model.
This creates a strong coupling between the internal model and the API, which has been a long-running source of complexity.

This RFC proposes a new structure for the Catalogue API index which should remove this coupling.

## Proposal

We restructure documents in the API index to have three top-level fields:

-   The `display` field contains the complete display document as a block of JSON.
    The API will return the contents of this field in public responses.

    This field is mapped in the Elasticsearch index as an object field with [enabled=true](https://www.elastic.co/guide/en/elasticsearch/reference/current/enabled.html), meaning Elasticsearch will ignore it for indexing.

-   The `query` field contains the values that we're indexing, e.g. work title.
    This will contain a subset of the work/image data that is indexed and analysed by Elasticsearch.

    This field must be consistently defined between the pipeline and the API, or values won't be in the right place for queries.

-   The `debug` field contains the values that we use for debugging the pipeline, e.g. the date a document was indexed.

    This field should only contain information that the API can ignore.

## Implementation

We can add these fields progressively, rather than in one massive update.
This is a rough approach, which we could do for all three top-level fields separately:

1.  We copy the display models into the pipeline repo, and modify the ingestor to store these new fields.
    This is a strictly additive step.

2.  We reindex the pipeline to add this field to all documents (this could be a new pipeline, or we could do it in-place in an existing pipeline).

3.  We update the catalogue API to use the new fields for public API responses, rather than handling its own models.

4.  We remove fields from the indexed Work model that aren't used for indexing/debugging.

## Future work

*   Rewrite the API in TypeScript.
    This is explicitly out of scope here – let's not try to change too much at once.

    Although this change opens the door to a TypeScript-based API, let's stabilise the index structure before we start changing the API.

## Open questions

*   Are these the best names for these fields?

*   Currently the API will check for internal model compatibility before it starts.
    Do we still want equivalent behaviour with index mappings?

    Because this change is meant to decouple the internal model and the API, I think we could get away with scrapping it for now – and bringing it back if and only if we see issues, rather than converting it to use index mappings pre-emptively.

*   Can we expunge the internal model library from the API repo entirely?

    We won't be using it in the application code, but it does have Work generators and index mappings that we use extensively in API tests.
    I think we have to keep it, but if we could get rid of it we'd get to simplify some build processes.
