"""
ID Minter implementation supporting:
- Lookup of existing canonical IDs
- Predecessor inheritance for migrated records
- Pre-generated ID pool claiming
- Idempotent writes for concurrency
"""

import random
import string
from typing import Optional, Tuple, Callable


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
    
    def mint_id(
        self, 
        ontology_type: str, 
        source_system: str, 
        source_id: str,
        predecessor: Optional[Tuple[str, str]] = None
    ) -> str:
        """
        Mint or lookup a canonical ID for a source identifier.
        
        Args:
            ontology_type: e.g., 'Work', 'Image'
            source_system: e.g., 'sierra-system-number', 'axiell-collections-id'
            source_id: The identifier value in the source system
            predecessor: Optional (source_system, source_id) to inherit canonical ID from
        
        Returns:
            The canonical ID (existing or newly minted)
        
        Raises:
            ValueError: If predecessor is specified but not found
            RuntimeError: If free ID pool is exhausted
        """
        cursor = self._get_cursor()
        
        # Step 1: Check if source identifier already has a canonical ID
        cursor.execute("""
            SELECT CanonicalId FROM identifiers 
            WHERE OntologyType = %s AND SourceSystem = %s AND SourceId = %s
        """, (ontology_type, source_system, source_id))
        
        result = cursor.fetchone()
        if result:
            return result['CanonicalId']
        
        # Step 2: If predecessor specified, inherit its canonical ID
        if predecessor:
            pred_system, pred_id = predecessor
            cursor.execute("""
                SELECT CanonicalId FROM identifiers 
                WHERE OntologyType = %s AND SourceSystem = %s AND SourceId = %s
            """, (ontology_type, pred_system, pred_id))
            
            pred_result = cursor.fetchone()
            if pred_result:
                canonical_id = pred_result['CanonicalId']
                # Insert with idempotent write
                cursor.execute("""
                    INSERT INTO identifiers (OntologyType, SourceSystem, SourceId, CanonicalId)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE CanonicalId = CanonicalId
                """, (ontology_type, source_system, source_id, canonical_id))
                self._commit()
                return canonical_id
            else:
                raise ValueError(f"Predecessor not found: {pred_system}/{pred_id}")
        
        # Step 3: Claim a free ID from the pool
        cursor.execute("""
            SELECT CanonicalId FROM canonical_ids 
            WHERE Status = 'free' 
            LIMIT 1 
            FOR UPDATE
        """)
        
        free_id_result = cursor.fetchone()
        if free_id_result:
            canonical_id = free_id_result['CanonicalId']
            
            # Mark as assigned
            cursor.execute("""
                UPDATE canonical_ids SET Status = 'assigned' WHERE CanonicalId = %s
            """, (canonical_id,))
            
            # Insert with idempotent write
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
            
            if actual_id != canonical_id:
                # Another process won, return our ID to the pool
                cursor.execute("""
                    UPDATE canonical_ids SET Status = 'free' WHERE CanonicalId = %s
                """, (canonical_id,))
                canonical_id = actual_id
            
            self._commit()
            return canonical_id
        
        # Step 4: Fallback - generate new ID (pool exhausted)
        raise RuntimeError("Free ID pool exhausted - implement fallback generation")
    
    def close(self):
        """Close the database connection."""
        if self.conn and self.conn.open:
            self.conn.close()
            self.conn = None
