import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# https://www.kaggle.com/datasets/oktayrdeki/traffic-accidents
traffic = pd.read_csv("traffic_accidents.csv")

df = traffic.copy()

#Sayısal Sütunları Burada Seçiyoruz
numeric_df = df.select_dtypes(include=["number"])

#Kategorik sütunları burada label encoding işlemine tabi tutuyoruz.
from sklearn.preprocessing import LabelEncoder

label_encoders = {}
for col in df.select_dtypes(include=["object"]).columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

correlation_matrix = df.corr()

plt.figure(figsize=(14, 10))
sns.heatmap(correlation_matrix, annot=False, cmap="coolwarm", linewidths=0.5)
plt.title("Kazalar Korelasyon Matrisi")
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
