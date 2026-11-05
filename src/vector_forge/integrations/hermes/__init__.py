
"""Hermes integration for Hindsight memory recall."""

from datetime import datetime
from typing import Optional

from vector_forge.models.memory import MemoryItem
from vector_forge.integrations.hermes.config import hermes_config


def _get_timestamp_prefix(item: MemoryItem) -> str:
    """
    Extract timestamp prefix for a memory item.

    Uses mentioned_at first, falls back to occurred_start.
    Returns empty string if neither is available or if feature is disabled.
    """
    if not hermes_config.recall_timestamp_prefix:
        return ""

    ts: Optional[datetime] = item.mentioned_at or item.occurred_start
    if ts is None:
        return ""
    return f"[{ts.strftime('%Y-%m-%d')}] "


def format_auto_recall_memory(item: MemoryItem) -> str:
    """
    Format a memory item for auto-recall block injection.

    Returns formatted string like "- [2026-09-22] memory text" or "- memory text".
    """
    prefix = _get_timestamp_prefix(item)
    return f"- {prefix}{item.text}"


def format_tool_memory(item: MemoryItem, index: int) -> str:
    """
    Format a memory item for hindsight_recall tool injection.

    Returns formatted string like "1. [2026-09-22] memory text" or "1. memory text".
    """
    prefix = _get_timestamp_prefix(item)
    return f"{index}. {prefix}{item.text}"
