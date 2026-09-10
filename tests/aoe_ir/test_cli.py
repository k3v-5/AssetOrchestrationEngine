import unittest
import subprocess
import tempfile
import json
import os

class TestCLI(unittest.TestCase):
    def test_build_batch_cli(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            input_file = os.path.join(tmpdir, "input.json")
            output_dir = os.path.join(tmpdir, "out")

            # Create mock batch config
            batch_config = {
                "batch_id": "cli_test_batch",
                "recipes": [
                    {"recipe_id": "Ninja", "base_mesh": "ninja.fbx", "appearance_id": "ninja_app"},
                    {"recipe_id": "Samurai", "base_mesh": "samurai.fbx", "appearance_id": "samurai_app"}
                ]
            }

            with open(input_file, 'w') as f:
                json.dump(batch_config, f)

            # Run CLI script
            cmd = ["python", "-m", "aoe_cli", "build_batch", "--input", input_file, "--output", output_dir]
            result = subprocess.run(cmd, capture_output=True, text=True)

            self.assertEqual(result.returncode, 0, f"CLI Failed: {result.stderr}")
            self.assertIn("Pipeline Execution Complete!", result.stderr)



if __name__ == '__main__':
    unittest.main()
