# RFC 020: Locations and requesting

**Last updated: 14 February 2020.**

## Background

As part of migrating users of Wellcome Library to Wellcome Collection, we need to support finding and requesting physical items on the new site. This will require changes and additions to how we describe item locations in the Catalogue API, to allow us to fully support digitised items alongside physical items open shelves and in closed stores.

We will also need to build a new API, the Stacks API, that lets logged in users request a physical item and see the items that they have requested. This should integrate with the Sierra API so that these requests can be managed as holds in Sierra.

## Proposed solution

### Principles

The are two key principles for how we should split data and functionality between the Catalogue API and Stacks API:

1. Descriptive data, which is also required for search, goes in the Catalogue API.
2. Availability data, which is realtime in nature, goes in the Stacks API.

This has two benefits. Firstly, it allows us to more easily guarantee immediate updates for realtime data and to apply different caching strategies for data updated at different frequencies. Secondly, it means that requesting is not quite as directly tied to the Sierra catalogue, allowing us to more easily support alternative request management systems in the future.

### Catalogue API

This work will require a number of changes to the modelling of item locations:

* Removal of separate types for `PhysicalLocation` and `DigitalLocation`
* Significant changes to the allowed values for `locationType`
* Additional properties that describe exactly where an item can be found

#### Example

```
GET /works/:id?include=items
```

```
{
  "items": [
    {
      "id": "{itemId}",
      "title": "{field v}",
      "copy": "{field 058}",
      "locations": [
        {
          "locationType": {
            "id": "open-shelves",
            "label": "Open shelves",
            "type": "LocationType"
          },
          "description": {
            "id": "medc",
            "label": "Medical Collection"
            "type": "LocationDescription",
          },
          "shelfmark": "W50 2009L89",
          "accessConditions": [
            {
              "terms": "Usage terms go here",
              "status": {
                "id": "open",
                "label": "Open",
                "type": "AccessStatus"
              },
              "type": "AccessCondition"
            }
          ],
          "type": "Location"
        },
        {
          "locationType": {
            "id": "online",
            "label": "Online",
            "type": "LocationType"
          },
          "description": {
            "id": "iiif-presentation",
            "label": "IIIF Presentation API",
            "type": "LocationDescription"
          },
          "url": "https://wellcomelibrary.org/iiif/b30598977/manifest",
          "license": {
            "id": "cc-by",
            "label": "Creative Commons Attribution",
            "type": "License"
          },
          "accessConditions": [
            {
              "terms": "Usage terms go here",
              "status": {
                "id": "open",
                "label": "Open",
                "type": "AccessStatus"
              },
              "type": "AccessCondition"
            }
          ],
          "type": "Location"
        }
      ],
      "type": "Item"
    }
  ]
}
```

#### Location types

Location types are used to group more specific kinds of location. They are intended for uses such as search filtering and helping a user determine if something needs to be requested.

They map to the location codes on bibs in Sierra, not items. The Sierra API for bib objects exposes this as `locations`, which is populated from MARC fixed field 026.

The proposed values for location types are:

| ID            | Label         | Sierra mapping         |
| ------------- | ------------- | ---------------------- |
| open-shelves  | Open shelves  | whml                   |
| closed-stores | Closed stores | stax, arch, mfvl, hamp |
| online        | Online        | elro, digi             |
| on-exhibition | On exhibition | \[TBD]                 |

Any other Sierra bib location code should be ignored.

#### Location descriptions

Location descriptions are used to more specifically describe where an item can be found. In the case of openly shelved items, this will be the shelf location. For closed stores, it will describe the method of request and for online locations it will be a description of the kind of resource used to retrieve the item.

The rules here are relatively complex, as they depend on the `locationType`, the item `location` in Sierra and the contents of field `108 OPACMSG` in Sierra.

| Location type | Sierra location | OPAC message | Location description |
| ------------- | --------------- | ------------ | -------------------- |
| closed-stores | ANY             | f            | online-request       |
| closed-stores | ANY             | a, n, p, q   | manual-request       |
| open-shelves  | ANY             | ANY          | Use Sierra location  |
| online        | elro            | ANY          | external-resource    |
| online        | digi            | ANY          | iiif-presentation    |
| on-exhibition | ANY             | ANY          | \[TBD]               |

