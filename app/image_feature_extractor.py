import clip
import torch
from PIL import Image
import requests
from io import BytesIO
import os
import time
import pickle


class ImageFeatureExtractor:
    def __init__(self, model_name="ViT-B/32", cache_dir=".cache"):
        """初始化 CLIP 模型和設備。"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name

        # 設置緩存目錄並確保其存在
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # 設置模型路徑
        self.model_path = os.path.join(self.cache_dir, f"{model_name.replace('/', '_')}_model.pkl")
        
        # 加載模型（使用緩存）
        self.load_model()

        print(f"當前使用的裝置是: {'GPU' if self.device == 'cuda' else 'CPU'}")

    def load_model(self):
        """從磁碟加載模型，如果模型不存在則下載並儲存。 """
        full_path = os.path.abspath(self.model_path)
        print(f"正在加載模型 {full_path} ...")

        if os.path.exists(self.model_path):
            # 從緩存中加載模型
            model_load_start = time.time()
            with open(self.model_path, "rb") as f:
                self.model, self.preprocess = pickle.load(f)
            model_load_end = time.time()
            print(f"模型加載時間: {model_load_end - model_load_start:.4f} 秒")            
            print("從緩存中加載模型")
        else:
            # 計時模型加載
            model_load_start = time.time()
            self.model, self.preprocess = clip.load(self.model_name, device=self.device)
            model_load_end = time.time()
            print(f"模型加載時間: {model_load_end - model_load_start:.4f} 秒")

            # 儲存模型到磁碟
            with open(self.model_path, "wb") as f:
                pickle.dump((self.model, self.preprocess), f)
            print(f"模型已儲存到 {self.model_path}")

    def load_image(self, image_path_or_url: str) -> Image.Image:
        """根據輸入類型加載圖片，可以是本地檔案或圖片網址。"""
        if os.path.isfile(image_path_or_url):
            # 本地檔案
            return Image.open(image_path_or_url)
        elif image_path_or_url.startswith("http://") or image_path_or_url.startswith(
            "https://"
        ):
            # 圖片網址
            return self.download_image(image_path_or_url)
        else:
            raise ValueError("提供的路徑既不是有效的本地檔案，也不是有效的圖片網址")

    def download_image(self, url: str) -> Image.Image:
        """從網址下載圖片並計算下載時間。"""
        start_time = time.time()  # 開始計時
        response = requests.get(url)
        response.raise_for_status()  # 確保下載成功
        end_time = time.time()  # 結束計時
        elapsed_time = end_time - start_time
        print(f"圖片下載時間: {elapsed_time:.4f} 秒")
        return Image.open(BytesIO(response.content))

    def extract_features(self, image_path_or_url: str) -> list:
        """提取圖片特徵。"""
        image = self.load_image(image_path_or_url)

        # 圖片預處理時間
        preprocess_start = time.time()
        image = self.preprocess(image).unsqueeze(0).to(self.device)
        preprocess_end = time.time()
        print(f"圖片預處理時間: {preprocess_end - preprocess_start:.4f} 秒")

        start_time = time.time()  # 開始計時
        with torch.no_grad():
            image_features = self.model.encode_image(image)
        end_time = time.time()  # 結束計時
        elapsed_time = end_time - start_time
        print(f"特徵計算時間: {elapsed_time:.4f} 秒")

        return image_features.cpu().numpy().tolist()
