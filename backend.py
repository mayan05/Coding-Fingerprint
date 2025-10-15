from flask import Flask, request, jsonify
import pickle
import traceback
import numpy as np

app = Flask(__name__)

MODEL_PATH = "model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

model = None
vectorizer = None
rank_model = None
country_model = None


def load_artifacts():
    global model, vectorizer, rank_model, country_model
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, "rb") as f:
        vectorizer = pickle.load(f)
    # Normalize handles
    if isinstance(model, dict):
        rank_model = model.get("rank_model") or model.get("rank")
        country_model = model.get("country_model") or model.get("country")
    elif isinstance(model, (list, tuple)) and len(model) == 2:
        rank_model, country_model = model[0], model[1]
    else:
        rank_model = model
        country_model = None


def most_probable_label(clf, X):
    try:
        if hasattr(clf, "predict_proba") and hasattr(clf, "classes_"):
            prob = clf.predict_proba(X)[0]
            idx = int(np.argmax(prob))
            return clf.classes_[idx]
        # Fall back to predict
        y = clf.predict(X)
        return y[0]
    except Exception:
        # Final fallback to prior if available
        if hasattr(clf, "class_count_") and hasattr(clf, "classes_"):
            counts = clf.class_count_
            return clf.classes_[int(np.argmax(counts))]
        if hasattr(clf, "class_prior_") and hasattr(clf, "classes_"):
            priors = clf.class_prior_
            return clf.classes_[int(np.argmax(priors))]
        return None


# Load artifacts at startup
try:
    load_artifacts()
except Exception as e:
    # Surface clear error so the user can fix artifacts
    print(f"Failed to load artifacts: {e}")


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

        if vectorizer is None or rank_model is None:
            return jsonify({"error": "Model or vectorizer not loaded"}), 500

        X = vectorizer.transform([code])

        # Rank
        rank_pred = most_probable_label(rank_model, X)
        if rank_pred is None:
            rank_pred = "Expert"

        # Country (if available)
        if country_model is not None:
            country_pred = most_probable_label(country_model, X)
            if country_pred is None:
                country_pred = "India"
        else:
            country_pred = "India"

        return jsonify({"rank": str(rank_pred), "country": str(country_pred)})

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)