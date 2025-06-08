from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   # ← 추가
from router import style_transform, merchant_qa, merchant_qa_manage

app = FastAPI()

# 🔥 CORS 설정 추가 (이 위치!)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 중엔 *로, 배포는 도메인 명시 권장
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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