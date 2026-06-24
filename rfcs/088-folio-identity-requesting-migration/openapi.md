# Wellcome Collection Identity API (v2)

> Generated from [`openapi.yaml`](openapi.yaml) by `render_docs.py`. Do not edit by hand.
> Regenerate with `uv run python render_docs.py`.

**Version:** `2.0.0-alpha`

Contract for the **v2 identity API**, the FOLIO-backed successor to the
Sierra-backed v1 identity API (served from the wellcomecollection/identity
repo at `v1-api.account.wellcomecollection.org`). It is named v2 because
its predecessor is v1; that this matches the catalogue API's current
version is coincidental.

This is the **intended** contract: the v1-compatible end-user surface the
website consumes, plus the v2-native machine (`/m2m/*`) and catalogue
availability (`/items`) routes. (The prototype additionally exposes some
transitional `/user/{user_id}/*` holds routes; those are omitted here, as
they are to be replaced by the v1-compat successors above before cutover.)

The spec is organised in three tag groups:

- **users:** the v1-compatible surface the website consumes today,
  reproduced faithfully from the v1 implementation. v2 must serve this
  contract before the website can switch over behind a toggle.
- **m2m:** v2-native machine endpoints called by the Auth0 actions
  (folio-register / folio-sync).
- **items:** v2-native catalogue availability lookup.

Authentication is layered: every route requires the gateway API key
(`x-api-key`); most also require an Auth0-issued JWT (end-user or
machine-to-machine), validated by a Lambda authorizer at the gateway.

## Servers

- `https://v2-api.stage.account.wellcomecollection.org`: Stage (planned)
- `https://v2-api.account.wellcomecollection.org`: Production (planned)

## Operations

### Tag: users

v1-compatible end-user surface

| Method | Path | Summary |
|---|---|---|
| `GET` | `/users/{userId}` | Get a user's profile |
| `PUT` | `/users/{userId}` | Update a user's email address |
| `PUT` | `/users/{userId}/password` | Change a user's password |
| `POST` | `/users/{userId}/validate` | Validate the user's current password |
| `PUT` | `/users/{userId}/deletion-request` | Request account deletion |
| `POST` | `/users/{userId}/send-verification-email` | Re-send the email verification message |
| `PUT` | `/users/{userId}/registration` | Complete registration by setting the user's name (M2M only) |
| `GET` | `/users/{userId}/item-requests` | List the user's item requests (holds) |
| `POST` | `/users/{userId}/item-requests` | Place an item request (hold) |

#### `GET /users/{userId}`

_Get a user's profile_

Faithful to v1 `GET /users/{userId}` (except the `userId` field type,
see the User schema). Requires scope `read:user`; access rule `isSelf`:
the path segment must equal the caller's bare sub (or be `me`); a
machine token may read any user.

**Security:** `ApiKey` + `Auth0UserToken` (read:user)

**Parameters:**

