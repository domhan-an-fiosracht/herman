"""Analysis message representation."""

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Self

from pydantic import ValidationError
from rich.panel import Panel
from rich.text import Text


class Severity(StrEnum):
    """Severity levels for analysis messages."""

    ERROR = "error"
    WARNING = "warning"
    NOTICE = "notice"

    @property
    def order(self) -> int:
        """Order for sorting severities."""
        return {
            Severity.ERROR: 0,
            Severity.WARNING: 1,
            Severity.NOTICE: 2,
        }[self]

    @property
    def icon(self) -> str:
        """Icon representing the severity level."""
        return {
            Severity.ERROR: "✗",
            Severity.WARNING: "⚠",
            Severity.NOTICE: "ℹ",  # noqa: RUF001
        }[self]

    @property
    def color(self) -> str:
        """Color associated with the severity level."""
        return {
            Severity.ERROR: "red",
            Severity.WARNING: "yellow",
            Severity.NOTICE: "cyan",
        }[self]

    def __lt__(self, other: Severity) -> bool:  # type: ignore[override] # ty: ignore[invalid-method-override]
        """Compare severities based on their order."""
        return self.order < other.order


@dataclass(order=True)
class AnalysisMessage:
    """Message produced during analysis."""

    sort_index: tuple[int, str, int, int, str, str] = field(init=False, repr=False)

    file: Path
    message: str
    code: str
    severity: Severity = Severity.ERROR
    line: int | None = None
    column: int | None = None

    def __post_init__(self) -> None:
        """Initialize the sort index for ordering messages."""
        self.sort_index = (
            self.severity.order,
            str(self.file),
            self.line if self.line is not None else -1,
            self.column if self.column is not None else -1,
            self.code,
            self.message,
        )

    @property
    def is_error(self) -> bool:
        """Check if the message is an error."""
        return self.severity.value == "error"

    @classmethod
    def from_text(
        cls,
        file: Path,
        message: str,
        code: str,
        severity: Severity = Severity.ERROR,
    ) -> Self:
        """Create an AnalysisMessage from plain text inputs."""
        return cls(file=file, message=message, code=code, severity=severity)

    @classmethod
    def from_pydantic_error(
        cls,
        file: Path,
        err: ValidationError,
    ) -> list["AnalysisMessage"]:
        """Convert a Pydantic ValidationError into AnalysisMessages.

        Extracts line & column if possible.
        """
        results: list[AnalysisMessage] = []

        for error in err.errors():
            loc = ".".join(str(x) for x in error["loc"])
            msg = error["msg"]

            results.append(
                AnalysisMessage(
                    file=file,
                    message=f"{loc}: {msg}",
                    code="metadata.validation",
                    severity=Severity.ERROR,
                    line=None,
                    column=None,
                ),
            )

        return results

    def to_dict(self) -> dict[str, str | int | None]:
        """JSON-friendly format."""
        return {
            "file": str(self.file),
            "message": self.message,
            "code": self.code,
            "severity": self.severity,
        }

    def to_rich(self) -> Panel:
        """Rich panel for local console output."""
        _header = Text(f"File: {self.file}", style="bold red")
        body = Text()
        if self.code:
            body.append(f"[{self.code}] ", style="yellow")
        body.append(self.message)
        return Panel(body, title=str(self.file), border_style="red")

    def to_github_annotation(self) -> str:
        """GitHub Actions annotation format."""
        code = f"[{self.code}] " if self.code else ""
        safe_msg = f"{code}{self.message}".replace("\n", " ")
        return f"::{self.severity} file={self.file}::{safe_msg}"
