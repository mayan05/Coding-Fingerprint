from flask import Flask, request, jsonify
import os
import pickle
import traceback
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

app = Flask(__name__)

MODEL_PATH = "model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

# ==============================
# STEP 1: Load or Train Model
# ==============================
def train_and_save_model():
    """Train a simple model if model.pkl and vectorizer.pkl are missing"""
    print("⚙️ Training a new model... (demo model for fallback)")

    # Create a small synthetic dataset (you can replace with your Codeforces dataset)
    data = {
        "source_code": [
            "#include<iostream>\nusing namespace std; int main(){cout<<'Hello';}",
            "def solve(): print('Hi')",
            "#include<bits/stdc++.h>\nint main(){int n;cin>>n;while(n--){cout<<n;}}",
            "for i in range(10): print(i)",
        ],
        "rank": ["Expert", "Candidate Master", "Master", "Expert"],
        "country": ["India", "USA", "Russia", "India"]
    }
    df = pd.DataFrame(data)

    X = df["source_code"]
    y = df["rank"]  # You can modify this to predict multiple targets if your model supports that

    vectorizer = TfidfVectorizer(max_features=500)
    X_vec = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)
    model = LogisticRegression()
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"✅ Demo model trained successfully (accuracy = {acc:.2f})")

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    print("💾 Model and vectorizer saved!")

# ==============================
# STEP 2: Initialize model
# ==============================
def load_model():
    """Load model and vectorizer from disk"""
    global model, vectorizer
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        with open(VECTORIZER_PATH, "rb") as f:
            vectorizer = pickle.load(f)
        print("✅ Model and vectorizer loaded successfully.")
    except Exception as e:
        print(f"❌ Could not load model/vectorizer: {e}")
        train_and_save_model()
        load_model()

# Load at startup
load_model()

# ==============================
# STEP 3: API Routes
# ==============================
@app.route("/")
def home():
    return "✅ Codeforces Prediction API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        code = data.get("source_code", "")
        if not code.strip():
            return jsonify({"error": "No source code provided"}), 400

        X = vectorizer.transform([code])
        rank_pred = model.predict(X)[0]

        # Dummy country prediction — optional
        country_pred = "India" if "cout" in code else "USA"

        return jsonify({"rank": rank_pred, "country": country_pred})

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

# ==============================
# STEP 4: Run server
# ==============================
if __name__ == "__main__":
    app.run(debug=True, port=5000)
