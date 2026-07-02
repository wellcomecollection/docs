"""
AxC → FOLIO mapping: payload models, normalization rules, and builders.

This is the single home for everything that decides *what an Axiell record
becomes in FOLIO*. It replaces the former mapping.yaml + yaml_mapper.py pair:
the rules are now ordinary Python and the payloads are typed Pydantic models,
so a malformed payload (missing/ill-typed required field, typo'd key) fails at
build time — before any OKAPI call — instead of surfacing as a FOLIO 422.

Everything a reviewer needs to understand or change the mapping lives here:

  • MATERIAL_TYPE          AxC source code → FOLIO standard material-type name
  • DEFAULTS / hrid scheme module-level constants
  • Instance/Holdings/Item Pydantic payload contracts
  • build_instance/holdings/item   the field-by-field mapping logic
  • build_payloads          orchestration → the dict shape upsert consumes

MARC *extraction* (which subfield holds what) stays in mapper.parse_marcxml,
which yields the CanonicalRecord these builders read from.

Output contract is unchanged from the YAML mapper: ``build_payloads`` returns
``{"instance": {...}, "holdings": {...}, "item": {...}, "meta": {...}}`` ready
for :func:`axiell_folio_sync.upsert.upsert_from_payloads`.
"""

from __future__ import annotations

from typing import Callable, Optional

from pydantic import BaseModel, ConfigDict, Field

from .mapper import CanonicalRecord, MappingError, extract, parse_xml
from .ref_cache import RefCache

# Bumped whenever the rules below change; stamped into every payload's meta.
VERSION = "2.1.0"


# ── inbound: which MARC field feeds which CanonicalRecord attribute ─────────────
#
# This table is the single source of truth for the Axiell/MARC *source* side.
# Spec syntax: "TAG$subfield" for datafields, "TAG" for controlfields.
MARC_SOURCE: dict[str, str] = {
    "source_id":             "001",     # Axiell GUID — identifies the record
    "title":                 "245$a",
    "location_code":         "852$b",
    "call_number":           "852$h",
    "call_number_prefix":    "852$c",
    "shelving_order":        "852$j",
    "barcode":               "949$a",
    "material_type_code":    "949$c",
    "loan_type_code":        "949$l",
    "copy_number":           "876$p",
    "volume":                "876$t",
    "electronic_access_uri": "856$u",
}


def parse_marcxml(xml_content: str, *, deleted: bool = False) -> CanonicalRecord:
    """Parse a single MARCXML string into a :class:`CanonicalRecord` via MARC_SOURCE.

    Raises :class:`MappingError` if MARC 001 is absent (record cannot be identified).
    """
    root = parse_xml(xml_content)
    values = {field: extract(root, spec) for field, spec in MARC_SOURCE.items()}

    source_id = values["source_id"]
    if not source_id:
        raise MappingError("Missing MARC 001 — cannot identify record")

    # Single GUID-based hrid scheme (see _instance_hrid / _holdings_hrid): every
    # hrid is derived purely from the Axiell GUID, never from location, so the
    # idempotency key stays stable even if a record's location changes.
    return CanonicalRecord(
        instance_hrid=_instance_hrid(source_id),
        holdings_hrid=_holdings_hrid(source_id),
        deleted=deleted,
        **values,
    )


# ── normalization tables & defaults ─────────────────────────────────────────────

# Axiell source code → FOLIO standard material-type name. Case-insensitive keys.
MATERIAL_TYPE: dict[str, str] = {
    "sound only": "sound recording",
    "audio-visual material - visual": "video recording",
    "audio-visual material - e-sound only": "sound recording",
    "audio-visual material - e-visual only": "video recording",
    "published material": "Books",
    "archives": "unspecified",
}

# Fallbacks used when the MARC record carries no value for a resolved field.
DEFAULT_MATERIAL_TYPE = "Books"
DEFAULT_LOAN_TYPE = "Can Circulate"
DEFAULT_LOCATION = "History of Medicine"
DEFAULT_HOLDINGS_SOURCE = "MARC"
AXIELL_LOCATION_NOTE_TYPE = "Axiell location"


def _instance_hrid(source_id: str) -> str:
    return f"AxC-instance-{source_id}"


def _holdings_hrid(source_id: str) -> str:
    return f"AxC-holding-{source_id}"


def _item_hrid(source_id: str) -> str:
    return f"AxC-item-{source_id}"


# ── payload models (the FOLIO contract) ─────────────────────────────────────────

class IdRef(BaseModel):
    """A FOLIO {"id": "<uuid>"} reference object."""
    id: str


class Status(BaseModel):
    name: str = "Available"


class Note(BaseModel):
    # noteType is resolved to itemNoteTypeId later by upsert._resolve_item_note_types.
    model_config = ConfigDict(extra="allow")
    note: str
    noteType: Optional[str] = None
    staffOnly: bool = False


class ElectronicAccess(BaseModel):
    uri: str


class Instance(BaseModel):
    model_config = ConfigDict(extra="forbid")  # guard against typo'd keys in our code
    hrid: str
    title: str
    source: str = "FOLIO"
    instanceTypeId: str


