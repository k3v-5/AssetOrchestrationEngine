# AOE AnimGraph Bridge Plugin

## Objetivo
Este plugin es el puente en tiempo de edición (Editor-Only) necesario para el motor Asset Orchestration Engine (AOE) v1.0. Expone funcionalidades de C++ hacia la API de Python de Unreal Engine 5, resolviendo la limitación nativa que impide crear, modificar o enlazar nodos visuales dentro del `AnimGraph` utilizando exclusivamente scripts de Python.

## Características
- **Inyección Cero-Riesgo:** Localiza el `Output Pose` del grafo, desconecta la cadena anterior, inserta el nuevo nodo y re-conecta. Nunca elimina el trabajo previo (State Machines, IK, etc).
- **Soft-Dependency para KawaiiPhysics:** El código está escrito de tal forma que no causará errores de compilador (linker errors) si descargas este plugin y no tienes `KawaiiPhysics` instalado. En su lugar, simplemente imprimirá una advertencia amarilla en consola sugiriendo su instalación.

## Uso desde Python (AOE Orchestrator)

El script autogenerado por AOE (`ue5_import_orchestrator.py`) ya contiene la llamada correcta, la cual se ve así:

```python
import unreal

# Asegúrate de tener cargado tu UAnimBlueprint en la variable 'abp'
bone_name = "hair_root_01"
physics_type = "KawaiiPhysics" # o "AnimDynamics"
stiffness = 0.5
damping = 0.2

try:
    success = unreal.AnimGraphEditorExtensions.create_and_wire_physics_node(abp, bone_name, physics_type, stiffness, damping)
    if not success:
        unreal.log_warning("El nodo no se inyectó. Revise si el plugin requerido está habilitado.")
except Exception as e:
    unreal.log_error(f"Error llamando al puente de C++: {e}")
```

## Instalación en tu Proyecto de Unreal Engine 5
1. Copia la carpeta `AOE_AnimGraphBridge` dentro de la carpeta `Plugins/` de tu proyecto de Unreal Engine 5 (ej. `MiJuego/Plugins/AOE_AnimGraphBridge/`).
2. Haz clic derecho sobre tu archivo `.uproject` y selecciona **"Generate Visual Studio project files"**.
3. Abre el proyecto en Visual Studio / Rider y compílalo (Build).
4. Abre el Unreal Editor. Asegúrate de tener activos:
   - `Python Editor Script Plugin`
   - `KawaiiPhysics` (si vas a utilizar físicas estilo Anime).
