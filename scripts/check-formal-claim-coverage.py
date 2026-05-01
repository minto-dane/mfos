#!/usr/bin/env python3
"""Root wrapper for the formal claim coverage check."""

from __future__ import annotations

from pathlib import Path
import runpy


TARGET = Path(__file__).resolve().parent / "checks/formal-claims/check-formal-claim-coverage.py"
runpy.run_path(str(TARGET), run_name="__main__")
