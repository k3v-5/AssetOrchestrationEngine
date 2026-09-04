# UAF-81: BACKLOG DE FASES PENDIENTES & HOJA DE RUTA ESTRATÉGICA

**Estado:** Documento de Planificación y Registro de Pendientes  
**Programa:** Universal Asset Factory (AOE / UAF)  
**Dependencias Previas Completadas:** UAF-81.0 → UAF-81.92 (100% verificado y certificado)  

Este documento registra formalmente las fases estratégicas identificadas y pendientes de ejecución para expandir la autonomía y profundidad del Universal Asset Framework en conjunción con Unreal Engine 5.

---

## 📋 Resumen del Backlog

| Fase | Título | Dominio Técnico | Prioridad |
| :--- | :--- | :--- | :--- |
| **UAF-81.93** | Dynamic Economy, Weapon Affixes & Procedural Loot Fabric | Progresión RPG, Loot Tables, Affixes, GAS & UE5 DataTables | Alta |
| **UAF-81.94** | Procedural Interactive Audio, Spatial Acoustics & MetaSounds | Síntesis interactiva, Acústica $RT_{60}$, MetaSounds & Quartz | Alta |
| **UAF-81.95** | Real-Time In-Engine Co-Piloting & Live Synchronization | WebSocket / gRPC LiveLink bidireccional AOE $\leftrightarrow$ UE5 | Media |
| **UAF-81.96** | Autonomous Gameplay Playtesting & AI QA Simulation | Agentes headless de QA, detección de softlocks y telemetría | Media |
| **UAF-81.97** | Procedural Cinematics, CineCamera Director & UE5 Sequencer | Encuadres dinámicos, Rule of Thirds, auto-DOF, LevelSequence | Media |
| **UAF-81.98** | Procedural Quest Graph, Branching Narrative & Dialogue Trees | Diálogos ramificados, skill checks, reputación y CommonUI | Media |
| **UAF-81.99** | Physics, Voronoi Fracturing & Chaos Destruction System | Fracturación Voronoi, UE5 Chaos GeometryCollection, escombros | Media |
| **UAF-81.100** | Volumetric Weather Cycles, Dynamic Day/Night & Atmosphere | Ciclos día/noche, SkyAtmosphere, niebla volumétrica y shaders | Media |
| **UAF-81.101** | Studio Web UI & Local Interactive Visual Dashboard | Interfaz local FastAPI + WebGL/Three.js, visor 3D y 1-click | Alta |
| **UAF-81.102** | One-Click Full Vertical Slice Builder (Macro-Orchestrator) | Pipeline unificado de nivel completo listo para jugar en UE5 | Alta |

---

## 1. UAF-81.93: DYNAMIC ECONOMY, WEAPON AFFIXES & PROCEDURAL LOOT FABRIC

### 1.1 Misión y Objetivos
Construir el sistema de economía procedural, itemización y generación de armas/equipo con presupuesto matemático de daño y atributos, exportable a **Gameplay Ability System (GAS)** y Data Tables de Unreal Engine 5.

### 1.2 Componentes Arquitectónicos
1. **Presupuesto de Poder (Power Budget Math)**:
   - Cálculo determinista del DPS, cadencia de fuego, dispersión, retroceso y masa según el nivel del item ($L$) y su nivel de rareza ($R \in \{\text{Common, Uncommon, Rare, Epic, Legendary}\}$):
     $$\text{Budget}(L, R) = \text{BasePower} \cdot (1 + 0.12 \cdot L) \cdot \text{RarityMultiplier}(R)$$
2. **Generador de Afijos (Prefijos y Sufijos)**:
   - Modificadores aleatorios balanceados que alteran atributos (e.g., *Criogénico*, *Perforador de Blindaje*, *Recarga Rápida*).
   - Sinérgias elementales (Fuego, Electricidad, Veneno, Corrosión) con mitigación según armaduras de enemigos (UAF-81.92).
3. **Economía y Curvas de Inflación**:
   - Precios de compra/venta dinámicos vinculados a la escasez de suministros regulada por el Director de Ritmo (UAF-81.90).
   - Reciclaje de chatarra (*scrap conversion rate*).
4. **Exportación UE5**:
   - Exportación de `UDataTable` (CSV y JSON estructurados) listos para `FWeaponItemDefinition`.
   - Mapeo directo a `UGameplayEffect` y `UAttributeSet` para integración nativa con el **Gameplay Ability System (GAS)**.

---

## 2. UAF-81.94: PROCEDURAL INTERACTIVE AUDIO, SPATIAL ACOUSTICS & METASOUNDS

### 2.1 Misión y Objetivos
Completar el ciclo audiovisual dinámico del motor mediante generación y orquestación adaptativa de audio, acústica física de reverberación calculada sobre la topología de niveles y exportación de parches de **MetaSounds**.

### 2.2 Componentes Arquitectónicos
1. **Motor de Música Adaptativa por Capas (Stems)**:
   - Sincronización rítmica por compás y compases fraccionarios (reloj de cuantización Quartz).
   - Fundido cruzado de stems según la fase del `DynamicPacingDirector` (UAF-81.90): `CALM`, `BUILDUP`, `PEAK`, `COOLDOWN`.
