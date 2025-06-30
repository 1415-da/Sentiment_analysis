# Stock Market Sentiment Analysis

A full-stack web application for analyzing the sentiment of stock market-related texts (news, tweets, etc.) using machine learning. The project features a visually appealing React frontend and a Flask backend with a trained sentiment analysis model.

---

## Features
- **Stock market themed UI** with animations
- **Input any text** (news, tweets, etc.) and get instant sentiment (positive/negative)
- **Machine learning backend** (Python, Flask, scikit-learn)
- **Pre-trained model** using TF-IDF and Logistic Regression
- **Easy deployment** (Vercel for frontend, Render/Heroku for backend)

---

## Project Structure
```
Sentiment_analysis/
│
├── Backend/           # Flask API
│   ├── app.py
│   ├── requirements.txt
│   └── model/
│       ├── sentiment_model.pkl
│       └── tfidf_vectorizer.pkl
│
├── Frontend/          # React app
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js
│       └── index.js
│
├── Model/             # Data and training scripts
│   ├── stock_data.csv
│   ├── train_model.py
│   └── preprocessDataset.py
│
└── README.md
```

---

## Getting Started (Local Development)

### 1. **Clone the repository**
```sh
git clone <your-repo-url>
cd Sentiment_analysis
```

### 2. **Backend Setup**
```sh
cd Backend
pip install -r requirements.txt
python app.py
```
- The backend will run on `http://localhost:5000`

### 3. **Frontend Setup**
```sh
cd Frontend
npm install
npm run dev
```
- The frontend will run on `http://localhost:3000`
- The browser should open automatically. If not, open it manually.

### 4. **Model Training (if needed)**
If you want to retrain the model:
```sh
cd Model
python train_model.py
```
This will update the model files in `Backend/model/`.


## API Endpoint
- **POST** `/predict`
  - **Body:** `{ "text": "Your text here" }`
  - **Response:** `{ "sentiment": 1 }` (1 = positive, -1 = negative)

---

## License
MIT
