import os
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "sentiment_model.pkl")
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "model", "Tfidf_vectorizer.pkl")

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

@app.route("/", methods=["GET"])
def home():
    return "Sentiment Analysis API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    # Preprocess (should match training)
    import re
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    nltk.download("stopwords")
    nltk.download("punkt")
    nltk.download("wordnet")
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    def clean_text(text):
        text = str(text).lower()
        text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word not in stop_words]
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        return " ".join(tokens)
    cleaned = clean_text(text)
    X = vectorizer.transform([cleaned])
    pred = model.predict(X)[0]
    return jsonify({"sentiment": int(pred)})

if __name__ == "__main__":
    app.run(debug=True) 