# RFC 090: Axiell-FOLIO Sync Architecture

## Purpose

Design a system to synchronize library location and item holdings from Axiell (legacy adapter) into FOLIO (new system of record) on a 15-minute cadence, with strict requirements for idempotency, auditability, and graceful error isolation.

**Last modified:** 2026-06-22

---

## Background

### Current State
- **Axiell Adapter Platform**: Runs on a 15-minute cadence, emitting changesets with new/modified/deleted records
- **FOLIO**: The new system of record for library data (items, holdings, locations)
- **Integration Gap**: Changesets are written to Apache Iceberg tables on S3, but FOLIO is not automatically updated
- **Volume**: ~10–500 records per changeset (15-minute window); typical day: ~1,000 records across 80 syncs

### Why This Matters
- Library staff rely on FOLIO for real-time item availability and location data
- Axiell-to-FOLIO sync is a core data pipeline for the new catalogue system
- Sync must be reliable, auditable, and manually recoverable

---

## Problem Statement

How do we build a system that:

1. **Reliably syncs incremental changesets** (10–500 records per 15-min window) from Axiell to FOLIO?
2. **Handles failures gracefully**: One bad record (mapping error, API failure) must not halt processing of others?
3. **Maintains a complete audit trail**: Every record must be traceable (created, updated, suppressed, failed)?
4. **Enables safe replay**: Failed changesets must be replayable without causing duplicates or data corruption?
5. **Keeps costs predictable**: For ~1K records/day, infrastructure cost should be minimal (~$5/month)?

---

## Executive Summary: Key Design Decisions

We propose a **Step Functions + Lambda + S3 architecture** with synchronous invocation, per-record error isolation, and 90-day audit retention. This approach balances **operational visibility**, **fault resilience**, and **simplicity**.

| Aspect | Choice | Primary Benefit |
|--------|--------|-----------------|
| **Orchestration** | AWS Step Functions | Configurable retries + rich execution history for audit |
| **Compute** | Lambda (ECR container) | Stateless, scales to 0, integrates with Step Functions |
| **Data Storage** | S3 NDJSON manifests (90-day TTL) | Cost-efficient batch writes + queryable via S3 Select |
| **Trigger** | EventBridge on adapter completion | Event-driven (not polling); decoupled from adapter |
| **Invocation** | Synchronous Lambda (via Step Function) | Natural backpressure; clear visibility on success/failure |
| **Error Handling** | Per-record isolation | Batch completes even if individual records fail |

**Expected outcomes:**
- Safe replay without data corruption (idempotent upserts via FOLIO HRIDs)
- Complete audit trail: every decision (create/update/suppress/skip) logged in S3 + CloudWatch
- Low operational overhead: ~$3–5/month for typical volume
- Clear mental model: no eventual consistency puzzles, ordered execution

---

## Architecture: Current Implementation

