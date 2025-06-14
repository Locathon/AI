from typing import Optional
from pydantic import BaseModel

class StyleTransformRequest(BaseModel):
    original_text: str
    tone: Optional[str] = None
    store_name: Optional[str] = None
    sns: Optional[str] = None

class StyleTransformResponse(BaseModel):
    original: str
    transformed: str