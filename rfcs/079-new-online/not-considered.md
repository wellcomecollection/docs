# Not considered at this time


## New Prismic Custom Type ingested by the content pipeline and available through the content API

**Dependent on decision regarding catalogue pipeline and API integration**

Create an additional [ETL pipeline](https://github.com/wellcomecollection/content-api/blob/6e9c4ba7285c7ea1b259038a0ccb7ce9f6219da1/pipeline/src/extractTransformLoad.ts#L31) in the content pipeline, to load the new Prismic type ("`featured-work`"?) into an index in the content cluster.

Potential `ElasticsearchFeaturedWork` type.  
No aggregations or filters required

```typescript
type ElasticsearchFeaturedWork = {
  id: string; // work id 
  display: FeaturedWork;
  query: {
    createdDate: string;
    id: string
    type: string[];
    feature: string; // eg. "new-online", "trending"
  };
};

type FeaturedWork = {
  id: string; // work id 
  url: string;  
  title: string;
  image: {
    contentUrl: string;
    width: number; // can we make this optional?
    height: number; // can we make this optional?
    alt?: string;
  };
  type: string[];
  feature: string; // eg. "new-online", "trending"
  meta?: string;
}
```

On the API side the data is exposed on the `/featured/new-online` endpoint, with optional `to`, `from` and `type` query params.  
Absent query params return `FeaturedWork[]` with the most recent of each of 4 default `types`, with feature="new-online".  
Query params enable flexibility as to the date range and type of `ElasticsearchFeaturedWork` documents returned. 

Pros: 
- integrates into existing infrastructure
- the Prismic Custom Type can be made to fit our needs
- doesn't require code change and deployment to update the works
- control over the types/labels
- control over the cover image
- can be kept up after stage 2. to provide override capabilities

Cons: 
- manually curated content risks getting stale 


### Create a /works/new-online route with custom ES query

Not considered because requirements for aggregartions have been withdrawn

Given that this search does not need to support faceting it might be easier to create a new route specifically for this query, to return the most recent digitised work for a list of formats/workTypes:

eg. `/works/new-online?workType=a%2Ch%2Cl%2Chdig` ie. a=Books h=Archives and manuscripts l=Ephemera hdig=Born-digital archives

Add to [WorksService](https://github.com/wellcomecollection/catalogue-api/blob/main/search/src/main/scala/weco/api/search/services/WorksService.scala):

```
def newOnline(
    index: Index,
    formatIncludes: Seq[String]
  ): Future[Either[ElasticsearchError, Map[String, Int]]] = {
    val searchResponse = elasticsearchService.executeSearchRequest(
      search(index)
        .size(0)
        .query {
          boolQuery().must(
            termsQuery(
              "filterableValues.items.locations.accessConditions.status",
              "open"
            )
          )
        }
        .aggs {
          termsAgg("formats", "filterableValues.format.id")
            .include(formatIncludes)
            .subaggs(
              TopHitsAggregation(
                name = "top_by_date",
                size = Some(1),
                sort = Seq(
                  fieldSort("filterableValues.items.locations.digitisedDate")
                    .desc()
                  
                )
                source = Some(Seq("display"))
              )
            )
        }
    )
  }
```

## DISCARDED: Separate New digitised service

Newly digitised as another content type in the content API.  
The data is instead harvested from S3 and loaded into a data store (DDB or ES index) for the content API to then serve up in the same way as described above.

<img src="./assets/newly_digitised.png" width="600" />

### ❓❓❓
Is the data that we need in the METS file?

```typescript
type WorkItem = {
  url: string; // work url, not available
  title: string; // yes, currently transformed in the pipeline
  image: {
    contentUrl: string; 
    // could be 
    // https://iiif.wellcomecollection.org/presentation/v2/{sourceIdentifier}
    // https://iiif.wellcomecollection.org/image/{sourceIdentifier}_0001.jp2/full/630,1024/0/default.jpg (1st image in the presentation)
    width: number;
    height: number;
    alt?: string;
  };
  labels: { text: string }[]; // yes, not currently transformed in the pipeline. May not match the values we want to display, eg. "monograph"
  meta?: string;
};
```

DISCARDED: because the work id is not available in the METS file, so the solution offers no onward journey
In order to include the work id, a request to the catalogue api would be necessary. 