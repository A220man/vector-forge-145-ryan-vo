"""Tests for Cohere-compatible reranker response parsing."""

from vector_forge.engine.cross_encoder import _CohereCompatibleRerankClient


def test_relevance_score_field():
    """Shape 1: {results: [{"index": int, "relevance_score": float}, ...]}"""
    result = {
        "results": [
            {"index": 2, "relevance_score": 0.95},
            {"index": 0, "relevance_score": 0.85},
            {"index": 1, "relevance_score": 0.72},
        ]
    }
    scores = _CohereCompatibleRerankClient.predict(result)
    assert scores == {2: 0.95, 0: 0.85, 1: 0.72}


def test_score_alias():
    """Shape 2: {results: [{"index": int, "score": float}, ...]} (score alias)"""
    result = {
        "results": [
            {"index": 2, "score": 0.95},
            {"index": 0, "score": 0.85},
            {"index": 1, "score": 0.72},
        ]
    }
    scores = _CohereCompatibleRerankClient.predict(result)
    assert scores == {2: 0.95, 0: 0.85, 1: 0.72}


def test_scores_indices_array_shape():
    """Shape 3: {scores: [float, ...], indices: [int, ...]}"""
    result = {
        "scores": [0.95, 0.85, 0.72],
        "indices": [2, 0, 1],
    }
    scores = _CohereCompatibleRerankClient.predict(result)
    assert scores == {2: 0.95, 0: 0.85, 1: 0.72}


def test_score_alias_with_relevance_score_takes_precedence():
    """If both 'score' and 'relevance_score' exist, relevance_score wins."""
    result = {
        "results": [
            {"index": 0, "relevance_score": 0.90, "score": 0.50},
            {"index": 1, "score": 0.80},
        ]
    }
    scores = _CohereCompatibleRerankClient.predict(result)
    # relevance_score takes precedence over score alias
    assert scores == {0: 0.90, 1: 0.80}


def test_skips_negative_indices():
    """Negative indices should be skipped, not crash."""
    result = {
        "results": [
            {"index": -1, "relevance_score": 0.95},
            {"index": 0, "relevance_score": 0.85},
        ]
    }
    scores = _CohereCompatibleRerankClient.predict(result)
    assert scores == {0: 0.85}  # -1 is skipped


def test_skips_out_of_range_indices():
    """Indices beyond reasonable range should be skipped."""
    result = {
        "results": [
            {"index": 5, "relevance_score": 0.95},  # valid
            {"index": 999, "relevance_score": 0.50},  # out of range, skip
        ]
    }
    scores = _CohereCompatibleRerankClient.predict(result)
    assert scores == {5: 0.95}  # 999 is skipped


def test_handles_missing_results_key():
    """Empty/missing results should return empty dict."""
    result = {}
    scores = _CohereCompatibleRerankClient.predict(result)
    assert scores == {}


def test_handles_missing_scores_keys():
    """Missing scores/indices keys should return empty dict."""
    result = {"other_key": "value"}
    scores = _CohereCompatibleRerankClient.predict(result)
    assert scores == {}


def test_handles_empty_results():
    """Empty results list should return empty dict."""
    result = {"results": []}
    scores = _CohereCompatibleRerankClient.predict(result)
    assert scores == {}


def test_handles_malformed_items():
    """Malformed items in results should be skipped gracefully."""
    result = {
        "results": [
            {"index": 0, "relevance_score": 0.95},
            "not a dict",
            {"no_index": 0, "relevance_score": 0.50},
            {"index": "not_int", "relevance_score": 0.30},
            {"index": 1},  # missing score
        ]
    }
    scores = _CohereCompatibleRerankClient.predict(result)
    assert scores == {0: 0.95}


def test_get_top_k():
    """Test get_top_k returns top-k indices sorted by score."""
    scores = {2: 0.95, 0: 0.85, 1: 0.72, 3: 0.60}
    top = _CohereCompatibleRerankClient.get_top_k(scores, k=2)
    assert top == [2, 0]


def test_get_top_k_larger_than_available():
    """get_top_k with k larger than available returns all sorted."""
    scores = {2: 0.95, 0: 0.85}
    top = _CohereCompatibleRerankClient.get_top_k(scores, k=10)
    assert top == [2, 0]


def test_scores_indices_array_shape_mismatched_lengths():
    """Shape 3: {scores: [...], indices: [...]} with mismatched lengths truncates to shorter list."""
    # scores has 3 elements, indices has 2 - should only use first 2
    result = {
        "scores": [0.95, 0.85, 0.72],
        "indices": [2, 0],
    }
    scores = _CohereCompatibleRerankClient.predict(result)
    assert scores == {2: 0.95, 0: 0.85}

    # scores has 2 elements, indices has 3 - should only use first 2
    result2 = {
        "scores": [0.95, 0.85],
        "indices": [2, 0, 1],
    }
    scores2 = _CohereCompatibleRerankClient.predict(result2)
    assert scores2 == {2: 0.95, 0: 0.85}
