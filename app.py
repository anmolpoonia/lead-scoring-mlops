import streamlit as st
import requests

API_URL = "https://lead-scoring-mlops.onrender.com"

  # Replace with your deployed FastAPI backend URL on Render.com

st.set_page_config(page_title="Lead Scoring System", layout="wide")
st.title("🎯 AI-Powered Lead Scoring System")

with st.form("lead_form"):
    email = st.text_input("Email", "test@example.com")
    credit_score = st.number_input("Credit Score", 300, 850, 650)
    income = st.number_input("Income ($)", 10000, 500000, 75000)
    clicks = st.number_input("Clicks", 1, 100, 15)
    time_on_site = st.number_input("Time On Site (Seconds)", 1, 3600, 300)
    age_group = st.selectbox("Age Group", ['18-25', '26-35', '36-50', '51+'])
    family_background = st.selectbox("Family Background", ['Single', 'Married', 'Married with Kids'])
    city_tier = st.selectbox("City Tier", ['T1', 'T2', 'T3'])
    comments = st.text_area("Comments", "interested in investment")

    submitted = st.form_submit_button("Score Lead")

if submitted:
    payload = {
        "email": email,
        "credit_score": credit_score,
        "income": income,
        "clicks": clicks,
        "time_on_site": time_on_site,
        "age_group": age_group,
        "family_background": family_background,
        "city_tier": city_tier,
        "comments": comments
    }

    try:
        response = requests.post(f"{API_URL}/score", json=payload)
        response.raise_for_status()
        data = response.json()

        st.metric("Initial Score", f"{data['initial_score']}%")
        st.metric("Reranked Score", f"{data['reranked_score']}%", delta=f"{data['reranked_score'] - data['initial_score']:.1f}%")
        st.info(f"Comment Impact: {data['comment_impact']}")
    except Exception as e:
        st.error(f"API request failed: {e}")
