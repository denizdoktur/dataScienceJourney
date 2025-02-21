import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# https://www.kaggle.com/datasets/asinow/car-price-dataset

df = pd.read_csv("car_price_dataset.csv")

#Veri seti marka ve model üzerinden tahmin yapmaya uygun değil. Owner count sütunu da gereksiz.
df.drop("Model", axis=1, inplace=True)
df.drop("Owner_Count", axis=1, inplace=True)

#Sayısal yorum yapılamyan kategorik değişkenleri one hot encoding ile sayısal hale getiriyoruz. Bu kategorik değişkenlerin arasında bir sıralama olmadığı için one hot encoding kullanıyoruz.Bu değişkenlerin arasında bir sıralama olsaydı label encoding kullanabilirdik.
#Dummy değişken tuzağından kurtulmak için de bir sütunu düşürüyoruz.
df = pd.get_dummies(df, columns=["Brand", "Fuel_Type", "Transmission"], drop_first=True)

#Bağımlı ve Bağımsız değişkenler
X = df.drop("Price", axis=1)  #Tahmin edeceğimiz sütun çıkarılıyor.
y = df["Price"]  #Hedef

#%70 eğitim, %30 test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.7, random_state=22)

#Farklı sütunlardaki değerlerin birbirine olan oranlarını daha isabetli yapabilmek için StandardScaler kullanıyoruz. StandartScaler sütunların ortalamasını 0 ve standart sapmasını 1 yapar. Min Max scaler da kullanılabilirdi.
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# lr=LinearRegression()
# model = lr.fit(X_train, y_train)
# print(model.score(X_test, y_test)) #Linear Regression 0.9990974657475485 değeri verdi. Overfitting olabilir.

# rf=RandomForestRegressor(n_estimators=300)
# model = rf.fit(X_train, y_train)
# print(model.score(X_test, y_test)) #Random Forest 0.954629940994636 değeri verdi. Daha iyi bir sonuç.

#Random Forest ile tahmin yapılacak.
model = RandomForestRegressor(n_estimators=200)
model.fit(X_train, y_train)

#Test verisi üzerinde tahmin
y_pred = model.predict(X_test)


print(df.info())
print(df.describe())

#Kullanıcı Inputları
year = int(input("Araç Yılı: "))
engine_size = float(input("Motor Hacmi (Litre): "))
mileage = int(input("Kilometre: "))
doors = int(input("Kapı Sayısı: "))

sample_data = pd.DataFrame({
    "Year": [year],
    "Engine_Size": [engine_size],
    "Mileage": [mileage],
    "Doors": [doors],
})

#Modelin beklediği tüm özellikleri tamamlıyoruz (eksik olan kategorik sütunları 0 olarak ekliyoruz)
for col in X.columns:
    if col not in sample_data.columns:
        sample_data[col] = 0  

#Kullanıcı verisini ölçeklendiriyoruz (daha önce kullanılan scaler ile dönüştürme yapılıyor)
sample_data = scaler.transform(sample_data)

#Model ile tahmin yapıyoruz
predicted_price = model.predict(sample_data)

print(f"Tahmini Araç Fiyatı: {predicted_price[0]:,.2f}")