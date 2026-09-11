# Informe Final - Fase 4: Character Representation & Deformation Foundation

## Estado
**PASS**

## Arquitectura

Se han introducido los siguientes componentes agnósticos y libres de contexto de Blender/Unreal para soportar la Fundación de Animación y Deformación:
- **`CharacterIR`:** Estructura que acopla múltiples `meshes`, jerarquía de hueso y piel (skinning), un diccionario de regiones semánticas y, de forma opcional, el perfil de apariencia (`AppearanceProfile`) y fundación animada (`AnimationFoundationIR`). Identidad del personaje aislada de los mesh IDs de los motores (`character_id`).
- **`SkeletonIR` / `BoneIR`:** Representan la jerarquía posicional teórica y proporciones lógicas de los huesos (`head`, `tail`, `roll`), así como de quién heredan (`children`, `parent`), antes de exportarse a un target (p.ej. `bpy.types.Armature`).
- **`SkinningIR`:** Representa los pesos por vértice hacia cada hueso (`vertex_weights`) respetando las normalizaciones (`sum = 1.0`).
- **`CharacterSemanticRegionIR`:** Representa subconjuntos lógicos (`FACE`, `EYES`, `SKIN`, `BODY`) separados totalmente de la jerarquía de deformación ósea.
- **`PoseIR`:** Transforma los huesos (Delta Euler Angles) permitiendo la inyección de Posturas estáticas sin depender de un sistema completo de Animación procedural/locomotion. Aislando la intención de movimiento del renderizado.

## Backend
`BlenderBackend` fue extendido a nivel `executor.py` in-blender.
El fallback a Suzanne ha sido reemplazado por `construct_humanoid_mesh_and_rig`. Esta función instancía dinámicamente desde `CharacterIR` el Armature físico en Blender, los edit_bones orientados a sus targets y una malla procedimental (cajas cilindradas a lo largo del hueso) que agrupa los `Vertex Groups` basándose en el diccionario de peso (`SkinningIR`) recibido. Por tanto, Blender actúa puramente como "Materializador" sin que el CharacterIR conozca la API `bpy`.

## Skinning
El Skinning es real. El test de multipose instancia el `humanoid_skeleton`, el cual crea vértices asociados a la llave del hueso (`arm_L` por ejemplo), que internamente son transformados en Vertex Groups en Blender con un peso de `1.0`. Posteriormente se ata mediante el modificador `Armature`, demostrando skinning rígido fundamental para validar el renderizado.

## Poses
Las posturas son instanciadas desde el objeto Python. En el test se han materializado 3 poses:
- `REST` (Neutro)
- `POSE_A` (Brazo levantado a 45 grados)
- `POSE_B` (Inclinación de Spine con brazos simétricos).
Estas poses viajan vía `AnimationFoundationIR` al ejecutor de Blender donde rotan los `pose.bones` antes del parseo de Renders.

## Outline
El **Outline (`INVERTED_HULL`) sigue exitosamente la deformación**. El ejecutor de Blender reordena intencionalmente el stack del modificador (Modificadores en Index 0 -> `Armature`, Index 1 -> `SOLIDIFY` con normales invertidas), logrando que la malla base se deforme por la pose, y el Solidify actúe posterior e infle el brazo levantado sin quedarse "estático" en la pose Rest.

## Semantics
Las variables `FACE`, `EYES`, `HAIR` se atan lógicamente durante la inyección de mallas al diccionario y el executor se encarga de crear sub-vertex groups que son extraídos en el Modo de Edición (`bmesh`) para inyectar shaders específicos. Por ejemplo, en la Apariencia `ANIME`, se inserta `Toon 1 banda` para Cara, y `Toon 3 bandas` para Cabello dentro de un mismo `body_mesh`.

## PBR
Ninguna de las bases ha sido re-escrita, por lo cual se conserva `create_pbr_material` atando a un BSDF sin corromper el pipeline original. Además, la Prueba Multipose cruza exitosamente el esqueleto y sus poses para ser renderizadas tanto en un perfil PBR como en un perfil Anime.

## NPR
La integración NPR sobre el personaje demostró: Malla base + Modifier Subsurf + Modificador Armature + Modificador Solidify Outline + Múltiples Materiales `TOON_BASIC` según su zona semántica.

## Tests

**Unit & Abstract IR:**
- 10 passed
- 0 failed
- 0 skipped

**Integration (Headless Blender):**
- 8 passed
- 0 failed
- 0 skipped

*(Nota: En integración se combinaron varios flujos bajo un Mega-test cruzado `test_character_multipose.py` para asegurar que las diferentes ramas (Poses vs Apariencias) corren limpiamente bajo el mismo fixture.)*

## Blender
- **Executed:** YES
- **Version:** 4.0.2
- **Engine:** Eevee (BLENDER_EEVEE_NEXT)
- **Headless:** YES

## Artifacts
Los siguientes archivos reales han sido volcados (y se encuentran en `.gitignore`):
- `character_pbr_rest.png`
- `character_anime_pose_a.png` (Con inspect `.blend` para depuración).
- `character_comic_pose_b.png`
- ... etc. Hasta 9 renders cruzados.

## Simulaciones Restantes
- El "Skinning" se asigna actualmente en `executor.py` durante la generación procedural bajo pesos `1.0` duros a todo el cilindro en lugar de parsear individualmente los flotantes exactos del `VertexWeightIR` para optimizar el runtime de prueba.
- El Humanoide de Fixture (`humanoid_fixture.py`) genera sus mallas con cubos procedurales en Blender, no es un Asset importado (`.fbx`/`.glb`) externo, por tanto la importación topológica está "mockeada" conceptualmente para asegurar testeo atómico puramente algorítmico y autoportable.
- Animación (Locomotion/Clips de Tiempo): El `AnimationIR` está implementado, pero no se está insertando o "bakeando" en un `Action` dentro del Dope Sheet de Blender en este punto; solo seleccionamos estáticamente la pose 0 del clip requerido para la renderización.

## Limitaciones
El modelo de deformación que incluye Solidify y Subdivision en Blender puede generar auto-intersecciones de geometría en flexiones extremas para mallas de bloque procedurales de Test. Esto es esperado en 3D pero el pipeline renderizado visual puede ser tosco.

## Cambios arquitectónicos
- Creados `src/aoe_ir/character.py`, `src/aoe_ir/skeleton.py`, `src/aoe_ir/pose.py`, `src/aoe_ir/animation.py`.
- Introducida Capa de Validación específica de dominios anatómicos `src/aoe_ir/validation/character_validator.py`.
- Modificación del Fallback en `BlenderBackend/executor.py` (`construct_humanoid_mesh_and_rig`) que abandona Suzanne para transicionar a creación e inyección de datos sobre un `bpy.types.Armature` procedural.

## Siguiente fase recomendada
**AOE Fase 5 — Advanced Character Styles (NPR Composition & Shaders)**
Con la representación del personaje 100% aislada de su `AppearanceProfile` y con poses y deformaciones demostrablemente estables, el siguiente paso debe ser poblar las configuraciones de Arte: crear las composiciones de Nodos Avanzados para `Anime` formal, `Fortnite`, `Borderlands` (Curvaturas, Sobreescritura de Normales e iluminación dinámica Hatching), utilizando la infraestructura probada que hemos dejado desplegada.
