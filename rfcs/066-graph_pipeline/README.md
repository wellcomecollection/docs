# RFC 066: Catalogue Graph pipeline

This RFC outlines considerations for the development of the cagalogue-graph pipeline. The first iteration of the graph will be focused on concepts and their enrichment with data from external ontologies, as discussed below.

## Loading data from external sources

Where possible, data for source concept nodes will be loaded to the graph in full. This currently applies to data from Library of Congress Subject Headings (LCSH), Library of Congress Name Authority File (LCNAF), and Medical Subject Headings (MeSH). Unless the size of the data is prohibitive (for example, in the case of Wikidata), the slightly higher storage needs will be outweighed by advantages associated with minimising dependencies, resulting in simplified pipeline logic and updates. 

If we were to only load source nodes linked to our concepts, we would need to fetch new data every time a previously unseen concept is added to the graph. This includes any label-derived concepts we want to match to LoC and MeSH. For example, let's say we add a new LoC source node, we would in turn have to fetch other nodes from LoC (for example, broader/narrower terms). Following this, we would need to add any Wikidata concepts associated with these. For these Wikidata entries, we would then need to check if there is a MeSH term associated to it. If the MeSH term is not already present in the graph, any parent terms which appear in the hierarchy would also need to be loaded. 

Instead, if we load source nodes and edges from LoC and MeSH in full, we only need to add an edge between the new concept and the source it is connected to. Source node and edge extraction can happen independently, and their frequency can be scheduled around updates to LoC and MeSH. To make sure there are no dependencies between different sources, the data will be loaded in multiple passes, whereby nodes and within-vocabulary edges will be loaded first, followed by edges between different vocabularies.

### Library of Congress

`SourceConcept` nodes from LCSH, as well as within-LoC edges will be loaded in full from https://id.loc.gov/download/authorities/subjects.skosrdf.jsonld.gz. `SourceName` nodes from LCNAF (including additional fields for birth date, death date, and birth place), as well as within-LoC edges will be loaded in full from https://id.loc.gov/download/authorities/names.skosrdf.jsonld.gz.

Given that location terms appear in both LCSH and LCNAF, there needs to be some pipeline logic to extract `SourceLocation` nodes from both (for instance, via their grouping into `MADS/RDF Geographic`). This is to avoid cross-links between `SourceConcept` and `SourceName` nodes via Wikidata and MeSH. It may be desirable to create new source nodes for other entities such as organisations in the future, so we can collect relevant metadata on these from Wikidata. For example, organisations are currently part of LCNAF and will therefore be `SourceName` nodes with empty birth/death dates. However, unlike geographic locations, they are not affected by any cross-linking issues and will thus be deprioritised in the first iteration of the graph pipeline.

