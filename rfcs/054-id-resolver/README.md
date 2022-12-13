# RFC 054: An Authoritative ID Resolver

## What?

A Catalogue Pipeline stage and Concepts API feature to retrieve additional information about Concepts that are derived from external authorities.

The additional information includes:

* The type of the referent
* Identifiers and types for any components of a composite type

## Where?

The Catalogue Pipeline stage belongs between the Transformers and the ID Minter.

The Concepts API feature will be associated with the authoritative-concepts index.

## Why is it Needed?

This proposal resolves four problems.  The first three of these problems manifest as either duplicate or missing Concepts in the Concepts API.

### Type Inference

Currently, transformers infer the type of a Concept from its use in the input. This can lead to incorrect and
inconsistent types being applied.

In MARC, for example, `x00` fields contain "Personal Name" fields, so are expected to contain Concepts of type Person.
Places can be found in `651` (Geographic Term) fields, etc.  In these cases, the Authoritative Identifier for the Concept 
is extracted from the `$0` subfield.

However, this is neither validated before reaching the pipeline, nor are these rules reliable.

In practice, a `700` field may contain a Person, or it may contain a text attributed to the named person.  Which one it is
can only be known by checking the identifier from `$0` against a known record. (see the Malmonides Problem, below)

### LoC namespace

MARC data from Sierra does not distinguish between LCSH and LCNames. They are both signalled by the use of `indicator2=0`.
As with type, above, the namespace is inferred from the field.  In "Name" fields (`x00`, `x10`, `x11`), it is assumed to be
LCNames. In "Term" fields (`648`, `650`, `651`), it is assumed to be LCSH.

This is not reliable.  Many "Geographical Terms" are in fact Names of Places.

I believe that this could be resolved by examining the first character of the identifier (n for LCNames, s for LCSH).

### Compound Concepts

Compound concepts in MARC data from Sierra bear an identifier referring to the whole concept, but the transformer
also breaks them up into the individual constituent concepts.  However, the identifiers for these constituent concepts 
are only "label-derived".  LoC and MeSH entries for compound concepts also contain the identifiers for the constituents,
so a new stage could populate these properly.

### Validation

Currently, there is no validation as to whether the given identifier actually exists within the given scheme.
Even if it does, there is no validation as to whether there is any correspondence between the name of the concept
and the identifier.

As a result, there are some errors that can currently only be detected by eye.

* Some MeSH identifiers have been found wrongly assigned to the LCSH scheme.  
* Two LCNames identifiers (n50034502 and n2001003970) do not exist
* Some identifiers in the LCSH scheme have been parsed/written incorrectly, so they are not identifiers at all.
* The wrong field was being extracted from some TEI records to find the LCSH id.

In addition, there may be some that are very difficult to detect by eye.  A real identifier that refers to something different
to the label of the field would only be detected when someone follows a link and finds themselves on a wholly unexpected Concept page.
`n2001003970`, mentioned above, does not exist but `nr2001003970` does.  
However, that identifer refers to the "Partnership for Governance Reform in Indonesia", whereas
the associated label in the offending Work is "Pseudo Aristotele., De coloribus., Latin".

## What about the Concepts Embedder?

The Concepts Embedder is a proposed new part of the catalogue pipeline that uses Concepts in the Concept Store.
It will include information from the Knowledge Graph.  The information described above would be available at the Concept Embedder
stage, but it is too late in the Catalogue Pipeline.

There is also a circular problem.  If a Concept is not used in the Catalogue, then it does not enter the Knowledge Graph and 
therefore does not become available at the Concept Embedder stage.  This may mean extra complexity at that stage
to determine the sameness of Concepts that have been recorded with the wrong Authority Namespace or Type.  Or where
an Authoritative Concept has been recorded as a top-level, atomic concept in one Work, and as part of a compound in another.
By resolving those issues before the ID Minter, those Concepts will actually be the same Concept when they reach the
Concepts Pipeline, rather than multiple Concepts that need to be understood as synonymous.

