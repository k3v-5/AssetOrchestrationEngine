# Asset Orchestration Engine (AOE) 🚀
**Autonomous, Deterministic 3D & Audio Asset Generation, Validation, and Optimization Pipeline**

[![Tests](https://img.shields.io/badge/Tests-1382%20Passed-brightgreen)](tests/)
[![Phases](https://img.shields.io/badge/Phases-F1--F80-blue)](docs/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Blender](https://img.shields.io/badge/Blender-4.x%20%2F%205.x-orange.svg)](https://www.blender.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🌟 Overview

The **Asset Orchestration Engine (AOE)** is an industrial-grade orchestration system that converts high-level natural language intents or technical specifications into production-ready 3D models, procedural meshes, PBR shaders, and sound effects for game engines (**Unreal Engine 5**, Unity, Godot).

Originally engineered for the AAA action game *DarX*, AOE is completely standalone and decoupled, enabling studio-grade autonomous generative pipelines in any game project or 3D production studio.

```
                  ┌─────────────────────────────────────┐
                  │    NATURAL INTENT / SPECIFICATION   │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                  ┌─────────────────────────────────────┐
                  │      INTENT COMPILER (F51/F71)      │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                  ┌─────────────────────────────────────┐
                  │   STRATEGY OPTIMIZER (F78/F79)      │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                  ┌─────────────────────────────────────┐
                  │   BLENDER MCP EXECUTION RUNTIME     │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                  ┌─────────────────────────────────────┐
                  │    AUTOMATED QA & CRITIC (F75-F77)  │
                  └──────────────────┬──────────────────┘
                                     │
                                     ▼
                  ┌─────────────────────────────────────┐
                  │  DELIVERY & PACKAGING (FBX/PBR/UE5) │
                  └─────────────────────────────────────┘
```

---

## 🎮 Production In Action: DarX Game Showcase (Before vs After)

> **Live Industry Proof**: AOE powers the asset generation and modernization pipeline of **DarX**, a first-person tactical sci-fi action/horror game currently in active development for **Unreal Engine 5 (UE5.5)**.

By leveraging AOE's procedural geometry generators, PBR material compilers, and deterministic zero-clipping spatial solvers, **16 entire character and boss entities** (6 main bosses and 10 combat troops) were transformed from rudimentary prototype whiteboxes into AAA production-ready skeletal meshes in seconds:

| Prototype Whitebox (Before) | AOE Production-Ready Asset (After) |
| :---: | :---: |
| *Crude box/sphere geometry, clipping artifacts, flat uncalibrated shaders* | *Bespoke silhouettes, military graphene/chrome PBR, zero-clipping guarantees* |

### 📸 Highlight Showcase:

#### 🤖 Containment Robot Boss (Boss 1)
![Boss 1: Before vs After](docs/images/case_studies_darx/boss1_antes_vs_despues.png)

#### ⚠️ THE ERROR Quantum Glitch Entity (Boss 2)
![Boss 2: Before vs After](docs/images/case_studies_darx/boss2_antes_vs_despues.png)

#### 👁️ The Observer Aerospace Drone (Troop 6)
![Observador: Before vs After](docs/images/case_studies_darx/observador_antes_vs_despues.png)

#### 💥 The Repulsor Kinetic Enforcer (Troop 8)
![Repulsor: Before vs After](docs/images/case_studies_darx/repulsor_antes_vs_despues.png)

#### 👤 The Static Shadow Glitch Demon (Troop 10)
![Static Shadow: Before vs After](docs/images/case_studies_darx/static_shadow_antes_vs_despues.png)

👉 **[Explore Full Case Study & All 16 Before vs After Comparisons](docs/DARX-PRODUCTION-CASE-STUDY.md)**

---

## 🛠️ Key Capabilities (Fases 1 to 80)

1. **Deterministic Intent Compilation**: Translates human/AI descriptions into geometric blueprints (`SemanticMeshSpec`, bounding volumes, socket definitions, and PBR node graphs).
2. **Strategy & Cost Optimizer**: Evaluates polycount, draw calls, synthesis time, memory footprint, and quality risk to select the optimal generation path.
3. **Blender MCP Integration**: Direct bridge with Blender 4.x/5.x via Model Context Protocol (MCP) or background batch runner (`blender -b`).
4. **Automated Visual & Geometric Critic**: Real-time evaluation of manifold integrity, watertightness, UV overlap, vertex density, and aesthetic symmetry.
5. **Self-Correction & Autonomous Recovery**: Automated patch generation for failed booleans, non-manifold edges, or texture baking errors without manual intervention.
6. **Multi-View Previsualization Engine**: Produces 4-quadrant orthogonal and action renders (Front, Back, 3/4 Action, FPS View) before exporting to game engine.

---

## 📁 Repository Structure

```
AssetOrchestrationEngine/
├── src/                         # Core AOE Engine (80 submodules)
│   ├── production_orchestration/# F80 Production Pipeline (19-stage orchestrator)
│   ├── cost_performance/       # F79 Multi-objective Cost/Performance Optimizer
│   ├── strategy_learning/      # F78 Historical Strategy Learning & Knowledge Base
│   ├── failure_analysis/       # F77 Semantic Failure Diagnosis & Root Cause
│   ├── autonomous_correction/  # F76 Automated Geometry & Shader Patcher
│   ├── automated_visual_eval/  # F75 PBR & Geometric Quality Scorer
│   ├── intent_compiler/        # F51/F71 Prompt to Mesh Specification Compiler
│   ├── tool_governance/        # F49 ResourceLockManager & ToolGuard
│   ├── blender/                # Blender Python bridge and operators
│   └── unreal/                 # Unreal Engine 5 export & bridge manifests
├── scripts/                     # Standalone generators & procedural builders
│   ├── blender_player_skin_*.py# Humanoid character & fluid runners
│   ├── blender_futuristic_*.py # Sci-fi firearms & energy weapons
│   └── test_*.py               # Diagnostic and verification tools
├── tests/                       # Complete Test Suite (1382 Automated Tests)
├── docs/                        # Complete Engineering Documentation
│   ├── ASSET-ORCHESTRATION-ENGINE-MASTER.md # Architecture Bible
│   ├── AI-AGENT-OPERATIONAL-GUIDE.md        # How AI Assistants operate AOE
│   ├── F80-PRODUCTION-ORCHESTRATION-VALIDATION.md
│   └── REGLAS-DE-TRABAJO.md
├── mcp/                         # Model Context Protocol Server & Addons
│   └── blender/
│       ├── blender_mcp_addon.py # Blender Addon (GUI/Background)
│       └── schemas/             # JSON schemas for MCP tools
├── runner.py                    # Global test runner
├── pyproject.toml               # Python package configuration
└── requirements.txt             # Dependencies
```

---

## 🚀 Quickstart Guide

### 1. Installation

```bash
git clone https://github.com/YourOrg/AssetOrchestrationEngine.git
cd AssetOrchestrationEngine
pip install -r requirements.txt
```

### 2. Run Test Suite

Verify the entire 80-phase engine integrity:
```bash
python runner.py
# or
python -m unittest discover -s tests -p "test_*.py"
```

### 3. Generate a 3D Asset via Python API

```python
from src.production_orchestration import ProductionOrchestrator, ProductionRequest

# Initialize the 19-stage orchestrator
orchestrator = ProductionOrchestrator()

# Dispatch an asset generation request
request = ProductionRequest(
    request_id="REQ_WEAPON_001",
    intent_prompt="Futuristic ceramic white rifle with cyan neon emissive strips and dark carbon accents",
    asset_category="Weapon",
    target_engine="UnrealEngine5",
    max_triangles=25000
)

result = orchestrator.execute_pipeline(request)
print(f"Asset Status: {result.status} (Quality Score: {result.quality_score}/100)")
print(f"Output Model: {result.exported_fbx_path}")
```

### 4. Headless Blender Generation

Execute any asset script directly via Blender:
```bash
blender.exe -b base.blend --python scripts/blender_futuristic_white_weapon.py -- --preview-output render.png
```

---

## 🤖 AI Agent Integration (Cursor, Claude, Copilot, Antigravity)

The AOE is designed from the ground up to allow AI coding assistants to produce production-ready 3D models with **single-turn batch commands**, saving up to **80% of context tokens**.

See [docs/AI-AGENT-OPERATIONAL-GUIDE.md](docs/AI-AGENT-OPERATIONAL-GUIDE.md) for full instructions, prompt templates, and execution protocols.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
