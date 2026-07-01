# RFC 090: Design Rationale

This document records *why* the [RFC 090 CMS→LMS sync](README.md) makes the
choices it does. The README states the decisions; this document holds the
trade-off analysis behind them, plus the cost evidence that backs the
"keep it simple" conclusions.

## Table of Contents

- [Mapping: Pydantic Models vs. YAML Mapper](#mapping-pydantic-models-vs-yaml-mapper)
- [Orchestration: Step Functions vs. Alternatives](#orchestration-step-functions-vs-alternatives)
- [Caching Strategy: Reference Data Scaling Options](#caching-strategy-reference-data-scaling-options)
- [Storage: S3 NDJSON vs. Alternatives](#storage-s3-ndjson-vs-alternatives)
- [Invocation Pattern: Ordering & Concurrency](#invocation-pattern-ordering--concurrency)
- [Error Handling: Per-Record Isolation](#error-handling-per-record-isolation)
- [SRS-backed Instances and the Update Path](#srs-backed-instances-and-the-update-path)
- [Cost Analysis](#cost-analysis)

---

## Mapping: Pydantic Models vs. YAML Mapper

| Approach | Pros | Cons |
|----------|------|------|
| **A: YAML mapper** (`mapping.yaml` + `YamlMapper`) | Mapping config separated from code; in principle non-programmers can read/adjust rules; changes are config-only | Errors surface only at runtime (often as a FOLIO 422); no type safety, so a typo'd key or wrong shape passes silently; a second engine (YAML schema + interpreter) to build, test, and document; awkward for normalization tables, per-field defaults, and composite hrids |
| **B: Typed Pydantic models** (`mapping.py`, chosen) | Validation at build time before any OKAPI call; payload shape is a typed contract (`extra="forbid"`); rules, defaults, and contracts in one reviewable module; full Python for normalization/conditionals; payloads stamped with `mapping_version` | Mapping changes need a Python edit + redeploy, not a config tweak; reading the rules assumes Python familiarity |

We chose the typed Pydantic models (B). The decisive factor is *when* errors surface: with typed models a missing or ill-typed required field (or an unknown key, since the models are `extra="forbid"`) raises `MappingError`/`ValidationError` during the build step, before any OKAPI call, whereas the YAML approach deferred the same failures to a FOLIO 422 mid-batch that is far harder to trace. Making the payload a typed contract also means a typo'd key is a build error rather than a silently dropped field, so the mapping and the FOLIO contract cannot drift apart unnoticed. Beyond correctness, it collapses two engines into one: ordinary Python replaces a bespoke YAML schema and its interpreter, so there is less to build, test, and document, and the normalization tables, defaults, and hrid scheme live beside the models. Every payload is also stamped with `mapping_version`, so any record in FOLIO or a manifest traces back to the exact rules that produced it.

The YAML mapper's headline appeal, letting non-programmers edit mappings as config, every rule change still went through review, tests, and a deploy, so config-versus-code made little practical difference, while the absence of type safety let malformed output reach FOLIO and fail there. As the rules grew (normalization tables, per-field defaults, composite GUID-based hrids) they simply read more clearly as Python than as declarative YAML.

> The YAML mapper (`mapping.yaml` + `YamlMapper`) was the original prototype design and has been **superseded** by the Pydantic approach. Remaining `mapping.yaml` references elsewhere in this RFC are historical.

---

## Orchestration: Step Functions vs. Alternatives

| Approach | Pros | Cons | Cost/mo |
|----------|------|------|---------|
| **A: Direct Lambda** (EventBridge → Lambda, fire-and-forget) | Fewer services, lower overhead, fastest time-to-invocation | No built-in retry logic, no execution history, hard to extend, silent failures possible | ~$2 |
| **B: Step Functions + Lambda** (chosen) | Explicit retry policy + audit trail, easy to parallelize later, clear visibility into success/failure | Extra service, marginal latency added | ~$3–5 |
| **C: Async Queue** (EventBridge → SQS → Lambda workers) | Decouples producer/consumer, handles bursts, resilient to adapter restarts | Complex ordering semantics, harder to reason about, no clear success/failure signal, monitoring overhead | ~$10–15 |

We chose Step Functions + Lambda (B): it buys an explicit retry policy and a full execution history. Every state transition is logged to CloudWatch, so a sync that fails partway is diagnosable from the execution history rather than by reconstructing state from Lambda logs, and max attempts and backoff are declarative, so operations can tune retries in the state-machine definition without code changes. The adapter triggers the sync asynchronously (`StartExecution`) and does not block; ordering safety comes from source-timestamp watermarking plus a Step Functions concurrency limit of 1 (see [Invocation Pattern](#invocation-pattern-ordering--concurrency)), not from backpressure. The design also leaves a clean extension point for scale: when volume outgrows a single invocation we swap in a Step Functions `Map` state to fan out per changeset, with no change to the manifest format. The cost is immaterial: pennies a month in state transitions at ~80 syncs/day (~2,400/month).

A direct EventBridge→Lambda trigger (A) was rejected because it gives no failure signal, no automatic retry, and no execution history, so debugging would mean parsing Lambda logs. An async SQS queue (C) is cheaper per invocation but doesn't guarantee processing order within a batch, needs workers to coordinate which changeset they own, and carries monitoring overhead (error tracking, retries, dead-letter management) that isn't justified at current volume.

---

## Caching Strategy: Reference Data Scaling Options

Reload-per-run assumes the reference set is small enough to bulk-load into Lambda memory cheaply (see [Reference Data Cache](README.md#reference-data-cache-ref_cachepy)). If we ever need **much more** reference data (many more types, or large per-record lookups), the choice of caching architecture matters. Options, cheapest first:

| Option | What it is | Best when | Cost / overhead | Freshness control |
|--------|-----------|-----------|-----------------|-------------------|
| **Warm singleton + reload-on-miss** | Module-global cache reused across warm invocations; fetch-and-memoize a code on a cache miss | Set still fits in memory; modest growth | None (in-process) | Self-healing on miss; lost on cold start |
| **S3 snapshot + scheduled refresher** | A cron (EventBridge) Lambda rebuilds a serialized snapshot (JSON/Parquet) from FOLIO every N hours; the sync Lambda reads it at startup (one GET) instead of N FOLIO calls | Whole set scanned each run; want to decouple sync from FOLIO availability | ~pennies/mo + one extra scheduled Lambda | Snapshot age = refresh cadence; pair with reload-on-miss |
| **DynamoDB lookup table** | Refresher populates `(type, code) → uuid`; sync Lambda `BatchGetItem`s only the codes a changeset needs | Set too big for memory, or only a subset is needed per run | On-demand $/read; native TTL | TTL / refresher cadence; pair with reload-on-miss |
| **ElastiCache (Redis)** | Shared in-memory cache across all invocations | Very large + hot lookups at high concurrency | Always-on (~$12+/mo), **requires VPC** (ENI cold-start + NAT to reach FOLIO/AWS APIs) | TTL |

**Recommended progression:** stay on reload-per-run → **S3 snapshot + scheduled refresher** (cheap, no VPC, scales via columnar formats, decouples from FOLIO reference endpoints) → **DynamoDB** only once the set outgrows Lambda memory or you genuinely need selective point lookups → **ElastiCache** only for high-concurrency hot-lookup workloads that justify always-on infra and the VPC tax. In every tier, keep a **reload-on-miss fallback to FOLIO** so a newly-added code resolves on first sight rather than failing the record.

---

## Storage: S3 NDJSON vs. Alternatives

| Approach | Pros | Cons | Cost/mo (90-day) |
|----------|------|------|------------------|
| **A: DynamoDB** (per-record writes, TTL) | Query-friendly, real-time dashboards possible, strong consistency | O(n) write cost, schema evolution painful, expensive for batches, not auditable | ~$20–50 |
| **B: S3 NDJSON** (chosen) | Batched writes (low cost), queryable (download + `jq`; Athena or S3 Select optional), matches the pipeline's NDJSON-manifest pattern, audit via versioning, easy to compress/archive | Requires S3 Select for queries (not real-time), not ideal for high-cardinality point lookups | ~$1–2 |
| **C: Streaming** (Kinesis/Firehose → Parquet) | High throughput, good for ML pipelines, efficient compression | Overkill for current volume, adds infrastructure complexity, higher cost | ~$5–15 |

We chose S3 NDJSON (B), and write-scaling is the main driver: per-record DynamoDB writes scale O(n) with record count, whereas the upserter batches its manifest writes into one S3 PUT per run (up to 5,000 records per object). At the current ~1,000 records/day across ~80 syncs that is about one object per run, so the batched model stays flat as volume grows rather than scaling per record. It is also explicitly the existing pipeline pattern rather than a new one: the adapter platform already emits per-job **NDJSON manifests** to S3, so reusing that format (and S3 generally) keeps backup, recovery, query, and downstream tooling consistent across the pipeline. And it stays queryable after the fact without any ETL. **S3 Select** is one convenient option (e.g. `SELECT * FROM s3://bucket/manifest.ndjson WHERE errors > 0`, ~500 ms on a 100 KB file), but note S3 Select is **not currently used elsewhere in the org**, so we don't depend on it: because the manifests are plain NDJSON, a failed-record list is equally available by just downloading the object and piping it through `jq`/`grep`, or by pointing Athena at the prefix if ad-hoc SQL is ever wanted. S3 Select is a nicety, not a load-bearing part of the design; whether to adopt it is an open question (see README). S3 versioning provides an audit trail (every write is a recoverable object version, with the metadata JSON tracking historical jobs), and after 90 days manifests archive cheaply to Glacier, something DynamoDB has no low-cost equivalent for.

DynamoDB (A) was rejected on fit rather than headline cost (at ~1,000 writes/day either store is cheap), because its per-record write model scales O(n), schema changes require a scan-and-rewrite, and there's no clean way to answer audit questions like "what was deleted last week?". Streaming via Kinesis/Firehose (C) is built for thousands of records per second (overkill for 10–500-record changesets) and adds buffer/flush operational complexity we don't need.

---

## Invocation Pattern: Ordering & Concurrency

The README specifies the mechanism as behaviour (the source-timestamp stale-write guard in [Step 4: Upsert to FOLIO](README.md#step-4-upsert-to-folio-per-record) and the [Upsert Key Strategy](README.md#upsert-key-strategy-idempotency), plus the Step Functions concurrency limit of 1). This is the reasoning behind it.

EventBridge publishes changeset events to Step Functions via `StartExecution` (asynchronous, fire-and-forget); the adapter does not block waiting for the sync to complete. Step Functions provides the execution visibility and retry policy, and all invocations (initial or retry) are decoupled from the adapter.

However, concurrent or retried executions create an **ordering risk**: if two changesets arrive within ~45 s of each other, or if a failed changeset is retried while a newer one is in flight, a naive last-write-wins upsert could apply an older state after a newer one, corrupting the FOLIO record. Similarly, idempotent replays (re-running failed changesets after a fix) must be no-ops if a newer changeset has already updated the same record.

**Source-timestamp watermarking.** The upsert layer compares each incoming record's Axiell `last_modified` timestamp (from the source data) against a watermark stored on the FOLIO record. The write proceeds only if the incoming timestamp is strictly newer; otherwise the record is skipped, leaving the FOLIO state intact. Where exactly that watermark lives in FOLIO (an administrative note, a custom property, or a version field) is itself an open question; see the README. This ensures:
- Out-of-order concurrent executions apply updates in source-timestamp order, not invocation order.
- Replays (re-running failed changesets) are idempotent: an older changeset re-run after a newer one succeeds does not overwrite the newer state.
- No coupling between adapter and sync (the adapter remains fire-and-forget).

**Concurrency control.** A Step Functions concurrency limit of 1 (via the state machine definition) is a secondary guard, preventing the GET–PUT gap between a query and an upsert; with a limit of 1, only one execution can be in the `Lambda` state at a time, so even if two changesets arrive within milliseconds, the second waits for the first to commit. This is loose (the adapter cadence is 15 minutes, so concurrency is naturally rare) but provides an extra safeguard against read-skew during retries.

Combined, these two mechanisms ensure ordering safety without blocking the adapter or introducing a queue.

---

## Error Handling: Per-Record Isolation

The guiding policy is that one bad record must never halt the batch.

Per-record errors are non-blocking. A mapping error (Pydantic validation, a missing required field, or an unresolved reference) is captured as `{"source_id": "...", "type": "mapping", "detail": "..."}` and an API error (FOLIO returns 4xx/5xx) as `{"source_id": "...", "type": "api", "detail": "..."}`; in either case the record is written to the S3 error manifest and processing moves on to the next record. Batch-level errors, by contrast, are blocking: an OKAPI auth failure, an Iceberg connection failure, or an S3 write failure raises an exception that the Step Function retries up to `max_retries`, and if those are exhausted the execution ends in the terminal `SyncFailed` state and raises an alert.

Failures are observable across four channels: CloudWatch Logs (`/aws/lambda/axiell-folio-sync`) for detailed per-record execution, the S3 `.ids.failures.ndjson` manifest for a queryable error list (via a plain download + `jq`, or optionally S3 Select; see the storage note), CloudWatch Metrics (`RecordsFailed`, `RecordsCreated`, and the like) for alerting on a high failure rate, and the Step Function history (`/aws/states/axiell-folio-sync-sfn`) for state transitions and retry events.

**Skipped records are also accounted for, not dropped silently.** Records skipped before a write (no `980 $a` harvest flag, `Level` gating, or the stale-write guard) are counted in a `RecordsSkipped` metric and recorded in the run's metadata manifest, so "why didn't record X appear in FOLIO?" is answerable after the fact rather than being an invisible no-op.

**Alert path:** alerting follows the existing pipeline pattern: a **CloudWatch metric alarm** (on `RecordsFailed`/the failure rate, and on `SyncFailed` Step Function executions) fires into the team's **Slack** channel via **Amazon Q Developer in chat applications**. No new notification mechanism is introduced; the alarms are wired to the same SNS-topic → Amazon Q → Slack route already used elsewhere in the catalogue pipeline.

---

## SRS-backed Instances and the Update Path

A consideration worth making explicit for the update path. Some FOLIO instances are backed by **Source Record Storage (SRS)** as MARC, for example anything migrated or loaded as MARC. For those records the bibliographic fields are controlled by the underlying SRS MARC record and **cannot be updated through the mod-inventory instance API**; only administrative data is editable there. MARC edits go through **quickMARC**, which writes to SRS and syncs the Inventory record. A `PUT` to mod-inventory may therefore fail or be silently ignored for an SRS-backed instance, whereas the current update logic assumes the PUT takes effect.

**Which storage do we create records in, Inventory-native (FOLIO source) or MARC/SRS?**
Records created the two ways behave differently on update, so a mixed estate is harder to reason about and maintain. This sync currently creates Inventory-native instances (`Instance.source = "FOLIO"`, with no linked SRS record), which keeps the bibliographic fields editable through mod-inventory and keeps the PUT-based update path valid.

**Catalogue-pipeline impact:** the catalogue pipeline harvests FOLIO over OAI-PMH using the `marc21_withholdings` prefix (see `catalogue_graph/src/adapters/extractors/oai_pmh/folio/config.py`). Under that prefix the instance bib comes from SRS when an SRS record is present, or is generated on the fly from Inventory depending on the **mod-oai-pmh record-source** setting, while holdings and items come from Inventory. So whether the records this sync creates appear in that feed, and in what form, depends on the storage type we choose together with the mod-oai-pmh configuration. This has now been confirmed via the prototype for Inventory-native records: a `source = "FOLIO"` instance created here is updatable through mod-inventory and is received on the FOLIO adapter in the catalogue pipeline. One gap remains under investigation, the item notes not appearing on the OAI-PMH feed; see the README open question.

---

## Cost Analysis

At ~80 syncs/day the pipeline runs ~2,400 times/month, so the monthly quantities below derive from that:

| Service | Operation | Qty/mo | Rate | Cost/mo |
|---------|-----------|--------|------|---------|
| Lambda | ~2,400 invocations × ~60s × 512 MB | ~2,400 invocations | $0.0000167/GB-s | ~$1.20 |
| Step Functions | ~2,400 state transitions | ~2,400 transitions | $0.000025/transition | ~$0.06 |
| EventBridge | ~2,400 events | ~2,400 events | $1/M events | ~$0.00 |
| S3 (manifests) | ~2,400 objects written, 90-day retention | ~2,400 objects + storage | $0.005/K PUTs + $0.023/GB/mo | ~$1.50 |
| CloudWatch Logs | ~2,400 × 5 KB ≈ 12 MB/month | 12 MB ingested | $0.50/GB ingested | ~$0.20 |
| **Total** | | | | **~$3–5** |
