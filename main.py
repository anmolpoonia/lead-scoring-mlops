from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from preprocess import LeadPreprocessor

app = FastAPI()

try:
    model = joblib.load('lead_model.pkl')
    prep = joblib.load('preprocessor.pkl')
except Exception as e:
    print(f"Error loading model/preprocessor: {e}")
    model = None
    prep = None

class LeadData(BaseModel):
    email: str
    credit_score: int
    income: int
    clicks: int
    time_on_site: int
    age_group: str
    family_background: str
    city_tier: str
    comments: str

class LeadScoreResponse(BaseModel):
    email: str
    initial_score: float
    reranked_score: float
    comment_impact: str

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/score", response_model=LeadScoreResponse)
def score_lead(lead: LeadData):
    if model is None or prep is None:
        raise HTTPException(status_code=500, detail="Model or preprocessor not loaded")

    data = lead.dict()
    x = prep.preprocess_single_lead(data)
    initial_prob = model.predict_proba([x])[0][1]
    reranked_score = prep.apply_reranker_adjustment(initial_prob, lead.comments)
    
    impact_delta = reranked_score - initial_prob * 100
    if impact_delta > 0:
        impact = f"Positive (+{impact_delta:.1f})"
    elif impact_delta < 0:
        impact = f"Negative ({impact_delta:.1f})"
    else:
        impact = "No impact (0)"

    return LeadScoreResponse(
        email=lead.email,
        initial_score=round(initial_prob * 100, 2),
        reranked_score=round(reranked_score, 2),
        comment_impact=impact
    )
