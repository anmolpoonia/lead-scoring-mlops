# AI-Powered Lead Scoring System with Reranker Adjustment

This project implements an end-to-end MLOps pipeline for lead scoring, including:

- Synthetic dataset generation (~1000 samples)
- Preprocessing with categorical encoding
- Model training with XGBoost and MLflow tracking
- FastAPI backend serving scoring predictions with comment-based reranker adjustment
- Optional Streamlit frontend for interactive lead input
- Dockerized for container deployment

## How to run locally

pip install -r requirements.txt
python generate_data.py
python train_model.py
uvicorn main:app --reload
streamlit run app.py

## Deployment

Designed for easy deployment on Render.com or any Docker-compatible cloud with zero infrastructure setup.
You now have a fully working modular MLOps repo that you can push to GitHub and deploy on Render.com or any Docker container service.
---

Feel free to explore, modify, and extend!

