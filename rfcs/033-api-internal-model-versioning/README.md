# RFC 033: Api internal model versioning

## Current status

Currently our API and catalogue pipeline both live in our catalogue repo and have a dependency to the internal model module.

This means that, if we need to make model changes, we can quickly make the corresponding changes in all services of
the pipeline that depend on it and in the API at the same time.

However, changes to the internal model that aren't backwards compatible require a reindex before we
can deploy the API and a reindex can take a few hours.

## Problem

This means that:
-  If there is a change to the internal model and a subsequent change to the API that is unrelated to the internal model change
   (i.e. a change on search queries or on display serialization), the change to the API cannot be deployed until a reindex
   has finished successfully because of the internal model dependency.

- If there are problems in the pipeline that delay a reindex, that means a deploy of the API is potentially delayed too.

- If there is a bug in the prod API, fixing it means potentially waiting for a reindex or deploying from a patch.

- We need integration tests that tell us if a build of the API is compatible with the currently available index and we
  can't guarantee that what is in master is always deployable and that integration tests should always pass.

## Proposed solution

The proposed solution is:
- for every build in master, release the internal model as an artifact with a new version
  and publish it to our s3 respository in a similar way as to how we release artifacts in the scala-libs repo.

- all catalogue pipeline services that depend on the internal model keep the dependency on the local module
  instead of the published artifact. When we work a something that require model changes, we work on our dev branch
  on model and pipeline services at the same time and once the branch is merged, a new version of the internal model
  is published.

- the catalogue API depends on the internal model artifact published in s3 instead of the internal model module.
  We update the version the API depends on in master only when we have an index compatible with that version. Any change
  in the API that does not require model changes can be merged in master and deployed without pointing the API to a new index.

- If we need to make changes both on the pipeline and on the API, we need to make that in three stages:
  - change the pipeline
  - reindex
  - change the API

## Advantages

This means that:
- changes to the API that don't need internal model changes can be deployed independently of reindexes
  and independently of any internal model change.

- If there are problems in the pipeline causing reindex delays, we can still deploy changes to the API,
  provided that we don't upgrade the version of the internal model dependency.

- We can fix bugs in the API by releasing a new version of the API if we don't need to upgrade model version.

- We can adopt a policy where we say integration tests should always pass and the API should always be deployable
  from master to production.

- We can split the API into its own repo which could allow us to think substantially differently about the API than
  the pipeline and have a different build.


## Potential problems with the proposed approach

- It's difficult to know from an index what version of the internal model was used to populate it. Ideally we might want to include
  the model version in the index name but because the pipeline services, including the ingestor, depend on the local internal_model,
  they don't know the version, so it's not straightforward to do. This means that we could run into issues if we update the index tha API
  is pointing to without updating the model dependency and viceversa.

- If we need to make changes to the API that require internal model changes, we need to wait on a new release of the internal model, before
  we can start working on it.





