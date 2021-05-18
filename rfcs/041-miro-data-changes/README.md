# Tracking changes to the Miro data

The Miro data was originally exported as a collection of XML files, one per letter prefix.
We have split these XML files into a series of JSON files, one per image.
These JSON files are stored in S3, with a pointer in DynamoDB:

```
MiroSourcePayload {
  id: String
  isClearedForCatalogueAPI: Boolean
  location: S3ObjectLocation
  version: Int
}

S3ObjectLocation {
  bucket: String
  key: String
}
```

Although the Miro data is static, we may change how we want to use it.
For example:

-   A contributor may ask us to remove an image from the site
-   We may change the license on an image
-   We may make an image available that we were previously unsure about

We need a way to apply these changes and record them.

### Principles

-   We should be able to override specific values in the Miro data/transformer.
    We should assume we will asked to make changes on an ongoing basis -- this isn't a one-off operation.
-   We should keep a record of our changes: who made them, when, and why
-   Our changes should be separate from the Miro exports

### Proposal

We extend the `MiroSourcePayload` model with two optional fields:

```
MiroSourcePayload {
  id: String
  isClearedForCatalogueAPI: Boolean
  location: S3ObjectLocation
  version: Int
  events: List[MiroUpdateEvent]?
  overrides: MiroSourceOverride?
}
```

The `MiroUpdateEvent` model will track our changes to the data:

```
MiroUpdateEvent {
  note: String
  date: Datetime
  user: String
}
```

and the `MiroSourceOverride` model will allow us to track overrides:

```
MiroSourceOverride {
  license: License?
}
```

This model can be extended to add new overrides as necessary.

When we make changes to a Miro record, we add a new MiroUpdateEvent to record the change, and we update the DynamoDB record.
This gives us change tracking that preserves the integrity of the original Miro data in S3.
