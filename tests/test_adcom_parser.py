"""Tests for Adcom v1.0 specification parser."""

import pytest
from pathlib import Path

from tools.spec_parser.adcom_parser import AdcomParser, parse_adcom_spec
from tools.spec_parser.md_tables import ObjectDef, FieldDef


def test_adcom_parser_initialization():
    """Test Adcom parser initialization."""
    test_content = "# Test\n## Object: TestObject\n"
    parser = AdcomParser(test_content)
    assert parser.content == test_content
    assert isinstance(parser.enums, dict)


def test_parse_adcom_spec():
    """Test parsing complete Adcom specification."""
    objects, enums = parse_adcom_spec()

    # Verify we got expected number of objects
    assert len(objects) >= 15, f"Expected at least 15 objects, got {len(objects)}"

    # Verify we got enums
    assert len(enums) >= 5, f"Expected at least 5 enums, got {len(enums)}"

    # Check for key objects
    object_names = [obj.name for obj in objects]
    assert "Ad" in object_names
    assert "Display" in object_names
    assert "Video" in object_names
    assert "Native" in object_names
    assert "Asset" in object_names
    assert "Publisher" in object_names
    assert "Device" in object_names


def test_parse_media_objects():
    """Test parsing of media objects."""
    objects, _ = parse_adcom_spec()
    object_dict = {obj.name: obj for obj in objects}

    # Check Ad object
    assert "Ad" in object_dict
    ad = object_dict["Ad"]
    assert len(ad.fields) >= 10
    field_names = [f.attribute for f in ad.fields]
    assert "id" in field_names
    assert "adomain" in field_names

    # Check required fields
    id_field = next(f for f in ad.fields if f.attribute == "id")
    assert id_field.required

    # Check Display object
    assert "Display" in object_dict
    display = object_dict["Display"]
    assert len(display.fields) >= 5

    # Check Video object
    assert "Video" in object_dict
    video = object_dict["Video"]
    assert len(video.fields) >= 5


def test_parse_asset_objects():
    """Test parsing of asset objects."""
    objects, _ = parse_adcom_spec()
    object_dict = {obj.name: obj for obj in objects}

    # Check Asset object
    assert "Asset" in object_dict

    # Check specific asset types
    assert "LinkAsset" in object_dict
    assert "ImageAsset" in object_dict
    assert "VideoAsset" in object_dict
    assert "TitleAsset" in object_dict
    assert "DataAsset" in object_dict

    # Verify LinkAsset has url field
    link_asset = object_dict["LinkAsset"]
    field_names = [f.attribute for f in link_asset.fields]
    assert "url" in field_names

    # Verify ImageAsset has url field
    image_asset = object_dict["ImageAsset"]
    field_names = [f.attribute for f in image_asset.fields]
    assert "url" in field_names


def test_parse_context_objects():
    """Test parsing of context objects."""
    objects, _ = parse_adcom_spec()
    object_dict = {obj.name: obj for obj in objects}

    # Check Publisher object
    assert "Publisher" in object_dict
    publisher = object_dict["Publisher"]
    field_names = [f.attribute for f in publisher.fields]
    assert "id" in field_names or "name" in field_names

    # Check Content object
    assert "Content" in object_dict
    content = object_dict["Content"]
    assert len(content.fields) >= 5

    # Check User object
    assert "User" in object_dict

    # Check Device object
    assert "Device" in object_dict
    device = object_dict["Device"]
    assert len(device.fields) >= 10

    # Check Geo object
    assert "Geo" in object_dict
    geo = object_dict["Geo"]
    field_names = [f.attribute for f in geo.fields]
    assert "lat" in field_names or "lon" in field_names


def test_parse_enums():
    """Test parsing of enum definitions."""
    _, enums = parse_adcom_spec()

    # Check for key enums
    enum_names = list(enums.keys())

    # API Frameworks
    assert "APIFrameworks" in enum_names
    api_frameworks = enums["APIFrameworks"]
    assert len(api_frameworks) >= 5

    # Device Types
    assert "DeviceTypes" in enum_names
    device_types = enums["DeviceTypes"]
    assert len(device_types) >= 5

    # Check enum format (value, description) tuples
    for enum_name, values in enums.items():
        assert len(values) > 0, f"Enum {enum_name} has no values"
        for value, description in values:
            assert value, f"Empty value in {enum_name}"
            assert description, f"Empty description in {enum_name}"


def test_parse_table_body():
    """Test parsing of Adcom table format."""
    parser = AdcomParser("")

    # Test Adcom table format (rows start with |)
    body = """| id* | Unique identifier | string |
| name | Object name | string |
| type | Object type | integer |"""

    fields = parser.parse_table_body(body)

    assert len(fields) == 3

    # Check first field
    assert fields[0].attribute == "id"
    assert fields[0].required is True
    assert "identifier" in fields[0].description.lower()
    assert fields[0].type_raw == "string"

    # Check second field
    assert fields[1].attribute == "name"
    assert fields[1].required is False
    assert fields[1].type_raw == "string"


def test_parse_enum_body():
    """Test parsing of enum table body."""
    parser = AdcomParser("")

    body = """| 1 | First value |
| 2 | Second value |
| 3 | Third value |"""

    values = parser.parse_enum_body(body)

    assert len(values) == 3
    assert values[0] == ("1", "First value")
    assert values[1] == ("2", "Second value")
    assert values[2] == ("3", "Third value")


def test_object_descriptions():
    """Test that objects have descriptions extracted."""
    objects, _ = parse_adcom_spec()

    # At least some objects should have descriptions
    objects_with_desc = [obj for obj in objects if obj.description]
    assert len(objects_with_desc) > 0

    # Check a specific object
    ad_obj = next((obj for obj in objects if obj.name == "Ad"), None)
    assert ad_obj is not None
    assert ad_obj.section == "adcom"


def test_field_types():
    """Test that field types are correctly extracted."""
    objects, _ = parse_adcom_spec()
    object_dict = {obj.name: obj for obj in objects}

    # Check various field types
    ad = object_dict["Ad"]

    # String field
    id_field = next((f for f in ad.fields if f.attribute == "id"), None)
    assert id_field is not None
    assert "string" in id_field.type_raw.lower()

    # Array field
    adomain_field = next((f for f in ad.fields if f.attribute == "adomain"), None)
    if adomain_field:
        assert "array" in adomain_field.type_raw.lower()

    # Integer field
    device = object_dict["Device"]
    int_fields = [f for f in device.fields if "integer" in f.type_raw.lower()]
    assert len(int_fields) > 0


@pytest.mark.parametrize(
    "object_name,min_fields",
    [
        ("Ad", 10),
        ("Display", 5),
        ("Video", 5),
        ("Audio", 5),
        ("Native", 3),
        ("Asset", 3),
        ("Publisher", 3),
        ("Device", 10),
        ("Geo", 5),
    ],
)
def test_object_field_counts(object_name, min_fields):
    """Test that objects have minimum expected field counts."""
    objects, _ = parse_adcom_spec()
    object_dict = {obj.name: obj for obj in objects}

    assert object_name in object_dict
    obj = object_dict[object_name]
    assert (
        len(obj.fields) >= min_fields
    ), f"{object_name} should have at least {min_fields} fields, got {len(obj.fields)}"


def test_spec_file_not_found():
    """Test error handling when spec file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        parse_adcom_spec(Path("/nonexistent/path/spec.md"))
