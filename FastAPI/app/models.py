from pydantic import BaseModel

class PredictionOutput(BaseModel):
    easyocr_text: str
    tesseract_text: str
    paddleocr_text: str