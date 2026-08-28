# Índice de Conocimiento Maestro — DarX Proyect

Todo lo que se ha investigado, diseñado, codificado y aprendido en este proyecto, dónde reside cada fichero y en qué orden leerlo. Escrito para que cualquier **desarrollador o agente de IA** pueda ponerse al día de inmediato con máxima velocidad y cero retrabajo.

> **Ubicación Canónica**: La raíz absoluta del proyecto es `E:\Darx_Proyect\` (con guion bajo).

---

## 🗺️ Por Dónde Empezar

Si solo vas a leer cuatro documentos clave, hazlo en este orden estricto:

1. **[`docs/REGLAS-DE-TRABAJO.md`](file:///E:/Darx_Proyect/docs/REGLAS-DE-TRABAJO.md)** — **Las 46 Reglas Operativas**. Cada una nacida de un fallo empírico real con su fecha, síntoma, causa raíz y solución obligatoria.
2. **[`docs/GDD.md`](file:///E:/Darx_Proyect/docs/GDD.md)** — Qué es el juego, loop principal de combate, progresión y mecánicas.
3. **[`docs/ARTE-BIBLIA.md`](file:///E:/Darx_Proyect/docs/ARTE-BIBLIA.md)** — Directivas visuales, paleta de colores, materiales PBR sin suciedad y composición de pantalla.
4. **[`docs/SISTEMA-TESTS-AUTOMATIZADOS.md`](file:///E:/Darx_Proyect/docs/SISTEMA-TESTS-AUTOMATIZADOS.md)** — Suite de validación en tiempo real (`.\ejecutar_tests.ps1`) para asegurar el 100% de éxito en assets, shaders, mallas y spawn.

---

## 📚 1. Catálogo Completo de Documentación Técnica (`docs/`)

### A. Diseño General y Universo
| Documento | Descripción y Contenido Clave |
| :--- | :--- |
| [`GDD.md`](file:///E:/Darx_Proyect/docs/GDD.md) | Documento de Diseño del Juego (Fases 1 a 12). |
| [`ARTE-BIBLIA.md`](file:///E:/Darx_Proyect/docs/ARTE-BIBLIA.md) | Guía artística obligatoria (iluminación, materiales y colores). |
| [`GUIA-PERSONAJE-FINAL.md`](file:///E:/Darx_Proyect/docs/GUIA-PERSONAJE-FINAL.md) | Especificación del modelo del jugador, rig y proporciones. |
| [`DISENO-ARMA.md`](file:///E:/Darx_Proyect/docs/DISENO-ARMA.md) | Pistola láser de energía (sustituye a `DISENO-REVOLVER.md`). |
| [`PLAN-UV-TEXTURAS.md`](file:///E:/Darx_Proyect/docs/PLAN-UV-TEXTURAS.md) | Densidad de texel y proyección triplanar en shaders de mundo. |

---

### B. Especificación de Jefes de Bioma (Bosses 1 a 6)
| Documento | Jefe | Mecánicas, Modelo 3D, Audio y Combate |
| :--- | :--- | :--- |
| [`BOSS-1-ROBOT-CONTENCION.md`](file:///E:/Darx_Proyect/docs/BOSS-1-ROBOT-CONTENCION.md) | **Robot de Contención** | Chasis bípedo pesado, pinzas hidráulicas, carga frontal y agarre de asfixia QTE. |
| [`BOSS-2-THE-ERROR.md`](file:///E:/Darx_Proyect/docs/BOSS-2-THE-ERROR.md) | **The Error** | Entidad glitch flotante, jaula dimensional, teletransporte estroboscópico y ecos. |
| [`BOSS-3-STATIC-MATRIX.md`](file:///E:/Darx_Proyect/docs/BOSS-3-STATIC-MATRIX.md) | **Static Matrix** | Matriz analógica CRT, desfasaje, sombras de interferencia e inversión de controles. |
| [`BOSS-4-FLORA-CARNIVORA.md`](file:///E:/Darx_Proyect/docs/BOSS-4-FLORA-CARNIVORA.md) | **Flora Carnívora** | Huésped atrapado en raíces cuadrúpedas, mortero de esporas ácidas y cepos terrestres. |
| [`BOSS-5-AMALGAMA-CELULAR.md`](file:///E:/Darx_Proyect/docs/BOSS-5-AMALGAMA-CELULAR.md) | **El Amalgama Celular** | Musculatura expuesta, mutación adaptativa, golpe demoledor y Fuga Metabólica. |
| [`BOSS-6-EXPERIMENTO-TELEQUINETICO.md`](file:///E:/Darx_Proyect/docs/BOSS-6-EXPERIMENTO-TELEQUINETICO.md) | **Sujeto Cero (Telekinetic)**| Arnés de levitación, predicción de trayectoria (*lead target*), cubos cinéticos y Salva Total. |

---

### C. Audio, Síntesis y MetaSounds
| Documento | Propósito y Contenido |
| :--- | :--- |
| [`PIPELINE-AUDIO-VITAL-ABLETON-UNREAL.md`](file:///E:/Darx_Proyect/docs/PIPELINE-AUDIO-VITAL-ABLETON-UNREAL.md) | **Pipeline Maestro de Audio**: Ableton Live MCP + Vital + Python + Unreal C++. |
| [`GUIA-SINTESIS-VITAL-SFX.md`](file:///E:/Darx_Proyect/docs/GUIA-SINTESIS-VITAL-SFX.md) | Manual psicoacústico de síntesis modular en Vital (recetas paso a paso). |
| [`ARQUITECTURA-MUSICA.md`](file:///E:/Darx_Proyect/docs/ARQUITECTURA-MUSICA.md) | Motor de música adaptativa por stems, Quartz Clock y MetaSounds en C++. |
| [`FASE-10-Contrato-Sonido.md`](file:///E:/Darx_Proyect/docs/FASE-10-Contrato-Sonido.md) | Contrato de efectos de sonido y mezcla maestra. |
| [`FASE-10.1-Contrato-Musica-Ampliada.md`](file:///E:/Darx_Proyect/docs/FASE-10.1-Contrato-Musica-Ampliada.md) | Evolución musical de 5 fases de intensidad y motivos por bioma. |
| [`FASE-10.2-Propuesta-Nuevos-Sonidos.md`](file:///E:/Darx_Proyect/docs/FASE-10.2-Propuesta-Nuevos-Sonidos.md) | Catálogo sonoro de los 9 arquetipos de tropas y 6 Bosses. |
| [`ASSETS-SONIDO-VITAL.md`](file:///E:/Darx_Proyect/docs/ASSETS-SONIDO-VITAL.md) y [`ASSETS-SONIDO.md`](file:///E:/Darx_Proyect/docs/ASSETS-SONIDO.md) | Registro de patches exportados e importados al motor. |

---

### D. Efectos Visuales, Renderizado e Iluminación
| Documento | Contenido Técnico |
| :--- | :--- |
| [`VFX-NIAGARA-SUITE-CATALOGO.md`](file:///E:/Darx_Proyect/docs/VFX-NIAGARA-SUITE-CATALOGO.md) | **Catálogo de 20 Sistemas Niagara**: Parámetros, emisores base y asignación en C++. |
| [`CALIBRACION-ILUMINACION-Y-LEDS.md`](file:///E:/Darx_Proyect/docs/CALIBRACION-ILUMINACION-Y-LEDS.md) | Auto-Exposición Adaptativa (`AEM_Histogram`), luz táctica y controles en vivo de LEDs. |
| [`FASE-12-Suite-RTX-DLSS-RayReconstruction.md`](file:///E:/Darx_Proyect/docs/FASE-12-Suite-RTX-DLSS-RayReconstruction.md) | NVIDIA DLSS Super Resolution, Frame Generation, Ray Reconstruction y Reflex. |

---

### E. Arquitectura del Motor, WorldGen, IA y Asset Engine
| [`ASSET-ORCHESTRATION-ENGINE-MASTER.md`](file:///E:/Darx_Proyect/docs/ASSET-ORCHESTRATION-ENGINE-MASTER.md) | **Documento Maestro del Asset Orchestration Engine (AOE)**: Fases 1 a 80 completadas (**1382 tests PASS**), orquestación de producción end-to-end (`ProductionOrchestratorAPI`), optimizador multiobjetivo de coste/rendimiento (`CostPerformanceAPI`), aprendizaje y optimización de estrategias (`StrategyLearningAPI`), análisis de fallos y self-debugging (`DiagnosticsAPI`), biblioteca oficial Golden Assets & Baselines (`GoldenAPI`), benchmark cuantitativo (`EvaluationBenchmarkAPI`), grafo de conocimiento (`ProjectKnowledgeGraphAPI`), memoria contextual (`ContextMemoryAPI`), contratos V2 y ToolGuard, persistencia y recuperación ante caídas, cumplimiento de la Regla 52 y hoja de ruta completa (Fases 81 a 84 + Auditoría Final). |
| [`F80-PRODUCTION-ORCHESTRATION-VALIDATION.md`](file:///E:/Darx_Proyect/docs/F80-PRODUCTION-ORCHESTRATION-VALIDATION.md) | **Informe de Validación Oficial Fase 80 (Production Orchestration)**: Pipeline end-to-end de 19 etapas, 17 estados, máquina de estados atómica, resiliencia F70, gobernanza F71/F72, validación real en Blender de `DARX Production Test Weapon`, cero duplicación y preservación estricta de `DarX_Assets.blend`. |
| [`FASE-11-Contrato-Generacion-Procedural.md`](file:///E:/Darx_Proyect/docs/FASE-11-Contrato-Generacion-Procedural.md) | Generador de mundo procedural de 3 biomas, esclusas y arenas de combate. |
| [`ARQUITECTURA-DIRECTOR-Y-PERSISTENCIA.md`](file:///E:/Darx_Proyect/docs/ARQUITECTURA-DIRECTOR-Y-PERSISTENCIA.md) | Director de IA multiclase, tabla de spawn ponderada y guardado por semilla. |
| [`FASE-9-AnimBP-Especificacion.md`](file:///E:/Darx_Proyect/docs/FASE-9-AnimBP-Especificacion.md) | Animation Blueprint del jugador en primera persona. |
| [`FASE-9-Contrato.md`](file:///E:/Darx_Proyect/docs/FASE-9-Contrato.md) | Contrato de integración del chasis del jugador. |
| [`FASE-1-Analisis-Tecnico.md`](file:///E:/Darx_Proyect/docs/FASE-1-Analisis-Tecnico.md) a [`FASE-2-Especificacion-Tecnica.md`](file:///E:/Darx_Proyect/docs/FASE-2-Especificacion-Tecnica.md) | Especificaciones base del mundo cúbico y movilidad. |

---

## 🛠️ 2. Scripts de Automatización y Pipelines (`Art/`)

| Script | Propósito y Comportamiento Atómico |
| :--- | :--- |
| `Art/Blender/rehacer_todo.py` | Reconstruye y exporta todas las mallas y rigs de Blender a FBX sin abrir la UI. |
| `Art/crear_master_materials_reales.py` | Instancia y compila los 16 Master Materials PBR con soporte Nanite/ISM. |
| `Art/calibrar_todos_los_materiales.py` | Calibra intensidades emisivas LED en todos los materiales del proyecto. |
| `Art/VFX/crear_suite_completa_niagara.py`| Instancia los 20 emisores de partículas Niagara en `/Game/DarX/VFX/`. |
| `Art/VFX/render_all_boss_and_mob_vfx.py` | Renderiza previsualizaciones gráficas de VFX en Blender. |
| `Art/Tests/test_suite_darx.py` | **Suite de 21 Pruebas Automatizadas** en Unreal Engine (100% de cobertura). |
| `compilar.ps1` | Compilador acelerado de C++ con UnrealBuildTool (`-Esperar`, `-Archivo`). |
| `ejecutar_tests.ps1` | Ejecutor desatendido de compilación y pruebas automatizadas. |

---

## 📌 3. Reglas de Oro Inflexibles (Resumen de `REGLAS-DE-TRABAJO.md`)

1. **Mide, no supongas (Regla 0 y 8)**: Ante cualquier anomalía, ejecutar scripts diagnósticos de lectura (`.py` / logs) antes de modificar código.
2. **Unicidad Visual Absoluta (Regla 3)**: Prohibido reciclar modelos entre Bosses y tropas.
3. **Previsualización Visual Obligatoria (Regla 4)**: Renderizar capturas antes de exportar a Unreal.
4. **Zero-Self-Collision y Buffer $\ge 30\text{ cm}$ (Regla 5)**: Accesorios y escudos separados del cuerpo para evitar clipping y colisiones internas.
5. **Sesión Centralizada de Ableton Live (Regla 6)**: Toda producción musical y de SFX reside en una única sesión organizada.
6. **Espacialización 3D Obligatoria (Regla 10)**: Todo sonido de enemigo o proyectil debe tener origen espacial y curva de caída $\le 18-20\text{ m}$.
7. **Pausa Obligatoria en Menús de Debug (Regla 9)**: Pausar el juego al abrir herramientas de inspección.
8. **Auto-Exposición Adaptativa y Vanos Libres (Reglas 44-46)**: Mantener vanos de paso abiertos entre salas y auto-exposición `AEM_Histogram` activa.
