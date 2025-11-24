"""Handler for command results processing."""

from collections.abc import Iterable

from herman.core import (
    AnalysisMessage,
    OutputFormat,
    render_messages,
)


def report_and_exit(
    *,
    messages: Iterable[AnalysisMessage] | None = None,
    output_format: OutputFormat | None = None,
) -> None:
    """Render messages (if any), compute exit code, and exit."""
    messages_list = list(messages or [])

    if messages_list:
        render_messages(messages_list, output_format=output_format)

    has_errors = any(msg.is_error for msg in messages_list)
    exit_code = 1 if has_errors else 0

    raise SystemExit(exit_code)
