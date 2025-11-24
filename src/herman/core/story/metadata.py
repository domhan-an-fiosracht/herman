"""Core data models for Herman."""

from datetime import date

from pydantic import Field

from ._base import HermanBaseModel


class StoryFileMetadata(HermanBaseModel):
    """Metadata for a story file."""

    title: str | None = None
    date_: date = Field(alias="date")
    scene_dates: str | None = None
    perspective: str
    characters: list[str]