2. **Propagación Acústica Espacial Topológica**:
   - Cálculo del tiempo de reverberación $RT_{60}$ basado en la fórmula de Sabine y Eyring sobre las dimensiones y materiales de las habitaciones de WFC:
     $$RT_{60} = \frac{0.161 \cdot V}{\sum S_i \alpha_i}$$
   - Oclusión de sonido a través de esquinas del grafo topológico y puertas cerradas (Lock-and-Key).
3. **Exportador UE5**:
   - Generación de grafos `.json` y presets para **MetaSounds Source Assets**.
   - Parámetros dinámicos expuestos (`StressIntensity`, `RoomVolume`, `OcclusionAlpha`).

---

## 3. UAF-81.95: REAL-TIME IN-ENGINE CO-PILOTING & LIVE SYNCHRONIZATION

### 3.1 Misión y Objetivos
Establecer un puente bidireccional continuo en tiempo real (vía WebSockets / gRPC) entre el orquestador headless de AOE/UAF y el editor activo de Unreal Engine 5.

### 3.2 Componentes Arquitectónicos
1. **Servidor y Cliente WebSocket/gRPC**:
   - `aoe-copilot-daemon`: Servicio ligero en segundo plano.
   - Integración con el plugin `UAFBridge` en UE5 para recibir comandos sin reiniciar ni pausar el editor.
2. **Edición Bidireccional en Vivo**:
   - Cambios de semillas o reglas en AOE actualizan el terreno y los spawners en el viewport de UE5 en menos de 500ms.
   - Movimiento de volúmenes o marcadores por el diseñador humano en UE5 se retroalimenta al grafo topológico de AOE.

---

## 4. UAF-81.96: AUTONOMOUS GAMEPLAY PLAYTESTING & AI QA SIMULATION

### 4.1 Misión y Objetivos
Validación autónoma del nivel y las mecánicas mediante agentes IA que juegan partidas completas en modo headless, detectando softlocks, picos de dificultad injustos o cuellos de botella de rendimiento.

### 4.2 Componentes Arquitectónicos
1. **Agente Simulador de Jugador (Headless QA Bot)**:
   - Simula movimiento, combate y resolución de puzzles (llaves y puertas de UAF-81.90).
   - Reporta caminos bloqueados o fallas de navegación.
2. **Telemetría y Mapas de Calor (Heatmaps)**:
   - Generación de mapas de calor de muertes de jugador, gasto de munición y tiempo por sala.
   - Feedback en bucle cerrado al `DynamicPacingDirector` para auto-calibración de la dificultad antes del empaquetado final.

---

## 5. UAF-81.97: PROCEDURAL CINEMATICS, CINECAMERA DIRECTOR & UE5 SEQUENCER

### 5.1 Misión y Objetivos
Generar secuencias cinemáticas in-engine y tomas dinámicas de cámara para hitos narrativos, introducciones de jefes, descubrimientos de salas WFC y cámaras de acción/combate.

### 5.2 Componentes Arquitectónicos
1. **Motor de Composición y Encuadre (`CinematicFramingEngine`)**:
   - Reglas de composición cinematográfica: regla de tercios, proporción áurea, encuadres *over-the-shoulder* y planos contraplano para diálogos.
2. **Planificador de Trayectorias de Cámara (`CameraTrajectorySolver`)**:
   - Curvas de spline continuas (Catmull-Rom) con prevención de colisiones contra mallas de salas WFC y orografía del terreno.
3. **Autofocus y Profundidad de Campo Dinámica (`AutoFocusDepthOfField`)**:
   - Control continuo de distancia focal y apertura de diafragma (*f-stop*) enfocando automáticamente al actor o amenaza de mayor relevancia táctica.
4. **Exportador UE5 Sequencer**:
   - Generación de assets `LevelSequence` nativos con tracks `MovieSceneCineCameraTrack`, canales de transformación y disparadores de eventos.

---

## 6. UAF-81.98: PROCEDURAL QUEST GRAPH, BRANCHING NARRATIVE & DIALOGUE TREES

### 6.1 Misión y Objetivos
Conectar el grafo de misiones de UAF-81.90 y el sistema de reputación de UAF-81.92 en un tejido narrativo procedural con ramificación de decisiones, árboles de diálogo interactivos y consecuencias de facción.

### 6.2 Componentes Arquitectónicos
1. **Grafo Narrativo Ramificado (`BranchingNarrativeDAG`)**:
   - Misiones primarias y contratos secundarios generados proceduralmente con bifurcaciones morales y resolución divergente.
2. **Compilador de Árboles de Diálogo (`DialogueTreeCompiler`)**:
   - Nodos de conversación con condiciones previas (*prerequisites*): nivel de reputación con la facción del NPC, ítems requeridos en inventario y tiradas de habilidad (*skill checks*).
3. **Registro de Banderas de Estado del Mundo (`WorldStateFlagRegistry`)**:
   - Seguimiento atómico de elecciones del jugador que alteran el comportamiento futuro de facciones e IA GOAP.
