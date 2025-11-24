"""CLI output renderers for analysis messages."""

from collections.abc import Iterable
from itertools import groupby
from operator import attrgetter

from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text

from herman.core import AnalysisMessage


def render_full(messages: Iterable[AnalysisMessage]) -> None:
    """Pretty, grouped, human-oriented output.

    Includes:
      - Rich panels
      - Icons
      - Colors
      - Footer summary per file
      - Line/column info
      - Grouping by file
    """
    console = Console()
    messages_sorted = sorted(messages)

    # No issues
    if not messages_sorted:
        console.print(
            Panel(
                "[bold green]✓ No issues found[/bold green]",
                border_style="green",
                padding=0,
            ),
        )
        return

    # Group by file
    for file_path, file_group_iter in groupby(messages_sorted, key=attrgetter("file")):
        file_messages = list(file_group_iter)

        # Build the body text
        body = Text()

        error_count = sum(m.severity.value == "error" for m in file_messages)
        warning_count = sum(m.severity.value == "warning" for m in file_messages)
        notice_count = sum(m.severity.value == "notice" for m in file_messages)

        for message in file_messages:
            severity_icon = message.severity.icon
            severity_color = message.severity.color

            prefix = Text(f"{severity_icon} [{message.code}] ", style=severity_color)
            message_text = Text(message.message, style="white")

            # Append location information if present
            if message.line is not None:
                loc = f" (line {message.line}"
                if message.column is not None:
                    loc += f", col {message.column}"
                loc += ")"
                message_text.append(loc, style="dim")

            body.append_text(prefix)
            body.append_text(message_text)
            body.append("\n")

        # Footer summary
        footer_parts: list[str] = []
        if error_count:
            footer_parts.append(
                f"✗ {error_count} error{'s' if error_count != 1 else ''}",
            )
        if warning_count:
            footer_parts.append(
                f"⚠ {warning_count} warning{'s' if warning_count != 1 else ''}",
            )
        if notice_count:
            footer_parts.append(
                f"ℹ {notice_count} notice{'s' if notice_count != 1 else ''}",  # noqa: RUF001
            )

        subtitle = " • ".join(footer_parts)

        console.print(
            Panel(
                body,
                title=Text(str(file_path), style=Style(bold=True, color="white")),
                title_align="left",
                subtitle=subtitle,
                subtitle_align="right",
                border_style="red",
                padding=0,
            ),
        )


def render_concise(messages: Iterable[AnalysisMessage]) -> None:
    """Compact, grep-friendly format.

    Prints one line per diagnostic:

        path:line:col: severity [code] message

    No icons, no colors, no grouping, no panels.
    """
    messages_sorted = sorted(messages)

    for message in messages_sorted:
        file_path = str(message.file)

        line = message.line if message.line is not None else 0
        column = message.column if message.column is not None else 0

        severity = message.severity.value
        code = message.code
        text = message.message

        print(f"{file_path}:{line}:{column}: {severity} [{code}] {text}")
