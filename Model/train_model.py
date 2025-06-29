import pandas as pd
import pickle
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

df=pd.read_csv("Model/dataset/stock_data_preprocessed.csv")

X=df["Cleaned_Text"].fillna("")
y=df["Sentiment"]

print(" Converting text into TF-IDF features.....")
vectorizer=TfidfVectorizer(max_features=5000)
X_tfidf=vectorizer.fit_transform(tqdm(X, desc="Processing text"))

X_train, X_test, y_train, y_test= train_test_split(X_tfidf, y, test_size=0.2, random_state=42)


print("Training Logistic Regression model")
model=LogisticRegression()
for _ in tqdm(range(1), desc="Training model"):
    model.fit(X_train, y_train)

y_pred= model.predict(X_test)
accuracy=accuracy_score(y_test, y_pred)

print("Model accuracy: {accuracy:.4f}")
print("\n Classification report:\n", classification_report(y_test, y_pred))


print("Saving model and vectorizer.....")
with open("sentiment_model.pkl","wb") as model_file:
    pickle.dump(model, model_file)

with open("Tfidf_vectorizer.pkl","wb") as vec_file:
    pickle.dump(vectorizer, vec_file)

print("Model training complete.")