4. **Exportación UE5**:
   - Exportación a `UDataTable` compatibles con widgets de interfaz `CommonUI` y plugins estándar de diálogo.

---

## 7. UAF-81.99: PHYSICS, VORONOI FRACTURING & CHAOS DESTRUCTION SYSTEM

### 7.1 Misión y Objetivos
Transformar la geometría modular estática de WFC y props ambientales en componentes reactivos destruibles mediante fracturación física de Unreal Engine Chaos.

### 7.2 Componentes Arquitectónicos
1. **Generador de Fracturas Voronoi y Planares (`VoronoiFractureEngine`)**:
   - Pre-corte procedural de piezas modulares (paredes de hormigón, columnas, cristaleras) en racimos jerárquicos (macro-pedazos estructurales y micro-escombros).
2. **Compilador de GeometryCollection (`ChaosGeometryCollectionCompiler`)**:
   - Asignación matemática de umbríos de rotura (*DamageThresholds*), densidades de masa física y campos de anclaje (*Anchor Fields*) para evitar derrumbes irreales.
3. **Dispersión de Escombros y Polvo Reactivo (`DebrisFieldEmitter`)**:
   - Generación de capas de micro-escombros estáticos y emisores de partículas Niagara de polvo tras el colapso estructural.

---

## 8. UAF-81.100: VOLUMETRIC WEATHER CYCLES, DYNAMIC DAY/NIGHT & ATMOSPHERE

### 8.1 Misión y Objetivos
Integrar los biomas ecológicos de Whittaker (UAF-81.91) con la iluminación dinámica Lumen, niebla volumétrica y ciclos climáticos realistas en Unreal Engine 5.

### 8.2 Componentes Arquitectónicos
1. **Perfiles Atmosféricos por Bioma (`BiomeAtmosphereProfile`)**:
   - Parámetros de `SkyAtmosphere`, `ExponentialHeightFog` y capas de `VolumetricCloud` calibrados para cada bioma (ventiscas polares, calimas desérticas, nieblas densas de pantano).
2. **Controlador de Ciclo Día/Noche (`DayNightCycleController`)**:
   - Trayectoria celeste calculada con dispersión física de Rayleigh y Mie, iluminación lunar nocturna y curvas de exposición ocular adaptativa.
3. **Shader Layering Climático Procedural (`EnvironmentalShaderBlender`)**:
   - Capas de material blend (*vertex color* y máscaras de altitud/pendiente) que aplican acumulación de nieve cenital, efectos de charcos y humedad de lluvia sobre todas las superficies del nivel.

---

## 9. UAF-81.101: STUDIO WEB UI & LOCAL INTERACTIVE VISUAL DASHBOARD

### 9.1 Misión y Objetivos
Proporcionar una estación de trabajo visual interactiva en navegador local (FastAPI + WebGL / Three.js) para inspeccionar mapas 3D, salas WFC, escuadras de IA y ajustar parámetros sin requerir software externo.

### 9.2 Componentes Arquitectónicos
1. **Servidor Local de Telemetría y Control (`LocalDashboardServer`)**:
   - Servicio ligero FastAPI con comunicación WebSocket para sincronización en tiempo real.
2. **Visor de Terrenos 3D WebGL (`WebGLTerrainViewer`)**:
   - Renderizado en GPU de los mapas de altura `.r16` y weightmaps con paletas de bioma y curvas de nivel en tiempo real.
3. **Inspección de Niveles WFC (`InteractiveWFCInspector`)**:
   - Explorador ortogonal e isométrico de habitaciones, puertas llave-cerradura, volúmenes de cobertura y patrullas de escuadrones GOAP.
4. **Panel de Ajustes Paramétricos & Exportación 1-Click**:
   - Controles interactivos para semillas de ruido, escalas de erosión y balance de dificultad, con botón de exportación directa a bundle UE5.

---

## 10. UAF-81.102: ONE-CLICK FULL VERTICAL SLICE BUILDER (MACRO-ORCHESTRATOR)

### 10.1 Misión y Objetivos
Diseñar el macro-orquestador definitivo que une todos los subsistemas (paisaje, interior WFC, IA de combate, economía, audio, clima y compuertas de calidad) bajo una única invocación ejecutable de punta a punta.

### 10.2 Componentes Arquitectónicos
1. **Orquestador Maestro CLI (`VerticalSliceMasterOrchestrator`)**:
   - Comando unificado: `aoe build-slice --theme <tema> --size <tamaño> --difficulty <dificultad>`.
2. **Solucionador de Restricciones Espaciales (`SpatialConstraintSolver`)**:
   - Acomoda y nivela las instalaciones WFC directamente sobre el macro-terreno erosionado, enlazando carreteras Catmull-Rom con las esclusas de acceso del búnker.
3. **Empaquetador de Mundo Unificado (`MasterPackageIntegrator`)**:
   - Genera el proyecto modular completo con subniveles para World Partition, mallas con LODs/Nanite, StateTrees y script de ingesta para Unreal Engine 5 listo para pulsar **Play**.

