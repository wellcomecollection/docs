# RFC 054: Better Handling of Source Identifiers in Concepts

## Executive Summary

Currently, some Concepts are missing or duplicated in the Concepts API because the type and scheme
of those Concepts in the Catalogue pipeline is inconsistent.

This is to be fixed in stages:

1. Ensure that, for any given document, all Authoritative Concepts with the same ID and scheme have the same ontologyType
2. Improve the way the Library of Congress scheme is determined in the Sierra transformer (LCSH vs LCNames)
3. Investigate the scale of the issue after these fixes
4. If necessary, modify the behaviour of the id minter to ignore concept ontologyTypes and/or request fixes in the source data

Steps 1 and 2 together should correct the largest number of incorrect Concepts with minimal impact on the flow of data that is already correct.

## What?

Currently, an authoritative identifier found in source data is transformed into a Concept which has 
a type and identifier type, both of which are determined from its use in the source document.

That combination of types, along with the identifier value is then mapped to a canonical id in the id minter.

Because the determination of both type and identifier type is imperfect (particularly in Sierra data),
this can lead to Concepts either being duplicated or omitted from the Concepts API.

Improvements to the extraction of type and identifier type information are needed, and ultimately, 
a new approach for minting canonical ids from authoritative identifiers may be needed.

### Why does duplication and omission occur?

The Concepts pipeline links in-use concepts (from the Works Catalogue) with extra information derived from the Authorities' datasets.

To do this, the id and scheme are used together as a key.  The data from the external authorities cannot be aware of the types we have assigned to
the Concepts we have generated from the source data.

Therefore, if multiple Concepts exist with the same identifier value and identifier type, but different concept types, only one of these will "win"
and become a Concept in the concepts-store feeding the Concepts API.

If multiple Concepts exist with the same identifier value, but different identifier types, then these are seen as two distinct identifiers,
and both will become Concepts in the concepts-store.

From the perspective of the Concepts pipeline, both of these behaviours are correct.

#### The Person/Agent (Maimonides) problem

Currently, there are a number of concepts that have the same LCNames identifier, where one is a Person, and the other is an Agent.
This is due to a rule in the Sierra Transformer that exists because a Personal Name contributor may actually refer to a text, rather than
a Person (if it has a $t subfield).

ca. 2700 examples where a 700 with $t uses a code in $0 that refers to the Person in $a
e.g. in https://wellcomecollection.org/works/hqqndr39 (b20241720) "Maimonides, Moses, 1135-1204. Maqālah fī sināʾat al-mantiq." has the id n78096039, 
which refers to the Person, and not 17115004, which refers to the text.
ca 800 examples where a 700 with a $t uses a code in $0 that refers to the text.
e.g. in https://wellcomecollection.org/works/nfnmnc6m (b20241781) (Karo, Joseph ben Ephraim, 1488-1575. Kesef mishneh) (not Karo, Joseph ben Ephraim)

This leads to there being a missing record in the Concepts API, because the input to the Concepts Recorder is necessarily only keyed on
the authoritative identifier.

This problem is currently masked by the fact that the Concepts Pipeline is only additive.  It is possible that each of the two Concepts can have passed
all the way through the Concepts Pipeline on separate occasions.  In which case, they will both be present on the API.  Whether this is the case for
any individual Concept a user requests is currently a question of luck.

The existence of this problem raises a question about one of the intended goals of the Concepts Pipeline and Concept Embedder - to ensure the consistent 
use of the proper label on any given Authoritative Concept.  If this is implemented, then (in the example above), the information about
`Maqālah fī sināʾat al-mantiq` will not be included in the final work.

#### The name/subject (Glasgow) problem

Currently, there are a number of concepts that have the same Library of Congress identifier, where one is in LCNames and the other
in LCSH.  This is because of a transformer rule that assumes that "Terms" refer to Subject Headings and "Names" refer to Names.

This leads to there being two records in the Concepts API for the same referent.

This is further complicated by the Sierra transformer deriving the type from the field - Glasgow is one of the terms that can be found
in the Corporate Name field, and so becomes a Concept of type Organisation when it is a Name, but also in the Geographic Term field,
meaning it becomes a Concept of type Place when it is a Subject Heading.

For example: https://wellcomecollection.org/works/uf3jv2sr, which lists Glasgow as both Contributor and Subject.  As a subject, it is of type Place
in the lc-subjects scheme, and as a Contributor, it is an Organisation in the lc-names scheme.  Neither of these combinations is correct.

