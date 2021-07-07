# Wellcome Collection Catalogue

Making Wellcome Collection's catalogue open, accessible and
discoverable.

The catalogue consists of multiple sources including:
* Library holdings
* Archives and manuscripts
* Born digital content
* Images from what was previously wellcomeimages.org

As and when these sources are made available digitally, we will consume
them via [our pipeline](./pipeline), unify them into a
[single model](../common/internal_model) and make them discoverable via
our [API](https://github.com/wellcomecollection/catalogue-api).

**Interested in how we make these services?**

[Take a look at our documentation on the design and decision making
processes of the services within the catalogue repo](https://github.com/wellcomecollection/docs).

**Interested in making use of our data to build your own products or
use in your research?**

[Take look at our developer documentation](https://developers.wellcomecollection.org/) or
[go straight to our API](https://api.wellcomecollection.org/catalogue/v2/works).

**Interested in other parts of the Wellome Collection digital platform
works?**

[Take a look at our Platform repo](https://github.com/wellcomecollection/platform)

**Interested in how all of this works**
[Keep reading about the architecture of the services in this repo](#architecture).

## Architecture

The catalogue consists of three main parts with supporting services.

These are:

* Adapters: Syncing data from multiple external sources, enabling retrieving data performantly and at scale:
  - [Sierra adapter](../sierra_adapter/README.md): [Sierra](https://www.iii.com/products/sierra-ils/) contains data on things in the library
  - [Calm adapter](../calm_adapter/README.md): [Calm](https://www.axiell.com/uk/solutions/product/calm/) contains data on things in the archive
  - [METS adapter](../mets_adapter/README.md): [METS](http://www.loc.gov/standards/mets/) data on digital assets from our workflow & archival storage systems. 
* [Pipeline](./pipeline/README.md): Taking adapter data and putting it into our query index. We use [Elasticsearch](https://www.elastic.co/elasticsearch/) as our underlying search engine.
* [API](https://github.com/wellcomecollection/catalogue-api/blob/main/README.md): The public APIs to query our catalogue data. The API services are stored in a different GitHub repository: https://github.com/wellcomecollection/catalogue-api

## Updating this documentation

See the [Workflow for editing in Gitbook](GITBOOK.md).

