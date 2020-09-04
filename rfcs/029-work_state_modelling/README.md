# RFC 029: Work state modelling

## Background

The central model to the catalogue pipeline and API is the `Work` model. We currently have a relatively complex type hierarchy to represent different sorts of work, as well as their state within the pipeline. For example works extending from `IdentifiedBaseWork` (`IdentifiedWork`, `IdentifiedInvisibleWork`, `IdentifiedRedirectedWork`) indicate works that have been minted by the ID minter, whereas corresponding works extending from `TransformedBaseWork` have not. Data that is common to these different sort of works is held in the `WorkData` case class. 

Having these as types is generally good as it makes a compile time guarantee that some particular piece of data exists at some point in the code: we would not have the same guarantees if for example we used the same work model regardless of whether the work had an ID or not (using an `Option` field), which would lead to more error handling code and potentially the introduction of subtle bugs which the type system would otherwise prevent.

There are some upcoming use cases where we need to modify the work modelling, such as adding relations (`parts`, `partOf`, `precededBy`, `succeededBy`) to the model for works after denormalisation by the relation embedder. Also @jamesgorrie and @jtweed have been investigating having additional sorts of works in the type hierarchy (such as collections, series, items) similarly to how there are different sorts of concepts.

## Problem

There are a number of issues with the way the modelling is currently implemented, primarily to do with composability of the types and the fact that they do not express our business logic as clearly as they could:

1) To add a new sort of work we need to add a large amount of subtypes. For example to add a work such as a `Collection` we would potentially need the addition of up to 6 new types: `UnidentifiedCollection`, `UnidentifiedInvisibleCollection` etc.

2) There is no way to add new state dependent data in a type safe manner without also adding more types of work for each case. To take the relation embedder as an example, that would require new types such as `DenormalisedWork`, `DenormalisedCollection` etc.

3) There are already 2 type parameters on `WorkData`, both for the identified state of things such as concepts, and also for the identified state of images. Also, if we decided to add relation data directly to `WorkData` (as optional fields) rather than creating new work types we would need an additional third type parameter (to express whether the referenced works are pre or post minter). These are all tied together so ideally we should be able to specify them with a single type parameter.

4) The type hierarchy from `BaseWork` downwards is quite complex and it can be hard to understand the meaning of particular types of work within the code. The naming could also do with changes in places (e.g. `TransformedBaseWork` does not make much sense as a name, given that the concept of a work does not exist before the transformer).

## Proposed Solution

This RFC proposes having a cleaner separation of the pipeline state of a work with the sort of work it is, namely with different forms of polymorphism:

1) Sub-typing is used for differentiating different sorts of work, with a `Work` being a sum type ADT consisting of the finite number of possible case classes. Note this proposed sub-typing is much simpler than the current implementation, having only a single level of depth and a single parent type.

2) Parameterisation of the `Work` by a state parameter indicates what stage of the pipeline it is in, and which can hold specific data depending on stage. By constraining the parameter to one of a set of known types, we can consider the `Work` model as a finite state machine with the stages in our pipeline each containing a particular transition.

By separating these two things like this we are able to add new types of work or new pipeline states without worrying about how one will impact the other. The following is a sketch of how this might look:

