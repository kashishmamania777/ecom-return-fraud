# 🛍️ E-commerce Return Fraud Detector — Complete Local Setup Guide

This guide helps you set up, train, test, and run the **AI + DevOps E-commerce Return Fraud Detection app** locally using **VS Code**.

It includes:
- 🧠 Model training (scikit-learn)
- ⚡ FastAPI service (`/predict`, `/health`, `/metrics`)
- 🐳 Docker build/run
- 🧪 Unit testing
- 🌐 Modern UI

---

## 🚀 Quick Copy-Paste Commands (PowerShell in VS Code)

> ⚠️ Run these **one section at a time** inside VS Code’s Terminal  
> (Make sure you’re in the project root folder: `C:\Users\kashu\ecom-return-fraud`)

```powershell
# =============================
# 🧩 1️⃣ SETUP ENVIRONMENT
# =============================

# Create and activate virtual environment
python -m venv .venv
# If activation fails, run this once:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1

# Upgrade pip and install dependencies
python -m pip install --upgrade pip
python -m pip install -r .\app\requirements.txt
python -m pip install pytest scikit-learn joblib pandas numpy

# Ensure __init__.py exists
if (-not (Test-Path .\app\__init__.py)) { New-Item -ItemType File -Path .\app\__init__.py -Force }

# =============================
# 🧠 2️⃣ TRAIN MODEL
# =============================
python train.py
# (Generates data/train.csv and model/model.pkl)

# =============================
# 🧪 3️⃣ RUN TESTS
# =============================
python -m pytest -q

# =============================
# ⚡ 4️⃣ START FASTAPI SERVER
# =============================
python -m uvicorn app.app:app --reload --host 0.0.0.0 --port 8000
# Keep this running — it serves your API and UI

# =============================
# 🔍 5️⃣ TEST ENDPOINTS (NEW TERMINAL)
# =============================

# HEALTH CHECK
Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET | Select-Object -ExpandProperty Content

# PREDICTION
Invoke-WebRequest -Uri "http://localhost:8000/predict" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"user_age":22,"order_value":320,"days_since_delivery":2,"num_prev_returns":2,"shipping_country_same":0}' |
  Select-Object -ExpandProperty Content

# METRICS
Invoke-WebRequest -Uri "http://localhost:8000/metrics" -Method GET | Select-Object -ExpandProperty Content

# =============================
# 🌐 6️⃣ OPEN WEB UI
# =============================
# Open in your browser:
# 👉 http://localhost:8000/
# (Do not use 0.0.0.0)

# =============================
# 🐳 7️⃣ DOCKER BUILD & RUN (OPTIONAL)
# =============================

# Build the image
docker build -t ecom-fraud-demo:latest .

# Run the container
docker run --rm -p 8000:8000 -v ${PWD}\model:/app/model ecom-fraud-demo:latest

# Test inside container
Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET | Select-Object -ExpandProperty Content

# =============================
# 🧱 8️⃣ DOCKER COMPOSE (OPTIONAL)
# =============================
docker-compose up --build
# To stop:
docker-compose down

# =============================
# 🧰 9️⃣ USEFUL DEBUGGING COMMANDS
# =============================
python -c "import sys; print(sys.executable)"      # Check Python path
Test-NetConnection -ComputerName localhost -Port 8000   # Check if port open
docker ps                                          # List running containers
docker logs -f <container_id>                      # View logs
docker-compose logs -f                             # Logs for docker-compose
