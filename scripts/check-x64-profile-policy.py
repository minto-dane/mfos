#!/usr/bin/env python3
"""Root entrypoint for the x86-64 target profile policy check."""

from __future__ import annotations

from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parent.parent
runpy.run_path(str(ROOT / "scripts/checks/check-x64-profile-policy.py"), run_name="__main__")
