"""Generate FastAPI routes from Adcom specification."""

from pathlib import Path
from typing import List, Set
from datetime import datetime

from tools.spec_parser.adcom_parser import parse_adcom_spec
from tools.spec_parser.md_tables import ObjectDef


class AdcomRouteGenerator:
    """Generate FastAPI routes for Adcom specification."""

    def __init__(self, output_dir: Path = None):
        """Initialize generator.

        Args:
            output_dir: Directory to write generated routes
        """
        self.output_dir = output_dir or Path("opendirect21/api/generated")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def get_route_prefix(self, model_name: str) -> str:
        """Get route prefix for a model.

        Args:
            model_name: Model class name

        Returns:
            Route prefix (e.g., "ads", "displays")
        """
        # Convert CamelCase to lowercase with s plural
        # Ad -> ads, Display -> displays
        name_lower = model_name.lower()

        # Handle special cases
        if name_lower.endswith("y"):
            # Publisher -> publishers (not publishery)
            return f"{name_lower[:-1]}ies" if name_lower not in ["display", "video", "audio"] else f"{name_lower}s"
        elif name_lower.endswith("s"):
            # Already ends with s
            return f"{name_lower}es"
        else:
            return f"{name_lower}s"

    def generate_routes_for_model(self, obj_def: ObjectDef) -> str:
        """Generate CRUD routes for a single model.

        Args:
            obj_def: Object definition

        Returns:
            Generated route code
        """
        model_name = obj_def.name
        route_prefix = self.get_route_prefix(model_name)

        lines = []
        lines.append(f"# Routes for {model_name}")
        lines.append(f'@router.get("/{route_prefix}", response_model=List[{model_name}])')
        lines.append(f'async def list_{route_prefix}(')
        lines.append(f"    skip: int = Query(0, ge=0),")
        lines.append(f"    limit: int = Query(100, ge=1, le=1000),")
        lines.append(f') -> List[{model_name}]:')
        lines.append(f'    """List all {model_name} objects with pagination."""')
        lines.append(f'    items = await store.list("{route_prefix}", skip=skip, limit=limit)')
        lines.append(f"    return [{model_name}(**item) for item in items]")
        lines.append("")

        lines.append(f'@router.get("/{route_prefix}/{{id}}", response_model={model_name})')
        lines.append(f"async def get_{model_name.lower()}(id: str) -> {model_name}:")
        lines.append(f'    """Get a specific {model_name} by ID."""')
        lines.append(f'    item = await store.get("{route_prefix}", id)')
        lines.append(f"    if not item:")
        lines.append(f'        raise HTTPException(status_code=404, detail="{model_name} not found")')
        lines.append(f"    return {model_name}(**item)")
        lines.append("")

        lines.append(f'@router.post("/{route_prefix}", response_model={model_name}, status_code=201)')
        lines.append(f"async def create_{model_name.lower()}(item: {model_name}) -> {model_name}:")
        lines.append(f'    """Create a new {model_name}."""')
        lines.append(f'    created = await store.create("{route_prefix}", item.model_dump())')
        lines.append(f"    return {model_name}(**created)")
        lines.append("")

        lines.append(f'@router.put("/{route_prefix}/{{id}}", response_model={model_name})')
        lines.append(f"async def update_{model_name.lower()}(id: str, item: {model_name}) -> {model_name}:")
        lines.append(f'    """Update an existing {model_name}."""')
        lines.append(f'    updated = await store.update("{route_prefix}", id, item.model_dump())')
        lines.append(f"    if not updated:")
        lines.append(f'        raise HTTPException(status_code=404, detail="{model_name} not found")')
        lines.append(f"    return {model_name}(**updated)")
        lines.append("")

        lines.append(f'@router.delete("/{route_prefix}/{{id}}", status_code=204)')
        lines.append(f"async def delete_{model_name.lower()}(id: str):")
        lines.append(f'    """Delete a {model_name}."""')
        lines.append(f'    deleted = await store.delete("{route_prefix}", id)')
        lines.append(f"    if not deleted:")
        lines.append(f'        raise HTTPException(status_code=404, detail="{model_name} not found")')
        lines.append(f"    return")
        lines.append("")

        return "\n".join(lines)

    def generate_file(self, objects: List[ObjectDef]) -> str:
        """Generate complete routes file.

        Args:
            objects: List of object definitions

        Returns:
            Complete Python file content
        """
        lines = []

        # File header
        lines.append('"""Auto-generated FastAPI routes for Adcom v1.0 specification.')
        lines.append("")
        lines.append("This file is auto-generated. Do not edit manually.")
        lines.append(f"Generated: {datetime.utcnow().isoformat()}Z")
        lines.append('"""')
        lines.append("")

        # Imports
        lines.append("from typing import List")
        lines.append("from fastapi import APIRouter, HTTPException, Query, status")
        lines.append("from opendirect21.store import InMemoryStore")
        lines.append("")

        # Import all models
        lines.append("from opendirect21.models.generated.adcom import (")
        for i, obj in enumerate(objects):
            comma = "," if i < len(objects) - 1 else ""
            lines.append(f"    {obj.name}{comma}")
        lines.append(")")
        lines.append("")
        lines.append("")

        # Create router and store
        lines.append('# Create router with /api/v1/adcom prefix')
        lines.append('router = APIRouter(')
        lines.append('    prefix="/api/v1/adcom",')
        lines.append('    tags=["adcom"],')
        lines.append(')')
        lines.append("")
        lines.append("# Initialize data store")
        lines.append("store = InMemoryStore()")
        lines.append("")
        lines.append("")

        # Generate routes for each model
        # Prioritize: Media objects, Asset objects, then Context objects
        media_objects = ["Ad", "Display", "Banner", "Video", "Audio", "Native"]
        asset_objects = ["Asset", "LinkAsset", "ImageAsset", "VideoAsset", "TitleAsset", "DataAsset", "Event"]
        context_objects = ["Publisher", "Content", "User", "Device", "Geo"]

        categories = [
            ("# " + "=" * 78 + "\n# Media Objects\n" + "# " + "=" * 78, media_objects),
            ("# " + "=" * 78 + "\n# Asset Objects\n" + "# " + "=" * 78, asset_objects),
            ("# " + "=" * 78 + "\n# Context Objects\n" + "# " + "=" * 78, context_objects),
        ]

        for header, category_names in categories:
            lines.append(header)
            lines.append("")

            for obj in objects:
                if obj.name in category_names:
                    routes_code = self.generate_routes_for_model(obj)
                    lines.append(routes_code)

        return "\n".join(lines)

    def generate_adcom_routes(self) -> Path:
        """Generate Adcom routes file.

        Returns:
            Path to generated file
        """
        print("🔍 Parsing Adcom specification...")
        objects, _ = parse_adcom_spec()

        print(f"📦 Found {len(objects)} objects")

        print("🔨 Generating FastAPI routes...")
        content = self.generate_file(objects)

        output_path = self.output_dir / "adcom_routes.py"
        output_path.write_text(content, encoding="utf-8")

        print(f"✅ Generated {output_path}")
        print(f"   - {len(objects) * 5} endpoints (CRUD for each model)")

        return output_path


def main():
    """Main entry point."""
    generator = AdcomRouteGenerator()
    generator.generate_adcom_routes()


if __name__ == "__main__":
    main()
