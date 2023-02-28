# Prismic API: exhibitions endpoint

## Example response

```
GET /exhibitions/{id}
{
    "type": "Exhibition",
    "id": "Y8VNbhEAAPJM-oki",
    "format": {
        "id": "Wvw6wSAAAAuy63fP",
        "label": "Permanent exhibition"
        "type": "ExhibitionFormat"
    },
    "title": "Milk",
    "start": "2022-11-24T00:00:00+0000",
    "end": "2023-04-22T23:00:00+0000",
    "caption": "A major new exhibition exploring our relationship with milk and its place in global politics, society and culture.",
    "place": {
        "id": "WrEgqSAAACAAPEw7",
        "label": "Gallery 1",
        "type": "Place"
    },
    "contributors": [ // behind ?includes=contributors
        {
            ... // reuse the Contributor model (without primaryContributor)
        },
        ...
    ],
    "image": {
        "type": "PrismicImage",
        "dimensions": { 
            "width": 4000, 
            "height": 2670
        },
        "alt": "Photograph of a gallery installation showing a bench with yellow cushions facing a large video projection. The projection shows the inside of a McDonalds restaurant looking down from a high viewpoint in which the restaurant floor is beginning to flood with water.',
        "copyright": "Flooded McDonalds by Superflex | | Wellcome Collection | | | |",
        "url": "https://images.prismic.io/wellcomecollection/1c4a250965a3f9bd17e636f5fc008b88e1e4c649_ep_000832_027.jpg?auto=compress,format",
        "32:15": {
            "dimensions": { 
                "width": 3200, 
                "height": 1500 
            },
            "alt": "Photograph of a gallery installation showing a bench with yellow cushions facing a large video projection. The projection shows the inside of a McDonalds restaurant looking down from a high viewpoint in which the restaurant floor is beginning to flood with water.",
            "copyright": "Flooded McDonalds by Superflex | | Wellcome Collection | | | |",
            "url": "https://images.prismic.io/wellcomecollection/35e056eb53143a449cd612828899b160cb63b3a8_ep_000832_027.jpg?auto=compress,format'
        },
        "16:9": {
            "dimensions": { 
                "width": 3200, 
                "height": 1800 
            },
            "alt": "Photograph of a gallery installation showing a bench with yellow cushions facing a large video projection. The projection shows the inside of a McDonalds restaurant looking down from a high viewpoint in which the restaurant floor is beginning to flood with water.",
            "copyright": "Flooded McDonalds by Superflex | | Wellcome Collection | | | |",
            "url": "https://images.prismic.io/wellcomecollection/09b89fe1bcd0a3a3091bcda6b5f62e5e53d572ca_ep_000832_027.jpg?auto=compress,format'
        },
        square: {
            "dimensions": { 
                "width": 3200, 
                "height": 3200 
            },
            "alt": "Photograph of a gallery installation showing a bench with yellow cushions facing a large video projection. The projection shows the inside of a McDonalds restaurant looking down from a high viewpoint in which the restaurant floor is beginning to flood with water.",
            "copyright": "Flooded McDonalds by Superflex | | Wellcome Collection | | | |",
            "url": "https://images.prismic.io/wellcomecollection/9ed554ac496cb5238a50674c840b40df4fc43acd_ep_000832_027.jpg?auto=compress,format'
        }
    },
}
```

```
GET /exhibitions?query=foo&filters=bar&sort=baz&sortOrder=asc
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
    "nextPage": "/exhibitions?query=foo&filters=bar&sort=baz&sortOrder=asc&page=2",
}
```

