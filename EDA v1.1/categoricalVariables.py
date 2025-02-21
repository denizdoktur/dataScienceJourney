import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

traffic = pd.read_csv("traffic_accidents.csv")

df = traffic.copy()

kat_df = df.select_dtypes(include=["object"])

df["damage"].value_counts().plot(kind="barh",  figsize=(10, 6))

plt.title("Zarar Dağılımı")
plt.xlabel("Kaza Sayısı")
plt.ylabel("Tahmini Zarar")

plt.show()