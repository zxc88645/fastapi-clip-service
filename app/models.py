from pydantic import BaseModel

class ImageRequest(BaseModel):
    url: str

class TextRequest(BaseModel):
    text: str

class CombinedRequest(BaseModel):
    url: str
    text: str
