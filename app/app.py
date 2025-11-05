from fastapi import FastAPI, Response
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from app.predict import Predictor

app = FastAPI(title="E-commerce Return Fraud Detector")

predictor = Predictor()

# Prometheus metrics
req_counter = Counter('predict_requests_total', 'Total predict requests')
suspicious_counter = Counter('suspicious_total', 'Total suspicious predictions')

class Req(BaseModel):
    user_age: int
    order_value: float
    days_since_delivery: int
    num_prev_returns: int
    shipping_country_same: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(r: Req):
    req_counter.inc()
    res = predictor.predict(r.dict())
    if res["suspicious"]:
        suspicious_counter.inc()
    return res

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
