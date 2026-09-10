# Documentación del Esquema JSON AOE v1.1

La versión 1.1 de Asset Orchestration Engine (AOE) introduce el soporte para la generación procedural de Niveles de Detalle (LODs) y límites automatizados de Quality Assurance (QA). Estos se configuran de manera declarativa al enviar una receta de personaje (`CharacterRecipe`) dentro del `ProductionBatchIR`.

A continuación se documentan los nuevos bloques JSON esperados.

## Bloque `lod_config` (Opcional)

Permite especificar cuántos niveles de reducción de polígonos deben generarse automáticamente y si deben conservar el modificador procedural de contorno (*Inverted Hull*).

```json
"lod_config": {
    "levels": [50, 25, 10],
    "keep_inverted_hull": [true, false, false]
}
```

*   **`levels` (Array de Enteros):** Define el porcentaje de retención de caras. En el ejemplo superior, LOD1 retiene el 50% de la malla, LOD2 el 25%, y LOD3 el 10%.
*   **`keep_inverted_hull` (Array de Booleanos):** Indica, por cada nivel definido, si la cáscara del Inverted Hull (usado en NPR) debe ser renderizada o eliminada para ahorrar rendimiento en las lejanías.

## Bloque `qa_limits` (Opcional)

Especifica las restricciones técnicas que la malla debe cumplir. Si estos límites se superan, el orquestador registrará un estado de `warning` y añadirá los detalles al archivo de salida `qa_report.json`.

```json
"qa_limits": {
    "max_triangles": 50000,
    "max_bones": 100,
    "max_texture_res": 4096
}
```

*   **`max_triangles`:** Límite máximo de triángulos en la malla base (LOD0) luego de ser triangulada por el backend.
*   **`max_bones`:** Cantidad máxima de huesos (`bones`) permitidos en la jerarquía (Armature).
*   **`max_texture_res`:** Resolución máxima en píxeles permitida para cualquier textura cargada en memoria y asociada a este asset.

### Ejemplo Completo de Receta v1.1

```json
{
    "batch_id": "production_sprint_1",
    "recipes": [
        {
            "recipe_id": "SK_Ninja",
            "base_mesh": "ninja_base.fbx",
            "appearance_id": "NPR_Comic",
            "lod_config": {
                "levels": [50, 25],
                "keep_inverted_hull": [true, false]
            },
            "qa_limits": {
                "max_triangles": 45000,
                "max_bones": 70,
                "max_texture_res": 2048
            }
        }
    ]
}
```
