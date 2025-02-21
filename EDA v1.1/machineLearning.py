import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
# https://www.kaggle.com/datasets/oktayrdeki/traffic-accidents
data = pd.read_csv('traffic_accidents.csv')

#crash_date sütununu düzenleme
data['crash_date'] = pd.to_datetime(data['crash_date'], format='%m/%d/%Y %I:%M:%S %p')
data['crash_date'] = data['crash_date'].astype('int64')

#kategorik sütunlara label encoding
label_encoders = {}
categorical_columns = ['traffic_control_device', 'weather_condition', 'lighting_condition', 'first_crash_type', 'trafficway_type',
                       'alignment', 'roadway_surface_cond', 'road_defect', 'crash_type', 'intersection_related_i',
                       'damage', 'prim_contributory_cause', 'most_severe_injury']

for column in categorical_columns:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

#Hedef değişken
y = data['crash_type']
X = data.drop('crash_type', axis=1)

#Standart Scaler
numeric_columns = X.select_dtypes(include=['int64', 'float64']).columns
scaler = StandardScaler()
X[numeric_columns] = scaler.fit_transform(X[numeric_columns])

# Eğitim ve test serisi ayrımı
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest modelinin kullanımı
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Doğruluk: {accuracy:.4f}")

print(classification_report(y_test, y_pred))

