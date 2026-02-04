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
        IDs should be processed individually via mint_id().
        
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
        
        This combines batch lookup with individual minting for efficiency:
        1. Batch lookup all source IDs (single query)
        2. For missing IDs with predecessors: lookup predecessor, inherit ID
        3. For missing IDs without predecessors: mint new IDs individually
        
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
        
        result = {}
        source_ids = [req[0] for req in requests]
        predecessors = {req[0]: req[1] for req in requests if req[1] is not None}
        
        # Step 1: Batch lookup all source IDs
        found = self.lookup_ids(source_ids)
        result.update(found)
        
        # Step 2: Process missing IDs individually
        missing = [sid for sid in source_ids if sid not in found]
        
        for source_key in missing:
            ontology_type, source_system, source_id = source_key
            predecessor = predecessors.get(source_key)
            
            canonical_id = self.mint_id(
                ontology_type=ontology_type,
                source_system=source_system,
                source_id=source_id,
                predecessor=predecessor
            )
            result[source_key] = canonical_id
        
        return result

    def mint_id(
        self, 
        ontology_type: str, 
        source_system: str, 
        source_id: str,
        predecessor: Optional[SourceId] = None
    ) -> str:
        """
        Mint or lookup a canonical ID for a source identifier.
        
        Args:
            ontology_type: e.g., 'Work', 'Image'
            source_system: e.g., 'sierra-system-number', 'axiell-collections-id'
            source_id: The identifier value in the source system
            predecessor: Optional (ontology_type, source_system, source_id) to inherit canonical ID from
        
        Returns:
            The canonical ID (existing or newly minted)
        
        Raises:
            ValueError: If predecessor is specified but not found
            RuntimeError: If free ID pool is exhausted
        """
        cursor = self._get_cursor()
        
        # Step 1: Query for source ID and predecessor in one round-trip
        if predecessor:
            pred_ontology, pred_system, pred_id = predecessor
            cursor.execute("""
                SELECT 
                    CanonicalId,
                    CASE 
                        WHEN OntologyType = %s AND SourceSystem = %s AND SourceId = %s THEN 'new'
                        ELSE 'predecessor'
                    END AS MatchType
                FROM identifiers
                WHERE (
                    (OntologyType = %s AND SourceSystem = %s AND SourceId = %s)
                    OR 
                    (OntologyType = %s AND SourceSystem = %s AND SourceId = %s)
                  )
            """, (ontology_type, source_system, source_id,
                  ontology_type, source_system, source_id, 
                  pred_ontology, pred_system, pred_id))
            
            results = cursor.fetchall()
            
            # Step 2: Evaluate query results
            new_match = next((r for r in results if r['MatchType'] == 'new'), None)
            pred_match = next((r for r in results if r['MatchType'] == 'predecessor'), None)
            
            # 2a: If new source ID found, return its CanonicalId
            if new_match:
                return new_match['CanonicalId']
            
            # 2b: If only predecessor found, insert new source ID with predecessor's CanonicalId
            if pred_match:
                canonical_id = pred_match['CanonicalId']
                cursor.execute("""
                    INSERT INTO identifiers (OntologyType, SourceSystem, SourceId, CanonicalId)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE CanonicalId = CanonicalId
                """, (ontology_type, source_system, source_id, canonical_id))
                self._commit()
                return canonical_id
            
            # 2c: Neither found - raise exception (predecessor should already exist)
            raise ValueError(f"Predecessor not found: {pred_ontology}/{pred_system}/{pred_id}")
        
        else:
            # No predecessor - simple lookup
            cursor.execute("""
                SELECT CanonicalId FROM identifiers 
                WHERE OntologyType = %s AND SourceSystem = %s AND SourceId = %s
            """, (ontology_type, source_system, source_id))
            
            result = cursor.fetchone()
            if result:
                return result['CanonicalId']
        
        # Step 3: Claim a free ID from the pool (SKIP LOCKED for concurrency)
        cursor.execute("""
            SELECT CanonicalId FROM canonical_ids 
            WHERE Status = 'free' 
            LIMIT 1 
            FOR UPDATE SKIP LOCKED
        """)
        
        free_id_result = cursor.fetchone()
        if free_id_result:
            canonical_id = free_id_result['CanonicalId']
            
            # Insert with idempotent write (row is locked, defer status update)
            cursor.execute("""
                INSERT INTO identifiers (OntologyType, SourceSystem, SourceId, CanonicalId)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE CanonicalId = CanonicalId
            """, (ontology_type, source_system, source_id, canonical_id))
            
            # Check if we actually inserted (or another process won)
            cursor.execute("""
                SELECT CanonicalId FROM identifiers 
                WHERE OntologyType = %s AND SourceSystem = %s AND SourceId = %s
            """, (ontology_type, source_system, source_id))
            
            actual_result = cursor.fetchone()
            actual_id = actual_result['CanonicalId']
            
            if actual_id == canonical_id:
                # We won - mark our ID as assigned
                cursor.execute("""
                    UPDATE canonical_ids SET Status = 'assigned' WHERE CanonicalId = %s
                """, (canonical_id,))
            # If we lost, our locked row stays 'free' - released on commit
            
            self._commit()
            return actual_id
        
        # Step 4: No free IDs available - fail fast
        raise RuntimeError("Free ID pool exhausted - trigger pre-generation job and retry")
    
    def close(self):
        """Close the database connection."""
        if self.conn and self.conn.open:
            self.conn.close()
            self.conn = None
