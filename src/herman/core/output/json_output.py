"""JSON output renderer for analysis messages."""

import json
from collections.abc import Iterable

from herman.core import AnalysisMessage


def render_json(messages: Iterable[AnalysisMessage]) -> None:
    """Render analysis messages as JSON."""
    json_ready: list[dict[str, str | int | None]] = [
        {
            "file": str(message.file),
            "line": message.line,
            "column": message.column,
            "severity": message.severity.value,
            "code": message.code,
            "message": message.message,
        }
        for message in sorted(messages)
    ]

    print(json.dumps(json_ready, indent=2))
