#!/usr/bin/env python3
"""Root wrapper for the Phase 1.3 Dataset/Catalog coverage check."""

from __future__ import annotations

from pathlib import Path
import runpy


TARGET = Path(__file__).resolve().parent / "phases/phase-1/check-phase1-3-dataset-catalog-coverage.py"
runpy.run_path(str(TARGET), run_name="__main__")
