# API faceting principles & expectations

**Status:** Draft

**Last updated:** 16/03/2021

## Background

We've had a few conversations that keep coming up around how we expect the API to behave, particularly in terms of:

- Filter naming
- Aggregation naming
- Combined effects of filters/aggregations
- Aggregation response types
- Empty aggregation buckets

These are the components required to build a useful faceted search interface which covers numerous dimensions: so that we can do this effectively, we want these expectations to be both explicit and adhered to. This RFC is an attempt to document, question, and codify those expectations.

## Principles

**1. Filters are named by the JSON paths of the attribute they use**

For example, given a display document that looks like:

```json
{
  "a": {
    "b": [
      {
        "c": "thing1"
      },
      {
        "c": "thing2"
      }
    ]
  }
}
```

Then a document filter that filtered by the values of the `c` property would use a query string like `a.b.c`. In this example, filtering for `c` equal to `thing2` might look like:

```
http://host.name/path/docs?a.b.c=thing2
```

**2. Aggregations are always paired with identically named filters**

It is not strictly necessary that all filters have aggregations, but all aggregations must be present alongside an identically named filter for the property that is being aggregated upon. This document will refer to these as "paired" filters and aggregations. For the above example, an aggregation on the values of the  `c` property would be used like this:

```
http://host.name/path/docs?aggregations=a.b.c
```

**3. Aggregations are returned in an `aggregations` field, with the same name by which they were requested** 

This means JSON paths are still represented as strings, rather than being expanded. For example, the response to the previous example would include at the top level

```
{
  ...,
  "aggregations": {
    "a.b.c": {
       "buckets": [
         ...
       ]
    }
  }
}
```



**4. Aggregation buckets contain a `data` field of the same type as the aggregated property's parent entity**

That is to say, while we aggregate on a specific string field (for example, an ID or a label), we want to return the full entity that contains the field. This is easiest to explain by example. Given the following display documents:

```json
{
  "a": {
    "b": [
      {
        "id": "id1",
        "label": "Thing 1"
      },
      {
        "id": "id2",
        "label": "The 2nd thing"
      }
    ]
  }
}
```

Then if we aggregate on the labels like this:

```
http://host.name/path/docs?aggregations=a.b.label
```

Then our response buckets will look something like this:

```
{
  "data": {
    "id": "id1",
    "label": "Thing 1"
  },
  "count": 1234
}
```

**5. When a filter and its paired aggregation are both applied, that aggregation's buckets are not filtered**

Conversely, filters do apply to the buckets of all aggregations other than the paired aggregation. This initially confusing requirement is necessary because - for mutually exclusive values - application of the filter to the aggregation buckets will remove all but the selected bucket, thus removing the ability of the interface to show other options for the given filter. This is explained further in the [Elasticsearch documentation for `post_filter`](https://www.elastic.co/guide/en/elasticsearch/reference/current/filter-search-results.html#post-filter).

**6. When a filter and its paired aggregation are both applied, the bucket corresponding to the filtered value is always present**

Explicitly: even if other filters or queries are present which cause that bucket to be empty (ie, it has a count of 0), it still appears in the aggregation. This is necessary so that the interface for the filter can still be rendered.

**7. Aggregations on fields contained in sum types return buckets of the type's components**

In other words - there can be a discriminator present on objects meaning that aggregations on identical string properties of those objects return separate objects for each type. For example, given the following display documents:

```json
{
  "a": {
    "b": [
      {
        "label": "A thing",
        "type": "TypeOne"
      },
      {
        "label": "A thing",
        "type": "TypeTwo"
      }
    ]
  }
}
```

Then an aggregation `a.b.label` would return separate buckets for each of the objects in `b`, even though their labels (the property being aggregated) are identical, because of the presence of the discriminator field `type`.

## Open questions

- Are these rules sufficient to tell us what we expect regarding empty buckets? Namely, that they should only be present when necessary to satisfy principle (6).
- Are there cases when aggregations/filters should be named differently to rule (1)? For example, if we want to aggregate on an `id` property is it sufficient to use the name of the identified entity (eg, `a.b` rather than `a.b.id`)?