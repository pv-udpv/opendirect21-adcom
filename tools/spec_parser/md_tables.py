"""Markdown table parser for extracting object definitions from specifications."""

import re
from dataclasses import dataclass
from typing import List, Iterator, Tuple, Optional


@dataclass
class FieldDef:
    """Field definition from specification table."""

    attribute: str
    description: str
    type_raw: str
    required: bool = False

    def __repr__(self) -> str:
        req_mark = "*" if self.required else ""
        return f"FieldDef({self.attribute}{req_mark}: {self.type_raw})"


@dataclass
class ObjectDef:
    """Object definition from specification."""

    name: str
    fields: List[FieldDef]
    section: Optional[str] = None
    description: Optional[str] = None

    def __repr__(self) -> str:
        return f"ObjectDef({self.name}, {len(self.fields)} fields)"


class MarkdownTableParser:
    """Parser for OpenDirect/Adcom markdown specifications."""

    # Regex to find object definitions
    OBJECT_RE = re.compile(r"^## Object: (?P<name>\w+)\s*$", re.MULTILINE)
    OBJECT_ALT_RE = re.compile(r"^### (?P<name>\w+)\s*$", re.MULTILINE)

    # Regex to find table with attributes
    TABLE_RE = re.compile(
        r"\|Attribute\|Description\|Type\|\n\|--\|--\|--\|\n(?P<body>.*?)(?=\n\n|^##|\Z)",
        re.MULTILINE | re.DOTALL,
    )

    def __init__(self, markdown_content: str):
        """Initialize parser with markdown content.
        
        Args:
            markdown_content: Raw markdown file content
        """
        self.content = markdown_content
        self.objects: List[ObjectDef] = []

    def parse_table_body(self, body: str) -> List[FieldDef]:
        """Parse table body and extract field definitions.
        
        Args:
            body: Table body content between header and next section
            
        Returns:
            List of FieldDef objects
        """
        fields: List[FieldDef] = []

        for line in body.split("\n"):
            line = line.strip()
            if not line:
                continue

            # Skip separator lines (e.g., |--|--|--|)
            if line.replace("|", "").replace("-", "").replace(" ", "") == "":
                continue

            # Split by | and strip only spaces (keep * for required detection)
            parts = [p.strip() for p in line.split("|")]
            if len(parts) < 4:
                continue

            try:
                attr, desc, typ = parts[1], parts[2], parts[3]
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

    def extract_objects(self) -> List[ObjectDef]:
        """Extract all objects from markdown.
        
        Returns:
            List of ObjectDef objects parsed from specification
        """
        objects = []

        # Try primary pattern (## Object: Name)
        for obj_match in self.OBJECT_RE.finditer(self.content):
            name = obj_match.group("name")
            start = obj_match.end()
            chunk = self.content[start:]
            table_match = self.TABLE_RE.search(chunk)

            if not table_match:
                continue

            body = table_match.group("body").strip()
            fields = self.parse_table_body(body)

            if fields:
                objects.append(ObjectDef(name=name, fields=fields))

        return objects

    def get_enum_values(self, text: str) -> List[Tuple[str, str]]:
        """Extract enum values from text section.
        
        Args:
            text: Text containing enum values like "A, B, C" or "(A|B|C)"
            
        Returns:
            List of (key, value) tuples
        """
        # Try parentheses format: enum (A, B, C)
        match = re.search(r"\((.*?)\)", text)
        if match:
            values = [v.strip() for v in match.group(1).split(",")]
            return [(v.upper().replace(" ", "_"), v) for v in values]

        # Try plain comma-separated
        values = [v.strip() for v in text.split(",")]
        if len(values) > 1:
            return [(v.upper().replace(" ", "_"), v) for v in values]

        return []
