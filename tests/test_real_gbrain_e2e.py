from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "lean_closeout.py"


def checkpoint() -> dict:
    return {
        "schema_version": 1,
        "workstream": "real-gbrain-e2e",
        "objective": "Verify the real GBrain CLI persistence contract",
        "what_happened": ["Initialized an isolated PGLite brain without embeddings."],
        "decisions": [],
        "current_state": "done",
        "blockers": [],
        "next_action": {"summary": "No pending action; this terminal can close."},
        "active_work": [],
        "references": [],
        "safety": {"contains_secrets": False, "contains_phi": False},
    }


@unittest.skipUnless(
    os.environ.get("LEAN_RUN_REAL_GBRAIN_E2E") == "1",
    "set LEAN_RUN_REAL_GBRAIN_E2E=1 to test the installed gbrain CLI",
)
class RealGBrainE2ETests(unittest.TestCase):
    def test_isolated_pglite_round_trip_and_idempotency(self) -> None:
        gbrain = shutil.which("gbrain")
        self.assertIsNotNone(gbrain, "gbrain must be installed for this opt-in test")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            brain_home = root / "gbrain-home"
            project = root / "project"
            memory = root / "memory"
            input_path = root / "checkpoint.json"
            isolated_home = root / "home"
            isolated_tmp = root / "tmp"
            project.mkdir()
            isolated_home.mkdir()
            isolated_tmp.mkdir()
            input_path.write_text(json.dumps(checkpoint()))

            environment = {
                "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
                "GBRAIN_HOME": str(brain_home),
                "HOME": str(isolated_home),
                "TMPDIR": str(isolated_tmp),
                "LANG": os.environ.get("LANG", "C.UTF-8"),
            }

            initialized = subprocess.run(
                [gbrain, "init", "--pglite", "--no-embedding"],
                capture_output=True,
                text=True,
                env=environment,
                timeout=30,
                check=False,
            )
            self.assertEqual(initialized.returncode, 0, initialized.stderr)

            command = [
                sys.executable,
                str(SCRIPT),
                "--input",
                str(input_path),
                "--project-root",
                str(project),
                "--memory-dir",
                str(memory),
                "--gbrain-bin",
                gbrain,
            ]
            first = subprocess.run(
                command,
                capture_output=True,
                text=True,
                env=environment,
                timeout=30,
                check=False,
            )
            second = subprocess.run(
                command,
                capture_output=True,
                text=True,
                env=environment,
                timeout=30,
                check=False,
            )
            first_receipt = json.loads(first.stdout)
            second_receipt = json.loads(second.stdout)

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertTrue(first_receipt["safe_to_clear"])
            self.assertEqual(first_receipt["gbrain"]["timeline"], "recorded")
            self.assertEqual(second_receipt["gbrain"]["timeline"], "already_recorded")
            self.assertEqual(first_receipt["checkpoint_id"], second_receipt["checkpoint_id"])