```scala
/** WorkState represents the state of the work in the pipeline, and contains
  * different data depending on what state it is. This allows us to consider the
  * Work model as a finite state machine with the following stages corresponding
  * to stages of the pipeline:
  *
  *      |
  *      | (transformer)
  *      ▼
  *   Unmerged
  *      |
  *      | (matcher / merger)
  *      ▼
  *   Merged
  *      |
  *      | (relation embedder)
  *      ▼
  * Denormalised
  *      |
  *      | (id minter)
  *      ▼
  *  Identified
  *
  * Each WorkState also has an associated IdentifierState which indicates whether
  * the corresponding WorkData is pre or post the minter.
  */
sealed trait WorkState {
  type Id <: IdentifierState
  type ImageId <: IdentifierState
}

object WorkState {

  case class Unmerged() extends WorkState {
    type Id = IdentifierState.Unminted
    type ImageId = IdentifierState.Unidentified
  }

  case class Merged() extends WorkState {
    type Id = IdentifierState.Unminted
    type ImageId = IdentifierState.Unidentified
  }

  case class Denormalised(
    relations: Relations[Denormalised],
    sourceIdentifier: SourceIdentifier,
    identifiedType: String = classOf[Identified].getSimpleName,
  ) extends WorkState {
    type Id = IdentifierState.Unminted
    type ImageId = IdentifierState.Unidentified
  }

  case class Identified(
    canonicalId: String,
    relations: Relations[Identified],
  ) extends WorkState {
    type Id = IdentifierState.Minted
    type ImageId = IdentifierState.Identified
  }
}

/** IdentifierState represents the state of individual pieces of work data
  * (such as genres, concepts etc), with Unminted used to indicate
  * pre-minter state and Minted used to indicate post-minter state
  */
sealed trait IdentifierState

object IdentifierState {

  sealed trait Unminted extends IdentifierState
  sealed trait Minted extends IdentifierState

  case class Unidentified(
    sourceIdentifier: SourceIdentifier
  ) extends Unminted

  case class Identified(
    sourceIdentifier: SourceIdentifier,
    canonicalId: String
  ) extends Minted

  case class Unidentifiable() extends Minted with Unminted
}

/** Work contains the work itself. It is parameterised by it's state, meaning
  * the same type of Work can be in a number of possible states depending on
  * where in the pipeline it is. This allows us to easily add new types of work
  * (such as if Collection is decided to be a seperate type to StandardWork),
  * with the state of the work in the pipeline being an orthogonal concern.
  */
sealed trait Work[State <: WorkState] {
  val sourceIdentifier: SourceIdentifier
  val version: Int
}

case class StandardWork[State <: WorkState](
  sourceIdentifier: SourceIdentifier,
  version: Int,
  data: WorkData[State],
  state: State,
) extends Work[State]

case class RedirectedWork[State <: WorkState](
  sourceIdentifier: SourceIdentifier,
  version: Int,
  state: State,
) extends Work[State]

case class InvisibleWork[State <: WorkState](
  sourceIdentifier: SourceIdentifier,
  version: Int,
  data: WorkData[State],
  state: State,
) extends Work[State]

/** WorkData contains data common to all types of works that can exist at any
  * stage of the pipeline. It is parameterised by a WorkState in order for
  * individual pieces of data to have the correct IdentifierState depending on
  * the stage of the pipeline.
  */
case class WorkData[State <: WorkState](
  title: Option[String] = None,
  genres: List[Genre[State#Id]] = Nil,
  images: List[Image[State#ImageId, State#Id]] = Nil,
  ...
)

/** Relations contain the related works for some particular work, and only exist
  * at the Denormalised and Identified stages of the pipeline.
  */
case class Relations[State <: WorkState](
  parts: Option[List[Work[State]]],
  partOf: Option[List[Work[State]]],
  precededBy: Option[List[Work[State]]],
  succeededBy: Option[List[Work[State]]]
)
```

## Potential Issues

* There may be some problems with the implementation of this with regards to the `id_minter` pipeline stage, which works on raw JSON data rather than Scala types. For example, in the `WorkState.Denormalised` case class above `sourceIdentifier` has been included again (it already exists in the work itself) as the `id_minter` will need to generate the `canonicalId` here for the output to be correct. Personally I think the `id_minter` could be implemented pretty simply on our types rather than raw JSON, which would make things a bit safer any avoid some of these idiosyncrasies, although a disadvantage of this is it would require a separate `id_minter` for `Work`, `Image` and any future types we wanted to attach IDs to.

* We use circe generated type names in a few places, so code relying on this might be messed up. For example, `IdentifiedWork` becomes `Work[Identified]`.

* The suggestion above although a big improvement does not completely solve the composability issue, as with the way it has been written still may require things like `InvisbleCollection` etc. However, I am not sure whether indicating invisibility of a work actually requires having a separate type rather than simply a boolean flag, which would be much more composable.