### System Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│ Axiell Adapter Platform (15-minute cadence)                             │
├──────────────────────────────────────────────────────────────────────────┤
│ • Writes changesets to Iceberg table (namespace, id, content, deleted)  │
│ • Emits EventBridge event: axiell.adapter.completed                    │
│   { changeset_ids: [...], job_id: "xyz", transformer_type: "axiell" }  │
└────────────────────┬─────────────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ EventBridge Rule: axiell-folio-sync-axiell-adapter-completed           │
│ • Pattern: source="axiell.adapter" + transformer_type="axiell"        │
│ • Target: Step Function (synchronous invocation)                      │
└────────────────────┬─────────────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ Step Function: axiell-folio-sync-sfn                                   │
│ • Passes event detail to Lambda                                        │
│ • Retry policy: max 3 attempts, exponential backoff (2s, 4s, 8s)      │
│ • Error handling: Catch-all → SyncFailed (terminal state)             │
│ • Execution history: CloudWatch Logs (30-day retention)               │
└────────────────────┬─────────────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ Lambda: axiell-folio-sync (ECR image)                                  │
│ • Timeout: 300s (5 min) — handles ~200 records with 3 API calls each │
│ • Memory: 1024 MB                                                     │
│                                                                        │
│ Execution Flow:                                                       │
│  1. Auth: Fetch OKAPI credentials from SSM, POST /authn/login        │
│  2. Scan: Query Iceberg for changesets (WHERE changeset_id IN [...]) │
│  3. Map & Validate: Apply YAML rules, build Instance/Holdings/Item  │
│  4. Upsert: For each record, POST/PUT to FOLIO (per-record errors)  │
│  5. Write Manifests: Flush to S3 NDJSON (success, errors, metadata) │
│                                                                        │
│ Environment Variables (injected by Terraform):                        │
│  • OKAPI_URL, OKAPI_TENANT, OKAPI_SECRET_PARAM                       │
│  • MANIFEST_S3_BUCKET, S3_TABLE_BUCKET_ARN, ICEBERG_TABLE_NAME      │
│  • AWS_REGION, DRY_RUN (override via event)                          │
└────────────────────┬─────────────────────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ S3: Manifest Storage (axiell-folio-sync-manifests-{account}-{region}) │
│                                                                        │
│ Files (per job_id):                                                   │
│  • {job_id}.ids.ndjson           — success records (5K/batch)        │
│  • {job_id}.ids.failures.ndjson  — error records (if any)            │
│  • {job_id}.manifest.json        — metadata summary                  │
│                                                                        │
│ Lifecycle: 90-day expiration (auto-delete old manifests)            │
│ Versioning: Enabled (audit trail for object changes)                │
│ Encryption: SSE-S3 (default)                                        │
└──────────────────────────────────────────────────────────────────────────┘
```

### 1. EventBridge Trigger

**Rule**: `axiell-folio-sync-axiell-adapter-completed`

**Event Pattern**:
```json
{
  "source": ["axiell.adapter"],
  "detail-type": ["axiell.adapter.completed"],
  "detail": {
    "transformer_type": ["axiell"]
  }
}
```

**Event Payload** (emitted by Axiell adapter):
```json
{
  "changeset_ids": ["axiell-cs-20260622-001", "axiell-cs-20260622-002"],
  "job_id": "adapter-job-xyz-12345",
  "transformer_type": "axiell",
  "dry_run": false,
  "sample_limit": null
}
```

**IAM Permissions**: `states:StartExecution` on Step Function ARN

---

### 2. Step Function State Machine

**Name**: `axiell-folio-sync-sfn`  
**Type**: STANDARD

**Flow**:
```
Input (from EventBridge)
  ↓
[Task] Invoke Lambda (pass event detail)
  ├─ Input path: $.detail
  ├─ Output: result JSON with counts, manifest URIs, errors
  │
  ├─ [Retry]
  │  • MaxAttempts: 3 (configurable)
  │  • BackoffRate: 2.0
  │  • IntervalSeconds: 2
  │
  └─ [Catch]
     • States.TaskFailed → SyncFailed (terminal)
     • Log to CloudWatch
  ↓
Output (Success) → SyncComplete
```

**Execution History**: Stored in CloudWatch Logs (`/aws/states/axiell-folio-sync-sfn`, 30-day retention)

**IAM Role Permissions**:
- `lambda:InvokeFunction` on sync Lambda ARN
- `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents` for CloudWatch

---

### 3. Lambda Function: axiell-folio-sync

**Docker Image**: ECR (`uk.ac.wellcome/axiell-folio-sync:TAG`)

**Execution Steps**:

#### Step 1: Authenticate with FOLIO
```
SSM Parameter Store (SecureString)
  Path: /axiell-folio-sync/okapi-creds
  Value: {"username": "service_account", "password": "..."}

POST /authn/login
  x-okapi-tenant: wellcome
  Body: credentials
  Response: x-okapi-token (valid 24h)
  → Reused for all subsequent API calls in this invocation
```

#### Step 2: Scan Iceberg Changesets
```
Query S3 Tables Iceberg catalog
  Bucket: {S3_TABLE_BUCKET_ARN}
  Table: {ICEBERG_TABLE_NAME} (e.g., default.axiell_changesets)
  
