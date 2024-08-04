from fastapi import FastAPI, HTTPException, Request, Depends, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
from dotenv import load_dotenv
from app.feature_extraction_service import FeatureExtractionService
from app.models import ImageRequest, TextRequest, CombinedRequest, CompareRequest

# 加載 .env 文件中的環境變數
load_dotenv()

# 環境變數
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
SECRET_KEY = os.getenv("SECRET_KEY")
USERNAME = os.getenv("APP_USER")
PASSWORD = os.getenv("APP_PASSWORD")

app = FastAPI(
    title="Fastapi clip service",
    description="該服務利用 FastAPI 框架提供 HTTP API 端點，支持從圖像和文本中提取特徵向量，使得開發者可以方便地在各種應用中集成先進的圖像和文本檢索功能。",
    version="1.0.0",
    contact={
        "name": "Owen",
        "email": "12877999+zxc88645@users.noreply.github.com",
    },
)
service = FeatureExtractionService()
templates = Jinja2Templates(directory="app/templates")

# OAuth2PasswordBearer 用於設置 Authorization 標頭
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str = Depends(oauth2_scheme)):
    """簡單的 token 驗證函數，根據實際情況修改"""
    if token != SECRET_KEY:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return token


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/extract-image-features/", tags=["Image Features"], summary="提取圖像特徵")
async def extract_image_features(
    request: ImageRequest, token: str = Depends(verify_token)
):
    """提取給定圖像 URL 的特徵。"""
    try:
        features = service.extract_features_from_image(request.url)
        return {"features": features}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract-text-features/", tags=["Text Features"], summary="提取文本特徵")
async def extract_text_features(
    request: TextRequest, token: str = Depends(verify_token)
):
    """提取給定文本的特徵。"""
    try:
        features = service.extract_features_from_text(request.text)
        return {"features": features}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract-combined-features/", tags=["Combined Features"], summary="提取結合特徵")
async def extract_combined_features(
    request: CombinedRequest, token: str = Depends(verify_token)
):
    """提取圖像 URL 和文本的結合特徵。"""
    try:
        features = service.extract_combined_features(request.url, request.text)
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare/", tags=["Feature Comparison"], summary="比較圖片與多組文字的相似度")
async def compare(request: CompareRequest, token: str = Depends(verify_token)):
    try:
        similarity = service.compare(request.url, request.text)
        return {"similarity": similarity.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/token", tags=["Authentication"], summary="用戶身份驗證")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """驗證用戶名和密碼，並返回訪問令牌。"""
    print(form_data.username, form_data.password)
    print(USERNAME, PASSWORD)
    if form_data.username == USERNAME and form_data.password == PASSWORD:
        return {"access_token": SECRET_KEY, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
