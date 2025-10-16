from typing import Optional

from pydantic import BaseModel, Field


class SentimentRequest(BaseModel):
    model_type: str = Field(..., description="distilbert | visobert | multilingual")
    text: str
    model_name: Optional[str] = None


class FillMaskRequest(BaseModel):
    text: str
    model_name: Optional[str] = None
    top_k: int = 10


