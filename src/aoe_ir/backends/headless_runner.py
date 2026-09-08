import os
import subprocess
import json
import logging
from typing import Dict, Any, Optional

class BlenderHeadlessRunner:
    """Runs a python script inside a headless Blender instance."""

    def __init__(self, blender_path: str = "blender"):
        self.blender_path = blender_path

    def check_availability(self) -> bool:
        try:
            result = subprocess.run([self.blender_path, "--version"], capture_output=True, text=True, check=True)
            return "Blender" in result.stdout
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def run_script(self, script_path: str, args: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Runs the script inside Blender and reads the result from stdout JSON."""

        cmd = [
            self.blender_path,
            "--background",
            "--python", script_path
        ]

        if args:
            # Pass args via environment variable for simplicity
            env = os.environ.copy()
            env["AOE_BLENDER_ARGS"] = json.dumps(args)
        else:
            env = os.environ.copy()

        logging.info(f"Launching Blender Headless: {' '.join(cmd)}")

        result = subprocess.run(cmd, env=env, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Blender crashed or script failed (Exit code: {result.returncode}):\n{result.stderr}\n{result.stdout}")

        # Parse output looking for the AOE_RESULT JSON marker
        for line in result.stdout.splitlines():
            if line.startswith("AOE_RESULT:"):
                return json.loads(line.replace("AOE_RESULT:", "").strip())

        return {"status": "SUCCESS", "message": "No JSON result found, but exited with 0", "stdout": result.stdout}
