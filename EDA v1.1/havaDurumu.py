import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.api.types import CategoricalDtype
# https://www.kaggle.com/datasets/oktayrdeki/traffic-accidents
traffic = pd.read_csv("traffic_accidents.csv")

df = traffic.copy()

crosstab2 = pd.crosstab(df["intersection_related_i"], df["most_severe_injury"])
plt.figure(figsize=(10, 5))
sns.heatmap(crosstab2, cmap="Blues", annot=True, fmt="d")
plt.title("Kesişime Bağlı Kazalar ve Yaralanma Şiddeti Arasındaki İlişki")
plt.xlabel("Yaralanma Durumu")
plt.ylabel("Kesişimle İlgili mi? (Evet/Hayır)")
plt.show()
