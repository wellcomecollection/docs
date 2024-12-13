# RFC 066: Catalogue Graph pipeline

This RFC outlines considerations for the development of the cagalogue-graph pipeline. The first iteration of the graph will be focused on concepts and their enrichment with data from external ontologies, as discussed below.

## Loading data from external sources

Where possible, data for source concept nodes will be loaded to the graph in full. This currently applies to data from Library of Congress Subject Headings (LCSH), Library of Congress Name Authority File (LCNAF), and MeSH. Unless the size of the data is prohibitive (for example, in the case of Wikidata), the slightly higher storage needs will be outweighed by advantages associated with minimising dependencies, resulting in simplified pipeline logic and updates. 

For instance, if we were to only load source entries which appear in our concepts, we would need to fetch new data every time a previously unseen concept is added to the graph. This includes any label-derived concepts we want to match to LoC and MeSH. For example, let's say we add a new LoC source node, we would in turn have to fetch other nodes from LoC (for example, broader/narrower terms). Following this, we would need to add any Wikidata concepts associated with these. For these Wikidata entries, we would then need to check if there is a MeSH term associated to it. If the MeSH term is not already present in the graph, any parent terms which appear in the hierarchy would also have to be loaded. 

Instead, if we load source nodes and edges from LoC and MeSH in full, we would only need to add an edge between the new concept and the source it is connected to. Source node and edge extraction can happen independently, and their frequency can be scheduled around updates to LoC and MeSH. To make sure there are no dependencies between different sources, the data will be loaded in multiple passes, whereby nodes and within-vocabulary edges will be loaded first, followed by edges between different vocabularies.

### Library of Congress

`SourceConcept` nodes from LCSH, as well as within-LoC edges will be loaded in full from "https://id.loc.gov/download/authorities/subjects.skosrdf.jsonld.gz". `SourceName` nodes from LCNAF (including additional fields for birth date, death date, and birth place), as well as within-LoC edges will be loaded in full from "https://id.loc.gov/download/authorities/names.skosrdf.jsonld.gz".

Given that location terms appear in both LCSH and LCNAF, there needs to be some pipeline logic to extract `SourceLocation` nodes from both via their being an instance of `MADS/RDF Geographic`. This is to avoid cross-links between `SourceConcept` and `SourceName` nodes via Wikidata and MeSH. It may be desirable create new source nodes for other entities such as organisations in the future, so we can collect relevant metadata on these from Wikidata. For example, organisations are currently part of LCNAF and will therefore be `SourceName` nodes with empty birth/death dates. However, unlike geographic locations, they are not affected by any cross-linking issues and will thus be deprioritised in the first iteration of the graph pipeline.

There are some LoC concepts which have the same label, but different identifiers. This mainly affects geographic locations, which sometimes have another entry with a `-781` suffix and do not contain any references to internal or external (Wikidata) concepts. These can be skipped during node extraction to avoid duplicates. Any `Concept` nodes referencing such an identifier should instead be connected to the respective source node without the suffix.

`SAME_AS` edges between LoC and Wikidata are present in "https://id.loc.gov/download/externallinks.nt.zip". As described above, edges linking different ontologies will be loaded in a second pass, after source nodes and within-ontology edges. It is worth noting that Wikidata also contains references back to LoC, and further investigation may be needed to quantify the amount of overlap and completeness of these links in the two source datasets. To simplify the pipeline, we can choose to load these edges only from one source and not the other. In the first pipeline iteration, it may be preferable to use the `SPARQL` query described in the next section to retrieve all Wikidata entries referencing any LoC identifier, instead of lookup queries of Wikidata identifiers extracted from LoC.

LoC source data has a monthly update frequency. Corresponding graph updates may be scheduled at a lower frequency, comparable to current reindexing of concepts in the concepts API.

### Wikidata

JSON dumps containing all Wikidata entities in a single JSON array can be found under "https://dumps.wikimedia.org/wikidatawiki/entities/". However, due to the large size of these data dumps (currently, `latest-all.json.gz` is approximately 140 GB), only as subset of Wikidata source concepts will be loaded to the graph. This is in contrast to the other data sources and may be associated with some additional pipeline complexities. 

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

Wikidata entries will reference MeSH identifiers either with or without qualifier, but not both.

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

### MeSH
MeSH data will be loaded in full from https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/. It will not be necessary to schedule frequent updates as the source data is only updated annually.

* Connecting MeSH to LoC via UMLS https://www.nlm.nih.gov/research/umls/index.html (something to consider for future iteration of graph pipeline)
* Data issues with manually tagged concepts - flag upstream and add checks in pipeline, e.g. for identifier matching label, before loading edges between concept and source nodes based on identifier

## Other considerations

These are other pipeline considerations which apply to the graph in general, independently from the source data.

### Edge directionality

* Edges are all directional in the database (undesirable for performance reasons to run an undirected query)
* Some edges should be queryable from both sides, e.g. `SAME_AS` (no inherent directionality). Represent with two directional edges

### List properties

* List properties not possible in Neptune (presumably due to query performance reasons) and will be set to concatenated strings
