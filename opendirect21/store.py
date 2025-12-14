"""In-memory data store for development and testing.

For production, replace with PostgreSQL or other database.
"""

import uuid
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Entity:
    """Base entity with metadata."""

    data: Dict[str, Any]
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class InMemoryStore:
    """Thread-safe in-memory data store.

    Usage:
        store = InMemoryStore()
        user = await store.create('users', {'name': 'John'})
        users = await store.list('users')
        updated = await store.update('users', user['id'], {'name': 'Jane'})
        await store.delete('users', user['id'])
    """

    def __init__(self):
        """Initialize empty store."""
        self.data: Dict[str, Dict[str, Entity]] = {}

    async def list(
        self, entity_type: str, skip: int = 0, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List all entities of a type with pagination."""
        if entity_type not in self.data:
            return []

        items = list(self.data[entity_type].values())
        return [e.data for e in items[skip : skip + limit]]

    async def get(self, entity_type: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get specific entity by ID."""
        if entity_type not in self.data or entity_id not in self.data[entity_type]:
            return None

        return self.data[entity_type][entity_id].data

    async def create(
        self, entity_type: str, entity_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create new entity with generated UUID."""
        entity_id = entity_data.get("id") or str(uuid.uuid4())
        entity_data["id"] = entity_id

        if entity_type not in self.data:
            self.data[entity_type] = {}

        entity = Entity(data=entity_data)
        self.data[entity_type][entity_id] = entity

        return entity.data

    async def update(
        self, entity_type: str, entity_id: str, updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update existing entity (merge updates)."""
        if entity_type not in self.data or entity_id not in self.data[entity_type]:
            return None

        entity = self.data[entity_type][entity_id]
        entity.data.update(updates)
        entity.updated_at = datetime.utcnow()

        return entity.data

    async def delete(self, entity_type: str, entity_id: str) -> bool:
        """Delete entity by ID."""
        if entity_type not in self.data or entity_id not in self.data[entity_type]:
            return False

        del self.data[entity_type][entity_id]
        return True

    async def delete_all(self, entity_type: str) -> int:
        """Delete all entities of a type."""
        if entity_type not in self.data:
            return 0

        count = len(self.data[entity_type])
        self.data[entity_type] = {}
        return count

    async def count(self, entity_type: str) -> int:
        """Count entities of a type."""
        return len(self.data.get(entity_type, {}))

    async def exists(self, entity_type: str, entity_id: str) -> bool:
        """Check if entity exists."""
        return entity_type in self.data and entity_id in self.data[entity_type]
