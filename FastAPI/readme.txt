# FastAPI ile Prediction Servisi Geliştirme

Bu projede, bir makine öğrenmesi modeli entegre edilerek tahmin yapabilen bir FastAPI tabanlı servis geliştirilecektir. Servis, belirlenen girdileri alarak modeli çalıştıracak ve buna karşılık uygun tahmin sonuçlarını döndürecektir. Projenin başarılı bir şekilde tamamlanabilmesi için aşağıda belirtilen kurallara uyulması gerekmektedir.

## 1. Genel Kurallar
- Kod yapısı düzenli olmalı: Tüm kodu tek bir main.py dosyasına koymayın. Daha okunabilir ve düzenli bir yapı için farklı dosyalara bölün.
- Model entegrasyonu: Servis, verilen veriyi kullanarak tahmin yapabilen bir modeli çalıştırmalıdır.
- Hata yönetimi: Kodunuzu try-except bloklarıyla güvenli hale getirin. Bir hata oluştuğunda, FastAPI’nin HTTPException özelliğini kullanarak anlamlı ve açıklayıcı hata mesajları döndürün.

## 2. Veri Modelleri (Pydantic)
Tahmin işlemi için giriş ve çıkış verileri Pydantic modelleri ile tanımlanmalıdır.

### Giriş (Input) Modeli
Birden fazla giriş değişkeni olabilir. Örneğin:

```python
from pydantic import BaseModel

class PredictionInput(BaseModel):

    text: str
```

### Çıkış (Output) Modeli
Modelin üreteceği tahmin çıktısı:

```python
from pydantic import BaseModel

class PredictionOutput(BaseModel):
    category: str
```

3. Servis Endpoint'leri
Servis aşağıdaki endpoint'leri içermelidir:
Endpoint    Method  Açıklama
/           GET     Root endpoint
/ping       GET     Servisin çalıştığını kontrol etmek için ({"ping": "pong!"} döner)
/predict    POST    Modeli çalıştırarak tahmin döndürür