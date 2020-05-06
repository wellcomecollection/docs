# RFC 023: Images endpoint

**Status:** :construction: Draft :building_construction:

**Last updated:** 27/04/2020

## Context and requirements

- There is a new entity in the catalogue API: `Image`. These are conceptual, like works, and consist of images from the visual collections and interesting images from inside books and other materials.
- We want to be able to search for images, and to fetch specified images.
- The images endpoint should be consistent with the works endpoint.

## Proposal

The initial images endpoint will be in **beta**, and therefore will be liable to have breaking changes made without a version bump.

### Image display model

```
{
  "id": String,
  "locations": List[DigitalLocation],
  "source": {
    "id": String,
    "type": "Work"
  },
  "type": "Image"
}
```

This is intentionally minimal at this point as we decide what fields an image should have; it's what is needed to render the panel on search results.

### Single image

**`GET`** `/catalogue/v2/images/:image_id`

*Query params*

- `include` - optional list of fields, as with works endpoint
  - `visuallySimilar` - includes a list of visually similar works

### Multiple images

**`GET`** `/catalogue/v2/images`

*Query params*

- `query` - text search query
- `include` - optional list of extra fields _not including `visuallySimilar`_
- `locations.license` - license to filter for
- `page`
- `pageSize`
