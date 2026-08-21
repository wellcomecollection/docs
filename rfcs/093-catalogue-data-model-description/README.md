# RFC 093: Describing the catalogue data model

**Last modified:** 2026-08-20T09:58:00+00:00

**Related RFCs:**

- [RFC 010: Data model](../010-data_model/README.md), which this RFC brings up to date
- [RFC 054: Authority vs canonical concept ids](../054-authority-vs-canonical-concept-ids/README.md)
- [RFC 064: Graph data model](../064-graph-data-model/README.md)

## Purpose

The catalogue API's structure is well documented. The meaning of the values it returns is documented
much less consistently. `reference/catalogue.yaml` records that a work carries a `workType` object
with an `id` and a `label`, but no published artefact records what the value `"k"` denotes, in which
direction the `narrowerThan` property points, or that a concept carrying an `lc-subjects` identifier
refers to the same entity as a record on `id.loc.gov`.

RFC 010 recorded an approach to this in 2019, over ontologies first written in 2017, and the artefacts
it produced have since diverged from the API. This RFC proposes rebuilding them alongside the OpenAPI
specification, publishing them from a new `id.wellcomecollection.org` domain, and adding automated
checks that fail the build when the artefacts and the API diverge. Its scope is limited to describing
Wellcome Collection's own model. Mapping that model onto external profiles is deliberately excluded.

## Context

### The position RFC 010 established

RFC 010 set out the following division:

> The ontologies are documented using OWL. We think that this is the best way to formally describe a
> complex domain model, as it makes the semantics of our data self-documenting and widely shareable.
> However, it is worth noting that although we use OWL to document the ontologies, we don't actually
> store or process any data as [RDF]. Our APIs do provide a context, which can be used to transform
> the data to an RDF model if required, but we consider them JSON-first.

The model is documented formally, the API serves JSON, and a context is offered to consumers who
require a graph representation. This RFC retains that division. The implementation has not been
maintained since.

### The current state of the artefacts

Verification carried out on 2026-08-20 established the following:

- Every Turtle link in RFC 010 returns a 404. The links reference
  `wellcometrust/platform/raw/master/...`; the organisation has since been renamed to
  `wellcomecollection` and the default branch to `main`. The files remain available at
  `wellcomecollection/platform/ontologies/Schema/`, where the last change to their content was on
  2018-12-19 and the last commit of any kind on 2019-01-29, which applied formatting.
- The API serves no context. `GET /catalogue/v2/works/{id}` contains no `@context` key and
  `/catalogue/v2/context.json` returns 404, so the statement quoted above no longer holds.
- The committed `context.json` describes an earlier version of the model. It maps `creators`,
  `publishers`, `placeOfPublication` and `publicationDate`, where the current API provides
  `contributors` and `production`. It contains no term for `subjects`, `notes`, `languages`,
  `availabilities`, `partOf` or `holdings`.
- The ontology and the context declare different namespaces. `work-ontology.ttl` uses
  `http://wellcomecollection.org/ontologies/work/` and `context.json` uses
  `http://wellcomecollection.org/ontologies/works/`. The divergence is traceable to a commit dated
  2018-12-19, titled "Changed works model to /work", which amended `work-ontology.ttl` alone.
- None of the URIs resolve. `wellcomecollection.org/ontologies/work` returns 404, and
  `id.wellcomecollection.org` has no DNS record.

That commit is a useful illustration. It changed `work-ontology.ttl` and nothing else, and no check
existed to report that the context no longer matched it.

### The machinery already in place

The OpenAPI layer has the maintenance mechanisms the model layer lacks:

| Piece | Location | Function |
| :--- | :--- | :--- |
| Specification | `catalogue-api/reference/catalogue.yaml` | OpenAPI 3.1, 43 component schemas, source of truth |
| Lint | `yarn lint:openapi` via `redocly.yaml` | Prevents a malformed specification reaching the docs site |
| Sync | `.github/workflows/sync-openapi-spec.yml` | Opens a pull request against the docs site on merge to main |
| Fan out | `.github/workflows/sync-catalogue-types.yml` | Notifies wellcomecollection.org to regenerate its TypeScript types |
| Drift tests | `OpenApiSpecEnumTest`, `OpenApiSpecEndpointTest`, `OpenApiSpecResponseTest`, `concepts/test/openapi.test.ts` | Enums against decoders, routes against paths, schemas against pipeline fixtures |
| Process documentation | `catalogue-api/reference/README.md` | Records the above, including the limits of each check |

