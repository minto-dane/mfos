#!/usr/bin/env python3
"""Root entrypoint for the architecture portability policy check."""

from __future__ import annotations

from pathlib import Path
import runpy


TARGET = Path(__file__).resolve().parent / "checks/check-architecture-portability-policy.py"
runpy.run_path(str(TARGET), run_name="__main__")
