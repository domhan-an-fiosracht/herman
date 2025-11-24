"""GitHub output renderer for analysis messages."""

from collections.abc import Iterable

from herman.core import AnalysisMessage


def render_github(messages: Iterable[AnalysisMessage]) -> None:
    """Render analysis messages as GitHub annotations."""
    messages_sorted = sorted(messages)

    for message in messages_sorted:
        severity = message.severity.value
        file_part = f"file={message.file}"
        line_part = f",line={message.line}" if message.line is not None else ""
        column_part = f",col={message.column}" if message.column is not None else ""

        # GitHub annotations don't support icons well; leave the main string clean
        annotation_text = f"[{message.code}] {message.message}"

        print(f"::{severity} {file_part}{line_part}{column_part}::{annotation_text}")
