from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.core.config import settings


def append_jsonl(filename: str, payload: dict[str, Any]) -> None:
    settings.logs_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        **payload,
    }
    output_path = Path(settings.logs_dir) / filename
    with output_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=True) + "\n")
