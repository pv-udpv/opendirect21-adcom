"""Tests for markdown table parser."""

import pytest
from tools.spec_parser.md_tables import MarkdownTableParser, ObjectDef, FieldDef


def test_parse_simple_table():
    """Test parsing a simple markdown table."""
    markdown = """
## Object: TestObject

|Attribute|Description|Type|
|--|--|--|
|id*|Unique identifier|string (36)|
|name*|Object name|string (255)|
|active|Is active|boolean|
"""
    parser = MarkdownTableParser(markdown)
    objects = parser.extract_objects()
    
    assert len(objects) == 1
    obj = objects[0]
    assert obj.name == "TestObject"
    assert len(obj.fields) == 3
    
    # Check required fields
    assert obj.fields[0].attribute == "id"
    assert obj.fields[0].required is True
    assert obj.fields[0].type_raw == "string (36)"
    
    assert obj.fields[1].attribute == "name"
    assert obj.fields[1].required is True
    
    assert obj.fields[2].attribute == "active"
    assert obj.fields[2].required is False


def test_parse_multiple_objects():
    """Test parsing multiple objects."""
    markdown = """
## Object: Organization

|Attribute|Description|Type|
|--|--|--|
|id*|Organization ID|string|
|name*|Organization name|string|

## Object: Account

|Attribute|Description|Type|
|--|--|--|
|id*|Account ID|string|
|orgId*|Organization ID|string|
"""
    parser = MarkdownTableParser(markdown)
    objects = parser.extract_objects()
    
    assert len(objects) == 2
    assert objects[0].name == "Organization"
    assert objects[1].name == "Account"
    assert len(objects[0].fields) == 2
    assert len(objects[1].fields) == 2


def test_parse_enum_types():
    """Test parsing enum types."""
    markdown = """
## Object: Product

|Attribute|Description|Type|
|--|--|--|
|status*|Current status|enum (Active, Inactive, Pending)|
|type|Product type|enum (Display, Video)|
"""
    parser = MarkdownTableParser(markdown)
    objects = parser.extract_objects()
    
    assert len(objects) == 1
    obj = objects[0]
    
    status_field = next(f for f in obj.fields if f.attribute == "status")
    assert "enum" in status_field.type_raw.lower()
    assert "Active" in status_field.type_raw
    assert status_field.required is True


def test_parse_array_types():
    """Test parsing array types."""
    markdown = """
## Object: Organization

|Attribute|Description|Type|
|--|--|--|
|contacts|Contact list|Contact[] array|
|categories|Category list|string array|
"""
    parser = MarkdownTableParser(markdown)
    objects = parser.extract_objects()
    
    obj = objects[0]
    contacts = next(f for f in obj.fields if f.attribute == "contacts")
    assert "array" in contacts.type_raw.lower() or "[]" in contacts.type_raw


def test_parse_nested_object_types():
    """Test parsing nested object references."""
    markdown = """
## Object: Order

|Attribute|Description|Type|
|--|--|--|
|account|Account information|Account object|
|brand|Brand info|AdvertiserBrand object|
"""
    parser = MarkdownTableParser(markdown)
    objects = parser.extract_objects()
    
    obj = objects[0]
    account = next(f for f in obj.fields if f.attribute == "account")
    assert "object" in account.type_raw.lower()
    assert "Account" in account.type_raw


def test_required_field_detection():
    """Test detection of required fields."""
    markdown = """
## Object: Test

|Attribute|Description|Type|
|--|--|--|
|id*|Required with asterisk|string|
|name|Optional field|string|
|email*|Required field|string|
"""
    parser = MarkdownTableParser(markdown)
    objects = parser.extract_objects()
    
    obj = objects[0]
    id_field = next(f for f in obj.fields if f.attribute == "id")
    name_field = next(f for f in obj.fields if f.attribute == "name")
    email_field = next(f for f in obj.fields if f.attribute == "email")
    
    assert id_field.required is True
    assert name_field.required is False
    assert email_field.required is True


def test_empty_table():
    """Test handling of empty or malformed tables."""
    markdown = """
## Object: Empty

|Attribute|Description|Type|
|--|--|--|
"""
    parser = MarkdownTableParser(markdown)
    objects = parser.extract_objects()
    
    # Should either skip or return object with no fields
    if len(objects) > 0:
        assert len(objects[0].fields) == 0


def test_get_enum_values():
    """Test extracting enum values."""
    parser = MarkdownTableParser("")
    
    # Test parentheses format
    values = parser.get_enum_values("enum (Active, Inactive, Pending)")
    assert len(values) >= 3
    
    # Test without parentheses
    values2 = parser.get_enum_values("Active, Inactive")
    assert len(values2) >= 2


def test_object_def_repr():
    """Test ObjectDef repr."""
    fields = [
        FieldDef("id", "ID", "string", required=True),
        FieldDef("name", "Name", "string", required=False),
    ]
    obj = ObjectDef("Test", fields)
    
    repr_str = repr(obj)
    assert "Test" in repr_str
    assert "2 fields" in repr_str


def test_field_def_repr():
    """Test FieldDef repr."""
    field = FieldDef("id", "ID field", "string", required=True)
    
    repr_str = repr(field)
    assert "id" in repr_str
    assert "*" in repr_str  # Required marker
    
    field2 = FieldDef("name", "Name field", "string", required=False)
    repr_str2 = repr(field2)
    assert "*" not in repr_str2


def test_table_at_end_of_document():
    """Test parsing table at the end of document (no double newline)."""
    markdown = """
## Object: LastObject

|Attribute|Description|Type|
|--|--|--|
|id*|Identifier|string|
|value|Some value|integer|"""
    
    parser = MarkdownTableParser(markdown)
    objects = parser.extract_objects()
    
    assert len(objects) == 1
    assert objects[0].name == "LastObject"
    assert len(objects[0].fields) == 2
