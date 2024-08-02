import requests

class ClipServiceClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def extract_image_features(self, image_url: str):
        response = requests.post(f"{self.base_url}/extract-image-features/", json={"url": image_url})
        return response.json()

    def extract_text_features(self, text: str):
        response = requests.post(f"{self.base_url}/extract-text-features/", json={"text": text})
        return response.json()

    def extract_combined_features(self, image_url: str, text: str):
        response = requests.post(f"{self.base_url}/extract-combined-features/", json={"url": image_url, "text": text})
        return response.json()

# 使用示例
if __name__ == "__main__":
    client = ClipServiceClient()
    print(client.extract_image_features("https://example.com/image.jpg"))
    print(client.extract_text_features("Example Product Name"))
