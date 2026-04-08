"""Core data models for Herman."""

from ._base import HermanBaseModel


class Character(HermanBaseModel, frozen=True):
    """Character model representing an individual character."""

    name: str


class StoryConfig(HermanBaseModel, frozen=True):
    """Story configuration model."""

    characters: dict[str, Character]