SELECT [namespace, id, content, changeset, last_modified, deleted]
WHERE changeset IN ({changeset_ids from event})

Schema:
  namespace        string    — e.g., "location", "item"
  id               string    — external identifier from Axiell
  content          string    — JSON-serialized record
  changeset        string    — changeset ID from adapter
  last_modified    timestamp — when record changed
  deleted          boolean   — true if marked deleted
```

#### Step 3: Map & Validate
```python
# Load YAML mapping rules (from mapping.yaml)
mapper = YamlMapper("mapping.yaml")

for row in iceberg_records:
    try:
        record = json.loads(row['content'])
        
        # Build Instance, Holdings, Item payloads
        instance_payload = mapper.build_instance_payload(record)
        holdings_payload = mapper.build_holdings_payload(record)
        item_payload = mapper.build_item_payload(record)
        
        # Validate required fields per FOLIO schema
        payloads.append({...})
    except MappingError as e:
        # Capture error, continue to next record
        errors.append({
            "source_id": row['id'],
            "type": "mapping",
            "detail": str(e)
        })
        continue
```

#### Step 4: Upsert to FOLIO (Per Record)
```
For each record:
  Execute: Instance → Holdings → Item (dependencies)
  
  Instance:
    If deleted=true:
      GET /inventory/instances/{instance_id}
      PUT with discoverySuppress=true
      Action: "suppress"
    Else:
      GET /inventory/instances?query=(hrid=={hrid})
      If exists: PUT (update)
      Else: POST (create)
      Action: "create" or "update"
  
  Holdings (if Instance succeeded):
    POST /holdings-storage/holdings (create linked to Instance)
    Action: "create"
  
  Item (if Holdings succeeded):
    POST /item-storage/items (create linked to Holdings)
    Action: "create"

Per-record error handling:
  • HTTP 4xx/5xx → captured, batch continues
  • All errors logged to CloudWatch AND accumulated
```

#### Step 5: Batch & Write Manifests
```python
# Success NDJSON (one record per line, 5K records per batch)
for i in range(0, len(success_results), 5000):
    batch = success_results[i:i+5000]
    ndjson_lines = [json.dumps(r) for r in batch]
    s3.put_object(
        Bucket=MANIFEST_S3_BUCKET,
        Key=f"manifests/{job_id}.ids.ndjson",
        Body="\n".join(ndjson_lines)
    )

# Error NDJSON (one error per line)
if errors:
    error_lines = [json.dumps(e) for e in errors]
    s3.put_object(
        Bucket=MANIFEST_S3_BUCKET,
        Key=f"manifests/{job_id}.ids.failures.ndjson",
        Body="\n".join(error_lines)
    )

# Metadata summary
metadata = {
    "job_id": job_id,
    "start_time": "2026-06-22T10:15:03Z",
    "end_time": "2026-06-22T10:15:45Z",
    "status": "SUCCESS|PARTIAL|FAILED",
    "counts": {
        "total": 247,
        "created": 10,
        "updated": 200,
        "suppressed": 25,
        "skipped": 12,
        "failed": 0
    },
    "success_manifest_uri": f"s3://{bucket}/manifests/{job_id}.ids.ndjson",
    "error_manifest_uri": f"s3://{bucket}/manifests/{job_id}.ids.failures.ndjson"
}
s3.put_object(
    Bucket=MANIFEST_S3_BUCKET,
    Key=f"manifests/{job_id}.manifest.json",
    Body=json.dumps(metadata, indent=2)
)

# CloudWatch Metrics
cloudwatch.put_metric_data(
    Namespace="AxiellFolioSync",
    MetricData=[
        {"MetricName": "RecordsCreated", "Value": metadata['counts']['created']},
        {"MetricName": "RecordsUpdated", "Value": metadata['counts']['updated']},
        {"MetricName": "RecordsSuppressed", "Value": metadata['counts']['suppressed']},
        {"MetricName": "RecordsFailed", "Value": metadata['counts']['failed']},
    ]
)

