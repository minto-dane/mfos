#!/usr/bin/env python3
"""Root wrapper for the Phase 1.4.1 Job/DD coverage check."""

from __future__ import annotations

from pathlib import Path
import runpy


TARGET = Path(__file__).resolve().parent / "phases/phase-1/check-phase1-4-1-job-dd-coverage.py"
runpy.run_path(str(TARGET), run_name="__main__")
