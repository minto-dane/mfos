#!/usr/bin/env python3
"""Root entrypoint for the roadmap phase-alignment check."""

from __future__ import annotations

from pathlib import Path
import runpy


TARGET = Path(__file__).resolve().parent / "checks/check-roadmap-phase-alignment.py"
runpy.run_path(str(TARGET), run_name="__main__")
