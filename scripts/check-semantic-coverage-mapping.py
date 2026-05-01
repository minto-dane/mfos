#!/usr/bin/env python3
"""Root wrapper for the semantic coverage mapping check."""

from __future__ import annotations

from pathlib import Path
import runpy


TARGET = Path(__file__).resolve().parent / "checks/semantic-coverage/check-semantic-coverage-mapping.py"
runpy.run_path(str(TARGET), run_name="__main__")
