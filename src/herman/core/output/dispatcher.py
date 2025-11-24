"""Dispatcher for rendering analysis messages in various formats."""

from typing import Literal

from herman.core import AnalysisMessage

from .cli_output import render_concise, render_full
from .github_output import render_github
from .json_output import render_json

OutputFormat = Literal["full", "concise", "json", "github"]


def render_messages(
    messages: list[AnalysisMessage],
    *,
    output_format: OutputFormat | None,
) -> int:
    """Select a renderer and execute it.

    - If `format` is provided explicitly, use that.
    - Otherwise auto-detect:
        - If running in CI, use GitHub annotations.
        - Else fallback to Rich console renderer.
    """
    if output_format is not None:
        match output_format:
            case "full":
                render_full(messages)
            case "concise":
                render_concise(messages)
            case "json":
                render_json(messages)
            case "github":
                render_github(messages)
            case _:
                msg = f"Unknown output format specified: {output_format}"
                raise ValueError(msg)
    else:
        render_full(messages)

    return 1 if any(m.severity == "error" for m in messages) else 0
