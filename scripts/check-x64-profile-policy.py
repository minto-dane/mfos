#!/usr/bin/env python3
"""Root entrypoint for the x86-64 target profile policy check."""

from __future__ import annotations

from pathlib import Path
import runpy


TARGET = Path(__file__).resolve().parent / "checks/check-x64-profile-policy.py"
runpy.run_path(str(TARGET), run_name="__main__")
