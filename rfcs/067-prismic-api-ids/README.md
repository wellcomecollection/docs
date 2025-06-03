# RFC 067: Prismic API ID casing

This RFC proposes a consistent casing for Prismic API IDs across custom types, fields, and slices, to align with Prismic defaults and improve maintainability.

**Last modified:** 2025-01-13T12:28:03+00:00

## Context 
We run a spike to assess time/effort/risk to do the following:

- Use kebab-case for Custom type API IDs (plural/singular for reusable/single respectively) – this has to be overridden in SliceMachine. Or _possibly_ convert all of these to snake_case (which wouldn't need to be overridden in SliceMachine) for consistency with Slice API IDs
- Use camelCase for all (Custom type and Slice) field API IDs – this has to be overridden in SliceMachine
- Use snake_case for Slice API IDs – this is SliceMachine default

We’d like to make sure our Prismic API IDs are written with consistent casing and that we’re following defaults from Prismic so that we’re going with the grain as far as possible and not having to manually override auto-generated SliceMachine files.

## Custom type API IDs
When we started using Prismic we decided that these should be kebab-cased. Also, if the type was ‘reusable’ it should be plural, if it was 'single' it should be singular. For example, the reusable 'Exhibition highlight tour' type has an API ID of `exhibition-highlight-tours` whereas the single 'Global alert' type has an API ID of `global-alert`.

SliceMachine makes these snake_case by default but allows this to be overridden easily in the Graphical User Interface (GUI) and to-date we have made *all* of them kebab-case, so there probably isn't a good case for changing these to snake_case now.

A couple of reusable content types have been given singular API IDs – `card` and `collection-venue` – should we consider changing these two to `cards` and `collection-venues`?

## Field API IDs
Field API IDs are individual properties on a Custom type or Slice. More often than not these are individual words (e.g. `title`), which keeps things simple. When there's more than one word, we now have a mixture of snake_case and camelCase field API IDs.

- [Example of a camelCase field](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/common/views/slices/CollectionVenue/model.json#L37)
- [Example of a snake_case field](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/common/views/slices/GuideStop/model.json#L31)

SliceMachine defaults to snake_case (based on the label), although this is readily overridable in the GUI at the point of adding the field.

We exclusively work with camelCased variables in TypeScript and while snake_cased object properties aren’t a problem (e.g. `data.some_property`), we wouldn’t be able to destructure those properties off the `data` object without it being a linting error:

```
const { some_property } = data; // <-- linting error
```

Whereas this isn’t a problem:

```
const { someProperty } = data; // <-- ✨
```

So perhaps the preference should be for updating the field names at point of creation to be camelCased to remove the need for an extra renaming variable step in the TypeScript.

## Slice IDs
Prior to our use of SliceMachine, we gave our Slices camelCased IDs. However, SliceMachine requires that Slices have snake_cased IDs (it doesn’t let you override it in the GUI). When we migrated to SliceMachine we updated the Slice IDs in the [code](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/common/views/slices/index.ts) and [type](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/common/prismicio-types.d.ts) files that it generates to be camelCased in order to be able to use our existing code consistently. But each subsequent change to the Slice through SliceMachine will revert the IDs to snake_case and we have to remember to override it back to camelCase in several places across these two files. For newer Slices we have kept the default (snake_case) ids rather than override them to camelCase. 

I don’t think we deal directly with the Slice IDs. Instead, we send all of them (in [a `components` object](https://github.com/wellcomecollection/wellcomecollection.org/blob/main/common/views/slices/index.ts#L5-L29)) along to SliceMachine, so the linting problems mentioned above don’t arise. As such, I propose that we move to using snake_case for all Slice IDs.

## New vs. legacy
Whatever pattern we decide to go with in future, we also need to decide whether we should apply it to legacy content. Doing it for all content old and new would obviously be good for consistency but needs to be weighed against the effort required and risks associated with migrating the content.

## Proposal
We do a spike to establish the effort and risk around renaming various API IDs and decide what to do next based on the outcomes.