There are some LoC concepts which have the same label, but different identifiers. This mainly affects geographic locations, which sometimes have another entry with a `-781` suffix and do not contain any references to internal or external (Wikidata) concepts. These can be skipped during node extraction to avoid duplicates. Any `Concept` nodes referencing such an identifier should instead be connected to the respective source node without the suffix. However, there are also duplicate LoC concepts which cannot be easily identified via a suffix. For example, the LCSH concept `Gambling` has two identifiers, [sh00002545](https://id.loc.gov/authorities/subjects/sh00002545.html) and [sh85052909](https://id.loc.gov/authorities/subjects/sh85052909.html), representing the same entity. This may result in duplicates when matching concepts from the catalogue to LoC via their identifier, where only one of the two concepts would be associated with onward connections. We can resolve this by adding `SAME_AS` edges between such LoC concepts in the future, which will avoid having to build complicated deduplication logic into the pipeline. Further investigation is needed to establish whether these can simply be matched by their label or if more complex methods are required to resolve LoC entities (for example, it is currently not clear if any of the duplicate labels are actually referring to different entities, or if there are additional LoC concepts with slightly different labels referring to the same entity).

`SAME_AS` edges between LoC and Wikidata are present in https://id.loc.gov/download/externallinks.nt.zip. As described above, edges linking different ontologies will be loaded in a second pass, after source nodes and within-ontology edges. It is worth noting that Wikidata also contains references back to LoC, and further investigation may be needed to quantify the amount of overlap and completeness of these links in the two source datasets. For example, the LCSH entry for [gene therapy](https://id.loc.gov/authorities/subjects/sh85053738.html) does not contain a reference to Wikidata, whereas the Wikidata entry for [gene therapy](https://www.wikidata.org/wiki/Q213901) does link back to LCSH. To simplify the pipeline in the first iteration, we may choose to load these edges only from one source and not the other. For example, it may be preferable to use the SPARQL query described in the next section to retrieve all Wikidata entries referencing any LoC identifier, instead of multiple lookup queries of Wikidata identifiers extracted from LoC.

LoC source data has a monthly update frequency. Corresponding graph updates may be scheduled at a lower frequency, comparable to current reindexing of concepts in the concepts API.

### Wikidata

JSON dumps containing all Wikidata entities in a single JSON array can be found under https://dumps.wikimedia.org/wikidatawiki/entities/. However, due to the large size of these data dumps (currently, `latest-all.json.gz` is approximately 140 GB), only as subset of Wikidata source concepts will be loaded to the graph. This is in contrast to the other data sources and may be associated with some additional pipeline complexities. 

The current plan is to use SPARQL queries to load tems which contain references to/from LoC and/or MeSH, as well as their parent terms.

The following query retrieves all Wikidata items referencing any LCSH or LCNAF identifier (`anyValueP244`), and returns the following properties for each item: 
* Wikidata identifier
* label
* description
* alternative labels
* Wikidata identifier, label, description, and alternative labels of `instance of` parent term
* Wikidata identifier, label, description, and alternative labels of `subclass of` parent term
* `date of birth` label
* `date of death` label
* `place of birth` label
* Wikidata identifier and label of `country`
* `coordinate location`
* `Library of Congress` identifier

Apart from the LoC identifier, the other properties are optional.

```
SELECT DISTINCT ?item ?itemDescription ?itemAltLabel ?instance_of ?instance_ofLabel ?instance_ofDescription ?instance_ofAltLabel ?subclass_of ?subclass_ofLabel ?subclass_ofDescription ?subclass_ofAltLabel ?date_of_birthLabel ?date_of_deathLabel ?place_of_birthLabel ?country ?countryLabel ?countryDescription ?countryAltLabel ?coordinate_location ?Library_of_Congress_authority_ID WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
  {
    SELECT DISTINCT ?item WHERE {
      ?item p:P244 ?statement0.
      ?statement0 ps:P244 _:anyValueP244.
    }
  }
  OPTIONAL { ?item wdt:P31 ?instance_of. }
  OPTIONAL { ?item wdt:P279 ?subclass_of. }
  OPTIONAL { ?item wdt:P569 ?date_of_birth. }
  OPTIONAL { ?item wdt:P570 ?date_of_death. }
  OPTIONAL { ?item wdt:P19 ?place_of_birth. }
  OPTIONAL { ?item wdt:P17 ?country. }
  OPTIONAL { ?item wdt:P625 ?coordinate_location. }
}
```

The following query retrieves all Wikidata items referencing any MeSH or MeSH+qualifier identifier (`anyValueP486` or `anyValueP9340`), and returns and returns the following properties for each item: 
* Wikidata identifier
* label
* description
* alternative labels
* Wikidata identifier, label, description, and alternative labels of `instance of` parent term
* Wikidata identifier, label, description, and alternative labels of `subclass of` parent term
* Wikidata identifier and label of `country`
* `coordinate location`
* `MeSH descriptor` identifier
* `MeSH descriptor and qualifier` identifier

Wikidata entries contain references to MeSH identifiers either with or without qualifier, but not both.

```
SELECT DISTINCT ?item ?itemDescription ?itemAltLabel ?instance_of ?instance_ofLabel ?instance_ofDescription ?instance_ofAltLabel ?subclass_of ?subclass_ofLabel ?subclass_ofDescription ?subclass_ofAltLabel ?country ?countryLabel ?countryDescription ?countryAltLabel ?coordinate_location ?MeSH_descriptor_ID ?MeSH_descriptor_qualifier_ID WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE]". }
  {
    SELECT DISTINCT ?item WHERE {
      {
        ?item p:P486 ?statement0.
        ?statement0 ps:P486 _:anyValueP486.
      }
      UNION
      {
        ?item p:P9340 ?statement1.
        ?statement1 ps:P9340 _:anyValueP9340.
      }
    }
  }
  OPTIONAL { ?item wdt:P31 ?instance_of. }
  OPTIONAL { ?item wdt:P279 ?subclass_of. }
  OPTIONAL { ?item wdt:P17 ?country. }
  OPTIONAL { ?item wdt:P625 ?coordinate_location. }
  OPTIONAL { ?item wdt:P486 ?MeSH_descriptor_ID. }
  OPTIONAL { ?item wdt:P9340 ?MeSH_descriptor_qualifier_ID. }
}
```

There needs to be some logic to split concepts from Wikidata correctly into `SourceConcept`, `SourceName`, and `SourceLocation` nodes, which can be designed in the following way: Any item with a `country` property will be a `SourceLocation`, anything referencing a LCNAF identifier which is not a location will be a `SourceName`, and anything else a `SourceConcept`.

As noted in [RFC #64](../064-graph-data-model/README.md), Wikidata has a wide range of properties, and we may need to modify our queries to include additional metadata in future iterations of the graph pipeline. For example, Wikidata includes links to a wide range of external databases (e.g.the National Portrait Gallery, OpenAlex and many more), which we may want to add to `alternative_ids`.

### MeSH
MeSH data will be loaded in full from https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/. The It will not be necessary to schedule frequent updates as the source data is only updated annually. 

Since MeSH does not contain any names, we only need to split these into `SourceConcept` and `SourceLocation`, which will be implemented as follows: MeSH terms from the `Geographicals` branch (identifiable via their `Z` tree code) will be loaded as `SourceLocation` nodes, everything else will be loaded as `SourceConcept`.

There are some concepts in the catalogue which come with a MeSH qualifier. MeSH identifiers with a qualifier code will be split such that the concept is linked to its MeSH identifier via a `HAS_SOURCE_CONCEPT` edge and the qualifier added as an edge property.

It is worth noting that an analysis of MeSH concepts from the catalogue has revealed data quality issues affecting some concepts, such as mismatches between labels and MeSH identifiers. For example, there are concepts tagged as MeSH but which have a LoC-type identifier, and MeSH terms such as Sanitation with an identifier which does not link back to Sanitation. Rather than building additional logic into the pipeline to clean this data, we will instead add data quality checks (to make sure we only load source nodes for concepts where the label matches the identifier) and flag these issues directly with the cataloguers. While this will result in a delay for some MeSH concepts to be added to the graph, it will avoid some complexity within the pipeline code.

MeSH concepts will initially only be indirectly linked to LoC concepts via `SAME_AS` edges between Wikidata and these sources. However, there is a possibility to extract direct links from the [UMLS metathesaurus](https://www.nlm.nih.gov/research/umls/index.html), which covers both MeSH and LCSH, in a future iteration of the graph pipeline.

## Other considerations

These are other pipeline considerations which apply to the graph in general, independently from the source data.

### Edge directionality

When creating an edge between two nodes in a graph database such as AWS Neptune, the edge is always directed, even if the direction is omitted in the Cypher query. For example, the following query will create a directed edge from node a to node b:
```
MATCH
    (a:NodeA {property_a: property_a}),
    (b:NodeB {property_b: property_b})
MERGE (a)-[r:REL]-(b)
```
Furthermore, it is undesirable in terms of query performance to run undirected queries, as explained [here](https://docs.aws.amazon.com/neptune/latest/userguide/best-practices-opencypher-directed-edges.html).

However, the current graph data model does include some edges which do not have any inherent directionality and should be queryable from both sides (for example, `SAME_AS` edges between two source concepts from different ontologies). To avoid introducing an artificial hierarchy between ontologies, and given that this will not add too much storage overhead, these relationships will be represented with two directed edges.

### List properties

It is not possible to create array type properties in AWS Neptune (see [here](https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load-tutorial-format-opencypher.html) for an overview of possible data types). Any list properties (such as `alternative_labels`) will be concatenated to a string, with a `||` separator between individual items. While this can be seen as a limitation, we may benefit from better query performance resulting from indexing of these strings in the graph database.

### Label-derived concepts

In the first iteration of the graph pipeline, label-derived nodes which have the `type` property `Concept` will be matched to `SourceConcept` nodes via their label and matches added as `HAS_SOURCE_CONCEPT` edges (the `matched_by` attribute will be set to `label`). Further analysis will be made on how to match other label-derived concept types (e.g. `Person`), which may be more ambiguous. In addition, there are label-derived concepts which are similar, but not exactly the same as another concept from an external ontology. A machine learning algorithm can be used to perform entity resolution on these label-derived concepts to match them to external sources. The proposed graph model (see [RFC #64](../064-graph-data-model/README.md)) and pipeline design will enable us to apply different matching algorithms and/or rules to subsets of label-derived concepts and store the results in the graph together with the source of the match (e.g. `label`, `ml-derived` etc.). This will make it straightforward to filter and selectively enable/disable merging of label-derived with external source concepts.