return metadata
```

---

### 4. S3 Manifest Storage

**Bucket**: `axiell-folio-sync-manifests-{account-id}-{region}`

**File Structure**:
```
manifests/
  ├─ adapter-job-xyz-20260622-10-15.ids.ndjson
  ├─ adapter-job-xyz-20260622-10-15.ids.failures.ndjson
  ├─ adapter-job-xyz-20260622-10-15.manifest.json
  ├─ adapter-job-xyz-20260622-10-30.ids.ndjson
  └─ ...
```

**Sample Success Record** (NDJSON):
```json
{
  "source_id": "location_item_123",
  "instance": {
    "action": "update",
    "id": "inst-abc-def",
    "hrid": "HRID-LOC-123"
  },
  "holdings": {
    "action": "create",
    "id": "hold-xyz-uvw"
  },
  "item": {
    "action": "create",
    "id": "item-001-002"
  },
  "errors": []
}
```

**Sample Error Record** (NDJSON):
```json
{
  "source_id": "location_item_456",
  "error": "Mapping error: required field 'barcode' missing",
  "detail": "YAML rule for barcode returned null",
  "type": "mapping"
}
```

**Lifecycle Policy**: 90-day expiration (auto-delete old manifests)

---

## Design Rationale: Why These Choices?

### Orchestration: Step Functions vs. Alternatives

| Approach | Pros | Cons | Cost/mo |
|----------|------|------|---------|
| **A: Direct Lambda** (EventBridge → Lambda, fire-and-forget) | Fewer services, lower overhead, fastest time-to-invocation | No built-in retry logic, no execution history, hard to extend, silent failures possible | ~$2 |
| **B: Step Functions + Lambda** ⭐ **CHOSEN** | Explicit retry policy + audit trail, easy to parallelize later, clear visibility into success/failure | Extra service, marginal latency added | ~$3–5 |
| **C: Async Queue** (EventBridge → SQS → Lambda workers) | Decouples producer/consumer, handles bursts, resilient to adapter restarts | Complex ordering semantics, harder to reason about, no clear success/failure signal, monitoring overhead | ~$10–15 |

**Why we chose B (Step Functions + Lambda):**

1. **Extension point for scale**: When volume grows beyond 500 records/event, we swap the Lambda invocation for a Step Function Map state (fan-out per changeset). Same manifest format, no breaking changes.

2. **Execution history = audit trail**: Every state transition is logged to CloudWatch. If a sync fails partway through, we know exactly where and why. No need to rebuild state from Lambda logs.

3. **Explicit retry policy**: Max attempts and backoff are declarative. Operations can tweak `max_retries` without code changes (configure in Step Function definition).

4. **Synchronous invocation provides backpressure**: Adapter waits for sync to complete → prevents queue buildup if FOLIO is slow. If sync times out, adapter knows to retry.

5. **Cost remains minimal**: At 1K records/day (~80 invocations), we're talking $0.50/month for Step Function state transitions. Not a material driver.

**Why not A (Direct Lambda)?**
- Silent failures: EventBridge doesn't tell us if the invocation succeeded or failed.
- No retry: If Lambda times out, there's no automatic retry. We'd have to implement our own (add complexity).
- No execution history: Debugging a failed sync means parsing Lambda logs. Step Function history is cleaner.

**Why not C (Async Queue)?**
- Ordering: SQS doesn't guarantee processing order within a batch. We'd need to handle out-of-order upserts or add logic to sort before processing.
- Complexity: Workers need to coordinate (who's processing which changeset?). Adds operational burden.
- Cost: For current volume, async queue is cheaper per invocation, but the monitoring overhead (error tracking, retry logic, dead-letter queue management) makes it not worth it.

---

### Storage: S3 NDJSON vs. Alternatives

| Approach | Pros | Cons | Cost/mo (90-day) |
|----------|------|------|------------------|
| **A: DynamoDB** (per-record writes, TTL) | Query-friendly, real-time dashboards possible, strong consistency | O(n) write cost, schema evolution painful, expensive for batches, not auditable | ~$20–50 |
| **B: S3 NDJSON** ⭐ **CHOSEN** | Batched writes (low cost), queryable (S3 Select), matches org patterns, audit via versioning, easy to compress/archive | Requires S3 Select for queries (not real-time), not ideal for high-cardinality point lookups | ~$1–2 |
| **C: Streaming** (Kinesis/Firehose → Parquet) | High throughput, good for ML pipelines, efficient compression | Overkill for current volume, adds infrastructure complexity, higher cost | ~$5–15 |

**Why we chose B (S3 NDJSON):**

1. **Cost scales with volume**: Per-record writes scale O(n). At 5K records/day, you'd pay for 5K DynamoDB writes. With S3 NDJSON, we batch-write every 5K records → 1 PUT per 5K records. Cost dominance flips at ~100 records/day (already exceeded).

2. **Matches existing patterns**: Axiell adapter platform already uses S3 for changesets. This keeps the operational model consistent (known backup, recovery, and query patterns).

3. **Queryable post-hoc**: S3 Select allows SQL-like queries without ETL:
   ```sql
   SELECT * FROM s3://bucket/manifest.ndjson WHERE errors > 0
   ```
   Takes ~500ms on 100 KB file. Good enough for operational investigation.

4. **Audit trail via versioning**: S3 versioning enabled → every write creates a new object version. If someone accidentally deletes a manifest, we can recover it. Metadata JSON tracks all historical jobs.

5. **Easy to compress/archive**: After 90 days, we can archive NDJSON to Glacier for long-term audit retention (pennies/month). DynamoDB has no cheap archive option.

**Why not A (DynamoDB)?**
- Per-record cost: 5K records/day = 5K write units (on-demand) = ~$2.50/day = ~$75/month. S3 is ~$0.05/month for the same data.
- Schema evolution: If we add a new field to the record (e.g., `retry_count`), DynamoDB requires a scan-and-rewrite. S3 NDJSON: just add the field to new records.
- Not suitable for audit: While DynamoDB TTL works, there's no clean way to query "what was deleted from this table last week?"

**Why not C (Streaming)?**
- Overkill: Typical changeset is 10–500 records. Kinesis + Firehose is designed for high-throughput (1000s records/sec). We'd be paying for infrastructure we don't use.
- Operational complexity: Firehose auto-flushes based on buffer size or timeout. Extra operational knowledge needed.

---

### Invocation Pattern: Synchronous vs. Asynchronous

| Approach | Pros | Cons |
|----------|------|------|
| **A: Async** (EventBridge → Lambda, fire-and-forget) | Decoupled, adapter doesn't wait, low latency | No backpressure; if adapter emits 10 events in quick succession, Lambda might queue up (can overwhelm FOLIO); no failure signal |
| **B: Synchronous** ⭐ **CHOSEN** | Backpressure (adapter waits), clear success/failure, enables replay on failure | Adapter must wait ~45 sec for sync to complete before next event; if FOLIO is slow, adapter is blocked |

**Why we chose B (Synchronous):**

1. **Natural backpressure**: If FOLIO is slow or unavailable, Step Function times out → adapter pauses before emitting next event. No need for queue management.

2. **Failure visibility**: If sync fails, EventBridge knows → can retry the same changeset. No silent failures.

3. **Replay support**: If sync fails partway (e.g., 100 of 200 records succeeded before timeout), we can:
   - Query S3 manifest to see which records failed
   - Fix the issue (e.g., restart FOLIO, fix mapping rule)
   - Re-trigger sync with same changeset_ids
   - Idempotent upserts (via FOLIO HRID lookup) prevent duplication

4. **Adapter is designed for it**: Axiell adapter runs on 15-min cycles. Waiting 45 sec for sync fits within the cadence.

**Why not A (Async)?**
- Queue buildup: If adapter emits 10 changesets in quick succession, and each sync takes 45 sec, we'd have a 7-minute backlog. Async doesn't naturally handle this (we'd need manual queue monitoring).
- Failure not visible: If a sync fails, the adapter doesn't know. No built-in retry or alerting.

---

### Error Handling: Per-Record Isolation

**Policy**: One bad record must not halt the entire batch.

**Error Levels**:

1. **Per-record errors** (non-blocking):
   - Mapping error (YAML validation fails): `{"source_id": "...", "type": "mapping", "detail": "..."}`
   - API error (FOLIO returns 4xx/5xx): `{"source_id": "...", "type": "api", "detail": "..."}`
   - Action: Log to S3 error manifest, continue to next record

2. **Batch-level errors** (blocking):
   - Auth failure (OKAPI login fails): Exception raised → Step Function retries up to `max_retries`
   - Iceberg connection failure: Exception raised → Step Function retries
   - S3 write failure: Exception raised → Step Function retries
   - Action: If retries exhausted → SyncFailed (terminal state), alert operations

**Observable via**:
- **CloudWatch Logs**: `/aws/lambda/axiell-folio-sync` (detailed per-record execution)
- **S3 Manifests**: `.ids.failures.ndjson` (queryable error list via S3 Select)
- **CloudWatch Metrics**: `RecordsFailed`, `RecordsCreated`, etc. (can alert on high failure rate)
- **Step Function History**: `/aws/states/axiell-folio-sync-sfn` (state transitions, retry events)

---

## Testing & Operations

### Test Levels

**Unit Tests** (in `tests/`):
- YAML mapper applies rules correctly to test records
- Upsert logic handles create/update/suppress/error scenarios
- Manifest NDJSON serialization and metadata structure

**Contract Tests** (against mock FOLIO):
- `dry_run=true`: Lambda computes changes but makes no writes
- Validates payload shape, required fields, API call sequence (no actual HTTP calls)

**Integration Tests** (against dev FOLIO):
- Create test changesets in Iceberg
- Trigger sync via EventBridge
- Verify records appear in FOLIO with expected fields
- Cleanup: suppress test records

**Smoke Tests** (pre-deployment):
- CloudFormation drift: no manual infrastructure changes
- Secrets: OKAPI credentials set in SSM
- EventBridge rule: active and routable to Step Function
- Lambda image: exists in ECR and is accessible
- Iceberg: S3 bucket and table readable

### Operational Runbooks

**Replay Failed Changesets**:
```
1. Identify failed changeset_id from CloudWatch or S3 manifest
2. Emit EventBridge event with same changeset_ids
3. Monitor S3 manifest and CloudWatch to confirm success
```

**Manual Inspection**:
```
# Query S3 manifest for records with errors
aws s3api select-object-content \
  --bucket axiell-folio-sync-manifests-123456-eu-west-1 \
  --key manifests/{job_id}.ids.failures.ndjson \
  --expression "SELECT * FROM s3object WHERE type = 'api'" \
  --expression-type SQL \
  --input-serialization '{"JSON": {}}' \
  --output-serialization '{"JSON": {}}' \
  output.json
