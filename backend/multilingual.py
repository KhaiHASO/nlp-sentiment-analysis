"""
Utilities for TabularisAI multilingual sentiment (5 classes, 23 languages).
Model: tabularisai/multilingual-sentiment-analysis
"""

from typing import Dict, Any, List

from transformers import pipeline


MULTILINGUAL_MODEL_NAME = "tabularisai/multilingual-sentiment-analysis"

# Canonical label mapping (model already outputs readable labels, but normalize casing)
CANONICAL_LABELS = [
    "VERY NEGATIVE",
    "NEGATIVE",
    "NEUTRAL",
    "POSITIVE",
    "VERY POSITIVE",
]


def load_multilingual_pipeline(model_name: str = MULTILINGUAL_MODEL_NAME):
    return pipeline("text-classification", model=model_name, return_all_scores=True)


def analyze_text(classifier, text: str) -> Dict[str, Any]:
    """Return top label and all scores for a single text."""
    outputs: List[Dict[str, Any]] = classifier(text)
    # pipelines with return_all_scores=True return List[List[score-dicts]]
    scores = outputs[0]
    # Normalize labels
    normalized = [
        {
            "label": str(item.get("label", "")).strip().upper(),
            "score": float(item.get("score", 0.0)),
        }
        for item in scores
    ]
    # Sort by score desc
    normalized.sort(key=lambda x: x["score"], reverse=True)
    top = normalized[0]
    return {"label": top["label"], "score": top["score"], "all_scores": normalized}


