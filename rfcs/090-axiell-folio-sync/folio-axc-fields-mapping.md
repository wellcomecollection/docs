# AxC → FOLIO Field Mapping

**Date:** 2026-06-30
**Status:** Reference guide for AxC to FOLIO data integration
**Code:** `prototypes/axiell-folio-sync/axiell_folio_sync/mapping.py` (typed Pydantic
models + builders, the source of truth) · `mapper.py` (MARC extraction via the
`MARC_SOURCE` table) · `ref_cache.py` (reference-data resolution)

> The payloads are **Pydantic models with `extra="forbid"`** (`mapping.py`), so only
> the fields listed as *(in model)* are emitted today; an unmodelled or typo'd key
> fails at build time. Rows marked *(not in model)* are recommended future additions.
> Every hrid is derived from the **Axiell GUID** (MARC `001`); `mapping_version` is
> stamped on each payload (currently `2.1.0`).

---

## Instance

`Instance` model: `hrid`, `title`, `source` (default `"FOLIO"`), `instanceTypeId`.

| FOLIO Field | Type | Status | AxC source | MARC Tag | Notes |
|-------------|------|--------|------------|----------|-------|
| `hrid` | string | Required *(in model)* | `guid` | `001` | Format `AxC-instance-{guid}`. Example: `AxC-instance-4d8f1208-9812-4bb5-84ef-da436b22d9e2` |
| `title` | string | Required *(in model)* | `Titles/title` | `245$a` | Fails the build with `MappingError` if absent. |
| `source` | string | Required *(in model)* | — | — | Hardcoded `"FOLIO"`. Inventory-native (no linked SRS MARC record), so bibliographic fields stay editable via mod-inventory. |
| `instanceTypeId` | UUID | Required *(in model)* | — | — | Resolved from RefCache; defaults to the `"text"` type. |
| `formerIds` | array | Recommended *(not in model)* | `guid` + `Alternative_number` | `035$a` + `244$a` | Preserve alternate identifiers for reference/migration. |
| `discoverySuppress` | boolean | Recommended *(not in model)* | `accession_status` | — | Today suppression is applied only to items on delete. |

---

## Holdings

`Holdings` model: `hrid`, `instanceId`, `sourceId`, `permanentLocationId`, `callNumber`, `callNumberPrefix`, `shelvingOrder`.

| FOLIO Field | Type | Status | AxC source | MARC Tag | Notes |
|-------------|------|--------|------------|----------|-------|
| `hrid` | string | Required *(in model)* | `guid` | `001` | Format `AxC-holding-{guid}`. |
| `instanceId` | UUID | Required *(in model)* | — | — | Injected by the upsert orchestrator after the instance resolves. |
| `sourceId` | UUID | Required *(in model)* | — | — | Holdings source; resolved from RefCache; default `"MARC"` (`DEFAULT_HOLDINGS_SOURCE`). |
| `permanentLocationId` | UUID | Required *(in model)* | `location` | `852$b` | Resolved from RefCache by code/name; default `"History of Medicine"`. Example: `215;B11;MR;84;3;7` → UUID. |
| `callNumber` | string | Optional *(in model)* | — | `852$h` | Call number suffix. |
| `callNumberPrefix` | string | Optional *(in model)* | — | `852$c` | Example: `"Arch"`, `"Ref"`. |
| `shelvingOrder` | string | Optional *(in model)* | — | `852$j` | Shelving sequence. |
| `formerIds` / `discoverySuppress` | — | Recommended *(not in model)* | — | — | Future additions. |

---

## Item

`Item` model: `hrid`, `holdingsRecordId`, `status`, `materialType` `{id}`, `permanentLoanType` `{id}`, `permanentLocationId`, `barcode`, `copyNumber`, `volume`, `electronicAccess`, `notes`.

| FOLIO Field | Type | Status | AxC source | MARC Tag | Notes |
|-------------|------|--------|------------|----------|-------|
| `hrid` | string | Required *(in model)* | `guid` | `001` | Format `AxC-item-{guid}`. |
| `holdingsRecordId` | UUID | Required *(in model)* | — | — | Injected by the upsert orchestrator after the holdings resolves. |
| `status.name` | string | Required *(in model)* | — | — | Defaults to `"Available"` (`status` is a nested object, `default_factory=Status`). |
| `materialType.id` | UUID | Required *(in model)* | `Object_category` | `949$c` | Inventory `{ "id": "<uuid>" }` reference. RefCache + `MATERIAL_TYPE` table; default `"Books"`. Example: `"archives"` → `"unspecified"`. |
| `permanentLoanType.id` | UUID | Required *(in model)* | `Free_texts` (`OrderingCodes`) | `949$l` | `{ "id": "<uuid>" }`. RefCache; default `"Can Circulate"`. |
| `permanentLocationId` | UUID | Required *(in model)* | `location` | `852$b` | Bare UUID (the writable field; `permanentLocation` is read-only in FOLIO); same location as holdings. RefCache; default `"History of Medicine"`. |
| `barcode` | string | Optional *(in model)* | — | `949$a` | May be absent for archival items. |
| `copyNumber` | string | Optional *(in model)* | — | `876$p` | Example: `"copy 1"`. |
| `volume` | string | Optional *(in model)* | — | `876$t` | Example: `"v.1"`. |
| `electronicAccess[].uri` | array | Optional *(in model)* | — | `856$u` | Omitted when no `856$u`. |
| `notes[]` (type `Axiell location`) | array | Optional *(in model)* | `location` | `852$b` | One note `{ note: "Axiell location: <code>", noteType: "Axiell location", staffOnly: false }`. The AxC current location in human-readable form; **refreshed from `852$b` on every update**. `noteType` resolves to `itemNoteTypeId` during upsert. |
| `formerIds` / `discoverySuppress` | — | Recommended *(not in model)* | — | — | Future additions; on delete the upsert sets `discoverySuppress` and `staffSuppress` on the existing item. |

---

## RefCache Resolution

All reference lookups (location, material type, loan type, holdings source, item note type, and the default instance type) are resolved at sync time via **RefCache** (`ref_cache.py`), which loads that FOLIO reference data once per run. Resolution is case-insensitive: each raw AxC value is normalised (optional lookup table), falls back to a default, then resolves to a UUID; if the resolved name is unknown to the tenant, the build fails with `MappingError`.

**Defaults** (used when the MARC record carries no value): material type `"Books"`, loan type `"Can Circulate"`, location `"History of Medicine"`, holdings source `"MARC"`. The item location note always uses note type `"Axiell location"` (`AXIELL_LOCATION_NOTE_TYPE`).

**Material-type normalisations** (`MATERIAL_TYPE` table, AxC `Object_category` → FOLIO material-type name, case-insensitive):
- `"archives"` → `"unspecified"`
- `"published material"` → `"Books"`
- `"sound only"` / `"audio-visual material - e-sound only"` → `"sound recording"`
- `"audio-visual material - visual"` / `"audio-visual material - e-visual only"` → `"video recording"`

Location and loan type resolve directly by code/name (no normalisation table): a location code such as `"215;B11;MR;84;3;7"` and an `OrderingCodes` value such as `"Archives - Requestable"` are looked up against the cached FOLIO records.

See `mapping.py` for the `MARC_SOURCE` table, `MATERIAL_TYPE`, and the `DEFAULT_*` constants, and `ref_cache.py` for the lookup implementation.