When it comes to the Recorder and beyond in the Concepts Pipeline, only the lc-names version will be enhanced with Authority data.  
The lc-subjects version is a fiction of our own making.

It may be more correct to exclude any "wrong" identifiers as part of the Recorder, but that would lead to the omission of all identifiers 
whose identifier type has been incorrectly guessed.

### Problems of homonymy

Neither of these are existing problems in Concepts, but are worth mentioning to ensure that we are aware of them in making 
any proposed solutions.

#### The Aberdeen problem - homonyms with different types

This is a hypothetical problem for which I have seen no evidence in Concepts, but should be mentioned in case any solution to the above
problems might cause it to arise.

Unidentified Concepts derive their identifiers from their labels.  It may be the case that multiple genuinely different 
referents have the same name, but are of different types (e.g. Aberdeen, the Granite City; vs. Aberdeen, the now disemvowelled company founded there)

This problem does exist in identifiers for Sierra Bibs vs. Items, and in Miro.

#### The John Smith problem - homonyms with the same type

There are evidently multiple authors by the name "John Smith" (https://wellcomecollection.org/concepts/t4jfabht), as they 
have authored works roughly 340 years apart.  In the case of t4jfabht, this corresponds to lc-names:n86851637,
but there may be some homonymous unidentified concepts.

This is not something that can be resolved by the pipeline(s).  It must be fixed (if desired) in the source data. However, 
as n86851637 appears to deliberately be a catch-all for any John Smiths that happen to exist, this is not necessarily a
problem that needs to be resolved at all.

### Goals

```gherkin
Feature: Concepts presented in the Works and Concepts APIs
```
The scenario representing the end goal for new Concepts with authoritative ids is clear
```
Scenario: Concepts with the same authoritative id
Given two Concepts with the same authoritative id
When the Concepts reach the end of the Works and Concepts pipelines
Then both Concepts have the same canonical identifier
And both Concepts have the same type
And the type accurately represents the real-world type of the referent
```

There is less clarity on non-authoritative ids (label-derived), but it is likely to be identical to the above.
```
Scenario: Concepts with the same non-authoritative id
Given two Concepts with the same label-derived id
When the Concepts reach the end of the Works and Concepts pipelines
Then (what happens? same as above?)
```

This is because of the hypothetical "Aberdeen Problem" - two concepts with the same name
that legitimately have different types.  I suspect that in this case, it should be treated 
in the same way as authoritative Concepts, with the Concept type not being used for differentiation.
If the Aberdeen problem arises here, it should be handled in the source data by adding an
authoritative id or differentiating the name.

The `Concepts with the same authoritative id` scenario, above, applies to new and existing concepts alike.
However, existing concepts have these further considerations:

Wrongly-namespaced identifiers are to be fixed. There is no need to retain the "wrong" canonical id.

```
Scenario: Wrong identifier scheme
Given a Concept that is currently in the wrong scheme
Then the Concept's canonical id will not be the same as it currently is
```

Correctly-namespaced identifiers should ideally retain their existing canonical id, but this is not always possible.
In instances of the Maimonedes problem, one of the Concepts will either cease to exist, or end up with a new canonical identifier.

```
Given a Concept that is currently in the right scheme
And the Concept is already in the id minter database
Then the Concept's canonical id should ideally be the same as it currently is

Given two matching Concepts that are already in the id minter database
And the two Concepts currently have different canonical ids.
Then the Concepts' shared canonical id should be the canonical id that is already assigned to one of them.
```

### Options

Logically, there are three options for resolving this problem.
All are built on an initial step of Perfecting the extraction of identifier types.

1. Perfect the extraction of types
2. Look up the types using the authority's data
3. Reduce the impact of incorrect concept types.

#### Perfecting the extraction of identifier types

The problem of incorrect identifier types, is specifically an issue for Library of Congress identifiers.
MARC data from Sierra does not distinguish between the various LoC schemes, which are all determined by the use of 
indicator2=0

However, the identifier type for any given LoC identifier can be correctly determined from its prefix,
`n` for lc-names and `s` for lc-subjects (strictly, sh, but we may not need to distinguish between that 
and other s-prefixed schemes like sj-. If we do, we can).

Non-LoC schemes (e.g. MeSH), can also be determined reliably from the combination of indicator2 and subfield 2.

TEI data also currently just distinguishes between LCSH (or any LoC) and MeSH in the same way. Other schemes are not used.

#### Perfecting the extraction of Concept types

This is impossible, for reasons outlined in the two "Problems", above.  
There is no way to reliably determine the type of the referent from Sierra MARC data.

#### Look up the types

The type of the referent of an identifier is managed by the authority that controls the record. This is 
one of the core reasons for using them.  To avoid the problem of two different things having the same 
colloquial name.

Therefore, this is likely to be the most reliable method, but it seems overly complex for what it gives us.

This could take the form of a Catalogue Pipeline stage (or preliminary step in the id minter) and a Concepts API feature to
retrieve additional information about Concepts that are derived from external authorities.

The additional information includes:

* The type of the referent
* Identifiers and types for any components of a composite type

Superficially, this approach appears to bring along extra benefits. For example, the constituents of a composite type
could be resolved much earlier in the Catalogue Pipeline.  However, on closer inspection of the LoC data, most constitutent
concepts are not identified, so this benefit cannot be realised (see Appendix - Loc Compound Concepts).

#### Mitigate the impact of incorrect types

The heart of this problem is that the uniqueness constraint for a Wellcome canonical id based on an external authority's id
differs from the uniqueness constraint used by the external authority itself.

The combination of external id and scheme alone provide sufficient uniqueness, whereas Wellcome canonical ids are keyed
on the Concept Type in addition to the external id and scheme.

Having fixed the extraction of identifier types, all instances of the "Glasgow Problem" (same id value, different scheme) 
become instances of the "Maimonides Problem" (same external id, different type).

Candidate options for mitigation (in order of how early in any pipeline they are):

1. Handle it in the source data
2. Ignore types altogether in the Works Pipeline.
3. Key canonical ids on scheme and id value alone (for external ids only?) (exec summary - this is the right one)
4. Gather all different in-use types as part of the Concept Pipeline (Aggregator) and handle it in the Knowledge Graph and Concepts Embedder 

Ideally, this issue should be handled as early as possible, rather than mitigated against after the problem 
has been propagated through databases.

##### Source data

This would be impractical even if possible.

Although some instances of these problems may be due to cataloguing errors, or could be remedied by asking
collections staff to add an extra marker to make it easier to determine the referent type, there may still be some
that cannot be fixed in this manner.

In any case, the disconnect between scheme-value-type and just scheme-value will still exist, it will just
(in a perfect scenario), be made inconsequential by the consistent extraction of the correct type.

##### Ignore types entirely

Concept Types are used in the APIs and front-end to indicate what kind of thing the concept is e.g. "Works about this (Person|Organisation|...)",
so they cannot be ignored entirely.

This may be feasible for concepts with authoritative identifiers, where the type could be inserted using the Concepts Embedder,
but not all Concepts are associated with authoritative identifiers. This would add complexity in having to deal with it having 
to sometimes estimate the type, and sometimes not.

##### Ignore types in the id minter

Some identifier types use the concept type for disambiguation (source system identifiers for Works - fill in from slack thread).
A solution will have to be defined that covers those.

Currently, when an identifier is processed by the id minter, it generates a key based on the scheme, value, and type of the Concept.

The reason for this is that ambiguity exists in identifiers from Miro and Sierra, where we do wish to differentiate between
the same id in the same scheme but with a different type.

(see [creating canonical identifiers](https://docs.wellcomecollection.org/catalogue-pipeline/transforming-records-into-a-single-common-model/creating-canonical-identifiers))

In order to retain the required disambiguation in Miro/Sierra identifiers, but remove the bogus disambiguation from
Concepts, we can change the id minter to ignore the distinction between different types of Concept, while leaving
the overall behaviour unchanged.  This involves up to four parts:

* Change the transformer(s) - This may be enough on its own.
* Change the id minter stage
* Migrate the id minter database
* Change the Concepts Aggregator 

###### Transformer(s)

The problem of inconsistent types only seems to occur at scale in Sierra data.  In most cases of the Glasgow Problem, 
two instances of the same Concept are present with different types in the same Work.

A change to the Sierra transformer that harmonises the types in any near-duplicate Concepts with the "most specific" (or "more likely to be correct") type 
used in the document would resolve most instances of the Maimonides Problem, and alongside fixing the lc-subjects vs lc-names derivation, it would
also fix most instances of the Glasgow Problem.

As Person isa Agent, the "most likely to be correct" type for the Maimonides problem would be Person.

For the Glasgow problem, it is less clear. Organisation and Place are siblings in the hierarchy of Concept, so either could be 
correct. I suspect that the type present in the Subject should take priority over the type present in any contributor fields.
Contributor fields are less flexible, in that the referent must be a kind of agent.  If a thing that is not an
agent has been squeezed into a contributor field, and is also present elsewhere in the document, then the other place is more
likely to contain the correct type.

It may be the case that the difficulty of choosing is only a problem for Places coerced into being Organisations.  It is unlikely
that an abstract concept would be listed as a contributor, and other potential occupants of both fields are likely to be 
correctly identified in both places (e.g. an autobiography is a Work by a Person about that same Person)

If the problem is sufficiently fixed by this step, then there should be no need to make the following modifications to the pipelines.

###### Minter stage

Change the behaviour of the id minter stage, so that any identifiers with a type that inherits from `Concept` will now
use `Concept` as the ontologyType when minting a canonical id.

The actual ontologyTypes should still be retained in the Work, as these go on to inform the Concepts Aggregator and ultimately
the Concepts API and Concepts Embedder, which in turn allow Concepts pages to display a type.

Because this involves a change to the critical data stored in the id minter database, the changes here should not be taken lightly.
If we only encounter minimal missing/duplicate Concepts after applying the fix to the Sierra transformer, then it may be better to 
resolve those remaining instances in the source data.

###### Database Migration

- For all entries that correspond to a Concept of any type:
  - Any ids that are already unique on scheme and value alone can simply have the type changed to Concept
  - For any group of ids that are not unique on scheme and value, the id of the "least specific" type is changed to `Concept`.
    - Where there is a clear hierarchy of types e.g. (Concept -> Agent -> Person) specificity is obvious,
      but some investigation is needed where types are "wrong" - (e.g. Organisation/Place)
      - That said, I don't think it matters which one is retained, as long as it is consistent.
      - retaining the least specific helps with this consistency (or its predictability), as the end result is a record with type `Concept`
      - The other id remains in the minter database, unchanged, and now unused.

###### Concepts Aggregator

Currently, the Concepts Aggregator simply inserts all the unique concepts it finds in any batch into the concepts-used index.

As a result, if one batch of works contains a Concept with one type, and a subsequent batch contains that same Concept with a 
different type, then the last one "wins".

In order to satisfy the requirement that `the type accurately represents the real-world type of the referent`, the Concepts Pipeline
must be able to determine or estimate the type of the referent.

In the case of an Authoritative Concept, the type will eventually be derived from Authority data, but that has not been
implemented yet.

In the case of label-derived Concept ids, and until we have Authoritative Types, 
the best-fit type will need to be determined from the collection of types assigned to any given Concept.

(Question: Is this really necessary, or can we simply tolerate that these types might be inconsistent?)


# Appendix: LoC Compound Concepts

Compound concepts in MARC data from Sierra bear an identifier referring to the whole concept, but the transformer
also breaks them up into the individual constituent concepts.  However, the identifiers for these constituent concepts 
are only "label-derived".  LoC and MeSH entries for compound concepts sometimes also contain the identifiers for the constituents,
so it might be expected that these could be populated properly directly from LoC data. This example demonstrates that this is not the case:

For example - from https://wellcomecollection.org/works/ypd9stvu (b21249842)

```
651  0 $aRhode Island $xHistory $yCivil War, 1861-1865 $xHospitals $0sh 85113730
```

The field above currently yields the following concepts:

* lc-subjects:sh85113730
* label-derived:rhode island
* label-derived:history
* label-derived:civil war, 1861-1865
* label-derived:hospitals

Whereas https://api.wellcomecollection.org/catalogue/v2/works/u97tvahb contains "Rhode Island" as a
top-level concept with an identifier (n79022912).

Sadly, if we examine the MADS entry for the compound concept: https://id.loc.gov/authorities/subjects/sh85113730.madsrdf.json
the only constituent concept that is identified is History (sh99005024), the others are just text labels.

This means that there is little, if anything, to be gained from this.  It will still be essential to 
discover almost all of the component concepts via same-as relationships in the knowledge graph.
