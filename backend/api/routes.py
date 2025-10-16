from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException

from backend.distilbert import (
    load_sentiment_pipeline as load_distilbert_pipeline,
    analyze_text as analyze_distilbert_text,
    DEFAULT_MODEL_NAME as DISTILBERT_DEFAULT,
)
from backend.visobert import (
    load_sentiment_pipeline as load_viso_sentiment,
    load_fill_mask_pipeline as load_viso_mask,
    analyze_text as analyze_viso_text,
    VISOBERT_MASK_MODEL as VISO_MASK_DEFAULT,
    VISOBERT_SENTIMENT_MODEL as VISO_SENT_DEFAULT,
)
from backend.multilingual import (
    load_multilingual_pipeline,
    analyze_text as analyze_multilingual_text,
    MULTILINGUAL_MODEL_NAME as MULTI_DEFAULT,
)
from backend.schemas.models import SentimentRequest, FillMaskRequest
from backend.services.scrape import fetch_comments_from_url
from fastapi import Query


router = APIRouter()


@router.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@router.get("/models")
def list_models() -> Dict[str, Any]:
    return {
        "distilbert": {"default": DISTILBERT_DEFAULT},
        "visobert": {
            "sentiment_default": VISO_SENT_DEFAULT,
            "fill_mask_default": VISO_MASK_DEFAULT,
        },
        "multilingual": {"default": MULTI_DEFAULT, "classes": 5},
    }


@router.post("/sentiment")
def sentiment(req: SentimentRequest) -> Dict[str, Any]:
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text is empty")

    model_type = req.model_type.lower()
    model_name = req.model_name

    if model_type == "distilbert":
        pipeline = load_distilbert_pipeline(model_name or DISTILBERT_DEFAULT)
        result = analyze_distilbert_text(pipeline, text)
        return {"model_type": model_type, "model_name": model_name or DISTILBERT_DEFAULT, **result}

    if model_type == "visobert":
        pipeline = load_viso_sentiment(model_name or VISO_SENT_DEFAULT)
        result = analyze_viso_text(pipeline, text)
        return {"model_type": model_type, "model_name": model_name or VISO_SENT_DEFAULT, **result}

    if model_type == "multilingual":
        pipeline = load_multilingual_pipeline()
        result = analyze_multilingual_text(pipeline, text)
        return {"model_type": model_type, "model_name": MULTI_DEFAULT, **result}

    raise HTTPException(status_code=400, detail="unsupported model_type")


@router.post("/fill-mask")
def fill_mask(req: FillMaskRequest) -> Dict[str, Any]:
    text = req.text
    if "<mask>" not in text:
        raise HTTPException(status_code=400, detail="text must contain <mask>")
    top_k = max(1, min(50, req.top_k))

    pipeline = load_viso_mask(req.model_name or VISO_MASK_DEFAULT)
    outputs = pipeline(text, top_k=top_k)
    if isinstance(outputs, dict):
        outputs = [outputs]

    candidates: List[Dict[str, Any]] = []
    for item in outputs:
        candidates.append(
            {
                "token_str": item.get("token_str"),
                "score": float(item.get("score", 0.0)),
                "sequence": item.get("sequence"),
            }
        )

    return {
        "model_type": "visobert",
        "model_name": req.model_name or VISO_MASK_DEFAULT,
        "top_k": top_k,
        "candidates": candidates,
    }


@router.get("/scrape-and-analyze")
async def scrape_and_analyze(
    url: str = Query(..., description="URL bài viết"),
    model_type: str = Query("visobert", description="distilbert|visobert|multilingual"),
    css: Optional[str] = Query(None, description="CSS selector cho comment (tuỳ chọn)"),
    limit: int = Query(30, ge=1, le=200),
):
    comments = await fetch_comments_from_url(url, css_selector=css, limit=limit)

    results = []
    for text in comments:
        # reuse sentiment endpoint logic quickly
        req = SentimentRequest(model_type=model_type, text=text)
        result = sentiment(req)
        results.append({"text": text, **result})

    # basic summary
    label_counts: dict[str, int] = {}
    for r in results:
        lbl = r["label"]
        label_counts[lbl] = label_counts.get(lbl, 0) + 1

    return {"count": len(results), "summary": label_counts, "items": results}


