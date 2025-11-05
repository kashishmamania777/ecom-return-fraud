import joblib

MODEL_PATH = "model/model.pkl"

class Predictor:
    def __init__(self, model_path=MODEL_PATH):
        self.model = joblib.load(model_path)
        self.features = [
            "user_age",
            "order_value",
            "days_since_delivery",
            "num_prev_returns",
            "shipping_country_same"
        ]

    def predict(self, payload: dict):
        x = [payload.get(f, 0) for f in self.features]
        proba = self.model.predict_proba([x])[0][1]
        label = int(proba > 0.5)
        return {"suspicious": label, "score": float(proba)}
