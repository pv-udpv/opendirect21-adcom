"""Generate Pydantic models from Adcom specification."""

import re
from pathlib import Path
from typing import List, Dict, Tuple, Set
from datetime import datetime

from tools.spec_parser.adcom_parser import parse_adcom_spec
from tools.spec_parser.md_tables import ObjectDef, FieldDef


class AdcomTypeMapper:
    """Maps Adcom specification types to Python types."""

    @staticmethod
    def map_type(spec_type: str, known_objects: Set[str]) -> Tuple[str, bool]:
        """Map spec type to Python type.

        Args:
            spec_type: Type from specification
            known_objects: Set of known object names for reference resolution

        Returns:
            (python_type, is_optional)
        """
        spec_type = spec_type.strip()

        # Handle optional
        is_optional = "optional" in spec_type.lower()
        spec_type = spec_type.replace("optional", "").strip()

        # Handle arrays - "array of X"
        if "array of" in spec_type.lower():
            base_type = spec_type.lower().replace("array of", "").strip()
            inner_type, _ = AdcomTypeMapper.map_type(base_type, known_objects)
            return f"List[{inner_type}]", is_optional

        # Handle object references (e.g., "Display object", "LinkAsset object")
        # Sort by length descending to match longer names first (e.g., TitleAsset before Asset)
        for obj_name in sorted(known_objects, key=len, reverse=True):
            # Check for exact match with word boundaries
            pattern = r'\b' + re.escape(obj_name.lower()) + r'\b'
            if re.search(pattern, spec_type.lower()) and "object" in spec_type.lower():
                # Forward reference for self-referential types
                return f'"{obj_name}"', is_optional

        # Primitive type mapping
        type_map = {
            "string": "str",
            "integer": "int",
            "int": "int",
            "number": "float",
            "float": "float",
            "double": "float",
            "boolean": "bool",
            "bool": "bool",
            "object": "Dict[str, Any]",
            "datetime": "datetime",
            "date-time": "datetime",
        }

        spec_lower = spec_type.lower()
        for key, value in type_map.items():
            if key in spec_lower:
                return value, is_optional

        # Default to str for unknown types
        return "str", is_optional


class AdcomModelGenerator:
    """Generate Pydantic models for Adcom specification."""

    def __init__(self, output_dir: Path = None):
        """Initialize generator.

        Args:
            output_dir: Directory to write generated models
        """
        self.output_dir = output_dir or Path("opendirect21/models/generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_enum_code(self, enum_name: str, values: List[Tuple[str, str]]) -> str:
        """Generate Python code for an enum.

        Args:
            enum_name: Enum class name
            values: List of (value, description) tuples

        Returns:
            Generated Python code
        """
        lines = []
        lines.append(f"class {enum_name}(str, Enum):")
        lines.append(f'    """{enum_name} enum values."""')
        lines.append("")

        for value, description in values:
            # Create a valid Python identifier
            member_name = f"VALUE_{value}".replace(" ", "_").replace("-", "_").upper()
            # Clean up the member name
            member_name = re.sub(r"[^\w]", "_", member_name)
            lines.append(f'    {member_name} = "{value}"  # {description}')

        return "\n".join(lines)

    def generate_model_code(
        self, obj_def: ObjectDef, known_objects: Set[str], enums: Set[str]
    ) -> str:
        """Generate Python code for a Pydantic model.

        Args:
            obj_def: Object definition
            known_objects: Set of known object names
            enums: Set of known enum names

        Returns:
            Generated Python code
        """
        lines = []
        lines.append(f"class {obj_def.name}(BaseModel):")

        # Docstring
        if obj_def.description:
            lines.append(f'    """{obj_def.description}"""')
        else:
            lines.append(f'    """{obj_def.name} model from Adcom specification."""')

        lines.append("")
        lines.append("    model_config = ConfigDict(extra='allow')")
        lines.append("")

        if not obj_def.fields:
            lines.append("    pass")
        else:
            for field in obj_def.fields:
                # Map type
                py_type, is_optional = AdcomTypeMapper.map_type(
                    field.type_raw, known_objects
                )

                # Determine if field should be optional
                if is_optional or not field.required:
                    full_type = f"Optional[{py_type}]"
                    default = " = None"
                else:
                    full_type = py_type
                    default = ""

                # Clean description for field
                desc = field.description.replace('"', "'")

                # Generate field line
                lines.append(
                    f'    {field.attribute}: {full_type}{default}  # {desc}'
                )

        return "\n".join(lines)

    def generate_file(
        self, objects: List[ObjectDef], enums: Dict[str, List[Tuple[str, str]]]
    ) -> str:
        """Generate complete Python file with all models.

        Args:
            objects: List of object definitions
            enums: Dictionary of enum definitions

        Returns:
            Complete Python file content
        """
        lines = []

        # File header
        lines.append('"""Auto-generated Pydantic models for Adcom v1.0 specification.')
        lines.append("")
        lines.append("This file is auto-generated. Do not edit manually.")
        lines.append(f"Generated: {datetime.utcnow().isoformat()}Z")
        lines.append('"""')
        lines.append("")

        # Imports
        lines.append("from typing import Optional, List, Dict, Any")
        lines.append("from enum import Enum")
        lines.append("from pydantic import BaseModel, Field, ConfigDict")
        lines.append("")
        lines.append("")

        # Generate enums first
        if enums:
            lines.append("# " + "=" * 78)
            lines.append("# Enums")
            lines.append("# " + "=" * 78)
            lines.append("")

            for enum_name, values in sorted(enums.items()):
                enum_code = self.generate_enum_code(enum_name, values)
                lines.append(enum_code)
                lines.append("")
                lines.append("")

        # Generate models
        lines.append("# " + "=" * 78)
        lines.append("# Models")
        lines.append("# " + "=" * 78)
        lines.append("")

        known_objects = {obj.name for obj in objects}
        enum_names = set(enums.keys())

        for obj in objects:
            model_code = self.generate_model_code(obj, known_objects, enum_names)
            lines.append(model_code)
            lines.append("")
            lines.append("")

        # Rebuild models to resolve forward references
        lines.append("# Rebuild models to resolve forward references")
        for obj in objects:
            lines.append(f"{obj.name}.model_rebuild()")
        lines.append("")

        return "\n".join(lines)

    def generate_adcom_models(self) -> Path:
        """Generate Adcom models file.

        Returns:
            Path to generated file
        """
        print("🔍 Parsing Adcom specification...")
        objects, enums = parse_adcom_spec()

        print(f"📦 Found {len(objects)} objects and {len(enums)} enums")

        print("🔨 Generating Pydantic models...")
        content = self.generate_file(objects, enums)

        output_path = self.output_dir / "adcom.py"
        output_path.write_text(content, encoding="utf-8")

        print(f"✅ Generated {output_path}")
        print(f"   - {len(objects)} models")
        print(f"   - {len(enums)} enums")

        return output_path


def main():
    """Main entry point."""
    generator = AdcomModelGenerator()
    generator.generate_adcom_models()


if __name__ == "__main__":
    main()
