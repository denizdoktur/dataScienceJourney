from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.ocr import perform_easyocr, perform_tesseract, perform_paddleocr

# API yönlendirmeleri için APIRouter nesnesi oluşturuluyor.
router = APIRouter()

# HTML dosyalarının bulunduğu dizini belirtiyoruz.
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # "upload.html kullanıcıya gönderiyoruz.
    return templates.TemplateResponse("upload.html", {"request": request})

# Servisin çalışır durumda olduğunu doğrulamak için {"ping": "pong!"} döner.
@router.get("/ping")
async def ping():
    return {"ping": "pong!"}

@router.post("/predict", response_class=HTMLResponse)
async def predict(request: Request, file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        
        # OCR modellerini kullanarak metinleri elde ediyoruz.
        easyocr_text = perform_easyocr(image_bytes)
        tesseract_text = perform_tesseract(image_bytes)
        paddleocr_text = perform_paddleocr(image_bytes)
        
        # Elde edilen sonuçları "results.html"e gönderiyoruz.
        return templates.TemplateResponse("results.html", {
            "request": request,
            "paddleocr_text": paddleocr_text,
            "easyocr_text": easyocr_text,
            "tesseract_text": tesseract_text
        })
    except Exception as e:
        # Hata durumunda HTTPException kullanarak 400 kodlu hata mesajı döndürüyoruz.
        raise HTTPException(status_code=400, detail=str(e))
