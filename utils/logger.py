from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)


def save_result(filename: str, data: dict[str, Any]) -> None:
    path = RESULTS_DIR / filename
    path.write_text(json.dumps(data, indent=2, default=str))


def timestamp() -> str:
    return datetime.now().isoformat(timespec="seconds")
