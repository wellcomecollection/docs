# Notes on the RFC 091 discussion (PR #159): implications for RFC 085

> Review notes on the comment thread of
> [wellcomecollection/docs#159](https://github.com/wellcomecollection/docs/pull/159)
> (RFC 091: Digitisation ingest identifiers during the Sierra to Folio migration),
> written 2026-08-04, while the thread's conclusion was awaiting discussion.
> Kept alongside RFC 085 because the thread's outcome inverts this RFC's
> "Use the Work ID" position. Generated with Claude Code from a review of the
> thread between @tomcrane, @kenoir and @paul-butcher. Revised the same day
> after reviewing RFC 089 (Identifiers API, merged via
> [#156](https://github.com/wellcomecollection/docs/pull/156)), which softens
> the "id form vs DDS parsing" concern to its structural core.

## The arc of the thread, and whether the landing point is right

This is one of those rare review threads that genuinely reversed an RFC's
central proposal, and the reversal looks correct. The original proposal (mint
catalogue-style ids at ingest, work towards `presentation/{workId}` as
canonical) died from three independent wounds, each fatal on its own:

1. **The pipeline constraint** (@kenoir) — the METS-sourced work's canonical id
   can never be the LMS target's id, because the merge is computed at merge
   time from mutable metadata. Baking the LMS work id into permanent object
   names (S3 keys, manifest filenames) would make immutable artefacts depend on
   a mutable join.
2. **The n:1 point** (@paul-butcher) — a merged work can aggregate multiple
   storage objects, so manifest:work was never guaranteed 1:1, and keeping the
   id schemes visibly distinct avoids false expectations when merge rules
   change.
3. **The URI-consistency argument** (@tomcrane, 2026-07-28) — probably the
   decisive one. Canvas ids, image URIs and annotation targets derive from METS
   filenames and can never be redirected. Renaming only the outer manifest URI
   to the workId buys a matching tail with the work page at the cost of
   *permanent internal inconsistency in every document*, for old and new
   content alike. The preservation-id-canonical scenario is the only one where
   a manifest and its contents agree.

The conclusion — preservation id stays the canonical manifest URI forever,
workId redirects to it, no upstream minting, Identifiers API stays read-only,
RFC 081 drops out of the ingest path — is also the smallest system by a wide
margin. The cost (work page and manifest permanently stop sharing a tail) is
real but is named honestly in the thread as a deliberate trade, which is what
an RFC should record.

The outcome is also kind to the DDS: the SQS message identifier stays the
preservation id, Goobi/Archivematica keep emitting the identifier DDS already
keys everything by, and the DDS identity service keeps its model intact rather
than being partly superseded.

## Points to raise before/during the RFC 091 rewrite

### The form of the new preservation id: what RFC 089 changes, and what it doesn't

An earlier draft of these notes said the id form "collides directly with DDS
parsing assumptions". With RFC 089 (Identifiers API, now merged) in the
picture, that needs splitting in two: the DDS identity service can *defer* to
the platform registry for work-level identity, so half of the concern
dissolves — but the other half is inherently local to DDS and no external
service can absorb it.

**What deferral fixes — the metadata half.** Today the DDS parser infers
source, generator and storage space from identifier shape ("starts with a
b-number → Sierra/Goobi/digitised, else CALM/Archivematica/born-digital").
A new opaque id would provisionally misclassify — but those values are
provisional by design, and DDS has authoritative sources for all of them: the
SQS message origin supplies the generator at ingest, a storage-service probe
validates the space, and the Identifiers API now adds resolution of any
identifier string to its canonical id and labelled source ids
(`sierra-system-number`, `calm-ref-no`, `folio-instance`, …). Shape-based
*inference* can shrink to shape-based *candidate generation* for lookups, with
results persisted in DDS's own identities table so the registry round-trip is
once per identifier. Timing works out too: at the very first workflow message
for a brand-new item the registry may not know the id yet (the pipeline mints
when the METS transformer runs, unordered relative to DDS) — but at that
moment the SQS origin covers it; deferral is only needed on the read path,
by which time the pipeline has caught up.

**What deferral cannot fix — the structural half.** RFC 089's canonical-first
principle explicitly stops at the work level: "it does not extend to sub-work
IIIF structure". Sub-package identity is DDS's to own, and the structural
questions bite *before* any lookup can be made:

- `wxyz9876_0002` (volume two of a new multi-volume item) must be split into
  package id + volume suffix before anything can be resolved; the registry
  will never answer suffix questions. And it is shape-identical to a CALM ref
  written with underscores (`PPCRI_A_1`), whose normalisation is
  underscores→slashes. Lookup-based disambiguation (try the full string, then
  candidate stems) is workable — the persisted identities table makes it a
  once-per-identifier cost — but a syntactically recognisable id form makes it
  a non-problem. Either the form is distinguishable, or the multi-volume
  suffix convention is defined alongside it; it can't be left implicit,
  because Goobi will stamp it into METS filenames and JP2 names
  (`<id>_0001.jp2`) on day one, upstream of any service.
- It must be **path-element safe as-is** (it becomes S3 keys, METS filenames,
  IIIF URIs, DLCS string references) and ideally **case-stable** — the one
  accepted risk left in the DDS identity service is CALM case-collision on the
  lowercased key; a new scheme should be defined lowercase from birth so it
  never inherits that problem. These are storage/URI constraints, not parsing
  ones; no registry helps.
- It should be **visibly distinct from the workId scheme** (the debugging
  argument from the thread) *and* from the b-number regex — RFC 091's
  transformer fallback ("matches Sierra regex → `sierra-system-number`, else
  `calm-ref-no`") would misclassify a new-form id unless a third branch is
  added. That fallback needs updating in the rewrite anyway once born-digital
  is in scope.

**A note on RFC 089 itself.** Its description of the DDS consumer is written
against pre-inversion RFC 085 (workId becomes the canonical IIIF URI, old
forms redirect to it). Under the RFC 091 thread outcome the redirect direction
flips — the preservation id stays canonical and the workId form redirects to
it — but the API contract the DDS needs is unchanged: "given a string, return
everything known about it" serves both directions. The API stays read-only,
which the RFC 091 outcome preserves (the secured mint endpoint extension is no
longer needed).

### The workId → preservation-id redirect becomes a committed contract

Under the agreed scenario, DDS's redirect duty extends to all content —
including born-digital, where today `SABTS/A/2/10` doesn't redirect and its
workId doesn't resolve on iiif.wellcomecollection.org at all. The DDS-side
binding for that redirect is effectively `DdsIdentity.CatalogueId` / the
Manifestations metadata.

Note that the Identifiers API does not replace this binding: as observed in
the RFC 091 thread, the registry "cannot hold the result of redirection from
merge" — which workId a digital object's work merged into is catalogue-api
knowledge. So the workId→manifest redirect remains a DDS responsibility backed
by its stored CatalogueId, with the Identifiers API complementing it for
source-id↔canonical-id translation.

A known design choice in the DDS identity service was load-bearing here:
**CatalogueId was never refreshed once a package was authoritative**, because
repeat generator messages returned the stored row early — so a catalogue merge
could silently stale the redirect data. The DDS side has since been adjusted:
known-generator messages now always re-take the write path, refreshing
CatalogueId (and re-validating storage space) on every reprocess.

### Smaller items for the rewrite

- The born-digital/preservation framing is now committed to — but hold the
  rewrite to the *examples matrix* (digitised/born-digital × Folio/Axiell,
  with actual identifier strings at each layer: storage, METS filename, image
  filename, manifest URI, workId, redirect). The `wxyz9876_0002` misparse
  above is exactly the kind of thing the matrix would have surfaced.
- RFC 085's "Use the Work ID" section inverting is mentioned in the thread but
  easy to lose — the 085 amendment should be a named deliverable of the RFC
  091 rewrite rather than a follow-up intention, so the two documents don't
  disagree in the interim.

## An open question the thread parks but doesn't answer

For **cross-migration CALM material moving to Axiell**: does the archival ref
survive identically (in which case the born-digital story is "no change,
ever"), or can refs be restructured in Axiell — in which case born-digital
needs the same predecessor mechanism as b-numbers, and that mechanism is
currently only specified for Sierra→Folio.
