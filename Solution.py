import streamlit as st
import joblib
import requests

# Load vectorizer and model
vectorizer = joblib.load("vectorizer.jb")
model = joblib.load("lr_model.jb")

# NewsAPI Key (Replace with your free API key)
NEWS_API_KEY = "0a7d08c67cb4402abb2c9d9b885e7682"

# Function to search real-time news using NewsAPI
def search_news_api(query):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()

    if response["status"] == "ok" and response["totalResults"] > 0:
        return True, response["articles"][0]["title"] + " - " + response["articles"][0]["description"]
    return False, None

st.title("Fake News Detector")
st.write("Enter a News Article below to check whether it is Fake or Real.")

news_input = st.text_area("News Article:", "")

if st.button("Check News"):
    if news_input.strip():
        # Search real-time news
        found, news_article = search_news_api(news_input)

        if found:
            st.success(f"✅ *Verified News!*\n\n{news_article}")
        else:
            # Predict using ML model
            transform_input = vectorizer.transform([news_input])
            prediction = model.predict(transform_input)

            if prediction[0] == 1:
                st.success("The News is Real!")
            else:
                st.error("The News is Fake!")

            st.warning("⚠ This news can't be verified in real-time.")
    else:
        st.warning("Please enter some text to analyze.")
