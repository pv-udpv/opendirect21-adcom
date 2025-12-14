"""In-memory data store for development and testing.

For production, replace with PostgreSQL or other database.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class Entity:
    """Base entity with metadata."""

    data: dict[str, Any]
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class InMemoryStore:
    """Thread-safe in-memory data store.

    Usage:
        store = get_store()
        user = store.create('users', {'name': 'John'})
        users = store.list('users')
        updated = store.update('users', user['id'], {'name': 'Jane'})
        store.delete('users', user['id'])
    """

    def __init__(self):
        """Initialize empty store."""
        self.data: dict[str, dict[str, Entity]] = {}

    def list(self, entity_type: str, skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """List all entities of a type with pagination."""
        if entity_type not in self.data:
            return []

        items = list(self.data[entity_type].values())
        return [e.data for e in items[skip : skip + limit]]

    def get(self, entity_type: str, entity_id: str) -> Optional[dict[str, Any]]:
        """Get specific entity by ID."""
        if entity_type not in self.data or entity_id not in self.data[entity_type]:
            return None

        return self.data[entity_type][entity_id].data

    def create(self, entity_type: str, entity_data: dict[str, Any]) -> dict[str, Any]:
        """Create new entity with generated UUID."""
        entity_id = entity_data.get("id") or str(uuid.uuid4())
        entity_data["id"] = entity_id

        if entity_type not in self.data:
            self.data[entity_type] = {}

        entity = Entity(data=entity_data)
        self.data[entity_type][entity_id] = entity

        return entity.data

    def update(
        self, entity_type: str, entity_id: str, updates: dict[str, Any]
    ) -> Optional[dict[str, Any]]:
        """Update existing entity (merge updates)."""
        if entity_type not in self.data or entity_id not in self.data[entity_type]:
            return None

        entity = self.data[entity_type][entity_id]
        entity.data.update(updates)
        entity.updated_at = datetime.utcnow()

        return entity.data

    def delete(self, entity_type: str, entity_id: str) -> bool:
        """Delete entity by ID."""
        if entity_type not in self.data or entity_id not in self.data[entity_type]:
            return False

        del self.data[entity_type][entity_id]
        return True

    def delete_all(self, entity_type: str) -> int:
        """Delete all entities of a type."""
        if entity_type not in self.data:
            return 0

        count = len(self.data[entity_type])
        self.data[entity_type] = {}
        return count

    def count(self, entity_type: str) -> int:
        """Count entities of a type."""
        return len(self.data.get(entity_type, {}))

    def exists(self, entity_type: str, entity_id: str) -> bool:
        """Check if entity exists."""
        return entity_type in self.data and entity_id in self.data[entity_type]


# Global store instance
_store: Optional[InMemoryStore] = None


def get_store() -> InMemoryStore:
    """Get the global store instance."""
    global _store
    if _store is None:
        _store = InMemoryStore()
    return _store