`OpenApiSpecResponseTest` provides the pattern to follow. It verifies coverage in both directions:
every field present in the pipeline's fixtures must be documented, and every documented field must
appear in at least one fixture unless listed on a named allowlist with a stated reason. It includes
negative controls and a guard that fails if the specification adopts schema keywords its traversal
does not support. This RFC proposes extending that mechanism to two further artefacts rather than
introducing a new one.

## Proposal

### Locate the artefacts alongside the specification

| Path | Status | Contents |
| :--- | :--- | :--- |
| `catalogue-api/reference/catalogue.yaml` | Existing | OpenAPI 3.1 |
| `catalogue-api/reference/context.json` | New | JSON-LD 1.1 context for works, images and concepts |
| `catalogue-api/reference/ontology/*.ttl` | Relocated and rewritten | OWL in Turtle, from `wellcomecollection/platform/ontologies/Schema/` |
| `catalogue-api/reference/vocab/*.ttl` | New | SKOS concept schemes for the controlled term lists |

All four use the existing sync workflow and are covered by tests in the existing package. The copies
in the platform repository are replaced by a pointer to this location.

### The JSON-LD context

The context maps the API's JSON keys onto the ontology's terms. Producing it requires the model to
answer questions the JSON API has not previously had to record. Four are worth setting out here.

Identifiers are returned as bare strings, so URIs must be constructed. The value `"a222tqng"` is not a
URI. The 2017 context addressed this with a global `@base` of `http://id.wellcomecollection.org/`,
which places works, images and concepts in a single identifier space and refers to a hostname that
does not resolve. A JSON-LD 1.1 type-scoped `@base` for each class produces correct URIs without any
change to the API; this was checked against one work record and one concept record. It remains a
workaround. Returning absolute URIs from the API would be preferable, and is a larger change than this
RFC proposes.

Related concepts need separate handling within that. `RelatedConcept` is the only entity in the
specification that names its discriminator `conceptType` rather than `type`, so a type-scoped `@base`
does not reach it and its identifiers resolve to nothing. Property-scoped `@base` declarations on the
eight `relatedConcepts` properties resolve them, and aliasing `conceptType` to `@type` in addition
recovers the class of each related concept. Both were checked against a live record in two independent
JSON-LD implementations, and neither requires a change to the API.

The `broaderThan` property maps to `skos:narrower`. The property names read in the opposite direction
to their meaning. For the concept "Surgery, Plastic", `narrowerThan` contains `["Transplantation"]` and
`broaderThan` contains `["Prostheses and Implants", "Skin Transplantation", "Rhinoplasty"]`, so
`narrowerThan` lists the concepts above it in the hierarchy. Mapping these names at face value would
invert the hierarchy, and the specification provides no description for any of the four properties
concerned.

The `sameAs` property maps to `skos:exactMatch` rather than `owl:sameAs`. An incorrect `owl:sameAs`
assertion merges all statements about both resources for any consumer performing inference, and the
error propagates to downstream consumers. SKOS provides a graded set of mapping properties from
`exactMatch` to `relatedMatch`, which represents crosswalks of known imprecision more accurately.

Language handling in the committed context does not do what it appears to. It coerces `title` and
`description` with `"@type": "rdf:langString"`, which both tested processors resolve by discarding the
coercion and emitting a plain literal with no language tag, and coerces `label` with
`"@type": "rdfs:Literal"`, which types the literal with a class rather than a datatype. Neither raises
an error. Language tagging requires `"@language"`.

### The ontology

The Turtle files are rewritten against the current 43 component schemas, in the namespace determined
below. OWL serves a documentary purpose here: class and property definitions, labels, comments,
domains and ranges, and those axioms that hold of the model, such as the disjointness of `Work` and
`Item`.