class Holdings(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hrid: str
    instanceId: Optional[str] = None  # injected by the upsert orchestrator
    sourceId: str
    permanentLocationId: str
    callNumber: Optional[str] = None
    callNumberPrefix: Optional[str] = None
    shelvingOrder: Optional[str] = None


class Item(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hrid: str
    holdingsRecordId: Optional[str] = None  # injected by the upsert orchestrator
    status: Status = Field(default_factory=Status)
    materialType: IdRef
    permanentLoanType: IdRef
    permanentLocationId: str  # bare UUID; `permanentLocation` is read-only in FOLIO
    barcode: Optional[str] = None
    copyNumber: Optional[str] = None
    volume: Optional[str] = None
    electronicAccess: Optional[list[ElectronicAccess]] = None
    notes: Optional[list[Note]] = None


# ── lookup helper (mirrors the YAML map → default → lookup chain) ────────────────

def _resolve(
    resolver: Callable[[Optional[str]], Optional[str]],
    raw: Optional[str],
    *,
    label: str,
    default: str,
    table: Optional[dict[str, str]] = None,
) -> str:
    """Normalize a raw AxC code, fall back to ``default``, then resolve to a UUID.

    Raises MappingError if the resolved name is unknown to the FOLIO tenant.
    """
    value = (raw or "").strip()
    if table:
        value = table.get(value.lower(), value)
    if not value:
        value = default
    uuid = resolver(value)
    if uuid is None:
        raise MappingError(
            f"Unresolved {label} {value!r} — add it to the FOLIO tenant or fix the MARC"
        )
    return uuid


# ── builders (the mapping) ──────────────────────────────────────────────────────

def build_instance(rec: CanonicalRecord, ref: RefCache) -> Instance:
    if not rec.title:
        raise MappingError(f"Missing 245$a (title) for source_id={rec.source_id}")
    return Instance(
        hrid=_instance_hrid(rec.source_id),
        title=rec.title.strip(),
        # FOLIO-native: we create the instance via the Inventory API with no
        # linked SRS MARC record, so the source is FOLIO, not MARC.
        source="FOLIO",
        instanceTypeId=ref.instance_type_id(),
    )


def build_holdings(rec: CanonicalRecord, ref: RefCache) -> Holdings:
    return Holdings(
        hrid=_holdings_hrid(rec.source_id),
        sourceId=_resolve(
            ref.resolve_holdings_source, DEFAULT_HOLDINGS_SOURCE,
            label="holdings source", default=DEFAULT_HOLDINGS_SOURCE,
        ),
        permanentLocationId=_resolve(
            ref.resolve_location, rec.location_code,
            label="location", default=DEFAULT_LOCATION,
        ),
        callNumber=rec.call_number,
        callNumberPrefix=rec.call_number_prefix,
        shelvingOrder=rec.shelving_order,
    )


def build_item(rec: CanonicalRecord, ref: RefCache) -> Item:
    location_id = _resolve(
        ref.resolve_location, rec.location_code,
        label="location", default=DEFAULT_LOCATION,
    )
    return Item(
        hrid=_item_hrid(rec.source_id),
        materialType=IdRef(id=_resolve(
            ref.resolve_material_type, rec.material_type_code,
            label="material type", default=DEFAULT_MATERIAL_TYPE, table=MATERIAL_TYPE,
        )),
        permanentLoanType=IdRef(id=_resolve(
            ref.resolve_loan_type, rec.loan_type_code,
            label="loan type", default=DEFAULT_LOAN_TYPE,
        )),
        permanentLocationId=location_id,
        barcode=rec.barcode,
        copyNumber=rec.copy_number,
        volume=rec.volume,
        electronicAccess=(
            [ElectronicAccess(uri=rec.electronic_access_uri)]
            if rec.electronic_access_uri else None
        ),
        notes=[Note(
            note=f"Axiell location: {rec.location_code or 'unknown'}",
            noteType=AXIELL_LOCATION_NOTE_TYPE,
            staffOnly=False,
        )],
    )


# ── orchestration ───────────────────────────────────────────────────────────────

def build_payloads(
    xml_content: str,
    ref_cache: RefCache,
    *,
    deleted: bool = False,
) -> dict:
    """Parse MARCXML and build the three FOLIO payloads as JSON-ready dicts.

    Drop-in replacement for ``YamlMapper.build_payloads`` — returns the same
    ``{"instance", "holdings", "item", "meta"}`` shape that
    :func:`axiell_folio_sync.upsert.upsert_from_payloads` consumes.

    Raises :class:`MappingError` for required-field violations or unresolved lookups.
    """
    rec = parse_marcxml(xml_content, deleted=deleted)

    instance = build_instance(rec, ref_cache)
    holdings = build_holdings(rec, ref_cache)
    item = build_item(rec, ref_cache)

    return {
        "instance": instance.model_dump(exclude_none=True),
        "holdings": holdings.model_dump(exclude_none=True),
        "item": item.model_dump(exclude_none=True),
        "meta": {
            "source_id": rec.source_id,
            "instance_hrid": _instance_hrid(rec.source_id),
            "holdings_hrid": _holdings_hrid(rec.source_id),
            "item_hrid": _item_hrid(rec.source_id),
            "mapping_version": VERSION,
            "deleted": deleted,
        },
    }
