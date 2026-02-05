"""
ID Minter implementation supporting:
- Batch lookup of existing canonical IDs
- Single-record minting for new IDs
- Predecessor inheritance for migrated records
- Pre-generated ID pool claiming
- Idempotent writes for concurrency
"""

import random
import string
from typing import Optional, Tuple, Callable, Dict, List

# Type alias for source identifier: (ontology_type, source_system, source_id)
SourceId = Tuple[str, str, str]


def generate_canonical_id() -> str:
    """
    Generate a canonical identifier compatible with XML rules.
    
    - Must be 8 characters long
    - Uses characters a-z and 2-9 (excludes confusing: 'o', 'i', 'l', '1')
    - First character must be a letter (XML identifiers cannot start with numbers)
    
    This yields an ID space of approximately 0.6 trillion unique identifiers:
    23 (first chars) × 31^7 (remaining chars) = 619,629,091,463
    """
    length = 8
    forbidden = {'o', 'i', 'l', '1'}
    numbers = set(str(n) for n in range(1, 10))
    letters = set(string.ascii_lowercase)
    
    allowed_chars = list((numbers | letters) - forbidden)
    first_chars = list(letters - forbidden)
    
    first = random.choice(first_chars)
    rest = ''.join(random.choice(allowed_chars) for _ in range(length - 1))
    
    return first + rest


