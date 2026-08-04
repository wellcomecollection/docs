# Notes on the RFC 091 discussion (PR #159): implications for RFC 085

> Review notes on the comment thread of
> [wellcomecollection/docs#159](https://github.com/wellcomecollection/docs/pull/159)
> (RFC 091: Digitisation ingest identifiers during the Sierra to Folio migration),
> written 2026-08-04, while the thread's conclusion was awaiting discussion.
> Kept alongside RFC 085 because the thread's outcome inverts this RFC's
> "Use the Work ID" position. Generated with Claude Code from a review of the
> thread between @tomcrane, @kenoir and @paul-butcher.

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

### The form of the new preservation id is not a cosmetic afterthought

It collides directly with DDS parsing assumptions. The thread defers the id
form ("concrete candidates" to come with the rewrite), but from the
iiif-builder side there are hard constraints worth stating now, because the
current parser infers everything from identifier shape:

- Anything that doesn't start with a b-number is currently assumed to be a
  **CALM ref: born-digital, Archivematica, and — critically — underscores are
  normalised to slashes**. A new opaque digitised id like `wxyz9876` would
  provisionally parse as born-digital/Archivematica (recoverable — the
  generator-authoritative write path in the DDS identity service exists
  precisely to overrule parsing), but `wxyz9876_0002` for volume two of a new
  multi-volume item would be *structurally misparsed* as CALM ref
  `wxyz9876/0002`. Volume/issue sub-structure parsing is b-number-only today.
  So the id form needs to either be syntactically distinguishable from CALM
  refs, or the multi-volume suffix convention needs defining alongside it — it
  can't be left implicit, because Goobi will stamp it into METS filenames and
  JP2 names (`<id>_0001.jp2`) on day one.
- It must be **path-element safe as-is** (it becomes S3 keys, METS filenames,
  IIIF URIs, DLCS string references) and ideally **case-stable** — the one
  accepted risk left in the DDS identity service is CALM case-collision on the
  lowercased key; a new scheme should be defined lowercase from birth so it
  never inherits that problem.
- It should be **visibly distinct from the workId scheme** (the debugging
  argument from the thread) *and* from the b-number regex — RFC 091's
  transformer fallback ("matches Sierra regex → `sierra-system-number`, else
  `calm-ref-no`") would misclassify a new-form id unless a third branch is
  added. That fallback needs updating in the rewrite anyway once born-digital
  is in scope.

### The workId → preservation-id redirect becomes a committed contract

Under the agreed scenario, DDS's redirect duty extends to all content —
including born-digital, where today `SABTS/A/2/10` doesn't redirect and its
workId doesn't resolve on iiif.wellcomecollection.org at all. The DDS-side
binding for that redirect is effectively `DdsIdentity.CatalogueId` / the
Manifestations metadata.

A known design choice in the DDS identity service becomes more load-bearing
here: **CatalogueId is never refreshed once a package is authoritative**,
because repeat generator messages return the stored row early. If a catalogue
merge changes which workId points at a digital object, the reverse redirect
data in DDS silently stales until something forces an update. Cheap to address
(refresh CatalogueId on repeat authoritative messages, or a periodic sweep),
but it should be on the list once RFC 091 lands.

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
