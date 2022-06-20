# RFC: 052: The Concepts Pipeline - phase one

**Status:** :construction: Draft :building_construction:

## Executive Summary

In order to populate a new index with concept data harvested from external sources, we will
create a new concepts pipeline. This pipeline will 
- 
- fetch data from the source, 
- mint Wellcome canonical IDs (with a new Concepts ID Minter).
- save the concepts to the new index.
- save sameAs relationships to a new table in the ID Minter database

This unfiltered concepts index will be used by the Concepts API in the first phase, with filtering added in a later phase.

At first, the pipeline will only import a single source, and will therefore not need to handle merging of synonyms.

We will then add further stages to this pipeline to merge synonyms, filter unused concepts and support the knowledge graph.

As a new pipeline operating only in batch mode, this offers an opportunity to use workflow orchestration software 
such as Apache Airflow or AWS Step Functions.

## End Goal

The result of running data through this pipeline is an index to serve the concepts API with concept data, 
harvested from an external authority (Initially Library of Congress, then MeSH, and Wikidata, with the possibility 
of adding other sources as we see fit), and assigned Wellcome canonical ids.

To allow the API to be as lightweight as possible, the indexed documents will match the form in which 
they are returned by the Concepts API - currently as below:

```json
{
  "id": "ews89aeb",
  "label": "United States",
  "identifiers": [
    {
      "identifierType": {
        "id": "lc-subjects",
        "label": "Library of Congress Subject Headings (LCSH)",
        "type": "IdentifierType"
      },
      "type": "Identifier",
      "value": "n78095330"
    }
  ],
  "type": "Subject"
}
```

## A New Pipeline

```mermaid
sequenceDiagram
participant Trigger
note over Trigger: e.g. Cloudwatch/EventBridge Schedule
participant Adaptor
participant ExternalAuthority as External Authority
participant Transformer
participant Minter as Concept ID Minter
participant ConceptsIndex as Concepts Index
Trigger -) Adaptor: Update
Adaptor ->> ExternalAuthority: GET updates
ExternalAuthority -->> Adaptor : OK
Note over Adaptor: Quit here if the source document is unchanged
Adaptor -) Transformer: Here is the data
Transformer ->> Transformer: Transform into concepts
Note over Transformer: The whole dataset is now saved in one file in Concept form
Note over Transformer: Quit here if the transformed source document is unchanged
Transformer -) Minter: Here is a batch of concepts
Minter ->> Minter: Mint IDs
Minter -) ConceptsIndex: Save concepts

```

### Triggering

This pipeline is to be triggered periodically based on the expected frequency with which we expect relevant updates to 
occur in the authority's concept list, and our desire to keep up to date with it.