```

**Emergency Shutdown**:
```
# Disable EventBridge rule (stops new syncs)
aws events disable-rule --name axiell-folio-sync-axiell-adapter-completed

# Monitor in-flight executions via Step Function console
# When all complete, investigate root cause
# Re-enable when ready
aws events enable-rule --name axiell-folio-sync-axiell-adapter-completed
```

---

## Future Scalability: Pipelining (When >500 Records/Event)

### Current Limits
- **Lambda timeout**: 300 seconds (5 min)
- **Typical performance**: ~200 records (with 3 API calls per record) in 45 sec
- **Token lifetime**: 24 hours (no refresh needed within 5-min window)

### Growth Trigger
When we observe >500 records per event (i.e., >80 records per changeset on average), parallelization becomes valuable:

**Baseline**: 1 Lambda processes 1 event → 200 records/45s → 1,600 records/hour
**Limit**: 5 min timeout → ~280 records/event max (not good)

**With parallelization**: 4 Lambda workers → 800 records/45s → 6,400 records/hour

### Proposed Pipelining Architecture

```
Step Function: Map state (fan-out per changeset)
  ├─ [Task] Fetch/cache OKAPI token (ElastiCache or in-memory)
  │
  ├─ [Map] Parallel workers (one per changeset)
  │  ├─ Worker 1: Process changeset 1 (reuse cached token)
  │  ├─ Worker 2: Process changeset 2
  │  ├─ Worker 3: Process changeset 3
  │  └─ [... N workers in parallel]
  │
  └─ [Join] Aggregate manifests
     • Collect all success/error manifests from workers
     • Write single metadata JSON (summarizing all workers)
     • Emit CloudWatch metrics (aggregated counts)
