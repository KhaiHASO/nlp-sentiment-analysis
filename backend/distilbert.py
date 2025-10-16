"""
Lightweight wrapper to load a Hugging Face sentiment pipeline
and run analysis. Makes it easy to swap models.
"""

from typing import Dict, Any

from transformers import pipeline


DEFAULT_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"


def load_sentiment_pipeline(model_name: str = DEFAULT_MODEL_NAME):
    """Return a cached HF pipeline for sentiment analysis."""
    return pipeline("sentiment-analysis", model=model_name)


def analyze_text(classifier, text: str) -> Dict[str, Any]:
    """Run the pipeline on a single text and normalize output."""
    result = classifier(text)[0]
    # Normalize label when models return LABEL_0/LABEL_1
    label = result.get("label", "").upper()
    if label.startswith("LABEL_"):
        try:
            label = "POSITIVE" if int(label.split("_")[-1]) == 1 else "NEGATIVE"
        except Exception:
            label = result.get("label", "UNKNOWN").upper()

    return {
        "label": label,
        "score": float(result.get("score", 0.0)),
    }


