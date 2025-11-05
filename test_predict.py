from app.predict import Predictor

def test_predict():
    p = Predictor(model_path="model/model.pkl")
    sample = {
        "user_age": 25,
        "order_value": 400,
        "days_since_delivery": 1,
        "num_prev_returns": 3,
        "shipping_country_same": 0
    }
    out = p.predict(sample)
    assert "score" in out and "suspicious" in out
    assert isinstance(out["suspicious"], int)