```

**Key Optimization: Token Caching**
- Current: Each Lambda auth calls OKAPI → O(N changesets) auth calls
- Future: Fetch token once, cache in ElastiCache or Lambda shared memory → O(1) auth calls

**Same Manifest Format**
- No breaking changes: Workers still write NDJSON to S3
- Single metadata JSON consolidates all results
- Queries remain unchanged (S3 Select can union multiple manifest files)

**Configuration Change**:
```terraform
# In Step Function definition, swap single Lambda invocation for Map state
# Lambda code changes: add token_cache parameter
# No changes to manifest format, API schema, or operational procedures
```

**Timeline**: Evaluate when we consistently see >500 records/event in production (track via CloudWatch metric `RecordsPerEvent`)

---

## Cost Analysis

### Current Volume: ~1,000 records/day

| Service | Operation | Qty/mo | Rate | Cost/mo |
|---------|-----------|--------|------|---------|
| Lambda | 80 invocations × 300s × 1 GB | 80 invocations | $0.0000167/GB-s | ~$1.20 |
| Step Functions | 80 state transitions | 80 transitions | $0.000025/transition | ~$0.02 |
| EventBridge | 80 events | 80 events | $1/M events | ~$0.00 |
| S3 (manifests) | ~80 objects written, 90-day retention | 80 objects + storage | $0.023/K objects + $0.023/GB/mo | ~$1.50 |
| CloudWatch Logs | ~80 × 5 KB = 400 KB/month | 400 KB ingested | $0.50/GB ingested | ~$0.20 |
| **Total** | | | | **~$3–5** |

### Future Volume: ~10,000 records/day (10x growth)

| Service | Cost/mo |
|---------|---------|
| Lambda | ~$12 (10x invocations, 4x longer processing time due to size) |
| Step Functions | ~$0.20 (10x transitions) |
| S3 | ~$15 (more objects, higher storage) |
| CloudWatch Logs | ~$2 (10x log volume) |
| **Total** | **~$30–40** |

**Note**: If >50 changesets/event, pipelining becomes cost-effective. With parallelization, Lambda compute cost would drop (faster wall-clock time → fewer seconds billed), but Step Function costs would increase (more state transitions per Map worker).

---

## Assumptions & Constraints

- **FOLIO HRID requirement**: Records must have a stable, unique HRID per type (Instance, Holdings, Item) for idempotent upserts. Axiell must provide this in mapping.yaml.
- **No real-time requirements**: 15-minute cadence is acceptable. If sub-minute sync becomes required, architecture must change (streaming Kinesis, real-time database).
- **FOLIO API stability**: Assumes FOLIO API is available and stable. If FOLIO is down for hours, sync manifests will accumulate (90-day retention allows manual replay after recovery).
- **Axiell stability**: Assumes Axiell adapter completes consistently. If adapter fails, no changeset is emitted → no sync triggered (not our problem, but should monitor).

---

## Next Steps

1. **Approval**: Review this RFC and confirm architectural choices align with Wellcome Collection platform strategy.
2. **Implementation**: Create Terraform modules, Lambda container image, Step Function definition, unit/integration tests.
3. **Deployment**: Stage in dev FOLIO → test end-to-end → deploy to prod with runbooks.
4. **Monitoring**: Set up CloudWatch dashboards, alarms on failure rate, manifest size growth.
5. **Feedback loop**: Monitor production for 1–2 months, adjust retry policy and timeout if needed.

---

## References

- **Axiell Adapter Platform**: Emits changesets to Iceberg; documentation in location-movement-control-docs
- **FOLIO API**: https://api-wellcome.folio.ebsco.com (OKAPI auth required)
- **AWS S3 Tables**: Iceberg catalog on S3; managed via Terraform
- **YAML Mapping Rules**: mapping.yaml (stored in Lambda container or S3)
