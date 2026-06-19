from fastapi import FastAPI
from app.routers.chat import router as chat_router
from app.routers.emotion import router as emotion_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Hackathon")

origins = [
    "http://localhost:5002",  # フロントエンドが動いているURL
    "http://127.0.0.1:5002",
    ""
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # 全許可にする場合は allow_origins=["*"]
    allow_credentials=True,
    allow_methods=["*"],            # POSTやOPTIONSなど、すべてのメソッドを許可
    allow_headers=["*"],            # Content-Typeなど、すべてのヘッダーを許可
)
app.include_router(chat_router)
app.include_router(emotion_router)

@app.get("/")
async def root():
    return{"message": "server running"}