# RFC 048: Concepts work plan

This RFC outlines the work plan for introducing concepts to the Wellcome digital platform, including the design of a concepts API, knowledge graph population, and integration with works.

**Last modified:** 2022-05-10T13:14:58+01:00

## Context

We are now starting work on introducing "concepts" to the Wellcome digital platform: identifiable entities like subjects, people, organisations, genres, etc. Works can be tagged with concepts, and concepts can be linked to other concepts by (for example) predicates, in this way forming a knowledge graph. We will start by using concepts that are manually tagged in the source catalogues, and in future we might infer a work's concepts.

This opens the door to a variety of possible user outcomes. A small number of these might be...

- Dedicated, search-engine-indexable pages for (eg) subjects and people. These can possibly include curated content.
- Searching by concept (rather than by keyword).
- Navigating between concepts by their relationships to one another.
- Having access to data on concepts from other sources (for example, Wikipedia) within the wc.org experience.

The initial stage of this work will be to implement a minimal version of the first of these points: we will call these pages **concept pages**. These will likely not refer externally to "concepts"; instead it will be restricted to the aforementioned subjects and people.

This RFC outlines the major technical decisions that will need to be made around data modelling, API design, and system architecture in order to serve this outcome - it does not aim to _make_ any of these decisions.

## What needs to be done

This approach presupposes the following architectural decisions:

- There is a separate API endpoint within the catalogue for concepts 
- There is a knowledge graph of concepts that exists independently of works
- Works will be tagged with identifiable concepts which (may) exist in the knowledge graph

#### 1. Concepts API Design

We need to design an API that will allow us to populate concept pages. This may be one API for all concept types (ie subjects or people), or different APIs may provide different types. It should be designed in such a way that the future inclusion of curated content is possible. There should be sufficient information on a concept to disambiguate it (eg birth/death dates for people).

#### 2. Knowledge graph population

We need to populate a knowledge graph (wherein the nodes are concepts or have an injective mapping to concepts) from arbitrary sources eg. LCSH, LC names, MeSH, Wikidata, Wikipedia. This will likely initially be just one source without consideration of edges.

#### 3. Identified concepts on works

Where works are tagged with identifiable (in practice, Library of Congress and MeSH) concepts, we need to be able to match these up with concepts in our knowledge graph. The outcome here is that, given a work, we should be able to know its subjects/agents/etc, and given a concept, we should be able to query for the works that are tagged with it.

## Extra thoughts

- Is there any level of denormalisation of concepts onto works / vice versa?
- How will we handle multiple source identifiers mapping to individual canonical identifiers?