class IDMinter:
    """
    ID Minter that supports predecessor inheritance for stable identifiers
    during source system migrations.
    """
    
    def __init__(self, get_connection_fn: Callable):
        """
        Initialize the ID Minter.
        
        Args:
            get_connection_fn: A callable that returns a database connection
                              with DictCursor configured.
        """
        self.conn = None
        self.get_connection = get_connection_fn
    
    def _get_cursor(self):
        if self.conn is None or not self.conn.open:
            self.conn = self.get_connection()
        return self.conn.cursor()
    
    def _commit(self):
        if self.conn:
            self.conn.commit()
    
    def lookup_ids(
        self,
        source_ids: List[SourceId]
    ) -> Dict[SourceId, str]:
        """
        Batch lookup of canonical IDs for multiple source identifiers.
        
        This is the optimized path for the common case where records already
        exist in the database. Returns only the IDs that were found — missing
        IDs should be processed via mint_ids().
        
        Args:
            source_ids: List of (ontology_type, source_system, source_id) tuples
        
        Returns:
            Dict mapping (ontology_type, source_system, source_id) -> canonical_id
            for all source IDs that were found. Missing IDs are not included.
        
        Example:
            >>> minter.lookup_ids([
            ...     ('Work', 'sierra-system-number', 'b1234'),
            ...     ('Image', 'mets-image', 'xyz'),
            ...     ('Work', 'axiell-collections-id', 'new-record')  # doesn't exist
            ... ])
            {
                ('Work', 'sierra-system-number', 'b1234'): 'abc12345',
                ('Image', 'mets-image', 'xyz'): 'def67890'
            }
            # ('Work', 'axiell-collections-id', 'new-record') not in result — needs minting
        """
        if not source_ids:
            return {}
        
        cursor = self._get_cursor()
        
        # Build query with IN clause for batch lookup of mixed ontology types
        # Using tuple comparison: (OntologyType, SourceSystem, SourceId) IN ((?, ?, ?), ...)
        placeholders = ', '.join(['(%s, %s, %s)'] * len(source_ids))
        params = []
        for ontology_type, source_system, source_id in source_ids:
            params.extend([ontology_type, source_system, source_id])
        
        cursor.execute(f"""
            SELECT OntologyType, SourceSystem, SourceId, CanonicalId 
            FROM identifiers 
            WHERE (OntologyType, SourceSystem, SourceId) IN ({placeholders})
        """, params)
        
        results = cursor.fetchall()
        
        return {
            (row['OntologyType'], row['SourceSystem'], row['SourceId']): row['CanonicalId']
            for row in results
        }
    
    def mint_ids(
        self,
        requests: List[Tuple[SourceId, Optional[SourceId]]]
    ) -> Dict[SourceId, str]:
        """
        Batch mint/lookup canonical IDs for multiple source identifiers.
        
        This is the optimized batch path that minimizes database round-trips:
        1. Batch lookup all source IDs + predecessor IDs (single query)
        2. Fail fast if any predecessors are missing
        3. Batch INSERT for predecessor inheritance cases
        4. Batch claim free IDs from pool (FOR UPDATE SKIP LOCKED)
        5. Batch INSERT for new ID cases
        6. Verify which IDs were actually assigned (race detection)
        7. Mark only used IDs as 'assigned', commit transaction
        
        All operations occur within a single transaction for atomicity.
        
        Args:
            requests: List of (source_id, predecessor_or_none) tuples where:
                     - source_id is (ontology_type, source_system, source_id)
                     - predecessor is (ontology_type, source_system, source_id) or None
        
        Returns:
            Dict mapping source_id -> canonical_id for all inputs
        
        Raises:
            ValueError: If a predecessor is specified but not found
            RuntimeError: If free ID pool is exhausted
        
        Example:
            >>> minter.mint_ids([
            ...     (('Work', 'axiell', 'AC-123'), ('Work', 'sierra', 'b1234')),  # with predecessor
            ...     (('Image', 'mets', 'xyz'), None),  # no predecessor
            ... ])
        """
        if not requests:
            return {}
        
        cursor = self._get_cursor()
        result: Dict[SourceId, str] = {}
        
        # Build lookup sets
        source_ids = [req[0] for req in requests]
        predecessors = {req[0]: req[1] for req in requests if req[1] is not None}
        predecessor_ids = list(predecessors.values())
        
        # Step 1: Batch lookup all source IDs + predecessor IDs together
        all_ids_to_lookup = list(set(source_ids + predecessor_ids))
        found = self.lookup_ids(all_ids_to_lookup)
        
        # Populate result with already-existing source IDs
        for sid in source_ids:
            if sid in found:
                result[sid] = found[sid]
        
        # Step 2: Categorize missing source IDs
        missing = [sid for sid in source_ids if sid not in found]
        needs_inheritance: List[Tuple[SourceId, str]] = []  # (source_id, canonical_id)
        needs_new_id: List[SourceId] = []
        
        for sid in missing:
            pred = predecessors.get(sid)
            if pred:
                if pred not in found:
                    raise ValueError(f"Predecessor not found: {pred[0]}/{pred[1]}/{pred[2]}")
                needs_inheritance.append((sid, found[pred]))
            else:
                needs_new_id.append(sid)
        
        # Step 3: Batch INSERT for predecessor inheritance
        if needs_inheritance:
            for source_key, canonical_id in needs_inheritance:
                ont, sys, sid = source_key
                cursor.execute("""
                    INSERT INTO identifiers (OntologyType, SourceSystem, SourceId, CanonicalId)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE CanonicalId = CanonicalId
                """, (ont, sys, sid, canonical_id))
                result[source_key] = canonical_id
        
        # Step 4: Claim free IDs from pool for new records
        if needs_new_id:
            num_needed = len(needs_new_id)
            cursor.execute(f"""
                SELECT CanonicalId FROM canonical_ids 
                WHERE Status = 'free' 
                LIMIT {num_needed}
                FOR UPDATE SKIP LOCKED
            """)
            
            free_ids = [row['CanonicalId'] for row in cursor.fetchall()]
            if len(free_ids) < num_needed:
                raise RuntimeError(
                    f"Free ID pool exhausted - needed {num_needed}, got {len(free_ids)}. "
                    "Trigger pre-generation job and retry."
                )
            
            # Step 5: Batch INSERT for new IDs
            claimed_mapping: Dict[SourceId, str] = {}
            for source_key, canonical_id in zip(needs_new_id, free_ids):
                ont, sys, sid = source_key
                cursor.execute("""
                    INSERT INTO identifiers (OntologyType, SourceSystem, SourceId, CanonicalId)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE CanonicalId = CanonicalId
                """, (ont, sys, sid, canonical_id))
                claimed_mapping[source_key] = canonical_id
            
            # Step 6: Verify which IDs were actually assigned (race detection)
            actual = self.lookup_ids(needs_new_id)
            
            # Step 7: Mark only used IDs as 'assigned'
            used_canonical_ids = set()
            for source_key in needs_new_id:
                actual_canonical = actual.get(source_key)
                if actual_canonical:
                    result[source_key] = actual_canonical
                    # Only mark as assigned if we won the race (our claimed ID was used)
                    if actual_canonical == claimed_mapping.get(source_key):
                        used_canonical_ids.add(actual_canonical)
            
            if used_canonical_ids:
                placeholders = ', '.join(['%s'] * len(used_canonical_ids))
                cursor.execute(f"""
                    UPDATE canonical_ids SET Status = 'assigned' 
                    WHERE CanonicalId IN ({placeholders})
                """, list(used_canonical_ids))
        
        self._commit()
        return result
    
    def close(self):
        """Close the database connection."""
        if self.conn and self.conn.open:
            self.conn.close()
            self.conn = None
