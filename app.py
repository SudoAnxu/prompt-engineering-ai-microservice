import streamlit as st
import requests

st.title("AI Prompt Generator")

API_URL = "https://prompt-engineering-ai-microservice.onrender.com"
USER_ID = "demo_user"

query = st.text_input("Enter your question/topic:")

if st.button("Generate"):
    with st.spinner("Generating responses..."):
        try:
            response = requests.post(f"{API_URL}/generate", json={"user_id": USER_ID, "query": query}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                st.subheader("Casual Response")
                st.write(data["casual_response"])
                st.subheader("Formal Response")
                st.write(data["formal_response"])
            else:
                st.error("Error generating response")
        except Exception as e:
            st.error(f"API call failed: {e}")

# Sidebar history
@st.cache_data(ttl=60)
def get_history():
    try:
        res = requests.get(f"{API_URL}/history", params={"user_id": USER_ID}, timeout=5)
        if res.status_code == 200:
            return res.json()
        else:
            return []
    except Exception as e:
        return []

st.sidebar.title("History")
history = get_history()
for item in history:
    with st.sidebar.expander(item["query"]):
        st.markdown(f"**Casual:** {item['casual']}")
        st.markdown(f"**Formal:** {item['formal']}")
        st.caption(item["timestamp"])
