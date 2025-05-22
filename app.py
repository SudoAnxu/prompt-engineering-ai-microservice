# app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # just in case you ever want to pull API_URL from env

st.title("AI Prompt Generator")

API_URL = os.getenv("API_URL", "https://prompt-engineering-ai-microservice.onrender.com")
USER_ID = os.getenv("USER_ID", "demo_user")

query = st.text_input("Enter your question/topic:")

if st.button("Generate"):
    with st.spinner("Generating responses..."):
        try:
            response = requests.post(
                f"{API_URL}/generate",
                json={"user_id": USER_ID, "query": query},
                timeout=15
            )
            response.raise_for_status()
            data = response.json()
            st.subheader("Casual Response")
            st.write(data["casual_response"])
            st.subheader("Formal Response")
            st.write(data["formal_response"])
        except requests.RequestException as e:
            st.error(f"Request error: {e}")

# Sidebar history
st.sidebar.title("History")
try:
    res = requests.get(
        f"{API_URL}/history",
        params={"user_id": USER_ID},
        timeout=10
    )
    res.raise_for_status()
    for item in res.json():
        with st.sidebar.expander(item["query"]):
            st.markdown(f"**Casual:** {item['casual']}")
            st.markdown(f"**Formal:** {item['formal']}")
            st.caption(item["timestamp"])
except requests.RequestException:
    st.sidebar.error("Could not load history.")