Online locations created from Miro images should have a location description of `iiif-image`. Those created from the METS ingest should have `iiif-presentation`.

#### Search filters and aggregations

We should enable filtering by both `locationType` and `description`. The first of these already exists, but as the values for this field are going to change, this work will have an impact on the front end.

```
GET /works?items.locations.locationType=online
GET /works?items.locations.description=iiif-presentation
```
We should also add an aggregation on `locationType`, so that a filter can be added to the results page.

Additionally, we should a filter and aggregation on access status as part of this work. This will allow the user to restrict to eg only openly available works:

```
GET /works?items.locations.accessConditions.status=open
```

### Stacks API

The Stacks API is a new service for interacting with items in the closed stores ("stacks" in library speak). It will provide the following functionality:

* Return realtime availability for the items on a work
* Let authenticated users place requests for items
* Let authenticated users see their current requests

#### Authentication

Unlike the Catalogue API, the Stacks API will not be openly available. All requests must specify an API key, which will be used for rate limiting. Placing requests on an item or viewing a user's current requests will be additionally secured behind an Oauth Authorization Code flow. The API will automatically restrict data to the user supplied in the token.

#### Item availability

As a work can have many items and we always display them all, item availability is requested by work. This means that a work page can be displayed with only two API requests: one for the descriptive data and one for realtime availability.

```
GET /works/{workId}
```

```
{
  "id": "{workId}",
  "items": [
    {
      "id": "{itemId}",
      "dueDate": "{dueDate}",
      "status": {
        "id": "-",
        "label": "Available",
        "type": "ItemStatus"
      }
      "type": "Item"
    },
    {
      "id": "{itemId}",
      "dueDate": "{dueDate}",
      "status": {
        "id": "b",
        "label": "As above",
        "type": "ItemStatus"
      }
      "type": "Item"
    }
  ],
  "type": "Work"
}
```

Item statuses will be passed through directly from Sierra for now. They are available in the Sierra API response for an item in fixed field `88`.

#### Request item

When an item is requested, the API will identify the user from the provided Oauth token and place a hold in Sierra for the requested item. This request will return an empty response.

```
POST /requests

{
  "item": {
    "id": "{itemId}",
    "type": "Item"
  },
  "pickupDate": "{date}",
  "type": "Request"
}
```

`pickupDate` is an optional field.

An accepted hold request will result in `204 Accepted`.

A rejected hold request will result in `409 Conflict`.

A conflict might will occur when a hold has been placed by another user before an items status has been updated.

The provided `pickupDate` maps to `neededBy` in the hold request to Sierra. 

This should in turn populate `notNeededAfterDate` on the created hold, but that still needs to be confirmed. There is no other date on a hold that can be specified via the Sierra API.

#### Current requests

When an item is requested, the API will identify the user from the provided Oauth token and retrieve their current holds from Sierra. No identifying user information should be returned in the response.

```
GET /requests
```

```
{
  "results": [
    {
      "item": {
        "id": "{itemId}",
        "type": "Item"
      },
      "pickupDate": "{date}",
      "pickupLocation": {
        "id": "sepbb",
        "label": "Rare Materials Room",
        "type": "LocationDescription"
      },
      "status": {
        "id": "i",
        "label": "Item hold ready for pickup.",
        "type": "RequestStatus"
      },
      "type": "Request"
    }
  ],
  "totalResults": 1,
  "type": "ResultList"
}
```

Hold statuses will be passed through directly from Sierra for now.

## Questions

1. Is it ok to remove the separate types for `DigitalLocation` and `PhysicalLocation`?
2. What is the impact on the front end from the change to `locationType`?
3. Are the location type mappings to Sierra locations correct?
4. How do we handle things like `bwith` (bound in above) and `cwith` (contained in above)?
5. Where can we get an up to date list of the values for `108 OPACMSG`?
6. Can we really suppress `OPACMSG` and are the mappings correct?
7. Is there a better naming than `LocationDescriptoin` to describe where something actually is?
8. How do we detect and handle items that are on exhibition?
9. The hold request to Sierra must specify a pickup location. What should we use?
10. Is it correct to populate `notNeededAfterDate` given current retrieval workflows?
