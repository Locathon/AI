from fastapi import FastAPI
from router import style_transform, merchant_qa, merchant_qa_manage

app = FastAPI()

# 라우터 등록
app.include_router(style_transform.router, prefix="/merchant", tags=["Style Transform"])
app.include_router(merchant_qa.router, prefix="/chat", tags=["Merchant Q&A"])
app.include_router(merchant_qa_manage.router, tags=["QA Management"])

@app.get("/")
def root():
    return {
        "message": "Merchant AI Service Running...",
        "endpoints": [
            "/merchant/style-transform",
            "/merchant/style-log",
            "/chat/merchant",
            "/qa/add",
            "/qa/edit",
            "/qa/delete",
            "/qa/list"
        ]
    }
