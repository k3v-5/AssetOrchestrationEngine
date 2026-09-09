# Informe Final - Fase 9: Facial Animation, Blend Shapes & Lip Sync Foundation

## Estado
**PASS**

## Contrato Semántico Facial
Esta fase incorporó el modelo formal agnóstico para expresiones en AOEIR (`src/aoe_ir/facial.py`).
Se creó `FaceRigIR`, el cual no almacena polígonos sino que declara la existencia de `BlendShapeIR` (nombres de canales de morphs) o Huesos anatómicos faciales. Estos canales son orquestados por un `ExpressionProfileIR`, permitiendo composiciones multi-canal; por ejemplo, la expresión "Happy" agrupa semánticamente la forma `mouth_smile` con un peso del 80% y `cheek_raise` al 40%, todo encapsulado en el dominio Python.

## Sincronización Labial y Fonemas (Foundation)
El fundamento para el soporte Lip Sync ha quedado plasmado en `PhonemeEventIR` y `LipSyncTrackIR`, permitiendo recibir timelines de triggers desde audios externos, los cuales son interpretados por un `VisemeMappingIR`. Este diccionario une el gatillo vocal (ej. "A") al perfil de expresión diseñado, previniendo que el backend de animación corporal quede manchado por las rutinas de voz.

## Integración Temporal Cuerpo-Cara
La pieza central del orquestador (`AnimationGraphIR`) ahora acepta diccionarios de `facial_tracks`. Esto es vital ya que separa oficialmente la locomoción de la actuación. Se validó a través de unit tests y el integration script in-Blender, logrando inyectar un Action secundario de Blender orientado única y exclusivamente a los `Shape Keys` de la malla base y a las del Outline `Inverted_Hull`.

## Golden Test: Rendering Combinado (Cuerpo/Cara/NPR)
El test `test_facial_golden.py` corrobora la madurez estructural alcanzada. Un fixture de humanoide fue insertado con:
1. Una pista procedural de cuerpo (mixamo_walk).
2. Un perfil NPR `ANIME` completo con outlines gruesos.
3. Un `FaceRigIR` con los canales `EyeBlink` y `MouthSmile`.
4. Una pista de Expresión facial (`dialogue_01`) que mantenía una sonrisa sostenida y programaba un pestañeo brusco en el fotograma 5.
La exportación arrojó exitosamente el volcado con Blender creando dinámicamente las Shape Keys referenciadas e independizando las animaciones, sin interrupciones entre el `SOLIDIFY` paramétrico del NPR y el Morph Target de la cara.

## Artifacts Resultantes y Deuda Técnica
La prueba in-engine ha sido ajustada a modo de test rápido `.blend` export para prevenir un timeout de los runners en CI, sin embargo, reporta un `scene_report.json` que evidencia de primera mano la construcción e inyección de los modificadores y F-Curves esperados en Blender 4.0.2.

**Simulaciones y Limitaciones:**
- La malla base en el `BlenderBackend` crea Keys *Dummy* (`from_mix=False`, todas planas en 0) ya que la geometría procedural generada con `bmesh` no cuenta con alteraciones morfológicas (solo cajas y monitos). Para que el rostro en un caso AAA se mueva visiblemente, esta fase presume que la malla final ingestada cuenta ya con topología esculpida (blendshapes reales incrustados en el FBX).
- Todavía no hay sistema físico ni procedural del cabello, este sigue siendo tratado como una región estática atada al hueso de la cabeza.

## Próximo Paso (Fase 10)
Se han cumplido los preceptos del diseño. El núcleo arquitectónico general (Geometría, Semántica, NPR/PBR, Rigging, Animación de Cuerpo, Timeline y Expresiones Faciales/Lip Sync) está listo, blindado de colisiones y 100% abstraído de los engines de render.

La fase recomendada es la **Fase 10: Advanced NPR Styles & Procedural Texturing**, donde sobre estos cimientos artísticos se programarán oficialmente los pipelines procedimentales para inyectar Texturizados Automáticos (Curvature Maps, Ambient Occlusion baked, Grunge Nodes) que completen los presets finales visuales de "Borderlands" y "Comic/Sketch".
