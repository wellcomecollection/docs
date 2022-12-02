# Fetching Data

How do we fetch data from Prismic? We do it in a number of ways across weco.org, as there are a number of ways Prismic gives us to fetch data from the Prismic API.
We use fetchlinks/predicates and Graphquery in `content/webapp` (which will be `weco.org/stories`, `/events`, `/exhibitions` etc). We make use of the Prismic GraphQL
endpoint for `catalogue/webapp` for `weco.org/search/stories` `/events` and `/exhibitions`. 


### Fetchlinks and Predicates

You can see an example including reference to `fetcher` function below.
https://github.com/wellcomecollection/wellcomecollection.org/blob/9c3d08f2ba684d4aef37767a6d7dd0f35c5a1eea/content/webapp/services/prismic/fetch/articles.ts#L29

The `fetcher` function uses predicates, you can see the full fetcher function here.
https://github.com/wellcomecollection/wellcomecollection.org/blob/cfe385593dfa4ddf912d8b183c4f1a7f80c0cf70/content/webapp/services/prismic/fetch/exhibitions.ts#L63

We call the Prismic REST API endpoint for this method `api/v2`.


### GraphQuery

Looks and sounds a lot like GraphQL, but it isn't. This is another way we can query particular documents from the API using a GraphQL style query language. An example below.
https://github.com/wellcomecollection/wellcomecollection.org/blob/9c3d08f2ba684d4aef37767a6d7dd0f35c5a1eea/content/webapp/services/prismic/fetch/articles.ts#L36

We also call the Prismic REST API endpoint for this method `api/v2`.

### GraphQL

We have made use of the Prismic GraphQL API endpoint for a lot of the `search/stories` work. You can find that below.
https://github.com/wellcomecollection/wellcomecollection.org/tree/main/catalogue/webapp/services/prismic/fetch

GraphQL allows us to use search functionality, where we can search for a String using the `fulltext` argument.
https://prismic.io/docs/query-data-graphql#filter-by-fulltext-search

The `fulltext` argument to search for documents that contain a given term (or terms). It searches the term(s) in the text of a document.`fulltext` search is not case-sensitive.

The Prismic GraphQL API endpoint will scan the following fields using `fulltext`:

-   Rich Text
-   Title
-   Key Text
-   UID
-   Select

We call the Prismic GraphQL enpoint for this method `/graphql`. 

** Note: We talked a lot about the potential of moving from using fetchlink, predicates and graphQuery based pagination to solely using GraphQL. The search/stories work forms a kind of 'proof of concept' for this work. **