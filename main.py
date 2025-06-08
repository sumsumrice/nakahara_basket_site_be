from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# 環境変数をロード
load_dotenv()

app = FastAPI(
    title="Your FastAPI App",
    description="FastAPI application deployed on Render",
    version="1.0.0"
)

# CORS設定（必要に応じて調整）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では具体的なドメインを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Hello World! FastAPI is running on Render",
        "status": "success"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    if item_id < 1:
        raise HTTPException(status_code=400, detail="Item ID must be positive")
    
    return {
        "item_id": item_id, 
        "q": q,
        "message": f"Item {item_id} retrieved successfully"
    }

# 環境変数からポートを取得（Renderが自動設定）
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)