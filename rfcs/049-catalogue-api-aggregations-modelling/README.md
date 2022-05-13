# RFC 049: Changing how aggregations are retrieved by the Catalogue API

For [RFC 047], we changed the catalogue API to serialise public API responses from an opaque `display` field in the Elasticsearch documents.

Previously we were storing the pipeline's internal model in Elasticsearch.
The API would retrieve the internal model, parse it, and convert it into the display model -- all as part of serving the request.
Now, the pipeline creates the display model and stores it in a new `display` field in Elasticsearch.
The API retrieves the `display` field, and treats it as opaque JSON -- without any knowledge of its structure.

We'd hoped this would allow us to remove the internal/display models from the API repos, but the current implementation of aggregations make this tricky.

This RFC proposes a change to how aggregations are handled that should remove this obstacle.

[RFC 047]: ../047-catalogue-api-index-structure.md



## Context: the desired behaviour

Clients of the catalogue API can request aggregations of certain values (e.g. languages, licenses, work types).

These are presented as a list of `AggregationBucket` in the API responses, i.e.:

```
AggregationBucket[T] {
  data: T
  count: Int
  type: String
}
```

where `T` is the same as the value appearing in the Work model.

For example, languages on a work appear as follows:

```
{
  "languages": [
    {
      "id": "eng",
      "label": "English",
      "type": "Language"
    },
    {
      "id": "fre",
      "label": "French",
      "type": "Language"
    }
  ],
  ...
}
```

and we see that `Language` type in the aggregation buckets:

```
"aggregations": {
  "languages": {
    "buckets": [
      {
        "data": {
          "id": "eng",
          "label": "English",
          "type": "Language"
        },
        "count": 691840,
        "type": "AggregationBucket"
      },
      {
        "data": {
          "id": "fre",
          "label": "French",
          "type": "Language"
        },
        "count": 67187,
        "type": "AggregationBucket"
      },
...
```

This presents a clean, consistent interface to clients – a value looks the same whether it's in a work or in an aggregation.

We don't want to change this behaviour.



## The current implementation, and the problems it poses

The API uses [Elasticsearch aggregations][es_aggs] to aggregate over a field in internal model.
Elasticsearch will return single string values, which the API then serialises into the display model.

For example, our language aggregation starts as [an ES terms aggregation][terms_agg] over the `data.languages.id` field:

```http
GET /works-indexed-2022-04-28/_search
{
  "aggs": {
    "languages": {
      "terms": { "field": "data.languages.id" }
    }
  }
}
```

The Elasticsearch API response can only use a single string in its buckets, for example:

```
{
  "aggregations" : {
    "languages" : {
      "buckets" : [
        {
          "key" : "eng",
          "doc_count" : 691840
        },
        {
          "key" : "fre",
          "doc_count" : 67187
        },
        ...
```

The API has to contain enough internal/display model logic to interpret these values -- to know that, say, `eng` means English and it's serialised as id/label/type.
This is precisely the sort of model coupling we're trying to get away from.

For more complex types, we've had to jump through hoops to shoehorn aggregations into this approach -- e.g. contributor values are stored like `person:Henry Wellcome` because we need both the type and the label to return them correctly.

It would be nice if we could remove this coupling and simplify how aggregations work in the API.

[es_aggs]: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations.html
[terms_agg]: https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html



## Proposed solution

We add a new field `query.aggregatableValues` to the documents we store in Elasticsearch.

```
type Query {
  aggregatableValues: Map[String, List[String]]
  ...
}
```

where the keys are the aggregation types (languages, work types, licenses) and the values are lists of display JSON stored as strings.

This is easiest to understand with an example:

```json
{
  "id": "example-work",
  "query": {
    "aggregatableValues": {
      "languages": [
        " { \"id\" : \"eng\", \"label\": \"English\", \"type\": \"Language\" } ",
        " { \"id\" : \"fre\", \"label\": \"French\", \"type\": \"Language\" } "
      ],
      "items.locations.license": [
        " { \"id\": \"pdm\", \"label\": \"Public Domain Mark\", \"url\": \"https://creativecommons.org/share-your-work/public-domain/pdm/\", \"type\": \"License\" } "
      ],
      ...
    }
  },
  ...
}
```

The ingestors would populate these `aggregatableValues` fields when it indexed a work.
This would be mapped as a `keyword` field in Elasticsearch.

The API would aggregate over these fields specifically, and copy the values into the `data` field of our aggregation buckets.

This would allow us to reduce the amount of model logic in the API, and would ensure a consistent rendering of values in aggregations and works.
