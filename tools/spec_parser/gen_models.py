"""Pydantic model generator from specification objects."""

import re
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class TypeMapping:
    """Maps specification types to Python types."""

    @staticmethod
    def map_type(spec_type: str) -> Tuple[str, bool, bool]:
        """Map spec type to Python type.

        Returns:
            (python_type, is_optional, is_enum)
        """
        spec_type = spec_type.strip()

        # Handle optional
        is_optional = "optional" in spec_type.lower()
        spec_type = spec_type.replace("optional", "").strip()

        # Handle enum
        is_enum = spec_type.startswith("enum")
        if is_enum:
            return "str", is_optional, True

        # Handle arrays
        if spec_type.endswith("[]") or "array" in spec_type.lower():
            base_type = spec_type.replace("[]", "").replace("array", "").strip()
            inner_type, inner_opt, inner_enum = TypeMapping.map_type(base_type)
            return f"List[{inner_type}]", is_optional, False

        # Primitive types
        type_map = {
            "string": "str",
            "integer": "int",
            "int": "int",
            "number": "float",
            "float": "float",
            "double": "float",
            "boolean": "bool",
            "bool": "bool",
            "datetime": "datetime",
            "date-time": "datetime",
            "date": "date",
            "uuid": "str",
        }

        for key, value in type_map.items():
            if key in spec_type.lower():
                return value, is_optional, False

        # Default to str for unknown types
        return "str", is_optional, False


class PydanticGenerator:
    """Generate Pydantic models from object definitions."""

    def __init__(self, output_dir: Path = None):
        """Initialize generator.

        Args:
            output_dir: Directory to write generated models
        """
        self.output_dir = output_dir or Path("opendirect21/models/generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_model_code(self, name: str, fields: List[dict]) -> str:
        """Generate Python code for a single model.

        Args:
            name: Model class name
            fields: List of field definitions

        Returns:
            Generated Python code
        """
        lines = []

        # Imports
        imports = set()
        imports.add("from pydantic import BaseModel, Field")
        imports.add("from typing import Optional, List")

        has_datetime = False
        for field in fields:
            py_type, _, _ = TypeMapping.map_type(field.get("type", "str"))
            if "datetime" in py_type:
                has_datetime = True

        if has_datetime:
            imports.add("from datetime import datetime")

        for imp in sorted(imports):
            lines.append(imp)

        lines.append("")
        lines.append("")
        lines.append(f"class {name}(BaseModel):")
        lines.append(f'    """Object definition from specification."""')
        lines.append("")

        if not fields:
            lines.append("    pass")
        else:
            for field in fields:
                name_str = field.get("attribute", "field")
                desc = field.get("description", "")
                py_type, is_opt, is_enum = TypeMapping.map_type(field.get("type", "str"))
                required = field.get("required", False)

                if is_opt and not required:
                    full_type = f"Optional[{py_type}]"
                    default = "None"
                else:
                    full_type = py_type
                    default = "..."

                lines.append(
                    f'    {name_str}: {full_type} = Field({default}, description="{desc}")'
                )

        return "\n".join(lines)


if __name__ == "__main__":
    print("Run: python -m tools.spec_parser.gen_models")