OWL under open-world semantics does not reject a record for a missing value; a cardinality constraint
infers the value instead. It is therefore not a substitute for response validation, which remains with
the JSON Schema in the OpenAPI specification, where it is already established.

### The controlled vocabularies

Each closed list of values the API returns is published as a SKOS concept scheme: `workType` (18
terms in use), `noteType`, `identifierType`, `locationType`, `accessStatus`, `accessMethod` and
`availability`. These values are currently returned in the form
`{"id": "k", "label": "Pictures", "type": "Format"}`, without definitions, hierarchy or external
mappings. The SKOS schemes hold the scope notes, the Sierra codes as `skos:notation`, and the mappings
to AAT and MARC relator terms.

Contributor roles are a candidate for the same treatment but are not yet eligible. `ContributionRole`
carries only `label` and `type`, with no `id`, so there is no stable value on which to key a scheme or
hang a mapping to MARC relator terms. Adding one is a change to the specification and to the
pipeline's display model, and is not proposed here.

SKOS is preferred to OWL classes for two reasons. Thesaurus hierarchy is not subsumption:
`rdfs:subClassOf` is strict and transitive, whereas `skos:broader` is neither by default, which
corresponds more closely to the behaviour of cataloguing hierarchies. Mapping between vocabularies
also requires graded predicates, which SKOS provides and OWL does not.

The `identifierType` scheme additionally holds a URI template for each identifier type, which converts
identifiers already present in the data into resolvable links. RFC 064 recorded the following source
identifier counts on concepts:

| Source | Count | Resolves to |
| :--- | ---: | :--- |
| `label-derived` | 308,908 | no external URI |
| `lc-names` | 197,509 | `https://id.loc.gov/authorities/names/{value}` |
| `lc-subjects` | 37,343 | `https://id.loc.gov/authorities/subjects/{value}` |
| `nlm-mesh` | 28,425 | `https://id.nlm.nih.gov/mesh/{value}` |
| `viaf` | 153 | `https://viaf.org/viaf/{value}` |
| `fihrist` | 130 | `https://www.fihrist.org.uk/` |

One identifier from each of the Library of Congress and MeSH patterns was checked and resolved. A
`skos:exactMatch` to those two authorities is therefore obtainable for a substantial minority of
concepts, requiring a template for each type rather than new cataloguing. The largest group,
`label-derived`, carries no external identifier and receives no mapping.

The identifiers themselves need checking before mappings are generated from them. RFC 064 records that
770 MeSH concepts do not match the label of the term they cite, and that 617 MeSH identifiers lack the
leading `D` that MeSH descriptors require, some of them appearing to be Library of Congress
identifiers instead. A data cleaning step is likely to be required, and the number of usable mappings
will be lower than the counts above suggest.

The mapping also stops at the concept records themselves. `RelatedConcept`, which is how the concepts
API expresses hierarchy, has no `identifiers` field, so a broader or narrower concept reached through
`relatedConcepts` cannot carry its own LCSH or MeSH link. Changing that is a question for the concepts
API rather than for this proposal.

### id.wellcomecollection.org

A static, read-only service holding the ontology and the controlled vocabularies, with no entity URIs.

The service is served from S3 behind CloudFront in the `catalogue` account, following the pattern
already used by `data.wellcomecollection.org` for snapshots. It requires no database, no dynamic
lookup, and no runtime dependency on the catalogue API.

Content negotiation follows the pattern used by `id.loc.gov`, which responds with a 303 and
`Vary: Accept`. A term URI returns HTML to a browser and Turtle to a linked data client:

```
GET /vocab/format/k
Accept: text/turtle
→ 200 OK, text/turtle

<https://id.wellcomecollection.org/vocab/format/k>
    a               skos:Concept ;
    skos:inScheme   <https://id.wellcomecollection.org/vocab/format> ;
    skos:prefLabel  "Pictures"@en ;
    skos:notation   "k" ;
    skos:scopeNote  "Two-dimensional visual works: prints, drawings, paintings, photographs."@en ;
    skos:closeMatch <http://vocab.getty.edu/aat/300264387> .
```

Ontology terms behave identically, returning their definition from the Turtle files.

