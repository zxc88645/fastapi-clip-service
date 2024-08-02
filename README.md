# fastapi-clip-service
fastapi-clip-service 是一個基於 OpenAI CLIP 模型的高效特徵提取服務。

該服務利用 FastAPI 框架提供 HTTP API 端點，支持從圖像和文本中提取特徵向量。
這使得開發者可以方便地在各種應用中集成先進的圖像和文本檢索功能。

以下是如何運行該應用的說明。

## 安裝

首先，確保你安裝了必要的 Python 包：

```bash
pip install -r requirements.txt
```

## 使用 Docker 運行
### 構建 Docker 映像：
```bash
docker build -t fastapi-clip-service .
```

###運行 Docker 容器：

```bash
docker run -p 8000:8000 fastapi-clip-service
```

## 使用客戶端庫
```python

from client import ClipServiceClient

client = ClipServiceClient()
image_features = client.extract_image_features("https://example.com/image.jpg")
text_features = client.extract_text_features("Example Product Name")
combined_features = client.extract_combined_features("https://example.com/image.jpg", "Example Product Name")

print("Image Features:", image_features)
print("Text Features:", text_features)
print("Combined Features:", combined_features)

```

## CLI 工具
使用命令行工具提取特徵：

```bash
複製程式碼
python cli.py --image-url "https://example.com/image.jpg"
python cli.py --text "Example Product Name"
```

API 端點
 - POST /extract-image-features/: 從提供的圖像 URL 中提取特徵。
 - POST /extract-text-features/: 從提供的文本中提取特徵。
 - POST /extract-combined-features/: 從提供的圖像 URL 和文本中提取特徵。
