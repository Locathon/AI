from fastapi import APIRouter, HTTPException
from schema.style_schema import StyleTransformRequest, StyleTransformResponse
from service.style_converter import convert_style
from service.log_writer import load_transform_log
router = APIRouter()

@router.post("/style-transform", response_model=StyleTransformResponse)

def transform_style(request: StyleTransformRequest):
    try:
        print("StyleTransformRequest 입력값:", request.dict())
        transformed = convert_style(
            request.original_text,
            request.tone,
            getattr(request, "store_name", None),
            getattr(request, "sns", None)
        )
        return StyleTransformResponse(original=request.original_text, transformed=transformed)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/style-log")
def get_style_log():
    try:
        log = load_transform_log()
        return log
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))