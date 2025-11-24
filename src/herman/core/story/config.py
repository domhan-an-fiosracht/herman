"""Core data models for Herman."""

from ._base import HermanBaseModel


class Character(HermanBaseModel):
    """Character model representing an individual character."""

    name: str


class StoryConfig(HermanBaseModel):
    """Story configuration model."""

    characters: dict[str, Character]
