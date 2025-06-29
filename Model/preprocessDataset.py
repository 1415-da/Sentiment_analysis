import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm
import os

# Download NLTK data only if not already present
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)

print("Current working directory:", os.getcwd())
print("Files in current directory:", os.listdir())

df = pd.read_csv("Model/dataset/stock_data.csv")

# Load stopwords and lemmatizer once
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

# Show progress bar for large datasets
tqdm.pandas(desc="Cleaning Text")
df["Cleaned_Text"] = df["Text"].progress_apply(clean_text)

df.to_csv("Model/dataset/stock_data_preprocessed.csv", index=False)
print("Dataset preprocessing complete.")