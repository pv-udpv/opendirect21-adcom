"""Pydantic model generator from specification objects."""

import re
from pathlib import Path
from typing import List, Tuple, Set, Dict
from dataclasses import dataclass
from tools.spec_parser.md_tables import ObjectDef, FieldDef


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

        # Handle object references (e.g., "Contact object", "Address object")
        if "object" in spec_type.lower() and not spec_type.lower() == "object":
            # Extract the object name
            obj_name = spec_type.replace("object", "").strip()
            if obj_name:
                return obj_name, is_optional, False

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
            "object": "Dict[str, Any]",
        }

        for key, value in type_map.items():
            if key in spec_type.lower():
                return value, is_optional, False

        # Default to str for unknown types
        return "str", is_optional, False

    @staticmethod
    def extract_enum_values(spec_type: str) -> List[str]:
        """Extract enum values from spec type like 'enum (Active, Inactive, Pending)'.
        
        Args:
            spec_type: Type string from specification
            
        Returns:
            List of enum value strings
        """
        match = re.search(r"enum\s*\((.*?)\)", spec_type, re.IGNORECASE)
        if match:
            values_str = match.group(1)
            values = [v.strip() for v in values_str.split(",")]
            return values
        return []


class PydanticGenerator:
    """Generate Pydantic models from object definitions."""
    
    # Python keywords that cannot be used as field names
    PYTHON_KEYWORDS = {
        'from', 'import', 'class', 'def', 'if', 'else', 'elif', 'while', 
        'for', 'return', 'yield', 'break', 'continue', 'pass', 'raise',
        'try', 'except', 'finally', 'with', 'as', 'assert', 'del', 'global',
        'lambda', 'nonlocal', 'and', 'or', 'not', 'is', 'in', 'type'
    }

    def __init__(self, output_dir: Path = None):
        """Initialize generator.

        Args:
            output_dir: Directory to write generated models
        """
        self.output_dir = output_dir or Path("opendirect21/models/generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def sanitize_field_name(self, field_name: str) -> Tuple[str, str]:
        """Sanitize field name to avoid Python keywords.
        
        Args:
            field_name: Original field name
            
        Returns:
            Tuple of (sanitized_name, original_name_for_alias)
        """
        if field_name.lower() in self.PYTHON_KEYWORDS:
            return f"{field_name}_field", field_name
        return field_name, field_name

    def generate_enum_class(self, field_name: str, values: List[str]) -> str:
        """Generate Python Enum class code.
        
        Args:
            field_name: Name of the field (used for enum class name)
            values: List of enum value strings
            
        Returns:
            Generated Python Enum class code
        """
        enum_name = f"{field_name.capitalize()}Enum"
        lines = []
        lines.append(f"class {enum_name}(str, Enum):")
        lines.append(f'    """Enum values for {field_name} field."""')
        
        for value in values:
            # Convert to valid Python identifier
            const_name = value.upper().replace(" ", "_").replace("-", "_")
            # Remove any non-alphanumeric characters except underscore
            const_name = re.sub(r'[^A-Z0-9_]', '', const_name)
            lines.append(f'    {const_name} = "{value}"')
        
        return "\n".join(lines)

    def generate_model_code(self, obj_def: ObjectDef) -> str:
        """Generate Python code for a single model.

        Args:
            obj_def: ObjectDef with name and fields

        Returns:
            Generated Python code
        """
        lines = []
        
        # Model class
        lines.append(f"class {obj_def.name}(BaseModel):")
        if obj_def.description:
            lines.append(f'    """{obj_def.description}"""')
        else:
            lines.append(f'    """{obj_def.name} model from OpenDirect specification."""')
        lines.append("")
        
        if not obj_def.fields:
            lines.append("    pass")
        else:
            for field in obj_def.fields:
                py_type, is_optional, is_enum = TypeMapping.map_type(field.type_raw)
                
                # Handle enum types
                if is_enum:
                    enum_values = TypeMapping.extract_enum_values(field.type_raw)
                    if enum_values:
                        py_type = f"{field.attribute.capitalize()}Enum"
                
                # For object references, use string literals to avoid forward reference issues
                if py_type in [o.name for o in [obj_def]]:  # Self-reference
                    py_type = f'"{py_type}"'
                elif not py_type.startswith(('str', 'int', 'float', 'bool', 'datetime', 'date', 'List', 'Dict')):
                    # It's probably a reference to another model, use string literal
                    if py_type not in ['Any'] and not py_type.endswith('Enum'):
                        py_type = f'"{py_type}"'
                
                # Sanitize field name
                field_name, original_name = self.sanitize_field_name(field.attribute)
                
                # Determine if field is optional (not required)
                if not field.required:
                    full_type = f"Optional[{py_type}]"
                    default = " = None"
                else:
                    full_type = py_type
                    default = ""
                
                # Escape quotes in description
                desc = field.description.replace('"', '\\"')
                
                # Use Field with alias if field name was sanitized
                if field_name != original_name:
                    if not field.required:
                        lines.append(
                            f'    {field_name}: {full_type} = Field(None, alias="{original_name}")  # {desc}'
                        )
                    else:
                        lines.append(
                            f'    {field_name}: {full_type} = Field(..., alias="{original_name}")  # {desc}'
                        )
                else:
                    lines.append(
                        f'    {field_name}: {full_type}{default}  # {desc}'
                    )
        
        return "\n".join(lines)

    def generate_all_models(self, objects: List[ObjectDef], output_file: str = "opendirect.py") -> str:
        """Generate complete Python file with all models.
        
        Args:
            objects: List of ObjectDef objects to generate
            output_file: Name of output file
            
        Returns:
            Path to generated file
        """
        lines = []
        
        # File header
        lines.append('"""Auto-generated Pydantic models from OpenDirect 2.1 specification."""')
        lines.append("")
        lines.append("# This file is auto-generated. Do not edit manually.")
        lines.append("")
        
        # Collect imports
        imports = {
            "from enum import Enum",
            "from typing import TYPE_CHECKING, Optional, List, Dict, Any",
            "from pydantic import BaseModel, Field",
        }
        
        needs_datetime = False
        needs_date = False
        
        for obj in objects:
            for field in obj.fields:
                py_type, _, _ = TypeMapping.map_type(field.type_raw)
                if "datetime" in py_type:
                    needs_datetime = True
                if "date" in py_type and "datetime" not in py_type:
                    needs_date = True
        
        if needs_datetime:
            imports.add("from datetime import datetime")
        if needs_date:
            imports.add("from datetime import date")
        
        for imp in sorted(imports):
            lines.append(imp)
        
        lines.append("")
        lines.append("")
        
        # Generate enum classes
        enum_classes = set()
        for obj in objects:
            for field in obj.fields:
                _, _, is_enum = TypeMapping.map_type(field.type_raw)
                if is_enum:
                    enum_values = TypeMapping.extract_enum_values(field.type_raw)
                    if enum_values:
                        enum_name = f"{field.attribute.capitalize()}Enum"
                        if enum_name not in enum_classes:
                            enum_classes.add(enum_name)
                            lines.append(self.generate_enum_class(field.attribute, enum_values))
                            lines.append("")
                            lines.append("")
        
        # Generate model classes
        for obj in objects:
            lines.append(self.generate_model_code(obj))
            lines.append("")
            lines.append("")
        
        # Rebuild models to resolve forward references
        lines.append("# Rebuild models to resolve forward references")
        for obj in objects:
            lines.append(f"{obj.name}.model_rebuild()")
        lines.append("")
        
        # Write to file
        output_path = self.output_dir / output_file
        content = "\n".join(lines)
        output_path.write_text(content)
        
        return str(output_path)


if __name__ == "__main__":
    from tools.spec_parser.md_tables import MarkdownTableParser
    
    # Load specification
    spec_file = Path(__file__).parent / "OpenDirect.v2.1.final.md"
    if not spec_file.exists():
        print(f"❌ Specification file not found: {spec_file}")
        exit(1)
    
    content = spec_file.read_text()
    parser = MarkdownTableParser(content)
    objects = parser.extract_objects()
    
    print(f"📦 Parsed {len(objects)} objects")
    
    # Generate models
    generator = PydanticGenerator()
    output_path = generator.generate_all_models(objects)
    
    print(f"✅ Generated models to: {output_path}")
    print(f"   Total objects: {len(objects)}")
    print(f"   Total fields: {sum(len(o.fields) for o in objects)}")

