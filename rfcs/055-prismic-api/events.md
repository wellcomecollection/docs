# Content API: Events endpoint

## Example response

```
GET /events/{id}
{
    "type": "Event",
    "id": "Y8aBHhEAAKRE_9AF",
    "format": {
        "type": "EventFormat",
        "id": "Wd-QYCcAACcAoiJS",
        "label": "Discussion"
    },
    "title": "Our Microbes and Our Health",
    "isOnline": false,
    "availableOnline": true,
    "isRelaxed": false,
    "caption": "Join Claudia Hammond from the BBC and a panel of experts to consider the explosion of scientific knowledge about the millions of microbes that live in and on our bodies. ",
    "interpretations": [
        {
            "id": "WmXl4iQAACUAnyDr",
            "label": "Captioned (screen)",
            "type": "EventInterpretation"
        },
        ...
    ],
    "audiences": [
        {
            "id": "WlYWByQAACQAWdA0",
            "label": "Schools",
            "type": "EventAudience"
        },
        ...
    ],
    "instantiations": [
        {
            "start": "2018-12-20T10:44:15+0000",
            "end": "2018-12-20T16:44:15+0000",
            "place": {
                "id": "Wn1fvyoAACgAH_yG",
                "label": "Reading Room",
                "type": "Place"
            }
        }
    ],
    "contributors": [
        {
            "contributor": {
                "id": "Y0QgwBEAAB-e0sFB",
                "label": "Jim Naughten",
                "type": "Person"
            },
            "role": {
                "id": "Wux6DyIAAO5n3lzk",
                "label": "Artist",
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
        "url": "https://images.prismic.io/wellcomecollection/1c4a250965a3f9bd17e636f5fc008b88e1e4c649_ep_000832_027.jpg?auto=compress,format",
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
GET /events?query=foo&filters=bar&sort=baz&sortOrder=asc
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
    "nextPage": "/events?query=foo&filters=bar&sort=baz&sortOrder=asc&page=2",
}
```
