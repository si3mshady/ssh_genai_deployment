import streamlit as st
import requests

API_URL = "http://backend:8000/analyze"
st.set_page_config(page_title="SRE + GenAI Log Analyzer", layout="wide")
st.title("🔍 SRE Log Analyzer with Mixtral")

uploaded_file = st.file_uploader("Upload logs to analyze", type=["log", "txt"])
if uploaded_file:
    with st.spinner("🧠 Contacting backend..."):
        try:
            res = requests.post(API_URL, files={"file": uploaded_file})
            data = res.json()
            st.success("✅ Analysis complete!")
            st.metric("Total Requests", data['total_requests'])
            st.metric("Errors", data['errors'])
            st.metric("Availability", f"{data['availability']}%")
            st.metric("Error Budget Remaining", f"{data['error_budget_remaining']}%")
            st.text_area("LLM Summary", value=data['summary'], height=200)
        except Exception as e:
            st.error(f"❌ Backend error: {e}")
