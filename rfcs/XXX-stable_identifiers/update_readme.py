#!/usr/bin/env python3
"""Script to update the README.md file with new identifier usage section."""

import re

# Read the file
with open('/Users/kennyr/workspace/docs/rfcs/XXX-stable_identifiers/README.md', 'r') as f:
    content = f.read()

# Find the section to replace using a regex pattern
# Pattern matches from "### Identifier usage in catalogue pipeline steps" to just before "#### If we make no changes"
pattern = r'(### Identifier usage in catalogue pipeline steps\n).*?(#### If we make no changes)'

new_section = '''### Identifier usage in catalogue pipeline steps

This section describes how identifiers are used and transformed at each step of the catalogue pipeline.

```mermaid
flowchart LR
    subgraph Adapter
        A_in[/"adapter-id/123"/]
        A_out[/"source-type/xyz"/]
    end

    subgraph Transformer
        T_in[/"source-type/xyz"/]
        T_out["source-type/xyz<br/>+ merge candidates<br/>(source-type/abc, ...)"]
    end

    subgraph ID Minter
        M_in["source-type/xyz<br/>+ merge candidates"]
        M_out["<b>cat-id</b> ← source-type/xyz<br/>+ merge candidates with cat-ids"]
    end

    subgraph Matcher
        Match_in["cat-id + merge candidate cat-ids"]
        Match_out["graph of connected cat-ids"]
    end

    subgraph Merger
        Merge_in["cat-ids in graph<br/>+ source-type for precedence"]
        Merge_out["merged work with<br/>canonical cat-id"]
    end

    A_out --> T_in
    T_out --> M_in
    M_out --> Match_in
    Match_out --> Merge_in
```

#### Adapter

The adapter uses **adapter identifiers** internally to track records in its datastore. These are often the same as source identifiers, but may differ depending on the source system. For example, the Sierra adapter uses the record's internal database ID as the adapter identifier. The adapter outputs records tagged with a **source identifier** (e.g. `sierra-system-number/b1161044x`).

#### Transformer

The transformer receives records identified by their **source identifier**. It extracts structured data from the source record and outputs a transformed work document. Crucially, the transformer also identifies **merge candidates** — other records that should be merged with this one. Merge candidates are expressed as source identifiers (e.g. `miro-image-number/V0012345`).

The transformer outputs:
- The work's **source identifier** (the primary identity of this record)
- A list of **merge candidate source identifiers** (records to be merged with this work)

#### ID Minter

The ID Minter receives transformed works with source identifiers and merge candidates. For each source identifier (both the work's own identifier and all merge candidates), it either:
- Looks up an existing **public catalogue identifier** from the ID Registry, or
- Mints a new catalogue identifier if one doesn't exist

The minter maintains a one-to-one mapping between source identifiers and catalogue identifiers in the ID Registry (Aurora database). After processing, each source identifier on the document is enriched with its corresponding catalogue identifier.

The ID Minter outputs:
- The work with its **catalogue identifier** (mapped from its source identifier)
- Merge candidates enriched with their **catalogue identifiers**

#### Matcher

The matcher receives works with catalogue identifiers and uses the merge candidates to build a graph of connected works. It maintains an adjacency list (in DynamoDB) keyed by catalogue identifier, which tracks which catalogue identifiers should be merged together.

When a work arrives, the matcher:
1. Looks up existing connections for its catalogue identifier
2. Adds connections for any new merge candidate catalogue identifiers
3. Produces a subgraph of all transitively connected catalogue identifiers

The matcher operates entirely on **catalogue identifiers** — source identifiers are not used at this step.

#### Merger

The merger receives a set of connected catalogue identifiers from the matcher and retrieves the full work documents for each. It then applies merge rules to combine these works into a single merged work.

Importantly, the merger uses **source identifier types** (not the identifiers themselves) to determine precedence rules. For example, a Sierra record might take precedence over a METS record for certain fields. The merge rules are expressed in terms of source system types (e.g. "sierra-system-number" vs "mets-file").

The merger outputs:
- A single merged work with one canonical **catalogue identifier**
- The merged work contains the combined data from all source records

#### Summary of identifier usage

| Step | Input identifiers | Output identifiers | Notes |
|------|-------------------|-------------------|-------|
| Adapter | Adapter IDs (internal) | Source IDs | Converts internal IDs to source system IDs |
| Transformer | Source IDs | Source IDs + merge candidate source IDs | Identifies related records for merging |
| ID Minter | Source IDs | Catalogue IDs | Maps source → catalogue IDs (1:1) |
| Matcher | Catalogue IDs | Graph of catalogue IDs | Builds merge graph using catalogue IDs only |
| Merger | Catalogue IDs + source types | Single catalogue ID | Uses source types for precedence rules |

#### If we make no changes'''

# Perform the replacement
new_content, count = re.subn(pattern, new_section, content, flags=re.DOTALL)

if count > 0:
    with open('/Users/kennyr/workspace/docs/rfcs/XXX-stable_identifiers/README.md', 'w') as f:
        f.write(new_content)
    print(f"Successfully replaced {count} occurrence(s)")
else:
    print("Pattern not found - no changes made")
