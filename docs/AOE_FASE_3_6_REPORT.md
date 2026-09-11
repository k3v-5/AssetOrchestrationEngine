# Informe Final - Fase 3.6: NPR Foundation Hardening + Deformable Asset Validation

## Estado
**PASS**

## Implementación real y Cambios Realizados
Las siguientes operaciones han sido confirmadas, endurecidas y ejecutadas bajo Blender Headless:

1. **Toon Lighting Real:**
   - Se demostró dinámicamente que `TOON_BASIC` reacciona a la luz. Se creó el test `test_lighting_dynamic.py` que mueve una luz a posiciones relativas distintas `(0, 5, 0), (5, 0, 0), (-5, -5, 5)` comprobando que el hasheado del render difiere (es decir, las zonas de sombra giran alrededor del modelo en lugar de ser asignaciones poligonales estáticas).
   - Se ajustó el algoritmo nodal para que la parametrización de 2, 3 y 4 bandas del `ColorRamp` escale apropiadamente distancias y colores a través del threshold N·L (Core shadow, Midtone, Highlight).

2. **Outline Desacoplado y Deformación (Inverted Hull):**
   - El test `test_deformation_outline.py` demuestra que al posear un esqueleto sobre una malla (generando 3 poses diferentes), el render difiere en cada pose.
   - El `scene_report.json` prueba que el modificador `Outline_Solidify` evalúa ESTRICTAMENTE DESPUÉS del modificador `Armature`. Esto garantiza que la malla original se deforma por los pesos primero, y solo *después* se infla en direcciones de la normal para crear el borde. (Respuesta a la Opción B: "Se genera mediante una técnica/modifier que naturalmente sigue al objeto deformado").

3. **Semantic Appearance Overrides:**
   - La prueba se amplió de "FACE" a abarcar `FACE`, `EYES` y `HAIR`. En Blender se generan grupos de vértices dedicados y múltiples materiales `override` que conviven de forma modular para un mismo objeto.

4. **Backend Capabilities Matrix:**
   - Se creó la estructura `BackendCapabilities` en `base.py`.
   - `BlenderBackend` declara ser capaz de `inverted_hull` pero rechaza `post_process_outline`.
   - `UnrealBackend` declara ser capaz de `post_process_outline` y `stencil`, pero rechaza `inverted_hull`.
   - Todo export levanta un flag `BackendCapabilityError` si se intenta orquestar apariencias incompatibles en el backend.

5. **Mejora del Sistema Perceptual (Golden Images):**
   - El test se refactorizó para no depender del hasheado exacto binario o delta de tamaño. Emplea la librería `Pillow` (PIL) calculando la Raíz del Error Cuadrático Medio (RMSE) basándose en las diferencias del histograma RGB, aceptando un threshold perceptual en los renderizados entre la escena Golden base y la de ejecución CI.

6. **Metadatos en Reporting:**
   - `scene_report.json` devuelto desde `executor.py` contiene ahora información in-engine validando a versión (`blender_version: "4.0.2"`) y el motor de render activo (`BLENDER_EEVEE_NEXT` / `BLENDER_EEVEE`).

## Simulaciones restantes
- No se han agregado las extensiones a perfiles como Anime, Sketch, Comic o Fortnite. Siguen en placeholder.
- La malla que usamos en las pruebas in-blender para ser deformada y aplicar semántica sigue siendo el test object mono Suzanne (`primitive_monkey_add`).

## Tests

**Unit & Abstract IR:**
- 7 passed
- 0 failed
- 0 skipped

**Integration (Headless Blender):**
- 8 passed (incluyendo Poses Dinámicas, Light Dinámica y Golden Perceptual Diffing)
- 0 failed
- 0 skipped

## Blender
- **Ejecutado realmente:** YES
- **Versión:** 4.0.2
- **Engine:** Eevee (BLENDER_EEVEE_NEXT fallback)
- **Headless:** YES

## Artifacts Reales Generados (ignorados en git):
- `render.png`
- `scene.blend`
- `scene_report.json`
- `toon_2band.png`
- `toon_3band.png`
- `toon_4band.png`
- `toon_outline.png`
- `toon_deformed.png`

## Problemas conocidos y Limitaciones
- `bmesh` tuvo que ser usado forzosamente dentro de la semántica para selección/deselección de materiales, ya que `bpy.ops` puede arrojar exepciones Context Error en modo puramente CLI/Headless si las ventanas no existen.
- Las luces, cámaras y esqueletos de los tests dentro de `executor.py` están hardcodeadas posicionalmente a la escala de la malla mono genérica, servirán pero cuando el engine lea mallas de diferentes escalas (humanos AAA), las luces de test requerirán parametrización de bounding box.

## Próximo Paso Recomendado
La Fase 3.6 completó su promesa: **AOE posee un núcleo NPR genérico, real y verificable bajo deformación**.

La siguiente fase ya puede ser: **Fase 4 - CharacterIR, SkeletonIR y Sistemas Semánticos Avanzados**, donde introduzcamos mallas complejas (humanoides) para probar el pipeline de rigging e implementemos oficialmente los perfiles `Anime` y `Comic` combinando estos cimientos comprobados.
