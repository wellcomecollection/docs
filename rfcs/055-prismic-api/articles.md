# Content API: articles endpoint

## Example response

```
GET /articles/{id}
{
    "type": "Article",
    "id": "XAEEIhQAACsA4eEl",
    "format": {
        "type": "ArticleFormat",
        "id": "W7TfJRAAAJ1D0eLK",
        "label": "Article"
    },
    "title": "Sick of being lonely",
    "publicationDate": "2018-12-20T10:44:15+0000",
    "caption": "When his relationship ended, Thom James first withdrew from the world, then began to suffer from illnesses with no apparent physical cause.",
    "contributors": [
        {
            "contributor": {
                "id": "XAaGDRQAAPE_-ePY",
                "label": "Thom James",
                "type": "Person"
            },
            "role": {
                "id": "WcUWeCgAAFws-nGh",
                "label": "Author",
                "type": "EditorialContributorRole"
            },
            "type": "Contributor"
        }
    ],
    "image": {
        "type": "PrismicImage",
        "dimensions": {
            "width": 4000,
            "height": 2670
        },
        "alt": "Photograph of a gallery installation showing a bench with yellow cushions facing a large video projection. The projection shows the inside of a McDonalds restaurant looking down from a high viewpoint in which the restaurant floor is beginning to flood with water.",
        "copyright": "Flooded McDonalds by Superflex | | Wellcome Collection | | | |",
        "url": "https: //images.prismic.io/wellcomecollection/1c4a250965a3f9bd17e636f5fc008b88e1e4c649_ep_000832_027.jpg?auto=compress,format",
        "32:15": {
            "dimensions": {
                "width": 3200,
                "height": 1500
            },
            "alt": "Photograph of a gallery installation showing a bench with yellow cushions facing a large video projection. The projection shows the inside of a McDonalds restaurant looking down from a high viewpoint in which the restaurant floor is beginning to flood with water.",
            "copyright": "Flooded McDonalds by Superflex | | Wellcome Collection | | | |",
            "url": "https://images.prismic.io/wellcomecollection/35e056eb53143a449cd612828899b160cb63b3a8_ep_000832_027.jpg?auto=compress,format"
        },
        "16:9": {
            "dimensions": {
                "width": 3200,
                "height": 1800
            },
            "alt": "Photograph of a gallery installation showing a bench with yellow cushions facing a large video projection. The projection shows the inside of a McDonalds restaurant looking down from a high viewpoint in which the restaurant floor is beginning to flood with water.",
            "copyright": "Flooded McDonalds by Superflex | | Wellcome Collection | | | |",
            "url": "https://images.prismic.io/wellcomecollection/09b89fe1bcd0a3a3091bcda6b5f62e5e53d572ca_ep_000832_027.jpg?auto=compress,format"
        },
        "square": {
            "dimensions": {
                "width": 3200,
                "height": 3200
            },
            "alt": "Photograph of a gallery installation showing a bench with yellow cushions facing a large video projection. The projection shows the inside of a McDonalds restaurant looking down from a high viewpoint in which the restaurant floor is beginning to flood with water.",
            "copyright": "Flooded McDonalds by Superflex | | Wellcome Collection | | | |",
            "url": "https://images.prismic.io/wellcomecollection/9ed554ac496cb5238a50674c840b40df4fc43acd_ep_000832_027.jpg?auto=compress,format"
        }
    }
}
```

```
GET /articles?query=foo&filters=bar&sort=baz&sortOrder=asc
{
    "type": "ResultList",
    "results": [
        {
            ... // as above
        },
        ...
    ],
    "pageSize": 100,
    "totalResults": 1000,
    "totalPages": 10,
    "nextPage": "/articles?query=foo&filters=bar&sort=baz&sortOrder=asc&page=2",
}
```

## Filters

- **publicationDate.from**
  YYYY-MM-DD
- **publicationDate.to**
  YYYY-MM-DD
- **contributors.contributor**
  Includes author, artists, photographers, etc.
- **format**
  IDs corresponding to [`Comic`, `Long read`, `Prose poem`, `Podcast`, `In pictures`, `Article`, `Photo story`, `Interview`, `Book extract`]

## Sort options

- relevance
- publicationDate

Default sort should be by relevance, with a fallback to id if no query is provided or where documents have the same score.

## Aggregations

- contributors.contributor
- format
