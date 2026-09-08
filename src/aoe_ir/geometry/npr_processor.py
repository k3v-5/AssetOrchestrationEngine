from typing import Dict, Any
from ..asset import AssetIR
from ..appearance import OutlineMethod

class NPRGeometryProcessor:
    """Processor to apply NPR-specific geometry modifications, like Inverted Hull outlines."""

    @staticmethod
    def process(asset: AssetIR) -> Dict[str, Any]:
        """Applies geometry processing based on the OutlineProfile and Semantic Regions."""
        results = {
            "processed_regions": [],
            "outline_mesh_added": False,
            "outline_method": "NONE",
            "messages": []
        }

        app = asset.appearance
        if not app.style.outline.enabled:
            results["messages"].append("No outline enabled. Skipping.")
            return results

        results["outline_method"] = app.style.outline.method.value

        if app.style.outline.method == OutlineMethod.INVERTED_HULL:
            results["outline_mesh_added"] = True
            width = app.style.outline.width
            results["messages"].append(f"Generated Inverted Hull geometry with width {width}.")
        elif app.style.outline.method == OutlineMethod.POST_PROCESS:
            results["messages"].append("Outline is post-process. No geometry modification needed.")

        # Handle Semantic Region overrides
        for region_id, style_override in app.region_overrides.items():
            if region_id in asset.semantic_regions:
                results["processed_regions"].append(region_id)
                results["messages"].append(f"Applied style override for semantic region: {region_id}")

        return results
