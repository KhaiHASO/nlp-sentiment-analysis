"""
Utilities for ViSoBERT models (Vietnamese): fill-mask and sentiment.
"""

from typing import Dict, Any

from transformers import pipeline


VISOBERT_MASK_MODEL = "5CD-AI/visobert-14gb-corpus"
VISOBERT_SENTIMENT_MODEL = "5CD-AI/vietnamese-sentiment-visobert"


def load_fill_mask_pipeline(model_name: str = VISOBERT_MASK_MODEL):
    return pipeline("fill-mask", model=model_name)


def load_sentiment_pipeline(model_name: str = VISOBERT_SENTIMENT_MODEL):
    return pipeline("sentiment-analysis", model=model_name, tokenizer=model_name)


def analyze_text(classifier, text: str) -> Dict[str, Any]:
    """Run sentiment pipeline and normalize label for VN models."""
    result = classifier(text)[0]
    label = str(result.get("label", "")).upper()
    if label.startswith("LABEL_"):
        try:
            label = "POSITIVE" if int(label.split("_")[-1]) == 1 else "NEGATIVE"
        except Exception:
            pass
    # Common Vietnamese outputs: POS/NEG/NEU
    if label in {"POS", "+"}:
        label = "POSITIVE"
    elif label in {"NEG", "-"}:
        label = "NEGATIVE"
    return {"label": label, "score": float(result.get("score", 0.0))}


