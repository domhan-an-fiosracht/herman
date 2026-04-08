"""Lint-related CLI commands."""

from pathlib import Path

import frontmatter
from pydantic import ValidationError

from herman.core import (
    AnalysisMessage,
    Severity,
    StoryConfig,
    StoryFileMetadata,
)


def lint_file(config: StoryConfig, file: Path) -> list[AnalysisMessage]:
    """Verify the metadata of a single story Markdown file."""
    messages: list[AnalysisMessage] = []
    post = frontmatter.load(str(file))

    try:
        metadata = StoryFileMetadata.model_validate(post.metadata)
    except ValidationError as ve:
        messages.extend(AnalysisMessage.from_pydantic_error(file, ve))
        return messages

    for slug in metadata.characters:
        if slug not in config.characters:
            messages.append(  # noqa: PERF401
                AnalysisMessage(
                    file=file,
                    message=f"Unknown character slug '{slug}'",
                    code="character.unknown",
                    severity=Severity.ERROR,
                ),
            )

    return messages


def lint_all_files(config: StoryConfig) -> list[AnalysisMessage]:
    """Return a list of all lint errors across story Markdown files."""
    results: list[AnalysisMessage] = []
    files = sorted(Path("story").glob("**/*.md"))

    for file in files:
        messages = lint_file(config, file)
        results.extend(messages)

    return results
