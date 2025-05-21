# app.py
import streamlit as st
import requests

st.title("AI Prompt Generator")
API_URL = "http://localhost:8000"
USER_ID = "demo_user"

query = st.text_input("Enter your question/topic:")

if st.button("Generate"):
    with st.spinner("Generating responses..."):
        response = requests.post(f"{API_URL}/generate", json={"user_id": USER_ID, "query": query})
        if response.status_code == 200:
            data = response.json()
            st.subheader("Casual Response")
            st.write(data["casual_response"])
            st.subheader("Formal Response")
            st.write(data["formal_response"])
        else:
            st.error("Error generating response")

# Sidebar history
st.sidebar.title("History")
res = requests.get(f"{API_URL}/history", params={"user_id": USER_ID})
if res.status_code == 200:
    for item in res.json():
        with st.sidebar.expander(item["query"]):
            st.markdown(f"**Casual:** {item['casual']}")
            st.markdown(f"**Formal:** {item['formal']}")
            st.caption(item["timestamp"])
