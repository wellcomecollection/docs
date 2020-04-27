# RFC 023: Images endpoint

**Status:** :construction: Draft :building_construction:

**Last updated:** 27/04/2020

## Context and requirements

- Images are now entities in the catalogue API
- We want to be able to search for images, and to fetch specified images
- The images endpoint should behave similarly to the works endpoint

## Proposal

The initial images endpoint will be in **beta**, and therefore will be liable to have breaking changes made without a version bump.

### Image display model

```
{
  "id": String,
	"location": DigitalLocation,
	"parentWork": String
}
```

This is intentionally minimal at this point as we decide what fields an image should have.

### Single image

**`GET`** `/catalogue/v2/images/:image_id`

*Query params*

- `include` - optional list of fields, as with works endpoint

### Multiple images

**`GET`** `/catalogue/v2/images`

*Query params*

- `query` - text search query
- `similarTo` - an image ID; returned images are sorted by visual similarity to this.
- `include` - as with the single image endpoint
- `license` - license to filter for
- `page`
- `pageSize`
