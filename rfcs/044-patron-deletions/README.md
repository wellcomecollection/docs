# RFC 044: Tracking Patron Deletions

**Status:** Draft

**Last updated:** 3/2/22

## Context

We use Sierra as a source of truth for patron accounts: all account information is held in Sierra as a sole source of truth, and Sierra is used for all credential validation. For us, Auth0 effectively acts as the implementation for all of the OAuth2 roles, on top of Sierra.

While Sierra is the source of truth, Auth0 does store a minimal amount of patron data (email, barcode, patron number). We need to be able to get rid of the records in Auth0 when a record is removed from Sierra, for GDPR reasons as much as anything else.

Sierra does not provide a change feed or any other kind of notification for events, so we need a polling solution. We already do this for items and bibs [in the Sierra adapter](https://github.com/wellcomecollection/catalogue-pipeline/tree/main/sierra_adapter#readme), by polling for changes in a given time window. We do not need the complex architecture of the Sierra adapter for tracking patron deletions: we don't need any information from within the records, and we don't need to merge anything. 

## Proposal

1. A **CloudWatch event** is run at some interval *T* to trigger a Lambda
2. The **Lambda** queries the Sierra API for patron records<sup>†</sup> that were deleted in the previous time window *W > T*. That is to say, time windows overlap to avoid records getting lost at the boundary.
3. The Lambda calls the [**Auth0 Management API**](https://auth0.com/docs/api/management/v2#!/Users/delete_users_by_id) to delete each of the records found in the query. If these are already deleted, or don't have any data in Auth0, this query 404s (which is fine).

<sup>†</sup> The Sierra API allows us to query by a `deletedDate` like `yyyy-MM-dd`, or an `updatedDate` like `yyyy-MM-dd'T'HH:mm:ssZZ` along with a `deleted: true` filter. While `deletedDate` has poor granularity, we should use it rather than `updatedDate`, as a deletion does not count as an update: the second option would not return records that were recently deleted but not otherwise updated.

## Questions and potential issues

- What happens if there are more deleted records than can be processed at once by the Lambda? *Mitigation: increase Lambda timeout to maximum*.