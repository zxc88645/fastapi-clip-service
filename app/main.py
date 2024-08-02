from fastapi import FastAPI, HTTPException, Request, Depends, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from .feature_extraction_service import FeatureExtractionService
from .models import ImageRequest, TextRequest, CombinedRequest

# 加載 .env 文件中的環境變數
load_dotenv()

# 環境變數
SECRET_KEY = os.getenv("SECRET_KEY")
USERNAME = os.getenv("APP_USER")
PASSWORD = os.getenv("APP_PASSWORD")

app = FastAPI()
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


@app.post("/extract-image-features/")
async def extract_image_features(
    request: ImageRequest, token: str = Depends(verify_token)
):
    try:
        features = service.extract_features_from_image(request.url)
        return {"features": features}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract-text-features/")
async def extract_text_features(
    request: TextRequest, token: str = Depends(verify_token)
):
    try:
        features = service.extract_features_from_text(request.text)
        return {"features": features}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract-combined-features/")
async def extract_combined_features(
    request: CombinedRequest, token: str = Depends(verify_token)
):
    try:
        features = service.extract_combined_features(request.url, request.text)
        return features
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """驗證用戶名和密碼"""
    print(form_data.username, form_data.password)
    print(USERNAME, PASSWORD)
    if form_data.username == USERNAME and form_data.password == PASSWORD:
        return {"access_token": SECRET_KEY, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
