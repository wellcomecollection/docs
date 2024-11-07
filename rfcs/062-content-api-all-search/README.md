# Content API: All search and indexation of missing content types

<!-- TODO add relevant sections -->
- [Background information](#background-information)

## Background information

The current "All" search (`/search`) displays separate, statically-ordered grids for Stories, Works, Images and Events. In doing so, we are unwillingly creating a hierarchy of importance between those content types which does not match their actual level of relevance. Each grid also requires its own query call, which is not efficient.

As a next step, we are looking at making the "All" search expose all Prismic content types whose documents are available to our users through a UID-based URL (["Addressable content types"](#addressable-content-types)), with the results being ordered by each individual document's relevance score. Works and Images ("Collection search") will also still be available on the page, although their relevance scores will not be weighed against Addressable content types', as you can see on the image below. 

<img src="./assets/prototype.png" alt="Design prototype for the 'All' search page" />

[Consult the design prototype here](https://www.figma.com/design/qssPpJy1lOWSFtuACajkZr/Global-search?node-id=4656-12994&node-type=canvas&m=dev). 

There is to be no filtering nor sorting feature on this page. Therefore, we aim to build something with minimalism in mind, allowing us to have query performance at the forefront of our concerns.

We will do so by creating a new endpoint: https://api.wellcomecollection.org/content/v0/all. 

Its response will return [an ordered list of Addressable content types](#api-response-addressable-content-types-list), as well as [the relevant results for the Collection search](#api-response-collection-search). (**TODO: figure out what that looks like**)


### Existing endpoints and indexes
We have wondered if this new endpoint removed the need for our existing, specialist ones (https://api.wellcomecollection.org/content/v0/articles, for example). Could we only use this new one and use a filter when needed? We have determined that the answer was no, as they serve a different purpose.

As the new endpoint and index are to be as minimalistic as possible, these "specialist" ones will still be the ones used in Content type-specific listing pages (wellcomecollection.org/stories) or search (wellcomecollection.org/search/articles), as they allow us to provide much more complex information, such as filters and aggregations.

## "All" index
We will be creating a single index in Elasticsearch containing all Addressable content types in their most minimalistic form (**TODO add link detailed this**).
<!-- TODO what does it look like? How does it get updated? -->

### Addressable content types
- Events
- Exhibitions
- Stories
- Pages
- Visual stories
- Exhibition text
- Exhibition highlight tour
- Books
- Projects
- Seasons

## API response: Addressable content types list
<!-- TODO figure out default order -->

## API response: Collection search
<!-- TODO, what shape does this have? -->


## Endpoint
`https://api.wellcomecollection.org/content/v0/all` 

## Documents format
- [Page document](./transformedDocuments/pageDocument.ts)
- [Visual story document](./transformedDocuments/visualStoryDocument.ts)

## API Response
<!-- [API response](./api-response.ts)  -->