# RFC 070: Concepts API changes

## Background

This RFC outlines plans towards replacing our existing concepts API (introduced in [this RFC](https://github.com/wellcomecollection/docs/tree/main/rfcs/050-concepts-api) and implemented [here](https://github.com/wellcomecollection/catalogue-api/tree/main/concepts)) 
with a new API to deliver all features included in our newly designed theme pages. The RFC builds on top of existing RFCs,
including [the graph pipeline RFC](https://github.com/wellcomecollection/docs/tree/main/rfcs/066-graph_pipeline) and the [catalogue graph ingestor RFC](https://github.com/wellcomecollection/docs/tree/main/rfcs/069-catalogue_graph_ingestor).

## The concepts API

The current concepts API is implemented in TypeScript and exposes two endpoints:
* *Single concept endpoint*: A GET endpoint for retrieving a single concept given an ID
* *Search endpoint*: A GET endpoint returning a list of concepts given some filters

When processing a request, both endpoints retrieve concepts data from an Elasticsearch index and return a response 
without doing any processing on the returned data.

The *single concept endpoint* is called whenever a user views a theme page. The *search endpoint* is not being
actively utilised.

## Replacing the concepts API

The new API will mirror the structure of the existing API, exposing the same *single concept endpoint*.
It will get its data from a new Elasticsearch index populated by the catalogue graph ingestor (see [here](https://github.com/wellcomecollection/docs/tree/main/rfcs/069-catalogue_graph_ingestor)).

Given the similarity of the two APIs, it makes sense to build the new API by modifying the existing one instead of starting from scratch.
This way we can make use of existing utilities (e.g. functions connecting to Elasticsearch and AWS) and the existing deployment setup. 

Since the current *search endpoint* is not being utilised and is not required to implement new theme pages,
only the *single concept endpoint* will be implemented.  


## New *single concept endpoint*

The *single concept endpoint* needs to supply all metadata displayed on a given theme page. The designs include three
kinds of theme pages, each with its own set of metadata — Contributor theme pages (based on Agent, Person, or Organisation concepts), Type/technique theme pages (based on `Genre` concepts),
and Subject theme pages (for all other concept types).

### Contributor theme pages

The screenshot below shows an example Agent/Organisation/Person theme page. All metadata fields are labelled with suggested field
names to be returned from the API. The labels are colour-coded:

* Information in green is already returned by the current concepts API and will be easy to reproduce in the new API.
* Information in orange is not currently returned by the concepts API, but it is already stored in the graph and will be easy to return from the new API. 
* Information in red is not currently returned by the concepts API and is not stored in the graph. Including it in the API response might involve a lot of effort.

(The screenshot does not show the full theme page. It only includes information which can be returned from the concepts API.
Information not in included in the screenshot will be returned from other APIs.)

> <img src="img/example_person_theme_page.png" alt="example_person_theme_page" width="600"/>

Refer to the table below for more details about each field:

| Field name        | Details                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| type              | Stored in the graph under the `type` field on all Concept nodes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| label             | Stored in the graph under the `label` field on all Concept and SourceConcept nodes. Sometimes multiple labels might be available (in cases where a concept is linked to multiple source concepts), in which case we will have to choose one label based on a priority ranking between sources (e.g. MeSH over LoC over Wikidata).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| alternativeLabels | Stored in the graph under the `alternativeLabels` field on all SourceConcept nodes. Sometimes many alternative labels might be available and choosing the most relevant one to display to the user might be difficult. In many cases, none of the alternative labels are relevant. For example, alternative labels for Library of Congress names often include transliterations of a given name into different scripts (rather than alternative names used by English speakers). Even if we decided to display transliterations, we cannot display all of them as there are often too many (20+ in some cases).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| description       | Stored in the graph under the `description` field on all SourceConcept nodes. Sometimes multiple descriptions might be available (in cases where a concept is linked to multiple source concepts), in which case we will have to choose one description based on a priority ranking between sources (e.g. MeSH over Wikidata).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| fieldOfWork       | Stored in the graph as SourceConceptHasFieldOfWork edges between Wikidata SourceName nodes and Wikidata SourceConcept nodes.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| relatedTo         | Family relationships are stored in the graph as SourceNameRelatedTos edges between pairs of Wikidata SourceName nodes. Other kinds of relationships are not stored in the graph and generally cannot be obtained from Wikidata. However, it is possible to show 'collaborator' relationships by listing people who are frequently referenced in the same works (i.e. connecting people through their edges to Work nodes).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| similarTo         | Can be obtained from the graph by filtering for people who are linked to a given field of work and whose birth date is in a given range. In some cases many people might be returned and choosing the most 'notable' ones might be difficult. One approach would be to determine notability based on how many works reference a given person as a concept (i.e. counting the number of edges).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | 
| memberOf          | Not stored in the graph at the moment, but can easily be obtained from the Wikidata API through the 'member of' field (P463) or the 'owner of' field (P1830).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| biography         | Not stored in the graph at the moment. To source this information from Wikipedia, we would need to extract it from the Wikipedia API via a new transformer. Alternatively, it might be possible to source this information from catalogue works, utilising the 'biographical note' field. However, there are a few practical limitations to this approach: <ul><li>The biographical note field is not very common and only exists for ~4,000 authors.</li><li>Where a biographical note is available, it often (in approx. 1,000 cases) contains general information, such as `Author contact details printed in source journal` or `Died Jun. 14 2000. GP Middlesbrough`.</li><li>In approx. 1,000, works with a biographical note have multiple contributors assigned to them, which makes it difficult to determine which contributor the note belongs to.</li><li>In some cases, the biographical note field does not contain any biographical information. For example, see [this work](https://wellcomecollection.org/works/btkphaqj) or [this work](https://wellcomecollection.org/works/qurf5s7c).</li></ul>  After filtering out all of these problematic biographical notes, we would be left with ~2,000 notes.  |
| linkedConcepts    | Can be obtained from the graph by querying for concepts which are commonly referenced in the same works (similar to 'collaborator' relationships in the `relatedTo` field).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |


### Type/technique theme pages

These theme pages are based on concepts of type `Genre`. The screenshot below shows all concept metadata exposed on this page type:

> <img src="img/example_type_theme_page.png" alt="example_type_theme_page" width="600"/>

This page has a few new pieces of information (refer to the table above for all other fields):

| Field name | Details                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| relatedTo  | Stored in the graph as a combination of multiple edge types — SourceConceptNarrowerThan (edge direction reversed), SourceConceptHasParent (edge direction reversed), and SourceConceptRelatedTo.                                                                                                                                                                                                                                                                                         |
| people     | Stored in the graph as the SourceConceptHasFieldOfWork edge (edge direction reversed). However, these edges link people to subjects (e.g. Photography) rather than techniques (e.g. Photograph). Linking subjects to techniques might be possible in some cases but it would require us to insert new edges into the graph. For example, the Wikidata entry for Photography links to the entry for Photograph via the `product, material, or service produced or provided` field (P1056). |


### Subject theme pages

Subject theme pages are based on any concept type that's not categorised as a contributor or as a type/technique. This includes Concept, Place, Meeting, and Period.
The screenshot below shows all concept metadata exposed on this page type:

> <img src="img/example_subject_theme_page.png" alt="example_subject_theme_page" width="600"/>

This page only has one additional piece of information not shown on other theme pages (refer to tables above for all other fields):


| Field name   | Details                                                                            |
|--------------|------------------------------------------------------------------------------------|
| narrowerThan | Stored in the graph as SourceConceptNarrowerThan and SourceConceptHasParent edges. |


## Works and images shown on theme pages

Like current theme pages, new theme page designs include sections listing works and images related to the given theme.
However, new theme pages expand the number of available tabs, providing more powerful filtering options.

### Contributor theme pages

For Contributor theme pages, this includes not only displaying `by <person name>` and `about <person name>` tabs,
but also additional tabs for filtering all works related to the Person/Agent/Organisation by 'format' (also known as `workType`): 

> <img src="img/works_tabs_person.png" alt="works_tabs_person" width="600"/>

In current theme pages, these tabs are populated by making a request to the catalogue API, specifying the canonical ID of
the given theme as a filter. New theme pages will use the same approach, applying additional `workType` filters
to display all the additional tabs. For example, to obtain all books about John Thomson,
a search request will be made to the works API, specifying a `subjects` filter and a `workType` filter.

### Subject theme pages

Subject theme page designs include additional tabs listing works linked to sub topics (child themes) of the given theme:

> <img src="img/works_tabs_concept.png" alt="works_tabs_concept" width="600"/>

To retrieve these works from the catalogue API, we need the *single concept endpoint* to return a list of relevant narrower topics
(in addition to the fields listed in the tables above):

| Field name  | Details                                                                                                                                                                                                                                          |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| broaderThan | Stored in the graph as SourceConceptNarrowerThan (edge direction reversed) and SourceConceptHasParent (edge direction reversed) edges. |

We can then make separate API calls to the catalogue API to retrieve a list of works for each sub topic.

However, this poses a challenge, because the relationships between works and concepts are not inherited. For example, if a work references
the concept `Sanitation - history`, it does **not** automatically reference the concept `Sanitation`, even though
`Sanitation - history` is a child (sub topic) of `Sanitation`. In general, this means that works which reference a child of
a given subject (but do not reference the subject directly) will not be automatically included in the `All` tab in
the screenshot above.

We can address this by modifying the catalogue API call to filter for all works referencing a given theme **or** any of its
sub topics (i.e. retrieving all works referencing either `Sanitation` or `Sanitation - history`). However, this would become complicated
and computationally expensive if done across multiple levels (i.e. retrieving works referencing sub topics, works referencing
sub topics of sub topics, etc.). Therefore, we should limit ourselves to one level only (i.e. direct children).


## Merging concepts across sources

Due to storing `HAS_SOURCE_CONCEPT` edges between catalogue concepts and source concepts, and `SAME_AS` edges
between source concepts, the catalogue graph allows us to 'merge' identical concepts into a single unified theme page.
For example, if a work references a LoC subject heading `Sanitation` and a different work references a MeSH term `Sanitation`,
both of these works would link to (and be listed on) the same `Sanitation` theme page.

To enable this functionality, all 'merged' concepts will be stored in the Elasticsearch index as a single document,
which will include all of their canonical IDs. This is similar to the `sameAs` field
in the current concepts index but is more space-efficient, since only one copy is stored 
of all identical concepts.
