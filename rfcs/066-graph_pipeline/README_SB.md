# RFC 066: Catalogue Graph pipeline

## Implementation

The catalogue graph pipeline will be implemented in Python. The pipeline will consist of the following components (see
diagram below):

* Each concept source (e.g. MeSH, LoC, Wellcome catalogue) will have a corresponding `Source` class, which will
  include logic for downloading raw concepts and stream them to subsequent components for processing.
* Each combination of concept source and concept type (e.g. LoC name, LoC location, MeSH concept) will have a
  corresponding `Transformer` class, which will include logic for extracting nodes and edges (separately) from each raw
  concept and converting them into the desired format for indexing into the Neptune database.
* Transformed concepts will be streamed in batches to the `CypherQueryBuilder`, which will be responsible for creating
  openCypher upsert queries.

![implementation.png](figures%2Fimplementation.png)

Items will be indexed in the order indicated in the diagram. This ordering ensures that nodes are always indexed
before edges, and source concepts are always loaded before Wellcome catalogue concepts.

`SAME_AS` edges between SourceConcept nodes will be extracted in two stages. The first involves running a SPARQL query
against Wikidata to extract all linked LoC and MeSH subjects. The second involves downloading the external links file
from LoC and extracting all linked Wikidata subjects. The ordering of these two stages does not matter, and in the
diagram they are both labeled `3`. In the first version of the graph, only one of these stages might be implemented.

`HAS_SOURCE_CONCEPT` edges will also be extracted in two stages. In the first stage, edges will be created
based on source concept IDs explicitly referenced by catalogue concepts. For example, if a given catalogue item lists
an LoC concept as a source concept, a `HAS_SOURCE_CONCEPT` edge will be created between the catalogue concept and the
LoC concept. (In the diagram, this stage is labeled `5`.) In the second stage, all catalogue concepts will be streamed
into the `ConceptsMatcher`, which will use an
algorithm to create additional `HAS_SOURCE_CONCEPT` edges. For the purposes of this RFC, the `ConceptsMatcher` is a
black box, but in practice it might create edges based on matching labels, or based on a machine learning
algorithm. (In the diagram, this stage is labeled `6`). In the first version of the graph, only the first stage might be
implemented.

Additionally, the implementation will follow these principles:

* All components will utilise streaming via Python generators when processing individual items to ensure that we only
  hold a fraction of the full dataset in memory at any given time.
* Neptune supports mixing several query languages, but we will stick to openCypher where possible for consistency.
* Final graph datatypes (included as yaml files in RFC 064) will be expressed as Pydantic models for automatic data
  validation and type safety.
* Repeatedly inserting the same node or edge into the graph should only result in one node or edge being created. In
  practice this means implementing all operations as "upsert" operations. In openCypher language, this means using
  `MERGE` instead of `CREATE`.

TODO: Is there a case where we would prefer using CREATE instead of MERGE?

## Architecture

The catalogue graph pipeline will run on a serverless event-driven architecture. All processing will be done by two
Lambda functions, an `extractor` Lambda function, and an `indexer` Lambda function.

The `extractor` will be responsible for:

1. Communicating with concept sources and extracting a stream of raw source concepts via `Source` classes.
2. Transforming each item in the stream into a source concept via `Transformer` classes, utilising the corresponding
   Pydantic models.
3. Batching multiple items and building final openCypher queries using the `CypherQueryBuilder` before sending the
   queries into an SNS topic, which will be connected to an SQS queue.

The `indexer` will be responsible for:

1. Consuming queries in the SQS queue via
   an [event source mapping](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html) and
   executing the queries against the cluster using
   the `NeptuneClient` class. Importantly, the `indexer` will be agnostic to the content of the queries, all logic
   constructing the queries will be contained in the `extractor`.

There are several reasons for separating out the `indexer` functionality into its own Lambda function and placing it
behind an SQS queue:

1. Due to the large number of indexed items (hundreds of thousands to millions), indexing from a single Lambda would
   likely exceed the maximum allowed execution time of 15 minutes. (We experimentally verified that we can index at most
   100 items per second to the Neptune cluster from a single thread, even when utilising batching via openCypher's
   UNWIND clause.)
2. Consuming from an SQS queue will allow multiple functions to run in parallel, allowing us to index items more quickly
   without having to implement multithreading logic in our code. (Overwhelming the cluster with multiple running Lambdas
   is not a concern as the serverless cluster should automatically scale based on traffic.)
3. The event source mapping can be configured to insert a query back into the queue in case of error, providing an
   automatic solution to transient faults. Additionally, queries which repeatedly fail will be placed in the DLQ, where
   they can be investigated.

The `extractor` could also be separated into several smaller microservices, but this would add a cost and performance
overhead, as processed items would have to be serialised and deserialised between individual steps.

Each invocation of the `extractor` Lambda function will only execute one Transformer, based on the input passed to the
Lambda function. Execution will be orchestrated via AWS Step Functions. Execution order will follow the ordering in the
diagram above — top to bottom, and nodes before edges.