The context is an artefact of the API rather than of the model, since it describes the JSON keys of a
particular API version. It should therefore be served from
`api.wellcomecollection.org/catalogue/v2/context.json` and versioned with the API. Ontology and
vocabulary terms should not be minted beneath `/catalogue/v2/`, as they are required to outlive it.

Entity URIs of the form `id.wellcomecollection.org/works/{id}` are excluded from this proposal on two
grounds. First, `api.wellcomecollection.org/catalogue/v2/works/{id}` and
`wellcomecollection.org/works/{id}` have been published for several years, and a third identifier
space would create a permanent reconciliation obligation. Second, RFC 054 records why a single
authority identifier maps to several canonical ids: the ontology type forms part of the minting key.
The concept for "Universities" currently carries 11 entries in its `sameAs` array. Minting persistent
public identifiers over an identifier space known to be split would be difficult to reverse, and
should follow the settlement of the merging work described in RFC 054.

### Drift detection

Three tests are added to `search/src/test/scala/weco/api/search/openapi/`, alongside the four already
present:

| Test | Assertion |
| :--- | :--- |
| Context against specification | Every property reachable from the `Work`, `Image` and `Concept` schemas has a term in `context.json`, and every term corresponds to an existing property. Reuses the existing schema traversal. |
| Ontology against context | Every IRI the context resolves to is defined in the Turtle with a label and an `rdfs:isDefinedBy`, and every defined term is reachable from the context. Deliberate exceptions are listed on a named allowlist. |
| Context against documents | Each display document in `test_documents/` converts to RDF with no unresolved relative IRIs, no blank-node subject for any entity carrying an `id`, and a non-trivial triple count. |

The second would have detected the 2018 inconsistency, which was a disagreement between the ontology
and the context. The third detects a class of error observed during investigation: converting one live
concept record with an incomplete draft context produced 121 triples, of which 91 carried an
unresolvable IRI, and correcting the context removed all of them. The test is worth having because
processors handle that failure differently and neither reports it, so pyld mints the unresolvable IRIs
beneath a fallback base while jsonld.js discards them, reducing the same record to 30 triples and
leaving a consumer with a truncated graph and no indication that anything is missing.

Two additional JVM dependencies are required:

| Requirement | Library | Version |
| :--- | :--- | :--- |
| Turtle parsing and validation | `org.apache.jena:jena-arq` | 6.1.0 |
| JSON-LD 1.1 processing | `com.apicatalog:titanium-json-ld` | 1.6.0 |

`com.github.jsonld-java` is not suitable. Its current release implements JSON-LD 1.0, whereas the
context requires 1.1 for type-scoped `@base`, `@nest` and set containers. Its behaviour on those
constructs was not tested, so this is a stated risk rather than a measured one: a 1.0 processor is not
required to reject them.

`redocly lint` covers neither new artefact. A `lint:linkeddata` step should validate the Turtle syntax
and parse the context, and the sync workflow should invoke it alongside `lint:openapi`, so that a
malformed artefact cannot reach the docs site.

### Developer documentation

Two additions to `developers.wellcomecollection.org`:

- A `docs/data-model.md` page covering the entity model, the use of the context, and a statement of
  what the model does not represent. The existing `docs/catalogue.md` is a short introduction to
  making requests and is not a suitable location for this material.
- Links to the published context and ontology, from wherever they are ultimately served.

`catalogue-api/reference/README.md` is extended rather than supplemented by a second process document.
It is the established location for describing how the reference artefacts are kept consistent, and it
already records the limits of the existing checks.

## Out of scope

- Mapping to Linked Art, CIDOC-CRM, schema.org or any other external profile. These merit separate
  consideration, and each would begin by doing much of the work proposed here.
- Entity URIs on `id.wellcomecollection.org`, for the reasons given above.
- An RDF triple store, a SPARQL endpoint, or a graph API. The context is offered to consumers who want
  it and imposes no obligation on the API.
- Any change to the catalogue graph or the edge vocabulary defined in RFC 064. That is an internal
  enrichment store structured for Neptune queries, whereas this proposal concerns a public description
  of API output. The two may inform one another subsequently, and neither is a prerequisite for the
  other.
