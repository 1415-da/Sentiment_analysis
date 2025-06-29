import pickle
import sys
from sklearn.feature_extraction.text import TfidfVectorizer

def load_pickle(file_path):
    """Loads a pickle file."""
    with open(file_path, "rb") as file:
        return pickle.load(file)
    


def predict_sentiment(news_text):
    """Predicts sentiment for a given news article."""
    vectorizer=load_pickle("Model/Tfidf_vectorizer.pkl")
    model=load_pickle("Model/sentiment_model.pkl")

    news_tfidf=vectorizer.transform([news_text])

    sentiment= model.predict(news_tfidf)[0]

    return "Positive" if sentiment == 1 else "Negative"


if __name__=="__main__":
    print(predict_sentiment("good growth ahead"))
    print(predict_sentiment("loss, downtrend, bad news"))