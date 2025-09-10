import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:5000"

st.title("📊 Smart Feedback Analyzer")
st.write("Submit feedback and analyze sentiment trends")

# Submit Feedback
st.header("Submit New Feedback")
user_feedback = st.text_area("Enter your feedback here:")

if st.button("Submit"):
    if user_feedback.strip():
        response = requests.post(f"{API_URL}/submit_feedback", json={"feedback": user_feedback})
        if response.status_code == 200:
            st.success("Feedback submitted successfully!")
            st.json(response.json())
        else:
            st.error("Failed to submit feedback")
    else:
        st.warning("Feedback cannot be empty")

# View Feedback Data
st.header("All Feedback Data")
response = requests.get(f"{API_URL}/get_feedback")

if response.status_code == 200:
    data = response.json()
    if data:
        df = pd.DataFrame(data)

        st.dataframe(df)

        # Sentiment Count Plot
        st.subheader("Sentiment Distribution")
        sentiment_counts = df["sentiment"].value_counts()
        fig, ax = plt.subplots()
        sentiment_counts.plot(kind="bar", ax=ax)
        ax.set_ylabel("Count")
        ax.set_xlabel("Sentiment")
        st.pyplot(fig)

    else:
        st.info("No feedback yet.")
else:
    st.error("Could not fetch feedback data.")
