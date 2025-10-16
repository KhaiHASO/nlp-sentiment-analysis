from typing import List
import os


def _split_csv(value: str, default: List[str]) -> List[str]:
    v = (value or "").strip()
    if not v:
        return default
    return [item.strip() for item in v.split(",") if item.strip()]


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "NLP Sentiment Backend")
    VERSION: str = os.getenv("APP_VERSION", "1.0.0")

    # CORS
    CORS_ALLOW_ORIGINS: List[str] = _split_csv(
        os.getenv("CORS_ALLOW_ORIGINS", "*"), ["*"]
    )
    CORS_ALLOW_METHODS: List[str] = _split_csv(
        os.getenv("CORS_ALLOW_METHODS", "*"), ["*"]
    )
    CORS_ALLOW_HEADERS: List[str] = _split_csv(
        os.getenv("CORS_ALLOW_HEADERS", "*"), ["*"]
    )

    # Default models (optional overrides)
    DISTILBERT_DEFAULT: str = os.getenv(
        "DISTILBERT_DEFAULT", "distilbert-base-uncased-finetuned-sst-2-english"
    )
    VISO_SENT_DEFAULT: str = os.getenv(
        "VISO_SENT_DEFAULT", "5CD-AI/vietnamese-sentiment-visobert"
    )
    VISO_MASK_DEFAULT: str = os.getenv(
        "VISO_MASK_DEFAULT", "5CD-AI/visobert-14gb-corpus"
    )
    MULTI_DEFAULT: str = os.getenv(
        "MULTI_DEFAULT", "tabularisai/multilingual-sentiment-analysis"
    )


settings = Settings()


