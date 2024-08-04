from app.image_utils import load_image, download_image
import clip
import torch
import time
import os
import pickle
from PIL import Image
import requests

from io import BytesIO


class FeatureExtractionService:
    def __init__(self, model_name="ViT-B/32", cache_dir=".cache"):
        """初始化 CLIP 模型和設備。"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name

        # 設置緩存目錄並確保其存在
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

        # 設置模型路徑
        self.model_path = os.path.join(
            self.cache_dir, f"{model_name.replace('/', '_')}_model.pkl"
        )

        # 加載模型
        self.load_model()

        print(f"當前使用的裝置是: {'GPU' if self.device == 'cuda' else 'CPU'}")

    def load_model(self):
        """從磁碟加載模型，如果模型不存在則下載並儲存。"""
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

    def extract_features_from_image(self, image_path_or_url: str) -> list:
        """提取圖片特徵。"""
        image = load_image(image_path_or_url)

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

    def extract_features_from_text(self, text: str) -> list:
        """從文本提取特徵。"""
        start_time = time.time()
        text_input = clip.tokenize([text]).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text_input)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"文本特徵計算時間: {elapsed_time:.4f} 秒")

        return text_features.cpu().numpy().tolist()

    def compare(self, image_path_or_url: str, text: list) -> float:
        """比較圖像和文本的相似性。"""
        image = load_image(image_path_or_url)
        image = self.preprocess(image).unsqueeze(0).to(self.device)
        text = clip.tokenize(text).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image)
            text_features = self.model.encode_text(text)

            logits_per_image, logits_per_text = self.model(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

        return probs
