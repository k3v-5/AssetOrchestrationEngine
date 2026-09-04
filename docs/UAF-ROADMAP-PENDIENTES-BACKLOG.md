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
