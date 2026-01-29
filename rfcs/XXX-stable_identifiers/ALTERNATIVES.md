# Alternative solutions considered

This document describes alternative approaches that were considered for maintaining stable public catalogue identifiers during the CALM/Sierra to Axiell Collections/Folio migration.

For background on the problem, see:
- [Discovery / Proposal for stable identifiers following Calm &amp; Sierra migrations](https://github.com/wellcomecollection/platform/issues/6246)
- [Allow idminter to connect multiple source identifiers to one canonical identifier](https://github.com/wellcomecollection/platform/issues/6258)

## Summary of approaches

| Approach | Description | Outcome |
|----------|-------------|---------|
| **Transformer ID swap** | Swap old/new IDs in transformer | Rejected — adds complexity, misleading source labels |
| **Many-to-one in ID Minter** | Allow multiple source IDs per canonical ID | **Selected** — see [PROPOSAL.md](PROPOSAL.md) |
| **Database swap** | Replace old IDs with new IDs directly in database | Rejected — creates orphaned IDs, doesn't preserve history |
| **Runtime ID matching** | Minter identifies original source at runtime | Rejected — combines downsides of other approaches |

## Transformer ID swap

**Approach:** Handle identifier continuity in the transformer rather than the ID Minter. When a record in the new system (Axiell/Folio) has been migrated from the old system (Sierra/CALM), the transformer would:

1. Detect the old identifier stored as an alternative identifier in the new record
2. Swap the old and new identifiers, so the record continues to use its Sierra/CALM source identifier downstream
3. Pass the new Axiell/Folio identifier as an alternative identifier instead

**Example:**
- Adapter output: `axiell-collections-id/12345` (new identifier)
- Transformer output: `sierra-system-number/b1161044x` (old identifier, swapped to primary position)
- Alternative identifier: `axiell-collections-id/12345`

**Concerns identified:**

1. **Misleading source system labels**: Records coming from Folio would have Sierra B numbers and be labelled as `sierra-system-number` in their source identifier, which is confusing and dishonest about the record's actual source.

2. **Read-before-update required**: Handling deletions and updates would require reading the existing record to find the ID to propagate. This breaks the pure function nature of the transformer, impacting performance.

3. **Risk of drift**: The old identifier field in the new system is not a controlled identifier. It could be edited or removed at any point, potentially orphaning records downstream.

4. **Multiple potential old identifiers**: A former Sierra record might also contain a CALM ID. The transformer would need logic to identify which old ID is the "correct" one to use.

5. **Multiplies transformer concerns**: Keeping permanent information about ID history in the transformer is undesirable as it adds complexity to what should be a straightforward transformation.

**Outcome:** Rejected. While this approach would work, it adds significant complexity to the transformer and results in records that misrepresent their source system. The ID Minter is a more appropriate place to handle identifier mapping.

## Many-to-one in ID Minter (selected approach)

**Approach:** Remove the strict 1:1 relationship between source identifiers and canonical IDs in the ID Minter. Allow multiple source identifiers to map to the same canonical ID through explicit predecessor relationships.

See [PROPOSAL.md](PROPOSAL.md) for the complete specification including:
- Database schema changes
- Minting logic with predecessor inheritance  
- Concurrency handling
- Migration steps

**Why this approach was selected:**

1. **Records are honest about their source**: New records identify as coming from Axiell/Folio, not Sierra/CALM.

2. **No transformer changes for ID handling**: Transformers emit a predecessor field but don't need read-before-update logic.

3. **Supports future migrations**: The schema handles additional source system migrations without modification.

4. **Preserves history**: Both old and new source identifiers are recorded, with timestamps showing the relationship.

5. **Matches merge behaviour**: METS records continue to merge correctly because canonical IDs are preserved.

## Database swap

**Approach:** Make no application changes. Instead, directly modify the ID Minter database before the migration:

1. Generate a list of mappings between old (Sierra/CALM) and new (Axiell/Folio) source identifiers
2. Update the database to replace all old source identifiers with new source identifiers
3. The ID Minter continues operating with its 1:1 constraint, but now uses new identifiers

**Concerns identified:**

1. **Orphaned canonical IDs**: If we later want to retain the old identifiers (e.g. as alternative identifiers on works), we'd create pointless new canonical IDs for them. This essentially moves the problem rather than solving it.

2. **Loss of history**: The database would no longer record that a canonical ID was originally minted for a Sierra/CALM record.

3. **All-or-nothing migration**: Requires complete identifier mapping before switchover. Any records missed would get new canonical IDs.

4. **References to old identifiers break**: Other systems (like METS) that reference Sierra B numbers would no longer find matches unless we also update those references.

**Outcome:** Rejected. This approach "works" in the narrow sense of preserving canonical IDs, but creates problems for maintaining alternative identifiers and loses valuable history about record provenance. It was considered as a fallback option if the many-to-one approach proved too complex.

## Runtime ID matching in Minter

**Approach:** Allow a 1:many relationship between canonical IDs and source IDs, with the ID Minter determining the correct mapping at runtime:

1. When a new record arrives, the minter examines alternative identifiers in the record
2. If an alternative identifier matches an existing source ID in the database, use that canonical ID
3. Otherwise mint a new canonical ID

**Concerns identified:**

1. **Minter needs source system knowledge**: The minter would need to understand which alternative identifier to look up based on the source system, making it tightly coupled to transformer output format.

2. **Duplicate handling**: What happens if a record has multiple potential matches? Or if the alternative identifier value changes?

3. **Combines downsides**: Has the complexity of multiple approaches without their benefits — still requires alternative identifier handling in transformers, plus schema changes in the minter.

**Outcome:** Rejected. This approach was identified as having "all the downsides of both ideas" (transformer approach and many-to-one approach) without clear advantages. The cleaner solution is to handle predecessor relationships explicitly.

## Why many-to-one was selected

The key insight from the discussion was that **whatever approach we take, we probably want to remove the 1:1 relationship** in the ID Minter. This is because:

1. We want to retain old identifiers (Sierra/CALM) as alternative identifiers on works, at least in the short term, since there will be references elsewhere (including physical pieces of paper).

2. If we retain the old identifiers as alternatives but don't update the ID Minter, we'd create new canonical IDs for them — essentially recreating the problem.

3. The ID Minter is the correct place to manage identifier mappings, not the transformer.

The many-to-one approach with predecessor relationships cleanly solves these issues while maintaining clear data provenance and supporting future migrations.
