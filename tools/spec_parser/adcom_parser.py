"""Adcom v1.0 specification parser for extracting object definitions."""

import re
from pathlib import Path
from typing import List, Dict, Tuple

from tools.spec_parser.md_tables import MarkdownTableParser, ObjectDef, FieldDef


class AdcomParser(MarkdownTableParser):
    """Parser specialized for Adcom v1.0 specification."""

    # Regex for Adcom object definitions
    OBJECT_RE = re.compile(r"^## Object: (?P<name>\w+)\s*$", re.MULTILINE)

    # Override table regex with flexible separator matching
    TABLE_RE = re.compile(
        r"\| ?Attribute ?\| ?Description ?\| ?Type ?\|\n\|[-]+\|[-]+\|[-]+\|\n(?P<body>.*?)(?=\n\n|^##|\Z)",
        re.MULTILINE | re.DOTALL,
    )

    # Regex for enum/list sections
    LIST_RE = re.compile(r"^### List: (?P<name>[\w\s]+)\s*$", re.MULTILINE)

    # Regex for enum tables
    ENUM_TABLE_RE = re.compile(
        r"\| ?Value ?\| ?Description ?\|\n\|[-]+\|[-]+\|\n(?P<body>.*?)(?=\n\n|^###|^##|\Z)",
        re.MULTILINE | re.DOTALL,
    )

    def __init__(self, markdown_content: str):
        """Initialize Adcom parser.

        Args:
            markdown_content: Raw markdown content from Adcom spec
        """
        super().__init__(markdown_content)
        self.enums: Dict[str, List[Tuple[str, str]]] = {}

    def parse_table_body(self, body: str) -> List[FieldDef]:
        """Parse table body for Adcom format (rows start with |).

        Args:
            body: Table body content

        Returns:
            List of FieldDef objects
        """
        fields: List[FieldDef] = []

        for line in body.split("\n"):
            line = line.strip()
            # Skip empty lines, but process lines starting with |
            if not line:
                continue

            # Split by | and filter empty parts
            parts = [p.strip() for p in line.split("|")]
            # Filter out empty strings from split
            parts = [p for p in parts if p]

            if len(parts) < 3:
                continue

            try:
                attr, desc, typ = parts[0], parts[1], parts[2]
            except IndexError:
                continue

            if not attr or not typ:
                continue

            # Check if required (marked with *)
            required = attr.endswith("*") or "required" in desc.lower()
            attr = attr.rstrip("*").strip()

            fields.append(
                FieldDef(
                    attribute=attr,
                    description=desc.strip(),
                    type_raw=typ.strip(),
                    required=required,
                )
            )

        return fields

    def parse_enum_body(self, body: str) -> List[Tuple[str, str]]:
        """Parse enum table body.

        Args:
            body: Table body with value/description pairs

        Returns:
            List of (key, description) tuples
        """
        enum_values = []

        for line in body.split("\n"):
            line = line.strip()
            if not line or not line.startswith("|"):
                continue

            # Split by | and filter
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 3:
                continue

            try:
                value, description = parts[1], parts[2]
                if value and description:
                    # Use the value as key
                    enum_values.append((value, description))
            except (IndexError, ValueError):
                continue

        return enum_values

    def extract_enums(self) -> Dict[str, List[Tuple[str, str]]]:
        """Extract all enum definitions from List sections.

        Returns:
            Dictionary mapping enum name to list of (value, description) tuples
        """
        enums = {}

        for list_match in self.LIST_RE.finditer(self.content):
            enum_name = list_match.group("name").strip()
            start = list_match.end()

            # Find the enum table after this list heading
            chunk = self.content[start : start + 2000]  # Look ahead 2000 chars
            table_match = self.ENUM_TABLE_RE.search(chunk)

            if not table_match:
                continue

            body = table_match.group("body").strip()
            values = self.parse_enum_body(body)

            if values:
                # Create a clean enum name (no spaces, CamelCase)
                clean_name = enum_name.replace(" ", "")
                enums[clean_name] = values

        return enums

    def extract_objects(self) -> List[ObjectDef]:
        """Extract all object definitions from Adcom spec.

        Returns:
            List of ObjectDef instances
        """
        objects = []

        # Find all object definitions
        for obj_match in self.OBJECT_RE.finditer(self.content):
            name = obj_match.group("name")
            start = obj_match.end()

            # Find next object or section to delimit this object
            next_match = self.OBJECT_RE.search(self.content, start + 1)
            if next_match:
                end = next_match.start()
            else:
                # Look for enum section
                list_match = self.LIST_RE.search(self.content, start + 1)
                end = list_match.start() if list_match else len(self.content)

            chunk = self.content[start:end]

            # Find the attributes table
            table_match = self.TABLE_RE.search(chunk)
            if not table_match:
                continue

            body = table_match.group("body").strip()
            fields = self.parse_table_body(body)

            if fields:
                # Extract description from text before table
                desc_text = chunk[: table_match.start()].strip()
                # Get first paragraph as description
                desc_lines = [
                    line.strip() for line in desc_text.split("\n") if line.strip()
                ]
                description = desc_lines[0] if desc_lines else None

                objects.append(
                    ObjectDef(name=name, fields=fields, section="adcom", description=description)
                )

        return objects

    def parse(self) -> Tuple[List[ObjectDef], Dict[str, List[Tuple[str, str]]]]:
        """Parse Adcom specification for objects and enums.

        Returns:
            Tuple of (objects, enums) where:
            - objects: List of ObjectDef instances
            - enums: Dict mapping enum name to (value, description) tuples
        """
        objects = self.extract_objects()
        enums = self.extract_enums()
        return objects, enums


def parse_adcom_spec(spec_path: Path = None) -> Tuple[List[ObjectDef], Dict[str, List[Tuple[str, str]]]]:
    """Parse Adcom specification file.

    Args:
        spec_path: Path to AdCOM specification markdown file.
                   Defaults to tools/spec_parser/AdCOM_v1.0_FINAL.md

    Returns:
        Tuple of (objects, enums)
    """
    if spec_path is None:
        spec_path = Path(__file__).parent / "AdCOM_v1.0_FINAL.md"

    if not spec_path.exists():
        raise FileNotFoundError(f"Adcom specification not found: {spec_path}")

    content = spec_path.read_text(encoding="utf-8")
    parser = AdcomParser(content)
    return parser.parse()


if __name__ == "__main__":
    # Test the parser
    objects, enums = parse_adcom_spec()

    print(f"✅ Parsed {len(objects)} objects from Adcom spec:")
    for obj in objects:
        print(f"  - {obj.name}: {len(obj.fields)} fields")

    print(f"\n✅ Parsed {len(enums)} enum definitions:")
    for enum_name, values in enums.items():
        print(f"  - {enum_name}: {len(values)} values")
