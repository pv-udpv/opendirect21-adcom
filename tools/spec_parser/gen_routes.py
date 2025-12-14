"""FastAPI route generator from specification objects."""

from pathlib import Path

from tools.spec_parser.md_tables import ObjectDef


class RouteGenerator:
    """Generate FastAPI routes from object definitions."""

    def __init__(self, output_dir: Path = None):
        """Initialize generator.

        Args:
            output_dir: Directory to write generated routes
        """
        self.output_dir = output_dir or Path("opendirect21/api/generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_crud_routes(self, obj_def: ObjectDef) -> str:
        """Generate CRUD routes for a single model.

        Args:
            obj_def: ObjectDef with name and fields

        Returns:
            Generated Python code for routes
        """
        model_name = obj_def.name
        route_prefix = f"/{model_name.lower()}s"
        var_name = model_name.lower()

        lines = []
        lines.append(f"# {model_name} routes")
        lines.append("")

        # List endpoint
        lines.append(f'@router.get("{route_prefix}", response_model=list[{model_name}])')
        lines.append(f"async def list_{var_name}s(")
        lines.append("    skip: int = Query(0, ge=0, description='Number of items to skip'),")
        lines.append(
            "    limit: int = Query(100, ge=1, le=1000, description='Max items to return'),"
        )
        lines.append("    store: InMemoryStore = Depends(get_store),")
        lines.append(") -> list[dict]:")
        lines.append(f'    """List all {model_name} objects with pagination."""')
        lines.append(f'    return store.list("{model_name}", skip=skip, limit=limit)')
        lines.append("")

        # Get by ID endpoint
        lines.append(f'@router.get("{route_prefix}/{{id}}", response_model={model_name})')
        lines.append(f"async def get_{var_name}(")
        lines.append("    id: str = Path(..., description='Unique identifier'),")
        lines.append("    store: InMemoryStore = Depends(get_store),")
        lines.append(") -> dict:")
        lines.append(f'    """Get a specific {model_name} by ID."""')
        lines.append(f'    entity = store.get("{model_name}", id)')
        lines.append("    if not entity:")
        lines.append(
            f'        raise HTTPException(status_code=404, detail="{model_name} not found")'
        )
        lines.append("    return entity")
        lines.append("")

        # Create endpoint
        lines.append(
            f'@router.post("{route_prefix}", response_model={model_name}, status_code=201)'
        )
        lines.append(f"async def create_{var_name}(")
        lines.append(f"    entity: {model_name},")
        lines.append("    store: InMemoryStore = Depends(get_store),")
        lines.append(") -> dict:")
        lines.append(f'    """Create a new {model_name}."""')
        lines.append(f'    created = store.create("{model_name}", entity.model_dump())')
        lines.append("    return created")
        lines.append("")

        # Update endpoint
        lines.append(f'@router.put("{route_prefix}/{{id}}", response_model={model_name})')
        lines.append(f"async def update_{var_name}(")
        lines.append(f"    entity: {model_name},")
        lines.append("    id: str = Path(..., description='Unique identifier'),")
        lines.append("    store: InMemoryStore = Depends(get_store),")
        lines.append(") -> dict:")
        lines.append(f'    """Update an existing {model_name}."""')
        lines.append(f'    updated = store.update("{model_name}", id, entity.model_dump())')
        lines.append("    if not updated:")
        lines.append(
            f'        raise HTTPException(status_code=404, detail="{model_name} not found")'
        )
        lines.append("    return updated")
        lines.append("")

        # Delete endpoint
        lines.append(f'@router.delete("{route_prefix}/{{id}}", status_code=204)')
        lines.append(f"async def delete_{var_name}(")
        lines.append("    id: str = Path(..., description='Unique identifier'),")
        lines.append("    store: InMemoryStore = Depends(get_store),")
        lines.append(") -> None:")
        lines.append(f'    """Delete a {model_name}."""')
        lines.append(f'    success = store.delete("{model_name}", id)')
        lines.append("    if not success:")
        lines.append(
            f'        raise HTTPException(status_code=404, detail="{model_name} not found")'
        )
        lines.append("")

        return "\n".join(lines)

    def generate_all_routes(
        self, objects: list[ObjectDef], output_file: str = "opendirect_routes.py"
    ) -> str:
        """Generate complete Python file with all routes.

        Args:
            objects: List of ObjectDef objects to generate routes for
            output_file: Name of output file

        Returns:
            Path to generated file
        """
        lines = []

        # File header
        lines.append('"""Auto-generated FastAPI routes from OpenDirect 2.1 specification."""')
        lines.append("")
        lines.append("# This file is auto-generated. Do not edit manually.")
        lines.append("")

        # Imports
        lines.append("from fastapi import APIRouter, HTTPException, Depends, Query, Path")
        lines.append("from opendirect21.store import InMemoryStore, get_store")
        lines.append("")

        # Import all models
        model_names = [obj.name for obj in objects]
        lines.append("from opendirect21.models.generated import (")
        for name in model_names:
            lines.append(f"    {name},")
        lines.append(")")
        lines.append("")
        lines.append("")

        # Create router
        lines.append('router = APIRouter(prefix="/api/v1", tags=["opendirect"])')
        lines.append("")
        lines.append("")

        # Generate routes for each object
        for obj in objects:
            lines.append(self.generate_crud_routes(obj))
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

    # Generate routes
    generator = RouteGenerator()
    output_path = generator.generate_all_routes(objects)

    print(f"✅ Generated routes to: {output_path}")
    print(f"   Total objects: {len(objects)}")
    print(f"   Total endpoints: {len(objects) * 5} (5 per object)")
