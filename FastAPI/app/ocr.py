import easyocr
import pytesseract
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np
import cv2
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# EasyOCR ve PaddleOCR için Reader nesneleri İngilizce dilinde oluşturuluyor.
easyocr_reader = easyocr.Reader(['en'])
paddleocr_reader = PaddleOCR(lang="en")

def perform_easyocr(image_bytes: bytes) -> str:
    # Byte'ları numpy dizisine dönüştürüp OpenCV ile görüntü haline getiriyoruz.
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    try:
        # Sadece metinleri içeren listeyi döndürür.
        results = easyocr_reader.readtext(img, detail=0)
        return " ".join(results)
    except Exception as e:
        # Hata durumunda HTTPException kullanarak hata mesajı döndürüyoruz.
        raise Exception(f"EasyOCR hatası: {str(e)}")

def perform_tesseract(image_bytes: bytes) -> str:
    try:
        # Bytes verisinden görüntü oluşturuyoruz.
        image = Image.open(io.BytesIO(image_bytes))
        # Tesseract ile metin tanıma işlemi yapıyoruz.
        result = pytesseract.image_to_string(image)
        return result
    except Exception as e:
        # Hata durumunda HTTPException kullanarak hata mesajı döndürüyoruz.
        raise Exception(f"Tesseract hatası: {str(e)}")

def perform_paddleocr(image_bytes: bytes) -> str:
    # Byte'ları numpy dizisine dönüştürüp OpenCV ile görüntü haline getiriyoruz.
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    try:
        # PaddleOCR ile OCR işlemi gerçekleştiriliyor (cls=True, sınıflandırma bilgisi için).
        result = paddleocr_reader.ocr(img, cls=True)
        texts = []
        # Her bir satır için OCR sonucunu işliyoruz.
        for line in result:
            # Öncelikle, sonuç yapısının beklenen formatta olup olmadığını kontrol ediyoruz.
            if len(line) >= 2 and isinstance(line[1], (list, tuple)):
                candidate = line[1][0]  # OCR tarafından tanınan metin (ilk eleman)
                # Eğer elde edilen değer metin değilse (örneğin liste ise), koordinatları metne çeviriyoruz.
                if not isinstance(candidate, str):
                    candidate = " ".join(str(coord) for coord in line[0])
            else:
                # Beklenen yapı sağlanamıyorsa, sadece koordinatları kullanarak metin oluşturuyoruz.
                candidate = " ".join(str(coord) for coord in line[0])
            texts.append(candidate)
        # Tüm metin parçalarını birleştirip döndürüyoruz.
        return " ".join(texts)
    except Exception as e:
        # Hata durumunda HTTPException kullanarak hata mesajı döndürüyoruz.
        raise Exception(f"PaddleOCR hatası: {str(e)}")