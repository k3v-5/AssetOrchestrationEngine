# Hoja de Ruta Estratégica: AOE v2.0 (Next-Gen)

Este documento detalla el plan de acción estructurado en fases para llevar el Asset Orchestration Engine (AOE) hacia su versión 2.0, enfocándose en Inteligencia Artificial, Escalabilidad Cloud y Calidad Artística Avanzada (Puntos 1, 3 y 4 del análisis de desarrollos futuros).

---

## Eje 1: Integración de Machine Learning e Inteligencia Artificial (Punto 1)

El objetivo de este eje es reemplazar cálculos procedimentales costosos por modelos neuronales optimizados y acelerar la creación de texturas mediante IA Generativa.

### Fase 17: Generación de Texturas IA Base (ControlNet Backend)
- [x] **17.1:** Integrar la API de Stable Diffusion (o instancia local mediante `diffusers`) en el orquestador de Python.
- [x] **17.2:** Desarrollar el módulo de extracción en Blender que genere pases en blanco y negro (UV Maps, Normal Maps, Cavity) para usarlos como capas de control (ControlNets).
- [x] **17.3:** Implementar el `GenerativeShadingIR` en la receta JSON para aceptar prompts de estilo (ej. *"Borderlands cell-shaded metal"*).
- [x] **17.4:** Horneado de la imagen generada sobre el material base del modelo.

### Fase 18: Recolección de Datos para ML Deformer (Physics/Cloth)
- [x] **18.1:** Construir un simulador offline masivo en Blender. Configurar *Cloth Dynamics* y *Soft Body* (Vellum) de alta resolución.
- [x] **18.2:** Orquestar secuencias de movimiento complejas (correr, saltar, pelear) y guardar la caché de vértices (Alembic).
- [x] **18.3:** Diseñar el pipeline de extracción de diferencias de vértices (Deltas) entre el esqueleto básico (Skinning) y la simulación compleja de tela.

### Fase 19: Entrenamiento e Integración de ML Deformer en UE5
- [ ] **19.1:** Utilizar los datos extraídos para entrenar el modelo NNI (Neural Network Inference) nativo de Unreal Engine 5.
- [x] **19.2:** Actualizar el orquestador de importación (`ue5_import_orchestrator.py`) para enlazar el archivo del modelo de red neuronal (Network Asset) al *Skeletal Mesh*.
- [ ] **19.3:** Desplegar el *ML Deformer Component* en el Actor para que evalúe pliegues en tiempo real sin cálculos de físicas de CPU.

---

## Eje 2: Infraestructura Cloud y Automatización CI/CD (Punto 3)

El objetivo es pasar de una ejecución local limitada por hardware a una granja de servidores escalable con integración continua al control de versiones del motor de juego.

### Fase 20: Dockerización del Pipeline AOE
- [x] **20.1:** Crear un `Dockerfile` que encapsule el entorno de ejecución: Python 3.10+, dependencias del CLI (`aoe_cli`), y una compilación *Headless* de Blender compatible con Linux.
- [x] **20.2:** Validar la ejecución del pipeline localmente dentro del contenedor para garantizar la exportación determinista del FBX y el Manifest.

### Fase 21: Orquestación Serverless / Kubernetes (Cloud Baking)
- [ ] **21.1:** Configurar Amazon EKS (Kubernetes) o AWS Batch para recibir el `ProductionBatchIR` masivo.
- [ ] **21.2:** Dividir el Batch en tareas individuales y despacharlas a N contenedores en paralelo.
- [ ] **21.3:** Integrar el volcado final a un bucket S3, consolidando todos los FBX y `manifest.json` generados de forma distribuida.

### Fase 22: Pipeline de Integración Continua (Perforce / Git LFS)
- [x] **22.1:** Conectar el script de UE5 (`ue5_import_orchestrator.py`) a la librería `P4Python` o a la API nativa de control de código de UE5.
- [x] **22.2:** Desarrollar la lógica de *Check-out* automático previo a la sobrescritura de assets importados.
- [x] **22.3:** Implementar *Add* para nuevos assets y *Submit/Commit* automático bajo un changelist generado por la IA (ej. "[AOE] Importación Lote Sprint 1").

---

## Eje 3: Evolución Artística del Renderizado NPR (Punto 4)

El objetivo es elevar la calidad gráfica a nivel AAA para producciones anime/estilizadas, resolviendo las limitaciones clásicas de las normales y facilitando el trabajo de los animadores.

### Fase 23: Data Transfer Procedural para Sombras de Anime
- [x] **23.1:** Crear el módulo `StylizedNormalProcessor` en el `BlenderBackend`.
- [x] **23.2:** Identificar automáticamente áreas críticas del rostro (cabeza, nariz, mejillas) usando Vertex Groups o Semantic Regions.
- [x] **23.3:** Aplicar un modificador procedural *Data Transfer* que proyecte las normales de un elipsoide invisible sobre el rostro, garantizando que el umbral de sombra corte suavemente bajo la luz direccional en UE5 (evitando sombras "rotas" por los polígonos de la nariz o labios).

### Fase 24: Generación Automatizada de Control Rigs Faciales
- [ ] **24.1:** Actualizar el esquema `UnrealAssetManifestIR` para incluir mapeos lógicos (huesos vs morfologías faciales).
- [ ] **24.2:** Desarrollar una extensión del plugin en C++ (`UControlRigExtensions`) que instancie el *Control Rig* procedimentalmente.
- [ ] **24.3:** Cablear nodos de Control Rig automáticamente desde Python para vincular los controles de interfaz (GIZMOS en el visor de UE5) con las curvas (Morph Targets) correspondientes.
- [ ] **24.4:** Validar el sistema garantizando que un animador puede manipular los controladores faciales sin abrir editores de malla externos.

---

## Resumen del Progreso Esperado (De v1.1 a v2.0)

Al ejecutar este Roadmap, el **AOE** dejará de ser únicamente una herramienta de traducción técnica y se convertirá en un hub integral distribuido. Será capaz de delegar trabajo a inteligencias artificiales en paralelo en la nube, y entregará a Unreal Engine modelos visualmente idénticos a los estándares de estudios modernos como Arc System Works, listos para integrarse al control de versiones corporativo sin intervención humana.
