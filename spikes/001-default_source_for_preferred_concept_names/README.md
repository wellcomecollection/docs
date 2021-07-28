# Default source for preferred concept names

## Why

Our prototype concepts enrichment pipeline uses third party sources (LoC subject headings, LoC names, MeSH, and wikidata) to find variant names for the concepts in our catalogue. Each of those third party sources sets a preferred name for each concept, and a list of 0 or more variant names. The preferred names for each concept vary from authority to authority, and Wellcome Collection has no existing view on which of these is "best".

Given that in most cases we won't want to display all of its variant names, we will also need to set a preferred name for each concept. With 10,000s of concepts in our catalogue, the choice of which variant name to use will need to be automated in almost every case.

We want to know which of those third party sources usually has the most reliable/commonly understandable names for their entities, and which one we should choose to display by default.

## What

We want to build a demo which asks users to choose the most understandable variant name for a set of randomly chosen concepts. By running this experiment many times with many types of user, we should get a sense of which source provides the best default names, and the order in which we should prefer them as sources.

## Hypotheses

Our assumption is that wikidata will be the preferred source for preferred concept names. As their dataset is maintained by a larger group of contributors who serve a more general audience, we expect that they will be more likely to converge on commonly understandable names than the LoC or MeSH maintainers.
