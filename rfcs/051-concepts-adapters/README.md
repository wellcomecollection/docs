# RFC 051: Ingesting Library of Congress concepts

This RFC outlines the design for the first phase of the concepts pipeline, specifically focusing on ingesting concepts from the Library of Congress (LoC) and preparing them for use in the Wellcome Collection catalogue.

**Last modified:** 2022-07-08T10:08:48+01:00

# Context

As per the high-level design of [RFC 052](https://github.com/wellcomecollection/docs/pull/83), one of the key areas of the concepts pipeline topology is an ingest section. This RFC outlines how this will be implemented for the first work phase (attaching only LoC concepts to works).

![High level outline of the architecture in this RFC](https://user-images.githubusercontent.com/4429247/177178393-8fd615f1-f178-4a0a-83b2-a1d5ee09634f.png)

### Retrieving concepts from bulk exports
LoC provide bulk exports of all [subject headings](https://id.loc.gov/authorities/subjects.html) (LCSH) and [names](https://id.loc.gov/authorities/names.html) (LCNAF). These come in variety of flavours: in both MADS and SKOS vocabularies; and in N-Triple, JSON-LD, Turtle, and XML formats. All of the bulk exports are gzipped.

We can re-run the ingest process on a schedule to capture the (infrequent) changes to LoC concepts, which are almost always additions rather than changes/deletions. 

In the architecture diagram above, the "adapter" and "transformer" are outlined as separate services. In practice, we can perform this mini-ETL operation more efficiently and simply as a streaming operation within one service when we use the gzipped JSON-LD files; these express "one concept per line" and so we needn't worry about traversing any trees or indeed caring much about the underlying RDF.

![A more detailed view of how a concepts ingestor might work](https://user-images.githubusercontent.com/4429247/177571629-56f7dd7b-9c43-4f38-bb11-aae53ed0c2e6.png)

The "transform" step here is (a) the most ill-defined and (b) the only step that needs to differ for LCSH and LCNAF ingestors.

### Transforming external concepts 

[RFC 050](https://github.com/wellcomecollection/docs/tree/main/rfcs/050-concepts-api) outlined the rough design of a concepts API: obviously, we need to store the external concepts in a way that is sufficient to construct these API documents. We also don't want to extraneous data, as the majority of the concepts won't be used in the catalogue. 

Based on this, we might transform the LCSH documents to something like:

```json
{
  "_id": "lc-subjects_sh12345678",
  "identifier": {
    "value": "sh12345678",
    "identifierType": "lc-subjects",
    "type": "Identifier"
  },
  "label": "<value of skos:prefLabel>",
  "alternativeLabels": [
    "<values of skos:altLabel>"
  ]
}
```

where the document `_id` is a QName-type identifier (but using an underscore instead of a slash so as not to cause headaches in ES).

We might also want to add some metadata about the source data provenance (eg the date that the dump is from).

### Ingesting changes 

_This section is a bit speculative - we don't necessarily need the answers right now._

We can start by just writing all of the source into an empty index - this is inefficient and we won't know what (if anything) changed, but it will never be wrong.

We want to know what's changed in the source data because we want to trigger downstream activity based on updates. To know what's changed, we have to start comparing to what's there already. 

This is of course very inefficient, but we can pass that inefficiency onto the ES cluster by using the [`doc_as_upsert`](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html#doc_as_upsert) feature of the `update` API alongside the [`noop`](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-update.html#_detect_noop_updates) feature: with a single API call we'll be able to know whether anything was added.

This leaves us with detecting deletions: the least likely kind of change (in fact, we're not sure if it ever happens?). I don't think this needs to be addressed right now - if it's something we become aware of we can just write into an empty index again.

## Questions

- The format proposed above doesn't follow the existing schema for `identifierType` - rather than just the id we have previously used an object for `identifierType`, like
  ```json
  {
    "id": "lc-subjects",
    "label": "Library of Congress Subject Headings (LCSH)",
    "type": "IdentifierType"
  }
  ```
  Is this OK? **Yes, we prefer this**
- Is the non-default `_id` on the documents actually necessary? **It's useful to be able to construct queries for these concepts, and the identifier proposed is scalable to various source schemas**
