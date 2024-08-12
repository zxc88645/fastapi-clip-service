from PIL import Image
import aiohttp
import asyncio
from io import BytesIO
import os
from typing import Union


async def load_image(image_path_or_data: Union[str, bytes]) -> Image.Image:
    """根據輸入類型加載圖片，可以是本地檔案、圖片網址或二進位數據。"""
    print(f"正在加載圖片: {repr(image_path_or_data)}")
    # 類型
    print(type(image_path_or_data))

    if isinstance(image_path_or_data, bytes):
        # 二進位數據
        return Image.open(BytesIO(image_path_or_data))
    elif os.path.isfile(image_path_or_data):
        # 本地檔案
        return Image.open(image_path_or_data)
    elif image_path_or_data.startswith("http://") or image_path_or_data.startswith(
        "https://"
    ):
        # 圖片網址
        return await download_image(image_path_or_data)
    else:
        raise ValueError("提供的路徑既不是有效的本地檔案，也不是有效的圖片網址")


async def download_image(url: str) -> Image.Image:
    """從網址下載圖片並計算下載時間。"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    start_time = asyncio.get_event_loop().time()  # 開始計時

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            response.raise_for_status()  # 確保下載成功
            data = await response.read()
            end_time = asyncio.get_event_loop().time()  # 結束計時
            elapsed_time = end_time - start_time
            print(f"圖片下載時間: {elapsed_time:.4f} 秒")
            return Image.open(BytesIO(data))
