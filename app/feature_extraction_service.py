from .image_feature_extractor import ImageFeatureExtractor
import clip
import torch
import time

class FeatureExtractionService:
    def __init__(self):
        self.image_extractor = ImageFeatureExtractor()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, _ = clip.load("ViT-B/32", device=self.device)

    def extract_features_from_image(self, image_path_or_url: str) -> list:
        """從圖像提取特徵。"""
        return self.image_extractor.extract_features(image_path_or_url)

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

    def extract_combined_features(self, image_path_or_url: str, text: str) -> dict:
        """提取圖像和文本的特徵。"""
        image_features = self.extract_features_from_image(image_path_or_url)
        text_features = self.extract_features_from_text(text)
        return {
            "image_features": image_features,
            "text_features": text_features
        }
