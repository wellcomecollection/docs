# FOLIO Minimum Fields Mapping (AxC → FOLIO)

**Date:** 2026-06-17  
**Status:** Reference guide for AxC to FOLIO data integration  
**Related:** [axc-folio-field-mapping.md](axc-folio-field-mapping.md) · [axiell-to-folio-upsert.md](axiell-to-folio-upsert.md)  
**Code:** `prototypes/axiell-folio-sync/axiell_folio_sync/mapper.py`

---

## Instance

Minimum recommended fields to create a discoverable, functional instance record in FOLIO Inventory.

| FOLIO Field | Type | Status | OIM Field (AxC) | MARC Tag | Notes |
|-------------|------|--------|-----------------|----------|-------|
| `hrid` | string | Required | `object_number` | `001` | Hierarchical record identifier. Format: `axiell:{source_id}`. Example: `axiell:PP/CJS/B.3/9` |
| `title` | string | Required | `Titles/title` | `245$a` | Primary title from object. Essential for discoverability; fails API if absent. Example: `Daniel Morley, an English Philosopher of the XIIth Century. Isis, 1920, iii, 263-9` |
| `source` | string | Required | — | — | Hardcoded to `"Axiell"` to mark origin system. |
| `instanceTypeId` | UUID | Required | — | — | Resolved from RefCache. Typically `"text"` or domain type (e.g., `"unspecified"` for mixed media). |
| `formerIds` | array | Recommended | `guid` + `Alternative_number` (Calm RefNo) | `035$a` + `244$a` | Preserve alternate identifiers for reference and migration. Includes AxC GUID and legacy Calm RefNo. Example: `["axiell:PP/CJS/B.3/9", "PPCJS/B/3/9"]` |
| `discoverySuppress` | boolean | Recommended | `accession_status` | — | Set `true` for RESTRICTED items or draft records. Default `false` for OPEN items. |

---

## Holdings

Minimum recommended fields to link instance to location and call numbers.

| FOLIO Field | Type | Status | OIM Field (AxC) | MARC Tag | Notes |
|-------------|------|--------|-----------------|----------|-------|
| `hrid` | string | Required | `object_number` + `location.default.name` | `001` + `852$b` | Composite identifier linking record to location. Format: `axiell:{source_id}-holding-{location_slug}`. Example: `axiell:PP/CJS/B.3/9-holding-215-b11-mr-84-3-7` where `location_slug` is lowercased, hyphenated. |
| `instanceId` | UUID | Required | — | — | FOLIO instance UUID. Resolved after instance POST succeeds. |
| `permanentLocationId` | UUID | Required | `location.default.name` | `852$b` | Hierarchical shelf location from AxC. Resolved from RefCache using location code string. Example: `215;B11;MR;84;3;7` → UUID lookup. |
| `callNumber` | string | Recommended | — | `852$h` | Call number suffix. Optional but aids patron retrieval. |
| `callNumberPrefix` | string | Optional | — | `852$c` | Call number prefix or classification. Example: `"Arch"`, `"Ref"`. |
| `shelvingOrder` | string | Optional | — | `852$j` | Sort/shelving sequence for physical ordering on shelf. |
| `formerIds` | array | Recommended | `guid` + `Alternative_number` | `035$a` + `244$a` | Preserve AxC identifiers. Example: `["axiell:PP/CJS/B.3/9"]` |
| `discoverySuppress` | boolean | Recommended | `accession_status` | — | Set `true` if holdings should not appear in public discovery. Inherits from instance or may override. |

---

## Item

Minimum recommended fields to represent the physical/digital object in circulation.

| FOLIO Field | Type | Status | OIM Field (AxC) | MARC Tag | Notes |
|-------------|------|--------|-----------------|----------|-------|
| `hrid` | string | Required | `object_number` | `001` | Item record identifier. Format: `axiell:{source_id}`. Example: `axiell:PP/CJS/B.3/9` |
| `holdingsRecordId` | UUID | Required | — | — | FOLIO holdings UUID. Resolved after holdings POST succeeds. |
| `status.name` | string | Required | — | — | Hardcoded to `"Available"` for initial sync. Valid values: `"Available"`, `"Awaiting pickup"`, `"Checked out"`, etc. |
| `materialTypeId` | UUID | Required | `Object_category/object_category` | `949$c` | Material type (format) of the item. Resolved from RefCache. Example: `Archives - Non-digital` → `unspecified` UUID. See material type normalisation table. |
| `permanentLoanTypeId` | UUID | Required | `Free_texts` (type=`OrderingCodes`) | `949$l` | Loan policy. Resolved from RefCache. Example: `"Archives - Requestable"` → loan type UUID. |
| `barcode` | string | Optional | — | `949$a` | Machine-readable barcode. Used for physical item tracking. May be absent for archival items. |
| `copyNumber` | string | Optional | — | `876$p` | Distinguishes multiple copies of the same item. Example: `"copy 1"`, `"copy 2"`. |
| `volume` | string | Optional | — | `876$t` | Volume designation for multi-part works. Example: `"v.1"`, `"disc 1 of 2"`. |
| `formerIds` | array | Recommended | `guid` | `035$a` | Preserve AxC GUID for reference. Example: `["axiell:4d8f1208-9812-4bb5-84ef-da436b22d9e2"]` |
| `discoverySuppress` | boolean | Recommended | `accession_status` | — | Set `true` for RESTRICTED items. Hides item from public search results. |

---

## RefCache Resolution

All reference fields (`permanentLocationId`, `instanceTypeId`, `materialTypeId`, `permanentLoanTypeId`) are resolved at sync time via **RefCache**, which caches FOLIO reference data (locations, material types, loan types, instance types). If a code cannot be resolved, the upsert fails with `MappingError`.

**Current normalisations:**
- **Material type:** AxC `Object_category` → FOLIO material type (e.g., `"Archives - Non-digital"` → `"unspecified"`; audio → `"sound recording"`).
- **Location:** AxC hierarchical location code (e.g., `"215;B11;MR;84;3;7"`) → FOLIO location UUID.
- **Loan type:** AxC `OrderingCodes` (e.g., `"Archives - Requestable"`) → FOLIO loan type UUID.

See `prototypes/axiell-folio-sync/axiell_folio_sync/ref_cache.py` for lookup implementation.
