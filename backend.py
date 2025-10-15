from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Possible ranks and countries
RANKS = ["Newbie", "Pupil", "Specialist", "Expert", "Candidate Master", "Master", "Grandmaster"]
COUNTRIES = ["India", "USA", "Russia", "Ukraine", "UK", "Germany", "China", "Canada"]

@app.route("/")
def home():
    return "✅ Prediction API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        code = data.get("source_code", "")

        if not code.strip():
            return jsonify({"error": "No source code provided"}), 400

        # Simple demo logic: random rank and country based on code length & language hints
        code_lower = code.lower()
        if "include" in code_lower or "int main" in code_lower:
            likely_lang = "C++"
        elif "def " in code_lower or "print(" in code_lower:
            likely_lang = "Python"
        elif "console.log" in code_lower:
            likely_lang = "JavaScript"
        else:
            likely_lang = "Other"

        # Random rank and country
        rank_pred = random.choice(RANKS)
        country_pred = random.choice(COUNTRIES)

        return jsonify({"rank": rank_pred, "country": country_pred})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "_main_":
    app.run(debug=True, port=5000)