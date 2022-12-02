# Search stories and GraphQL

In `catalogue/webapp`, we make use of the Prismic GraphQL endpoint for `search/stories` and in `/events` and `/exhibitions`.
The forms the beginning of us getting Prismic data into global search. Eventually we will put the Prismic data into Elasticsearch,
and this will allow us to use our own API to query that data. Until the Prismic data is Elasticsearch we are querying Prismic
directly (fetching) and transforming that data to render it in a `ResultList` type object for `/stories` (and events and exhibitions)
results. 

Prismic give a good overview of what is available in the GraphQL endpoint and how to implement it [here](https://prismic.io/docs/query-data-graphql#the-graphql-api-endpoint).
We make of [graphql-request](https://github.com/wellcomecollection/wellcomecollection.org/issues/8953) to format our `GET` GraphQL queries to the Prismic GraphQL API. (**note we have a ticket in the backlog to implement a schema so that we get fewer warnings
around recognising the underlying schema for our Custom Types in Prismic GraphQL [here](https://github.com/wellcomecollection/wellcomecollection.org/issues/8953)** )

You can test GraphQL queries in the Prismic GraphQL explorer [here](https://wellcomecollection.prismic.io/graphql). 
To get you started, here is the base query that we would use to `fulltext` search in Articles.

``` json
query {
  allArticless(fulltext: "heatlh" sortBy: title_ASC) {
        totalCount
    pageInfo {
      hasNextPage
      hasPreviousPage
    }
    edges {
      node {
        title
        _meta {
          type
        }
                body {
          ...on ArticlesBodyStandfirst {
            primary {
              text
            }
          }
        }
        promo {
          ...on ArticlesPromoEditorialimage {
            primary {
              image
              link
              caption
            }
          }
        }
      }
    }
  }
}
```

If you want to look at the queries we use for `search/` you can check out the relevant folder for stories(articles), events and
exhibitions [here](https://github.com/wellcomecollection/wellcomecollection.org/tree/main/catalogue/webapp/services/prismic/fetch).

## Pagination

In `catalogue/webapp` for `weco.org/search` our Works and Images API responses both allow us to use previous and next pages to ensure that the SearchPagination component can be used to paginate through pages using the query parameters in the url e.g `https://wellcomecollection.org/search/stories?query=cats&page=2`.

The Prismic GraphQL API response format is different, we don't get urls for the previous or next page.
Prismic GraphQL results contain nodes that each will have a cursor String value. 
A node represents a story/event/exhibition result. 
In our implementation of pagination for `search/stories` I have taken the pageSize value (how many results we want in each page) and mapped the relevant starting cursor to the relevant page number. 
If the query params contain a page, we grab the corresponding cursor and pass this to the GraphQL query and get the next pageSize (6) results.

More information on Prismic GraphQL pagination can be found [here](https://prismic.io/docs/query-data-graphql#pagination) for reference.
