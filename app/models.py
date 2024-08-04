from pydantic import BaseModel


class ImageRequestUrl(BaseModel):
    url: str


class TextRequest(BaseModel):
    text: str


class CombinedRequest(BaseModel):
    url: str
    text: str


class CompareRequest(BaseModel):
    url: str
    text: list
