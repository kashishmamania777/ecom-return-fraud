import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

os.makedirs("data", exist_ok=True)
os.makedirs("model", exist_ok=True)

# Generate synthetic data
np.random.seed(0)
n = 300
user_age = np.random.randint(18, 70, size=n)
order_value = np.random.uniform(10, 500, size=n)
days_since_delivery = np.random.randint(0, 60, size=n)
num_prev_returns = np.random.poisson(0.3, size=n)
shipping_country_same = np.random.choice([0, 1], size=n, p=[0.2, 0.8])

# Define suspiciousness score
score = (order_value / 200) + (num_prev_returns * 1.5) + (1 - shipping_country_same) * 1.2 - (days_since_delivery / 30)
prob = 1 / (1 + np.exp(-score))
y = (prob > 0.6).astype(int)

df = pd.DataFrame({
    "user_age": user_age,
    "order_value": order_value,
    "days_since_delivery": days_since_delivery,
    "num_prev_returns": num_prev_returns,
    "shipping_country_same": shipping_country_same,
    "is_suspicious": y
})
df.to_csv("data/train.csv", index=False)

# Train model
X = df.drop(columns=["is_suspicious"])
y = df["is_suspicious"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
clf = RandomForestClassifier(n_estimators=50, random_state=1)
clf.fit(X_train, y_train)
acc = clf.score(X_test, y_test)

joblib.dump(clf, "model/model.pkl")
print(f"✅ Model trained and saved to model/model.pkl | Accuracy: {acc:.2f}")
