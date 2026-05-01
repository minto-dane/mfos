#!/usr/bin/env python3
"""Root entrypoint for the roadmap phase-alignment check."""

from __future__ import annotations

from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parent.parent
runpy.run_path(str(ROOT / "scripts/checks/check-roadmap-phase-alignment.py"), run_name="__main__")
