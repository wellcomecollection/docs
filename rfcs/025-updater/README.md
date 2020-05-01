# RFC 024: Updater

**Status:** 🏗 Draft 🚧

**Last updated:** 2020/05/01

## Problem

We are now able to take data from the catalogue pipeline
and, via inferrer service, enrich that data and store it in
other indeces.

While this is incredibly useful, namely to

* be able to query by this enriched data via the `/works` endpoint
* display much more interesting, clean, and consitent versions of the tranformed 
data on the `/works/data` endpoint.

An example of search would be someone searching for `Vinayaka`.

Whilst we have loads of works on `Ganesha`, these will never be
surfaced in our current state.

By having an enriched concept as part of the work, we would be able to.

e.g.
```
{
  "type": "Work"
  "concepts": [
    {
      "label": "Ganesha",
      "aka": ["Vinayaka"]
    }
  ]
}
```

Synonyms is just an example of where this setup will bring much benefit.

Outdated language, robust data cleansing, autocomplete, filtering,
peace love and understanding are just a few areas that this would impact positively.
