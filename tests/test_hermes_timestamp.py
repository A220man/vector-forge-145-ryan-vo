
"""Tests for Hermes integration timestamp prefix feature."""

from datetime import UTC, datetime
from unittest.mock import patch

from vector_forge.integrations.hermes import (
    format_auto_recall_memory,
    format_tool_memory,
)
from vector_forge.integrations.hermes.config import hermes_config
from vector_forge.models.memory import MemoryItem


def test_format_auto_recall_memory_no_prefix_by_default():
    """Auto-recall memory should not have prefix when feature is disabled."""
    item = MemoryItem(
        text="User prefers dark mode",
        bank_id="test-bank",
        mentioned_at=datetime(2026, 9, 22, 10, 30, tzinfo=UTC),
    )
    result = format_auto_recall_memory(item)
    assert result == "- User prefers dark mode"


def test_format_auto_recall_memory_with_mentioned_at():
    """Auto-recall memory should use mentioned_at when prefix enabled."""
    with patch.object(hermes_config, "recall_timestamp_prefix", True):
        item = MemoryItem(
            text="User prefers dark mode",
            bank_id="test-bank",
            mentioned_at=datetime(2026, 9, 22, 10, 30, tzinfo=UTC),
        )
        result = format_auto_recall_memory(item)
        assert result == "- [2026-09-22] User prefers dark mode"


def test_format_auto_recall_memory_fallback_to_occurred_start():
    """Auto-recall memory should fall back to occurred_start when mentioned_at is None."""
    with patch.object(hermes_config, "recall_timestamp_prefix", True):
        item = MemoryItem(
            text="User works in UTC-5",
            bank_id="test-bank",
            mentioned_at=None,
            occurred_start=datetime(2026, 8, 15, 14, 0, tzinfo=UTC),
        )
        result = format_auto_recall_memory(item)
        assert result == "- [2026-08-15] User works in UTC-5"


def test_format_auto_recall_memory_no_timestamp_available():
    """Auto-recall memory should not have prefix when no timestamp available."""
    with patch.object(hermes_config, "recall_timestamp_prefix", True):
        item = MemoryItem(
            text="User likes Python",
            bank_id="test-bank",
            mentioned_at=None,
            occurred_start=None,
        )
        result = format_auto_recall_memory(item)
        assert result == "- User likes Python"


def test_format_tool_memory_no_prefix_by_default():
    """Tool memory should not have prefix when feature is disabled."""
    item = MemoryItem(
        text="User prefers dark mode",
        bank_id="test-bank",
        mentioned_at=datetime(2026, 9, 22, 10, 30, tzinfo=UTC),
    )
    result = format_tool_memory(item, 1)
    assert result == "1. User prefers dark mode"


def test_format_tool_memory_with_mentioned_at():
    """Tool memory should use mentioned_at when prefix enabled."""
    with patch.object(hermes_config, "recall_timestamp_prefix", True):
        item = MemoryItem(
            text="User prefers dark mode",
            bank_id="test-bank",
            mentioned_at=datetime(2026, 9, 22, 10, 30, tzinfo=UTC),
        )
        result = format_tool_memory(item, 1)
        assert result == "1. [2026-09-22] User prefers dark mode"


def test_format_tool_memory_fallback_to_occurred_start():
    """Tool memory should fall back to occurred_start when mentioned_at is None."""
    with patch.object(hermes_config, "recall_timestamp_prefix", True):
        item = MemoryItem(
            text="User works in UTC-5",
            bank_id="test-bank",
            mentioned_at=None,
            occurred_start=datetime(2026, 8, 15, 14, 0, tzinfo=UTC),
        )
        result = format_tool_memory(item, 2)
        assert result == "2. [2026-08-15] User works in UTC-5"


def test_format_tool_memory_no_timestamp_available():
    """Tool memory should not have prefix when no timestamp available."""
    with patch.object(hermes_config, "recall_timestamp_prefix", True):
        item = MemoryItem(
            text="User likes Python",
            bank_id="test-bank",
            mentioned_at=None,
            occurred_start=None,
        )
        result = format_tool_memory(item, 3)
        assert result == "3. User likes Python"


def test_config_reads_from_env():
    """Config should read HERMES_RECALL_TIMESTAMP_PREFIX from environment."""
    import os

    os.environ["HERMES_RECALL_TIMESTAMP_PREFIX"] = "true"
    try:
        from vector_forge.integrations.hermes.config import HermesConfig

        config = HermesConfig()
        assert config.recall_timestamp_prefix is True
    finally:
        del os.environ["HERMES_RECALL_TIMESTAMP_PREFIX"]