The proposed stage here operates on Authoritative Concept Identifiers, ensuring that the resulting Catalogue Concepts 
are correct and consistent before new Canonical Identifiers are minted for them.

## How?

### Concepts Pipeline/API
The Concepts Pipeline Ingestor(s) should, where available, store the official types (maybe translated to our types) 
and compositions of each Concept in the authoritative-concepts index.

The Concepts API should have a service that can be called with one or more authoritative identifiers, and returns that information
from the authoritative index.  This may be a separate private/internal API instance.

The Sierra Transformer should stop guessing whether to use LCNames or LCSubjects, and instead use a new scheme, "LC".

The Catalogue Pipeline should have a new stage between the transformers and the id minter, the new stage:

* extracts identifiers in the same way the id minter does, and requests the official type/composition for any that are in a scheme supported by the API.
* replaces the type and identifiertype with the "right" value from the API
* replaces the identifier values of any constituent concepts that have label-derived identifiers, with the official ones (based on similarity of label).
* rejects and/or warns about documents containing any wrong identifiers (initially, just not known in that scheme, later, consider some comparison between labels).

Everything downstream will behave exactly as it currently does.

## Why a new stage?

This must be done after the identifiers have been found by a transformer and
before the ID Minter mints canonical identifiers in the id minter database.

Therefore, other options for doing this work could include adding to the ID Minter or the transformers.

It does not belong in the transformers.  Although this problem mostly manifests in Sierra data, it could come from anywhere.
For example, there are examples coming from TEI data.  The transformers work best by being self-contained, and only transform
the input given into a Work, rather than performing lookups elsewhere.  So it is best not to burden transformers with this.

It may belong in the ID Minter.  There is some duplication between this task and the id minter, in the extraction of source
identifiers from the input Work. The only reasons for keeping it separate are - 

* better observability (weak, it's probably just as clear what has happened if resolution and minting are in the same stage)
* the minter is fairly critical and may be best left alone (also weak, it's well covered in tests) 

## Current Problem Manifestations

### The Person/Agent (Maimonides) problem

Currently, there are a number of concepts that have the same LCNames identifier, where one is a Person, and the other is an Agent.
This is due to a rule in the Sierra Transformer that exists because a Personal Name contributor may actually refer to a text, rather than
a Person (if it has a $t subfield).

ca. 2700 examples where a 700 with $t uses a code in $0 that refers to the Person in $a
e.g. in https://wellcomecollection.org/works/hqqndr39 (b20241720) "Maimonides, Moses, 1135-1204. Maqālah fī sināʾat al-mantiq." has the id n78096039, which refers to the Person, and not 17115004, which refers to the text.
ca 800 examples where a 700 with a $t uses a code in $0 that refers to the text.
e.g. in https://wellcomecollection.org/works/nfnmnc6m (b20241781) (Karo, Joseph ben Ephraim, 1488-1575. Kesef mishneh) (not Karo, Joseph ben Ephraim)

This leads to there being a missing record in the Concepts API, because the input to the Concepts Recorder is necessarily only keyed on
the authoritative identifier.

This problem is currently masked by the fact that the Concepts Pipeline is only additive.  It is possible that each of the two Concepts can have passed
all the way through the Concepts Pipeline on separate occasions.  In which case, they will both be present on the API.  Whether this is the case for
any individual Concept a user requests is currently a question of luck.

### The name/subject (Glasgow) problem

Currently, there are a number of concepts that have the same Library of Congress identifier, where one is in LCNames and the other 
in LCSH.  This is because of a transformer rule that assumes that "Terms" refer to Subject Headings and "Names" refer to Names.

This leads to there being two records in the Concepts API for the same referent.

This is further complicated by the Sierra transformer deriving the type from the field - Glasgow is one of the terms that can be found 
in the Corporate Name field, and so becomes a Concept of type Organisation when it is a Name, but also in the Geographic Term field, 
meaning it becomes a Concept of type Place when it is a Subject Heading.
