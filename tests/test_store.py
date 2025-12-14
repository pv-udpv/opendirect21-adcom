"""Tests for data store."""

from opendirect21.store import InMemoryStore


def test_create_entity(store: InMemoryStore):
    """Test creating entity."""
    data = {"name": "Test Organization", "type": "Publisher"}
    result = store.create("organizations", data)

    assert result["id"] is not None
    assert result["name"] == "Test Organization"
    assert result["type"] == "Publisher"


def test_get_entity(store: InMemoryStore):
    """Test getting entity by ID."""
    data = {"name": "Test", "type": "Publisher"}
    created = store.create("organizations", data)
    entity_id = created["id"]

    retrieved = store.get("organizations", entity_id)
    assert retrieved is not None
    assert retrieved["id"] == entity_id
    assert retrieved["name"] == "Test"


def test_list_entities(store: InMemoryStore):
    """Test listing entities."""
    store.create("organizations", {"name": "Org 1"})
    store.create("organizations", {"name": "Org 2"})
    store.create("organizations", {"name": "Org 3"})

    items = store.list("organizations")
    assert len(items) == 3


def test_update_entity(store: InMemoryStore):
    """Test updating entity."""
    data = {"name": "Original", "type": "Publisher"}
    created = store.create("organizations", data)
    entity_id = created["id"]

    updated = store.update("organizations", entity_id, {"name": "Updated"})
    assert updated is not None
    assert updated["name"] == "Updated"
    assert updated["type"] == "Publisher"


def test_delete_entity(store: InMemoryStore):
    """Test deleting entity."""
    data = {"name": "To Delete"}
    created = store.create("organizations", data)
    entity_id = created["id"]

    deleted = store.delete("organizations", entity_id)
    assert deleted is True

    retrieved = store.get("organizations", entity_id)
    assert retrieved is None


def test_pagination(store: InMemoryStore):
    """Test pagination in list."""
    for i in range(10):
        store.create("organizations", {"name": f"Org {i}"})

    page1 = store.list("organizations", skip=0, limit=3)
    page2 = store.list("organizations", skip=3, limit=3)

    assert len(page1) == 3
    assert len(page2) == 3
    assert page1[0]["name"] != page2[0]["name"]


def test_count_entities(store: InMemoryStore):
    """Test counting entities."""
    store.create("organizations", {"name": "Org 1"})
    store.create("organizations", {"name": "Org 2"})

    count = store.count("organizations")
    assert count == 2


def test_exists_entity(store: InMemoryStore):
    """Test checking entity existence."""
    data = {"name": "Test"}
    created = store.create("organizations", data)
    entity_id = created["id"]

    exists = store.exists("organizations", entity_id)
    assert exists is True

    not_exists = store.exists("organizations", "non-existent-id")
    assert not_exists is False
