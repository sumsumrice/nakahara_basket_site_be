from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="疎通確認API", version="1.0.0")

# CORS設定（フロントエンドからのアクセスを許可）
# ローカル開発時に使うための設定
""" app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Reactの開発サーバーのポート
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) """

# または、開発中は全てのオリジンを許可（本番では推奨されません）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# レスポンス用のモデル
class HealthResponse(BaseModel):
    status: str
    message: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

# ヘルスチェック用エンドポイント
@app.get("/", response_model=HealthResponse)
async def root():
    return {"status": "success", "message": "バックエンドが正常に動作しています！"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "healthy", "message": "API is running"}

# サンプルデータを返すエンドポイント
@app.get("/users", response_model=List[UserResponse])
async def get_users():
    sample_users = [
        {"id": 1, "name": "田中太郎", "email": "tanaka@example.com"},
        {"id": 2, "name": "佐藤花子", "email": "sato@example.com"},
        {"id": 3, "name": "鈴木一郎", "email": "suzuki@example.com"}
    ]
    return sample_users

# POST用のサンプルエンドポイント
class MessageRequest(BaseModel):
    message: str

@app.post("/echo", response_model=dict)
async def echo_message(request: MessageRequest):
    return {
        "received_message": request.message,
        "response": f"サーバーから: {request.message}を受信しました！",
        "timestamp": "2025-06-08"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)