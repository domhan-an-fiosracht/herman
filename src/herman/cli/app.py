"""Main CLI application definition."""

import tomllib
from dataclasses import dataclass
from pathlib import Path

import typer
from typer import Context as TyperContext
from typer import Option

from herman.core import (
    AnalysisMessage,
    OutputFormat,
    Severity,
    StoryConfig,
)
from herman.core.analysis.rules import lint_all_files, lint_file
from herman.core.handlers import report_and_exit

app = typer.Typer()


@dataclass(frozen=True, slots=True)
class Context:
    """Global CLI context object."""

    config: StoryConfig
    output_format: OutputFormat | None


@app.callback()
def main(
    ctx: TyperContext,
    config_file: Path = Option("story.toml", help="Path to story config"),
    output_format: OutputFormat | None = Option(
        None,
        "--output-format",
        help="Output format",
    ),
) -> None:
    """Hi I'm Herman."""
    config = StoryConfig.model_validate(tomllib.loads(config_file.read_text()))
    ctx.obj = Context(config=config, output_format=output_format)


@app.command()
def build_llm_text_files(_ctx: TyperContext) -> None:
    """Build text files for LLM processing."""
    path = Path("out/llm-text")
    path.mkdir(exist_ok=True, parents=True)
    files = sorted(Path("story").glob("**/*.md"))
    with (path / "full-story.md").open("w", encoding="utf-8") as out_file:
        for file in files:
            content = file.read_text(encoding="utf-8")
            out_file.write(f"\n---\n\n{content}")


@app.command()
def lint(
    ctx: TyperContext,
    file: Path | None = typer.Argument(
        None,
        help="Optional path to a single Markdown file to lint.",
        exists=False,
    ),
) -> None:
    """Verify metadata across all story Markdown files."""
    cfg = ctx.obj.config
    output_format = ctx.obj.output_format

    if file is not None and not file.exists():
        messages = [
            AnalysisMessage(
                file=file,
                message="File does not exist.",
                code="io.not_found",
                severity=Severity.ERROR,
            ),
        ]
        report_and_exit(messages=messages, output_format=output_format)

    if file:  # noqa: SIM108
        messages = lint_file(cfg, file)
    else:
        messages = lint_all_files(cfg)

    report_and_exit(messages=messages, output_format=output_format)
