"""Cohere-compatible reranker client for Hindsight."""

from __future__ import annotations

from typing import Any, Dict, List


class _CohereCompatibleRerankClient:
    """
    Parse Cohere-compatible rerank responses in multiple shapes.

    Real-world response shapes we tolerate:
      1. {results: [{"index": int, "relevance_score": float}, ...]}
      2. {results: [{"index": int, "score": float}, ...]}  (score alias)
      3. {scores: [float, ...], indices: [int, ...]}       (array shape)
    """

    # Reasonable maximum index value; indices beyond this are considered
    # out-of-range and skipped to prevent IndexError in downstream usage.
    MAX_VALID_INDEX: int = 100

    @staticmethod
    def predict(result: Dict[str, Any]) -> Dict[int, float]:
        """
        Convert a rerank response into a mapping of original index -> score.

        Returns an empty dict if the response cannot be parsed.
        Skips out-of-range indices instead of crashing.
        """
        all_scores: Dict[int, float] = {}

        # Shape 3: {scores: [...], indices: [...]} array format
        if "scores" in result and "indices" in result:
            scores = result["scores"]
            indices = result["indices"]
            if isinstance(scores, list) and isinstance(indices, list):
                for idx, score in zip(indices, scores):
                    try:
                        idx_int = int(idx)
                        # Only accept valid, in-range indices
                        if 0 <= idx_int <= _CohereCompatibleRerankClient.MAX_VALID_INDEX:
                            all_scores[idx_int] = float(score)
                    except (ValueError, TypeError):
                        continue
                return all_scores

        # Shapes 1 & 2: {results: [{"index": int, "relevance_score": float}, ...]}
        results = result.get("results")
        if isinstance(results, list):
            for item in results:
                if not isinstance(item, dict):
                    continue
                # Shape 1: relevance_score field
                # Shape 2: score field (alias)
                score = item.get("relevance_score") if "relevance_score" in item else item.get("score")
                if score is None:
                    continue
                try:
                    score_float = float(score)
                except (ValueError, TypeError):
                    continue

                original_idx = item.get("index")
                if original_idx is None:
                    continue
                try:
                    idx_int = int(original_idx)
                except (ValueError, TypeError):
                    continue

                # Skip out-of-range indices (negative or unreasonably large)
                if not (0 <= idx_int <= _CohereCompatibleRerankClient.MAX_VALID_INDEX):
                    continue

                all_scores[idx_int] = score_float

        return all_scores

    @staticmethod
    def get_top_k(scores: Dict[int, float], k: int = 5) -> List[int]:
        """Return the top-k indices sorted by score (descending)."""
        sorted_indices = sorted(scores.keys(), key=lambda i: scores[i], reverse=True)
        return sorted_indices[:k]


# Convenience alias used by the engine
CohereCompatibleRerankClient = _CohereCompatibleRerankClient
