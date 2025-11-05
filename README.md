# 🛍️ E-commerce Return Fraud Detector (AI + DevOps Demo)

**One-line summary:**  
We used AI + DevOps to detect suspicious product returns in E-commerce by training a small model in CI, packaging it in Docker, and deploying an API that serves predictions and metrics.

---

## 🚀 Features
- Trains a small ML model (RandomForest) on synthetic data  
- FastAPI service exposing:
  - `/predict` → classify return request as suspicious or not
  - `/health` → health check
  - `/metrics` → Prometheus metrics
- Dockerized app + GitHub Actions CI pipeline
- Simple deployment via `docker-compose`

---

## 🧠 How to run locally

```bash
python train.py
pytest -q
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
