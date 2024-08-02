from PIL import Image
import requests
from io import BytesIO
import os
import time

def load_image(image_path_or_url: str) -> Image.Image:
    """根據輸入類型加載圖片，可以是本地檔案或圖片網址。"""
    if os.path.isfile(image_path_or_url):
        # 本地檔案
        return Image.open(image_path_or_url)
    elif image_path_or_url.startswith('http://') or image_path_or_url.startswith('https://'):
        # 圖片網址
        return download_image(image_path_or_url)
    else:
        raise ValueError("提供的路徑既不是有效的本地檔案，也不是有效的圖片網址")

def download_image(url: str) -> Image.Image:
    """從網址下載圖片並計算下載時間。"""
    start_time = time.time()  # 開始計時
    response = requests.get(url)
    response.raise_for_status()  # 確保下載成功
    end_time = time.time()  # 結束計時
    elapsed_time = end_time - start_time
    print(f"圖片下載時間: {elapsed_time:.4f} 秒")
    return Image.open(BytesIO(response.content))
