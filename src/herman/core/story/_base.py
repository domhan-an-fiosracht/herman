"""Private base model for Herman."""

from pydantic import BaseModel as PydanticBaseModel


class HermanBaseModel(
    PydanticBaseModel,
    strict=True,
    frozen=True,
    extra="forbid",
):
    """Base model with strict validation."""