The Library of Congress publishes [monthly lists of changes](https://classweb.org/approved-subjects/), implying
that running this pipeline on a similar frequency would be sufficient.

### Data Flow

This pipeline is expected to run on bulk batches only, and not on updates of single concept entries.  Therefore, the
entire batch of concepts is to be kept intact as far into the pipeline as possible.

If, instead, the lists were split into individual concepts at the earliest opportunity, then later stages would have
to gather batches for efficient processing.  Sending queries for multiple IDs to the Minter database,
and bulk updates to Elasticsearch are better than doing the same thing one record at a time.

Data is stored between stages, and the next stage is then notified about the document to process.

### Quitting Early
There are two conditions under which the pipeline may quit early.

1. The document fetched from the authority is unchanged since the previous run.
   - There is no need to run the pipeline if there is nothing to do
   - How this is determined may depend on the authority
2. The document produced by the Transformer is unchanged since the previous run.
    - It is possible that some changes to a source document are irrelevant to our use of concepts and are dropped in transformation

A third situation where the pipeline produces no change, would be where all of the identifiers are already present
in the index, but as this would be discovered in the final stage, it is not really an early exit.

### The new Concepts ID Minter
#### Goal

An application that accepts a Concept object with one external identifier, and adds a persistent 
Wellcome canonical id to it.

#### Detail

A new id minter application should be created for this pipeline, to mint IDs for objects in the identifiers list. It will
accept a JSONL document, and process an appropriate number of lines with each pass.

The new minter application will use the same database as the catalogue pipeline minter, and identifier objects will be
in the same form.  This ensures that we do not have identifier collisions between Concepts and Works.

A new table in the ID Minter database will be created to maintain sameAs relationships.  This allows the existing minter
to continue working in exactly the same way - providing 1:1 mappings between canonical ids and other existing ids, 
and relying on uniqueness constraints to ensure newly minted ids genuinely new, whilst still providing a persistent 
store that can map between one Wellcome canonical id and multiple external ids.

Although the existing id minter in the catalogue pipeline is mostly agnostic as to the format of the JSON it processes,
it is not perfectly reusable as-is. At the top level, it still relies on processing Works retrieved from Elasticsearch.
This minter will be processing Concepts extracted from a JSONL document.

Unlike catalogue entries, which may contain multiple identifiers referring to other documents, a Concept object is the 
thing being identified itself.  The identifiable object is a Concept with an identifierType of wellcome-concept, akin 
finding this JSON snippet in a Work.

```
"sourceIdentifier": {
   "identifierType": {
      "id": "wellcome-concept"
   },
   "value": "${canonicalId}",
   "ontologyType": "Concept"
}
```

Where canonicalId is an identifier newly created by the same method as in [Identifiable.scala](https://github.com/wellcomecollection/catalogue-pipeline/blob/main/pipeline/id_minter/src/main/scala/weco/pipeline/id_minter/utils/Identifiable.scala),
This identifier string will serve as the id for the Concept record, and will also be stored in the identifiers list:

```json
{
  "id": "ews89aeb",
  "label": "United States",
  "identifiers": [
     {
        "identifierType": {
           "id": "wellcome-canonical",
           "label": "Wellcome Canonical Identifier",
           "type": "IdentifierType"
        },
        "type": "Identifier",
        "value": "ews89aeb"
     },
    {
      "identifierType": {
        "id": "lc-subjects",
        "label": "Library of Congress Subject Headings (LCSH)",
        "type": "IdentifierType"
      },
      "type": "Identifier",
      "value": "n78095330"
    }
  ],
  "type": "Subject"
}
```

Thus, any new identifier encountered will create a new record with two identifiers.
1. The new identifier from the authority
2. The wellcome canonical identifier generated by the minter.

Subsequent identifiers for the same concept from different authorities will be added to that list.

This diagram shows the expected flow for an individual concept identifier when encountered in either pipeline.

```mermaid
graph TD
    A[Concept Pipeline] ==>|Here's a concept id <br/>from an authority| B
    B{In Concepts Index?}
    B -->|Yes| C[No further action]
    B ==>|No| D{synonym for existing concept?}
    D -->|Yes| E[Add it to identifiers list of that Concept]
    D ==>|No| I{In sameAs table?}
    I -->|Yes| J[Create Concept object from sameAs record]
    J --> H
    I ==>|No| K[Create new Concept object with new ID]
    K ==> G
    G ==> H[Put Concepts record into Concepts Index]
    E --> G[Add QNAME->canonicalID to sameAs table in minter DB]
```

This illustrates the per-ID behaviour, but in both cases, the process will be batched appropriately, 
rather than operating on individual identifiers.

The method by which this pipeline determines that a new identifier refers to the same concept as an existing entry
is out of scope for this RFC.

#### Usage in Relation to Works

Although the identifiers are available in the same database used by the catalogue pipeline id minter, external 
identifiers in Works should not be "mintable" by that application.

This is to avoid the possibility of an identifier being minted without first 
setting up the appropriate sameAs record(s).

Instead, the flow when such a record is encountered should be as follows:

```mermaid
graph TD
    A[Catalogue Pipeline or API] -->|Here's a concept id from an authority| B
    B{In Concepts Index?}
    B -->|Yes| C[Return Concept Record]
    B -->|No| D[Ignore/Warn/label only]
```

Were canonical Ids minted as part of the catalogue pipeline, then they would 
have to be "corrected" by this pipeline when, which would add complexity, and
cause thousands of unused canonical ids to be created.

### Indexing

Each concept should index (at least) the following keyword fields from each of its identifiers.

* identifierType.id
* a concatenation of the identifierType.id and the identifier value (QName)

Indexing the identifier type id separately allows us to create queries with type filters for efficient Elasticsearch querying.

Indexing the combined identifier type and identifier as a QName guards against potential id collisions across different
schemes.  When Elasticsearch indexes the fields from an array of objects, it does so independently, meaning that it is
difficult or impossible to write queries that unambiguously matches one of these records but not the other:

* a record with a field containing an object with field1=value1 and field2=value2
* a record with a field containing at least two objects, one with this field1=value1 and another with field2=value2

Indexing in this way would allow a terms query to be used to batch retrieve identifiers when checking if they already
exist.

```json
{
   "query": {
      "filter": {
          "term": {",identifiers.identifierType": "lc-subjects"}
      },
      "terms": {
         "indentifiers.qname": [
            "lc-subjects:n78095330",
            "lc-subjects:sh85027252",
            ...
         ]
      }
   }
}
```

## Out of scope

There are some aspects of the eventual pipeline that are out of scope of this RFC.

### Fetching from more than one data source

At this point, we will only be importing from LCSH.  This RFC considers the need to fetch from multiple sources
and merging synonyms, and attempts to ensure that we do not put something in place that makes it difficult or 
impossible to do so, but does not specify how this will work.

#### Identifying synonyms

As we only have one data source, there are no synonyms to identify. Eventually, Wikidata will be the 
source of sameAs relationships that will allow us to assign the same Wellcome id to all ids referring to
the same concept.

### Fetching/prcessing deltas

When the LCSH dataset is updated, a dump of the whole set is published.  It is expected to be small enough to
process the whole set in a reasonable time.  Therefore, no consideration is given in this RFC to the method of
processing updates, instead of full dumps.

Large datasets may publish a stream of updates (e.g. Wikidata) or periodic deltas.  Where a dataset is very large,
it would be beneficial to process the full set once, then process only the updates in subsequent runs.

### Destructive changes

There are two types of destructive change that may occur in the eventual pipeline:

1. Deletion of an external identifier
2. Moving an external identifier to a different Concept

#### Deletion

Although there are [processes for deletion](https://www.loc.gov/aba/publications/FreeSHM/H0193.pdf) of LCSH entries,
the eventual Concepts index is expected to be driven by Wellcome's usage of identifiers.  Deleting identifiers
when the external authority deletes them should be driven by cataloguing practice.

#### Moving

In this phase, there will be a 1:1 correspondence between external authority identifiers and Wellcome identifiers.
Moving identifiers will become an issue when we incorporate multiple data sources and resolve synonyms, and should
be given some serious thought when that implementation is designed.

##### Example

An example for consideration when designing for moving identifiers:

Wikidata Q166907 currently tells us that these two are the same, but at one point, they were not.

- MeSH: D003027
- LCSH: sh85027252

Day 1:
- D003027 = Q166907
- sh85027252 not present on Wikidata

After processing:
- D003027 = canonical_id_1
- sh85027252 = canonical_id_2

Day 2:
- D003027 = Q166907
- sh85027252 = Q166907

Now sh85027252 should be canonical_id_1 (or D003027 should be canonical_id_2)

Day 3:
- D003027 = not present on Wikidata - how do we detect that?
- sh85027252 = Q166907

What happens now?

### The Knowledge Graph

A knowledge graph that links different concepts will eventually exist.  When it does, it can be used
and/or populated in a new stage in the pipeline.

### Filtering Unused Concepts

At first, we will simply use the entire set of imported concepts. This will be needed regardless of whether we filter 
them.  Later, we can add a stage to filter the concepts based on what we actually use.  This will likely come after the 
end of the pipeline described in this document, and will copy all matching concepts from the index created here into a 
new index which will become the Concepts Index used by the Concepts API and Catalogue pipeline.

Consideration will also need to be given to how previously removed Concepts
will be "unfiltered" when a new Work references them.

### Triggering Concept Changes in Works

This RFC governs the first phase of developing a pipeline to store Concepts for the Concepts API. It does not 
govern how Concepts are to be used by Works.

When changes to Concepts occur, it would be correct to ensure that those changes are reflected everywhere they are
used.  However, this phase only involves identifiers from one external Authority.  It is unlikely that there will be
changes that need to be reflected immediately elsewhere.

## Other Future/Related Work

### ID Minter Service

For some time, the idea of an ID Minter service (e.g. an API) has been floated. This would be a service used by 
the existing catalogue pipeline and any other system that requires it.

The Concepts Pipeline would be one such "other system". This RFC does not propose setting up that service now
as a prerequisite to the pipeline.  However, were one to exist, this would use it.

## Open Questions

### Platform
As a new, batch-only pipeline, this offers the opportunity to use a workflow orchestration system 
like [Apache Airflow](https://airflow.apache.org) or [AWS Step Functions](https://docs.aws.amazon.com/step-functions/index.html). What should we use?

AWS Step functions offers a Workflow Designer and Data flow simulator, and can easily be triggered 
by a CloudWatch/EventBridge definition.

![The flowchart shows the various steps (as AWS Lambdas) and choices described in this document.](/Users/butcherp/Documents/GitHub/docs/rfcs/052-concepts-pipeline/StepFunctionsDesign.png "A chart depicting an example AWS Step Function for this pipeline")
![This flowchart shows how AWS Step Functions displays an execution of a pipeline, with different coloured nodes based on what happened at that stage](StepFunctionsRun.png "Hello World example")

These definitions show Lambda invocations, but pretty much any AWS Service can be 
invoked by a Step Function.

### Works
When Works are presented via the API, do we want to distinguish between concept ids added by cataloguers 
and those inherited by sameness?

How are we to ensure that changes to Concepts are reflected in the Works associated with them?

Will any of those decisions influence decisions within the scope of this RFC.

## Local Glossary

### Authority

An external organisation that maintains a set of concept identifiers.

### External Identifier

The identifier used by an Authority for a Concept.

### QName

The concatenation of the identifier of an Authority, with an identifier from that authority.

Analogous to a [prefixed XML QName](https://en.wikipedia.org/wiki/QName).

### Source Document

The published, downloadable form of an authority's set of concepts, e.g. a JSONL dump.

