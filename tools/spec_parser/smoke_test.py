"""Smoke tests for parser verification."""

from pathlib import Path
from tools.spec_parser.md_tables import MarkdownTableParser


def test_markdown_parser():
    """Test markdown table parser."""
    # Create test markdown
    test_md = """
## Object: Organization

|Attribute|Description|Type|
|--|--|--|
|id*|Organization ID|string (36)|
|name*|Organization name|string (255)|
|type*|Organization type|enum (Publisher, Buyer)|
|contact|Contact info|Contact object|

## Object: Account

|Attribute|Description|Type|
|--|--|--|
|id*|Account ID|string (36)|
|name*|Account name|string (255)|
|status|Account status|enum (Active, Inactive)|
"""

    parser = MarkdownTableParser(test_md)
    objects = parser.extract_objects()

    assert len(objects) >= 2, f"Expected at least 2 objects, got {len(objects)}"

    org = next((o for o in objects if o.name == "Organization"), None)
    assert org is not None, "Organization object not found"
    assert len(org.fields) >= 4, f"Expected at least 4 fields in Organization"

    # Check field names
    field_names = [f.attribute for f in org.fields]
    assert "id" in field_names
    assert "name" in field_names
    assert "type" in field_names

    # Check required marking
    id_field = next(f for f in org.fields if f.attribute == "id")
    assert id_field.required, "id field should be required"

    print("✅ Markdown parser test passed")
    print(f"Found {len(objects)} objects")
    for obj in objects:
        print(f"  - {obj.name}: {len(obj.fields)} fields")


if __name__ == "__main__":
    test_markdown_parser()
    print("\n✅ All smoke tests passed!")
