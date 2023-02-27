# Prismic API: Events endpoint

## Example response

```
GET /events/{id}
{
    "type": "Event",
    "id": "",
    "format": {
        "id": "",
        "label": ""
        "type": "EventFormat"
    },
    "title": "",
    "availableOnline": boolean,
    "interpretations": [
        {
            "label": "",
            "type": "EventInterpretation"
        },
        ...
    ],
    "audiences": [
        {
            "label": "",
            "type": "EventAudience"
        },
        ...
    ],
    "instantiations": [
        {
            "start": "", // ISO 8601 datetime
            "end": "", // ISO 8601 datetime
            "place": {
                "id": "",
                "label": "",
                "type": "Place"
            },
            "isOnline": boolean
        }
    ],
    "contributors": [ // behind ?includes=contributors
        {
            ... // reuse the Contributor model
        },
        ...
    ],
    "image": {
        "thumbnail": {
            ... // reuse the DigitalLocation model
        },
        "alt": ""
    },
    "caption": "",
    "partOf": [
        {
            ... // reuse the partOf model for series and seasons
        }
    ]
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

## Filter

- **instantiations.start.from**
  DD-MM-YYYY
- **instantiations.start.to**
  DD-MM-YYYY
- **instantiations.end.from**
  DD-MM-YYYY
- **instantiations.end.to**
  DD-MM-YYYY
- **interpretation**
  Interpretations are useful accessibility tools for event searching. They are, for example: Captioned, BSL, Wheelchair friendly
- **place.label**
  List of physical locations, would also include "Online".
- **format.label**
  [`Session`, `Game`, `Installation`, `Discussion`, `Performance`, `Workshop`, `Chill out`, `Shopping`, `Festival`, `Screening`, `SEND workshop`, `Late`, `Symposium`, `Gallery tour`, `Seminar`, `Study day`, `Walking tour`]
- **partOf**
  Part of a series of events (I'm not sure this is possible?)
- **audience**
  The public this is geared towards, e.g. Schools
- **contributor.agent.label**
  e.g. Facilitator, Host
- **availableOnline**
  Was recorded and the video is made available for a rewatch online.

## Sort

- instantiations.start
- instantiations.end
- relevance

Default sort should be by relevance, with a fallback to id if no query is provided or where documents have the same score.

## Aggregations

- place
- contributor
- format
- audience
