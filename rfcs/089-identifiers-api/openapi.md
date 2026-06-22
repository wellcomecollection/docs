# Wellcome Collection Identifiers API

> Generated from [`openapi.yaml`](openapi.yaml) by `render_docs.py`. Do not edit by hand.
> Regenerate with `uv run python render_docs.py`.

**Version:** `1.0.0`

Resolves public catalogue (canonical) identifiers to their source identifiers and back. Mappings are one-to-many: a single canonical id can carry several source identifiers (an original plus "predecessor" aliases inherited during source-system migration).

## Servers

- `https://api.wellcomecollection.org`: Production edge

## Operations

### Tag: (untagged)

| Method | Path | Summary |
|---|---|---|
| `GET` | `/v1/identifiers/{canonicalId}` | Resolve a canonical id to its source identifiers |
| `GET` | `/v1/identifiers/by-source/{sourceSystem}/{value}` | Resolve a source identifier to its canonical id |

#### `GET /v1/identifiers/{canonicalId}`

_Resolve a canonical id to its source identifiers_

Returns the full set of source identifiers that share this canonical id, ordered by createdAt ascending so the original is always first. The set can grow during a source-system migration as aliases are inherited, so responses are cached with a bounded TTL and revalidated via ETag.

**Security:** `ApiKeyAuth`

**Parameters:**

| Name | In | Required | Type | Description |
|---|---|---|---|---|
| `canonicalId` | path | yes | string | 8-char public catalogue id. Alphabet a-z and 2-9, excluding o/i/l/1, first character a letter. Malformed ids are rejected at the gateway. |

**Responses:**

| Status | Body | Description |
|---|---|---|
| `200` | [`IdentifierSet`](#identifierset) | Canonical id is assigned and has at least one mapping. |
| `304` | n/a |  |
| `400` | n/a |  |
| `404` | n/a |  |

#### `GET /v1/identifiers/by-source/{sourceSystem}/{value}`

_Resolve a source identifier to its canonical id_

Point lookup on the (OntologyType, SourceSystem, SourceId) primary key. By default returns only the canonical id. With include=siblings it also returns every source identifier sharing that canonical id (identical element shape to the forward lookup). The queried tuple is included in that set.

Freshness differs by variant: the bare lookup is immutable once minted and cached hard; include=siblings carries the mutable canonical->sources set and inherits the bounded-TTL + ETag treatment.

**Security:** `ApiKeyAuth`

**Parameters:**

| Name | In | Required | Type | Description |
|---|---|---|---|---|
| `sourceSystem` | path | yes | string | Source system identifier type. |
| `value` | path | yes | string | The identifier value within the source system. Must be a single, URL-encoded path segment. Source-id formats are heterogeneous, so this is not pattern-validated; unknown values resolve to 404 rather than 400. |
| `type` | query | no | string (enum: Work, Image, Item) | Ontology type. Part of the lookup key; defaults to Work. |
| `include` | query | no | string (enum: siblings) | Set to "siblings" to also return all source identifiers sharing the resolved canonical id. Omit for the canonical id alone. |

**Responses:**

| Status | Body | Description |
|---|---|---|
| `200` | [`CanonicalIdRef`](#canonicalidref) \| [`IdentifierSet`](#identifierset) | A mapping exists for the supplied tuple. |
| `304` | n/a |  |
| `400` | n/a |  |
| `404` | n/a |  |

## Schemas

### SourceIdentifier

A single source identifier mapped to a canonical id.

**Required:** `type`, `sourceSystem`, `value`, `isAlias`, `createdAt`

| Property | Type | Required | Description |
|---|---|---|---|
| `type` | string (enum: Work, Image, Item) | yes | Ontology type for this row. Kept per-row because a canonical id can carry rows of differing types (cross-type predecessors are allowed). |
| `sourceSystem` | string | yes |  |
| `value` | string | yes |  |
| `isAlias` | boolean | yes | False for the original (earliest createdAt), true for inherited predecessor aliases. |
| `createdAt` | string (date-time) | yes |  |

### IdentifierSet

A canonical id and the full set of source identifiers sharing it.

**Required:** `canonicalId`, `sourceIdentifiers`

| Property | Type | Required | Description |
|---|---|---|---|
| `canonicalId` | string | yes |  |
| `sourceIdentifiers` | array of [`SourceIdentifier`](#sourceidentifier) | yes | Ordered by createdAt ascending; original first. |

### CanonicalIdRef

Bare canonical id reference (default reverse-lookup response).

**Required:** `canonicalId`

| Property | Type | Required | Description |
|---|---|---|---|
| `canonicalId` | string | yes |  |

### Error

**Required:** `error`, `message`

| Property | Type | Required | Description |
|---|---|---|---|
| `error` | string | yes | Stable machine-readable code. |
| `message` | string | yes | Human-readable detail. |
