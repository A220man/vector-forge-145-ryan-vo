
"""Hermes integration configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings


class HermesConfig(BaseSettings):
    """Hermes integration configuration."""

    recall_timestamp_prefix: bool = Field(
        default=False,
        description="Prefix recalled memories with [YYYY-MM-DD] timestamp",
    )

    class Config:
        env_prefix = "HERMES_"
        case_sensitive = False


hermes_config = HermesConfig()
