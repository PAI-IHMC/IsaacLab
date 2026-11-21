# Copyright (c) 2022-2026, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""App-free checks that every Kit app using the Fabric Scene Delegate enables material merging."""

from __future__ import annotations

import re
from pathlib import Path

_APPS_DIR = Path(__file__).resolve().parents[4] / "apps"

_FSD_KEY = "app.useFabricSceneDelegate"
_MERGE_MATERIALS_KEY = "app.usdrt.population.utils.mergeMaterials"


def _kit_value(content: str, key: str) -> str | None:
    """Return the value assigned to ``key`` (comment stripped), or ``None`` if unset."""
    match = re.search(rf"^\s*{re.escape(key)}\s*=\s*(.+?)\s*$", content, re.MULTILINE)
    if match is None:
        return None
    return match.group(1).split("#", 1)[0].strip()


def _fsd_kits() -> list[Path]:
    """Return the Kit app files under ``apps/`` that enable the Fabric Scene Delegate."""
    return [path for path in sorted(_APPS_DIR.glob("*.kit")) if _kit_value(path.read_text(), _FSD_KEY) == "true"]


def test_fsd_kits_exist():
    """At least one Kit app enables the Fabric Scene Delegate, so the merge check below is not vacuous."""
    assert _fsd_kits(), f"No Kit app under {_APPS_DIR} sets {_FSD_KEY} = true"


def test_fsd_kits_enable_material_merging():
    """Every Kit app that enables the Fabric Scene Delegate also enables material merging."""
    missing = [path.name for path in _fsd_kits() if _kit_value(path.read_text(), _MERGE_MATERIALS_KEY) != "true"]
    assert not missing, f"Kit apps enable {_FSD_KEY} without {_MERGE_MATERIALS_KEY} = true: {missing}"