| Name | In | Required | Type | Description |
|---|---|---|---|---|
| `userId` | path | yes | string | The bare Auth0 user_id (the token subject minus its `auth0\|` prefix), or the literal `me` for the caller's own record. Two id forms exist: `p{digits}` for patrons migrated from the legacy system (their patron number) and an Auth0-generated 24-char hex id for newer signups. `isSelf` is a plain string comparison of this segment against the caller's bare sub. Machine tokens cannot use `me`. (v1 used the bare numeric patron number here; the website's BFF proxy only ever sends `me`, so accepting the Auth0 id is not a breaking change for it.) |

**Responses:**

| Status | Body | Description |
|---|---|---|
| `200` | [`User`](#user) | The user. |
| `401` | n/a |  |
| `403` | n/a |  |
| `404` | n/a |  |
| `500` | n/a |  |

#### `PUT /users/{userId}`

_Update a user's email address_

Faithful to v1 `PUT /users/{userId}`. The current password must be
supplied and is re-validated before the email is changed. Returns
**304** when the new email is missing/empty or equals the current email.
Requires scope `update:email`; `isSelf`.

**Security:** `ApiKey` + `Auth0UserToken` (update:email)

**Parameters:**

| Name | In | Required | Type | Description |
|---|---|---|---|---|
| `userId` | path | yes | string | The bare Auth0 user_id (the token subject minus its `auth0\|` prefix), or the literal `me` for the caller's own record. Two id forms exist: `p{digits}` for patrons migrated from the legacy system (their patron number) and an Auth0-generated 24-char hex id for newer signups. `isSelf` is a plain string comparison of this segment against the caller's bare sub. Machine tokens cannot use `me`. (v1 used the bare numeric patron number here; the website's BFF proxy only ever sends `me`, so accepting the Auth0 id is not a breaking change for it.) |

**Request body** (required):

- [`UpdateUserRequest`](#updateuserrequest)

**Responses:**

| Status | Body | Description |
|---|---|---|
| `200` | [`User`](#user) | Email updated; returns the updated user. |
| `304` | n/a | No change needed (email missing or identical to current). |
| `400` | n/a |  |
| `401` | n/a |  |
| `403` | n/a |  |
| `404` | n/a |  |
| `409` | [`IdentityError`](#identityerror) | The email address is already in use by another user. |
| `500` | n/a |  |

#### `PUT /users/{userId}/password`

_Change a user's password_

Faithful to v1 `PUT /users/{userId}/password`. The current password is
validated before the new one is set. Success is **200 with no body**.
Requires scope `update:password`; `isSelf`.

**Security:** `ApiKey` + `Auth0UserToken` (update:password)

**Parameters:**

| Name | In | Required | Type | Description |
|---|---|---|---|---|
| `userId` | path | yes | string | The bare Auth0 user_id (the token subject minus its `auth0\|` prefix), or the literal `me` for the caller's own record. Two id forms exist: `p{digits}` for patrons migrated from the legacy system (their patron number) and an Auth0-generated 24-char hex id for newer signups. `isSelf` is a plain string comparison of this segment against the caller's bare sub. Machine tokens cannot use `me`. (v1 used the bare numeric patron number here; the website's BFF proxy only ever sends `me`, so accepting the Auth0 id is not a breaking change for it.) |

**Request body** (required):

- [`UpdatePasswordRequest`](#updatepasswordrequest)

**Responses:**

| Status | Body | Description |
|---|---|---|
| `200` | n/a | Password updated (no body). |
| `400` | n/a |  |
| `401` | n/a |  |
| `403` | n/a |  |
| `404` | n/a |  |
| `422` | [`IdentityError`](#identityerror) | The new password does not meet the password policy. |
| `500` | n/a |  |

#### `POST /users/{userId}/validate`

_Validate the user's current password_

Faithful to v1 `POST /users/{userId}/validate`. Standalone credential
check (used by the webapp before sensitive actions). Success is **200
with no body**. No scope required; `isSelf`.

**Security:** `ApiKey` + `Auth0UserToken`

**Parameters:**

| Name | In | Required | Type | Description |
|---|---|---|---|---|
| `userId` | path | yes | string | The bare Auth0 user_id (the token subject minus its `auth0\|` prefix), or the literal `me` for the caller's own record. Two id forms exist: `p{digits}` for patrons migrated from the legacy system (their patron number) and an Auth0-generated 24-char hex id for newer signups. `isSelf` is a plain string comparison of this segment against the caller's bare sub. Machine tokens cannot use `me`. (v1 used the bare numeric patron number here; the website's BFF proxy only ever sends `me`, so accepting the Auth0 id is not a breaking change for it.) |

**Request body** (required):

| Property | Type | Required | Description |
|---|---|---|---|
| `password` | string | yes |  |

**Responses:**

| Status | Body | Description |
|---|---|---|
| `200` | n/a | Password is valid (no body). |
| `400` | n/a |  |
| `401` | n/a |  |
| `403` | n/a |  |
| `404` | n/a |  |
| `500` | n/a |  |

#### `PUT /users/{userId}/deletion-request`

_Request account deletion_

Faithful to v1 `PUT /users/{userId}/deletion-request`, extended for
v2: re-validates the password, emails the admin inbox and the user
(notifications are sent *before* recording, per v1; an email failure
is a 500 with nothing recorded), **deactivates the FOLIO patron and
tags the record `delete-requested`** (the tag distinguishes pending
deletion from other inactive states and is filterable in the FOLIO
Users app), then records `deleteRequested` and blocks the Auth0
account. Success is **200 with no body**; **304** when a deletion
request is already pending. Requires scope `delete:patron`; `isSelf`.

**Security:** `ApiKey` + `Auth0UserToken` (delete:patron)

**Parameters:**

| Name | In | Required | Type | Description |
|---|---|---|---|---|
| `userId` | path | yes | string | The bare Auth0 user_id (the token subject minus its `auth0\|` prefix), or the literal `me` for the caller's own record. Two id forms exist: `p{digits}` for patrons migrated from the legacy system (their patron number) and an Auth0-generated 24-char hex id for newer signups. `isSelf` is a plain string comparison of this segment against the caller's bare sub. Machine tokens cannot use `me`. (v1 used the bare numeric patron number here; the website's BFF proxy only ever sends `me`, so accepting the Auth0 id is not a breaking change for it.) |

**Request body** (required):

| Property | Type | Required | Description |
|---|---|---|---|
| `password` | string | yes |  |

**Responses:**

| Status | Body | Description |
|---|---|---|
| `200` | n/a | Deletion request recorded (no body). |
| `304` | n/a | A deletion request is already pending for this user. |
| `400` | n/a |  |
| `401` | n/a |  |
| `403` | n/a |  |
| `404` | n/a |  |
| `500` | n/a |  |

#### `POST /users/{userId}/send-verification-email`

_Re-send the email verification message_

Faithful to v1 `POST /users/{userId}/send-verification-email`. Requires
scope `send:verification-emails`; `isSelf`.

**Security:** `ApiKey` + `Auth0UserToken` (send:verification-emails)

**Parameters:**

| Name | In | Required | Type | Description |
|---|---|---|---|---|
| `userId` | path | yes | string | The bare Auth0 user_id (the token subject minus its `auth0\|` prefix), or the literal `me` for the caller's own record. Two id forms exist: `p{digits}` for patrons migrated from the legacy system (their patron number) and an Auth0-generated 24-char hex id for newer signups. `isSelf` is a plain string comparison of this segment against the caller's bare sub. Machine tokens cannot use `me`. (v1 used the bare numeric patron number here; the website's BFF proxy only ever sends `me`, so accepting the Auth0 id is not a breaking change for it.) |

**Responses:**

| Status | Body | Description |
|---|---|---|
| `204` | n/a | Verification email queued. |
| `401` | n/a |  |
| `403` | n/a |  |
| `404` | n/a |  |
| `500` | n/a |  |

#### `PUT /users/{userId}/registration`

_Complete registration by setting the user's name (M2M only)_

Faithful to v1 `PUT /users/{userId}/registration`. Restricted to
machine-to-machine tokens (`sub` ending `@clients`, scope
`register:write`, via the m2m authorizer). Guarded by v1's
placeholder-name check: new signups carry the
`Auth0_Registration_temp*` names in Folio until this route replaces
them, so the name may only be completed, never changed (409 when
already registered with a real name; idempotent 204 when it matches;
blank-name records predating the placeholder convention may also be
completed). The Auth0 root profile is mirrored immediately so the
caller's session can refresh without re-login.

**Security:** `ApiKey` + `Auth0M2MToken`

**Parameters:**

| Name | In | Required | Type | Description |
|---|---|---|---|---|
| `userId` | path | yes | string | The bare Auth0 user_id (`p{digits}` for migrated patrons, Auth0-generated hex for newer signups). Unlike the other user routes, `me` is not meaningful here: this route is machine-to-machine only (the webapp's BFF calls it with a client-credentials token during registration). |

**Request body** (required):

| Property | Type | Required | Description |
|---|---|---|---|
| `firstName` | string | yes |  |
| `lastName` | string | yes |  |

**Responses:**

| Status | Body | Description |
|---|---|---|
| `204` | n/a | Name set (or already correct). |
| `400` | n/a |  |
| `401` | n/a |  |
| `404` | n/a |  |
| `409` | [`IdentityError`](#identityerror) | The user is already registered with a different name. |
| `500` | n/a |  |

#### `GET /users/{userId}/item-requests`

_List the user's item requests (holds)_

Part of the v1-consumed surface (in v1 this is proxied at the gateway to
the requests service from the catalogue-api repo; in v2 it is served
from Folio holds). Response shape is the website's `RequestsList`;
`pickupDate` carries the Folio request expiration date, and `workId` is
resolved via identifier translation (see Open questions). NB: this route
group uses the catalogue-style `WellcomeApiError` error shape, not the
identity `{message}` shape. Requires scope `read:requests`; `isSelf`.

**Security:** `ApiKey` + `Auth0UserToken` (read:requests)

**Parameters:**

| Name | In | Required | Type | Description |
|---|---|---|---|---|
| `userId` | path | yes | string | The bare Auth0 user_id (the token subject minus its `auth0\|` prefix), or the literal `me` for the caller's own record. Two id forms exist: `p{digits}` for patrons migrated from the legacy system (their patron number) and an Auth0-generated 24-char hex id for newer signups. `isSelf` is a plain string comparison of this segment against the caller's bare sub. Machine tokens cannot use `me`. (v1 used the bare numeric patron number here; the website's BFF proxy only ever sends `me`, so accepting the Auth0 id is not a breaking change for it.) |

**Responses:**

| Status | Body | Description |
|---|---|---|
| `200` | [`RequestsList`](#requestslist) | The user's current requests. |
| `401` | n/a |  |
| `403` | n/a |  |
| `500` | [`WellcomeApiError`](#wellcomeapierror) | Upstream failure. |

#### `POST /users/{userId}/item-requests`

_Place an item request (hold)_

Part of the v1-consumed surface. Request body is what the website sends
today. The `itemId` is the canonical catalogue id and is translated to
the Folio item UUID (see Open questions). Success is **202 Accepted**
(the website treats any 2xx as success and refetches the list). Errors
use the catalogue-style `WellcomeApiError` shape; the website displays
its `description` field. Requires scope `create:requests`; `isSelf`.

**Security:** `ApiKey` + `Auth0UserToken` (create:requests)

**Parameters:**

| Name | In | Required | Type | Description |
|---|---|---|---|---|
| `userId` | path | yes | string | The bare Auth0 user_id (the token subject minus its `auth0\|` prefix), or the literal `me` for the caller's own record. Two id forms exist: `p{digits}` for patrons migrated from the legacy system (their patron number) and an Auth0-generated 24-char hex id for newer signups. `isSelf` is a plain string comparison of this segment against the caller's bare sub. Machine tokens cannot use `me`. (v1 used the bare numeric patron number here; the website's BFF proxy only ever sends `me`, so accepting the Auth0 id is not a breaking change for it.) |

**Request body** (required):

- [`ItemRequest`](#itemrequest)

**Responses:**

| Status | Body | Description |
|---|---|---|
| `202` | n/a | Request accepted. |
| `400` | [`WellcomeApiError`](#wellcomeapierror) | Invalid request (e.g. bad pickup date). |
| `401` | n/a |  |
| `403` | n/a |  |
| `409` | [`WellcomeApiError`](#wellcomeapierror) | A request already exists for this item, or the user is at their hold limit. |
| `500` | [`WellcomeApiError`](#wellcomeapierror) | Upstream failure. |

### Tag: m2m

Machine-to-machine endpoints for the Auth0 actions

| Method | Path | Summary |
|---|---|---|
| `POST` | `/m2m/register` | Create a Folio patron for a new Auth0 signup |
| `POST` | `/m2m/enrich` | Login-time enrichment and reconciliation |

#### `POST /m2m/register`

_Create a Folio patron for a new Auth0 signup_

Called by the **folio-register** pre-user-registration Auth0 action,
before the Auth0 account is committed; if this fails, the Auth0 user is
never created. The patron is created inactive with `username` and
`externalSystemId` set to the email (the Auth0 user_id does not exist
yet; `/m2m/enrich` backfills it on first login). A blank `given_name` /
`family_name` is stored as the v1 placeholder
(`Auth0_Registration_tempFirstName` / `Auth0_Registration_tempLastName`)
until registration completes. Requires an M2M token with scope
`register:write`.

**Security:** `ApiKey` + `Auth0M2MToken` (register:write)

**Request body** (required):

| Property | Type | Required | Description |
|---|---|---|---|
| `email` | string | yes |  |
| `given_name` | string | no |  |
| `family_name` | string | no |  |

**Responses:**

| Status | Body | Description |
|---|---|---|
| `201` | object | Folio patron created. |
| `400` | n/a |  |
| `409` | [`IdentityError`](#identityerror) | A Folio account already exists for this email. |
| `500` | n/a |  |

#### `POST /m2m/enrich`

_Login-time enrichment and reconciliation_

Called by the **folio-sync** post-login Auth0 action on every login.
Resolves the Folio user (fast path: `folio_user_id`; migration path: a
legacy patron id parsed from `auth0_user_id`, cross-checked against the
email), mirrors the Auth0 identity onto the Folio record, activates the
patron once name-complete and email-verified, and returns the
`app_metadata` for the action to persist into Auth0. Requires an M2M
token with scope `enrich:read`.

**Security:** `ApiKey` + `Auth0M2MToken` (enrich:read)

**Request body** (required):

| Property | Type | Required | Description |
|---|---|---|---|
| `folio_user_id` | string or null (uuid) | no | Fast path; absent on a patron's first login. |
| `auth0_user_id` | string or null | no | The Auth0 user_id (sub), e.g. `auth0\|p11215550`. |
| `email` | string | no |  |
| `given_name` | string or null | no |  |
| `family_name` | string or null | no |  |
| `email_verified` | boolean | no |  |

**Responses:**

| Status | Body | Description |
|---|---|---|
| `200` | [`EnrichResponse`](#enrichresponse) | Enrichment payload for the Auth0 action. |
| `404` | [`IdentityError`](#identityerror) | No Folio user could be resolved. |

### Tag: items

Catalogue availability (API-key only; no user data)

| Method | Path | Summary |
|---|---|---|
| `GET` | `/items` | Items and availability for a catalogue instance |

#### `GET /items`

_Items and availability for a catalogue instance_

Catalogue/availability data only (no user data), so the route is
API-key gated with no Auth0 authorizer. `requestable` here is a
catalogue pre-filter (no open request, not suppressed, circulating
status); per-patron requestability is confirmed separately against
Folio's allowed-service-points via a `/users/{userId}` route.

**Security:** `ApiKey`

**Parameters:**

| Name | In | Required | Type | Description |
|---|---|---|---|---|
| `instanceHrid` | query | yes | string |  |

**Responses:**

| Status | Body | Description |
|---|---|---|
| `200` | [`ItemsResponse`](#itemsresponse) | The instance and its items. |
| `400` | [`IdentityError`](#identityerror) | Missing instanceHrid. |
| `404` | [`IdentityError`](#identityerror) | Instance not found. |
| `502` | [`IdentityError`](#identityerror) | Folio unreachable. |

## Schemas

### User

Faithful to v1 `models/user.ts`, sourced from the Auth0 profile (and in v2, Folio), except `userId`, which is a **string** in v2: the bare Auth0 user_id (`p{digits}` for migrated patrons, Auth0-generated hex for newer signups). This is a deliberate divergence from v1 (which returned the numeric patron number): the website derives its own userId from the session sub and never reads this field, so the change is unconsumed-on-the-wire.

**Required:** `userId`, `email`, `emailValidated`, `locked`, `creationDate`, `updatedDate`

| Property | Type | Required | Description |
|---|---|---|---|
| `userId` | string | yes | The bare Auth0 user_id, e.g. `p1234567` or a 24-char hex id. |
| `barcode` | string | no |  |
| `firstName` | string | no |  |
| `lastName` | string | no |  |
| `email` | string | yes |  |
| `emailValidated` | boolean | yes |  |
| `locked` | boolean | yes |  |
| `creationDate` | string (date-time) | yes |  |
| `updatedDate` | string (date-time) | yes |  |
| `lastLoginDate` | string or null (date-time) | no |  |
| `lastLoginIp` | string or null | no |  |
| `totalLogins` | integer or null | no |  |
| `deleteRequested` | string (date-time) | no |  |

### UpdateUserRequest

**Required:** `email`, `password`

| Property | Type | Required | Description |
|---|---|---|---|
| `email` | string | yes | The new email address. |
| `password` | string | yes | The current password, re-validated before the change. |

### UpdatePasswordRequest

**Required:** `password`, `newPassword`

| Property | Type | Required | Description |
|---|---|---|---|
| `password` | string | yes | The current password. |
| `newPassword` | string | yes |  |

### IdentityError

v1 identity API error shape.

**Required:** `message`

| Property | Type | Required | Description |
|---|---|---|---|
| `message` | string | yes |  |

### WellcomeApiError

Catalogue-platform error shape, used by the item-requests route group (the website displays `description`).

**Required:** `errorType`, `httpStatus`, `label`, `description`, `type`

| Property | Type | Required | Description |
|---|---|---|---|
| `errorType` | string | yes |  |
| `httpStatus` | integer | yes |  |
| `label` | string | yes |  |
| `description` | string | yes |  |
| `type` | `Error` (const) | yes |  |

### ItemRequest

What the website's item-request modal sends today.

**Required:** `workId`, `itemId`, `pickupDate`, `type`

| Property | Type | Required | Description |
|---|---|---|---|
| `workId` | string | yes |  |
| `itemId` | string | yes |  |
| `pickupDate` | string | yes | Formatted by the website before submission. |
| `type` | `Item` (const) | yes |  |

### RequestsList

The website's requests list shape.

**Required:** `results`, `totalResults`, `type`

| Property | Type | Required | Description |
|---|---|---|---|
| `type` | `ResultList` (const) | yes |  |
| `totalResults` | integer | yes |  |
| `results` | array of [`RequestItem`](#requestitem) | yes |  |

### RequestItem

**Required:** `item`, `workId`, `pickupLocation`, `status`, `type`

| Property | Type | Required | Description |
|---|---|---|---|
| `item` | object | yes |  |
| `workId` | string | yes |  |
| `workTitle` | string | no |  |
| `pickupLocation` | object | yes |  |
| `pickupDate` | string or null | no |  |
| `status` | object | yes |  |
| `type` | `Request` (const) | yes |  |

### EnrichResponse

**Required:** `app_metadata`, `profile`

| Property | Type | Required | Description |
|---|---|---|---|
| `app_metadata` | object | yes |  |
| `profile` | object | yes |  |

### ItemsResponse

**Required:** `instanceHrid`, `instanceId`, `title`, `items`

| Property | Type | Required | Description |
|---|---|---|---|
| `instanceHrid` | string | yes |  |
| `instanceId` | string (uuid) | yes |  |
| `title` | string or null | yes |  |
| `items` | array of object | yes |  |
