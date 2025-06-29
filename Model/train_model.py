import pandas as pd
import re
import nltk
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import os

nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")

df = pd.read_csv("Model/stock_data.csv")
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

df["Cleaned_Text"] = df["Text"].apply(clean_text)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["Cleaned_Text"])
y = df["Sentiment"]

model = LogisticRegression(max_iter=200)
model.fit(X, y)

# Ensure Backend/model directory exists
os.makedirs("../Backend/model", exist_ok=True)

with open("../Backend/model/tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
with open("../Backend/model/sentiment_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model and vectorizer saved!")