- Any change to API response bodies beyond an added `@context` key. The `identifiers` field missing
  from `RelatedConcept` limits the mapping coverage described above, and is noted there, but changing
  it is a question for the concepts API.

## Alternatives considered

- **Refresh the RFC 010 artefacts in their current location.** This is cheaper, but exhibits the same
  failure mode. The files were held in a repository against which nothing was tested, and the
  2018-12-19 commit demonstrates how readily they diverge. Any option adopted must place the artefacts
  where an automated check can reach them.
- **Generate the context from the Scala display models rather than from the specification.** This is
  not available from `catalogue-api`. Both services return a pre-rendered `display` document directly
  from Elasticsearch, which is why the response schemas in `catalogue.yaml` are written by hand and
  why `OpenApiSpecResponseTest` validates against pipeline fixtures rather than against code.
  Generating from the pipeline's own display model was not investigated and may be worth considering
  separately. Within this repository, the specification is the closest machine-readable description of
  the response that exists.
- **Model the controlled vocabularies as OWL classes rather than SKOS concepts.** This provides
  inference the model does not need, and cannot express approximate mappings. Asserting
  `rdfs:subClassOf` across a
  cataloguing hierarchy generates unintended entailments, and `owl:equivalentClass` cannot represent an
  approximate match.
- **Serve all artefacts, including ontology terms, from the API.** This is simpler and uses existing
  infrastructure, but embeds `/catalogue/v2/` in URIs that must outlive API v2. Separating the context
  from the model terms costs one additional domain and avoids that outcome.
- **Derive the controlled vocabularies from the catalogue graph.** The graph already links concepts to
  LCSH, MeSH and Wikidata. However, its vocabulary (`HAS_SOURCE_CONCEPT`, `SAME_AS`, `NARROWER_THAN`,
  `HAS_PARENT`) is structured for graph traversal rather than for publication, and it covers concepts
  rather than the controlled term lists that form the majority of this proposal. The graph is a
  plausible future source for concept-level mappings but is not a source for the `workType` scheme.
- **Take no action.** The API surface remains documented, and the meaning of the values it returns
  remains undocumented. Consumers must reconstruct these mappings themselves from data we hold but do
  not publish as links, and any future publication in an external profile begins by undertaking this
  work regardless.

## Impact

- **Consumers.** One additional key in response bodies, which JSON consumers may ignore. No breaking
  change to any existing field.
- **The team.** Three further tests to maintain, two allowlists requiring stated reasons, one
  additional artefact in the sync workflow, and a small static deployment to own.
- **Cataloguing.** Scope notes and AAT mappings for the `workType` and `noteType` schemes require
  input from staff familiar with the meaning of the terms. The vocabularies can be published without
  them, carrying labels and notations only, and enriched subsequently, though their utility in that
  state is considerably reduced. This dependency should be understood before the work begins.
- **Risks.** Publishing URIs is a long-term commitment; those proposed here cover small closed lists
  that change infrequently, which limits the exposure. The new tests will fail when the pipeline's
  display model changes, which is the intended behaviour, but it means such changes will arrive with
  more failing tests than at present.

## Next steps

1. Agree the namespace. Resolve the singular and plural inconsistency, confirm
   `id.wellcomecollection.org`, and record the domain in `architecture/domain_names.md`.
2. Relocate the Turtle files to `catalogue-api/reference/ontology/`, rewrite them against the current
   43 schemas, and leave a pointer in the platform repository.
3. Add `catalogue-api/reference/context.json`.
4. Add the three drift tests and the Jena and Titanium dependencies, and add `lint:linkeddata` to the
   sync workflow.
5. Author the SKOS schemes, beginning with `workType` and `identifierType`, which offer the clearest
   return.
6. Deploy `id.wellcomecollection.org` as static objects with content negotiation.
7. Serve the context from the API and write `docs/data-model.md`, once the artefacts they describe
   exist.

Steps 2 to 4 are contained within `catalogue-api` and follow patterns already established there. Step
1 is the only step requiring a decision outside the team, and steps 5 to 7 depend on it.
