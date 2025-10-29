# Showcase recently digitised works on the Collections landing page

**Last modified:** 2025-10-15T10:50:00Z

## Context

> The online collection is continually evolving, primarily through ongoing digitisation efforts, as well as through cataloguing of born-digital works. Users could benefit from knowing what is newly available to view and download online.

See [Notion page](https://www.notion.so/wellcometrust/Showcase-recently-digitised-works-1e06687658a180439819e069fac2601f) for more details.

The [New online component](https://github.com/wellcomecollection/wellcomecollection.org/issues/12303) has been built and uses hard-coded data as a first step. See [Collections landing page](https://wellcomecollection.org/collections).

[`WorkItem`](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/content/webapp/views/components/WorkCard/index.tsx) type expected by the component.
NOTE: there is some flexibility here, as this was built as a temporary/POC solution. 

```typescript
type WorkItem = {
  url: string;
  title: string;
  image: {
    contentUrl: string;
    width: number;
    height: number;
    alt?: string;
  };
  labels: { text: string }[];
  partOf?: string;
  contributor?: string;
  date?: string;
};
```

This RFC aims to describe how we might integrate a `digitisedDate` into the Work model, and how the catalogue-api might expose this data.

## Requirements

- ~~New Online is to only display works that have been digitised by the Wellcome Collection team and born-digital archives, ie. works that have a METS file. It is not meant to include other digital works such as EBSCO journals.~~
- ~~We want to display 4 works and they can all be of the same format, eg. archives and manuscripts~~
- a "New Online" page which lists all the recently digitised works by descending `digitisedDate` order 
- the 4 "New Online" works on the landing page will be selected among the above, and editorialised through Prismic

## Integrate the digitised date in the Work model and the catalogue pipeline.

- The digitisedDate will not always be strictly accurate: when a work is digitised again, the `CREATEDATE` is that of the latest digitisation. We can mitigate this by only extracting and loading `digitisedDate` for METS works that are on their v1.
- What do we do for work with advisory? We can filter for `items.locations.accessConditions.status.id": ["open"]`

### METS file - digitised or born-digital

The digitisation date is present in the METS's header, both in digitised and born-digital items.  

**NOTE**: there can be multiple versions of a digital item, each with their respective `CREATEDATE`. Since we extract and transform the most recent version, the `CREATEDATE` will not always be the one when the item was digitised for the first time. 

```xml
  <mets:metsHdr CREATEDATE="2018-04-28T10:33:56Z">
    <mets:agent OTHERTYPE="SOFTWARE" ROLE="CREATOR" TYPE="OTHER">
      <mets:name>Goobi - ugh-3.0-6d40b80 - 06−September−2017</mets:name>
      <mets:note>Goobi</mets:note>
    </mets:agent>
  </mets:metsHdr>
```

### Work model

[`WorkData`](https://github.com/wellcomecollection/catalogue-pipeline/blob/53d04e063a75600236ac8ed41934b9c52b451624/common/internal_model/src/main/scala/weco/catalogue/internal_model/work/Work.scala#L102) contains data common to all types of works that can exist at any stage of the pipeline, including a list of [`Item`](https://github.com/wellcomecollection/catalogue-pipeline/blob/53d04e063a75600236ac8ed41934b9c52b451624/common/internal_model/src/main/scala/weco/catalogue/internal_model/work/Item.scala#L6) and their (in this case, Digital) [`Location`](https://github.com/wellcomecollection/catalogue-pipeline/blob/53d04e063a75600236ac8ed41934b9c52b451624/common/internal_model/src/main/scala/weco/catalogue/internal_model/locations/Location.scala#L15)

`DigitalLocation` extends `Location` and is distinct from `PhysicalLocation`.

```scala
case class DigitalLocation(
  url: String,
  locationType: DigitalLocationType,
  license: Option[License] = None,
  credit: Option[String] = None,
  linkText: Option[String] = None,
  accessConditions: List[AccessCondition] = Nil,
  digitisedDate: Option[String] = None, 🆕
) extends Location
``` 

#### Other works with a DigitalLocation

Ebsco and Miro works do not have a digitised date or version. Much like `linkText`, `digitisedDate` and `digitisedVersion` are Options and default to None if not present or applicable.

### works-source/works-denormalised `data.items`

```json
"items": [
  {
    "id": {
      "type": "Unidentifiable"
    },
    "locations": [
      {
        "url": "https://iiif.wellcomecollection.org/presentation/v2/b30601241",
        "locationType": {
          "id": "iiif-presentation"
        },
        "license": {
          "id": "pdm"
        },
        "accessConditions": [
          {
            "method": {
              "type": "ViewOnline"
            },
            "status": {
              "type": "Open"
            }
          }
        ],
        "digitisedDate": "2019-09-13T14:33:15.254Z",
        "type": "DigitalLocation"
      }
    ]
  }
]
```

### `works-indexed` mapping

```json
{
  "works-indexed-2025-08-14": {
    "mappings": {
      "dynamic": "strict",
      "properties": {
        "aggregatableValues": {},
        "debug": {},
        "display": {
          "type": "object",
          "enabled": false
        },
        "filterableValues": {
          "properties": {
            "availabilities": {},
            "contributors": {},
            "format": {
              "properties": {
                "id": {
                  "type": "keyword"
                }
              }
            },
            "genres": {},
            "identifiers": {},
            "items": {
              "properties": {
                "id": {
                  "type": "keyword"
                },
                "identifiers": {
                  "properties": {
                    "value": {
                      "type": "keyword"
                    }
                  }
                },
                "locations": {
                  "properties": {
                    "accessConditions": {},
                    "license": {},
                    "locationType": {},
                    "digitisedDate": { 
                      "type": "date"
                    }
                  }
                }
              }
            },
            "languages": {},
            "partOf": {},
            "production": {},
            "subjects": {},
            "workType": {}
          }
        },
        "query": {},
        "redirectTarget": {
          "type": "object",
          "dynamic": "false"
        },
        "type": {
          "type": "keyword"
        }
      }
    }
  }
}
```

NOTE: the `display` object is not strictly mapped, so as to offer flexibility in what the API returns to the client. In this case it would not be necessary to extend the display object to include the `digitisedDate` as there is no plan for this to appear in the "New online" Work card. 


## Catalogue-api

Once the digitisedDate is part of the Work model and indexed in `works-indexed-pipeline-date`, we can extend the [SearchApi](https://github.com/wellcomecollection/catalogue-api/blob/main/search/src/main/scala/weco/api/search/SearchApi.scala) to enable additional sorting.

Essentially we want to return: 
- documents filtered by `accessConditions.status": ["open"]`
- sorted by most recent `digitisedDate`

ES query would need to look like this:

```json
{
  "query": {
    "bool": {
      "must": [
        {
          "terms": {
            "filterableValues.items.locations.accessConditions.status.id": ["open"] 
          }
        }
      ]
    }
  },
    "sort": [
    {
      "filterableValues.items.locations.digisedDate": {
        "order": "desc",
        "missing": "_last" // Place documents with missing fields at the end
      }
    }
  ]
}
```

### Use existing /works endpoint

We can exercise the existing [AccessStatusFilter](https://github.com/wellcomecollection/catalogue-api/blob/09b4612d6f15c604b40a432ffd98b95ca35becf5/search/src/main/scala/weco/api/search/models/DocumentFilter.scala#L72) and add a new SortRequest alongside `ProductionDateSortRequest`, eg. `DigitisedDateSortRequest`

The `open` items sorted by most recent `digitisedDate` can be requested like so:

```
search/works?items.locations.accessConditions.status=open&sortOrder=desc&sort=items.locations.digitisedDate
```



