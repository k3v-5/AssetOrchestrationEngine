# Informe Final - Fase 5: NPR Appearance Architecture & Production Shaders

## Estado
**PASS**

## Arquitectura de Shading (ToonShaderIR)
En lugar de crear múltiples shaders monolíticos por "franquicia" (Anime, Comic, Fortnite, Borderlands), se extendió la arquitectura base NPR en `src/aoe_ir/appearance.py` para abstraer un sistema modular genérico. El `ShadingProfile` ahora incorpora:
- Colores programáticos definibles: `shadow_color`, `midtone_color`, `highlight_color`.
- Variables de gradación: `band_count` (escalable a N), `shadow_threshold`, `shadow_softness`.
- Un componente de contorno luminoso: `RimLightProfile` (intensidad, suavidad, anchura, color).
- Control de especularidad: `SpecularProfile` (para reflejos en los ojos, brillos de anillos en cabello anime).

## Modelos de Estilo (Configuraciones)
Se construyó `src/aoe_ir/style_presets.py`, que expone una factoría `StylePresets` para inyectar un **StyleProfile** parametrizado al asset base. Se han validado las siguientes composiciones conceptuales:
- **Anime:** Toon Shader a 2 bandas para piel, sombra rígida (softness 0.0). Outline muy fino (`width: 0.012`). Override semántico para el Cabello a 3 bandas + specularity y Cara con sombra rígida de 1 sola banda y exclusión de rim-lights.
- **Cartoon:** Toon Shader a 3 bandas con suavidad (`shadow_softness=0.15`) que interpola gradientes, Rim light suave (`softness=0.3`), y Outline de grosor intermedio grisáceo.
- **Comic:** Toon Shader a 4 bandas, sombra densa (`#1a1a24`), potente Rim light (`intensity=1.0`), Outline grueso negro (`width: 0.035`) y activadores de mapas de textura base (curvature, grunge y hatching) planificados.

## Implementación Real en Blender
El nodo de generación en `executor.py` (`create_toon_basic_material`) fue reconstruido al superset `create_toon_advanced_material` que inyecta en el ShaderGraph de `bpy`:
- **N·L Vector & ColorRamp:** Adapta su interpolación entre `CONSTANT` y `B_SPLINE` en base a la variable `softness`. Sus N elementos de posición se construyen procedimentalmente (Midtone se posiciona al `0.7 * threshold` y Core Shadow al `0.5 * threshold`, si es necesario).
- **Fresnel/Rim Light:** Añade un grupo condicional basado en `ShaderNodeLayerWeight`, enlazando un rampa secundaria que inyecta la luminosidad y un MixRGB configurado en `SCREEN` sumándolo al output NPR.

## Validaciones y Regresión
- **Iluminación Dinámica:** Las pruebas in-engine (`test_lighting_dynamic.py`) han corrido usando el preset más avanzado (Cartoon + Fresnel). Moviendo un target de luz a diferentes puntos espaciales, demostramos que todos los canales y nodos adicionales responden sin romper el material y alteran físicamente las zonas sombreadas.
- **Deformación/Pose:** Los tests de `test_deformation_outline.py` re-corridos garantizan que ni los Rim Lights por normales (`LayerWeight`) ni los ColorRamps fallan cuando el sistema de Armature y Skinning desplaza los vértices de la malla.
- **PBR y Semántica:** Continúan funcionales; los overrides semánticos aceptan estos nuevos estilos híbridos sin problemas.

## Siguiente Paso (Fase 6)
Al tener el `CharacterIR` fundamentado e independiente y todos los `NPR Appearance Profiles` programáticos y reaccionando a la luz y a las poses estáticas de manera validada, el ecosistema está listo para la **Fase 6: Animation Production**. En la siguiente fase se debe dar vida a la propiedad de `AnimationFoundationIR`, inyectando keyframes desde el Engine, "bakeando" clips (ej: Walk Cycles, Combates, Face Shapes) y permitiendo al sistema renderizar los fotogramas en sucesión manteniendo estable el estilo artístico bajo Locomotion.
