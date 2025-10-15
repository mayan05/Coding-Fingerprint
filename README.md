# Coding-Fingerprint

A lightweight ML-powered tool that predicts a Codeforces user's rank and country from their source code. It consists of a Flask API for inference and a Streamlit UI for an easy, polished user experience.

Made with ❤️ by Mohammed Bilal and Mayan Sequeira.

## Features
- Simple REST API: `POST /predict` with `source_code`
- Streamlit frontend: paste or upload `.cpp`, `.py`, `.java`, `.txt`
- Robust inference: supports `predict_proba` or falls back to `predict`
- Ready-made artifacts: `model.pkl`, `vectorizer.pkl`

## Quickstart
1) Create environment and install deps
   - With uv (recommended):
     ```bash
     uv venv
     uv pip install -r <(uv pip compile pyproject.toml -q) || true
     uv pip install flask streamlit scikit-learn
     ```
   - With pip:
     ```bash
     python -m venv .venv
     .venv\\Scripts\\activate  # Windows PowerShell
     pip install -U pip
     pip install -r requirements.txt  # if you create one
     pip install flask streamlit scikit-learn numpy pandas requests
     ```

2) Ensure artifacts are present in project root
   - `model.pkl` (can contain rank and optionally country classifier)
   - `vectorizer.pkl` (the text/code vectorizer)

3) Run backend (Flask API)
   ```bash
   python backend.py
   ```
   - Starts at `http://127.0.0.1:5000/`

4) Run frontend (Streamlit UI)
   ```bash
   streamlit run frontend.py
   ```
   - By default, it expects the backend at `http://127.0.0.1:5000/predict`

## API
### POST /predict
Request
```json
{
  "source_code": "# your source code as a single string"
}
```

Response (success)
```json
{
  "rank": "Expert",
  "country": "India"
}
```

Response (error)
```json
{
  "error": "Model or vectorizer not loaded"
}
```

## Project Structure
```
Coding-Fingerprint/
├─ backend.py                 # Flask inference API
├─ frontend.py                # Streamlit UI
├─ data_creation.py           # Codeforces data collection to CSV
├─ model.pkl                  # Trained model (rank and optionally country)
├─ vectorizer.pkl             # Fitted vectorizer for source code
├─ enhanced_codeforces_dataset.csv
├─ codeforces_filtered_users.csv
├─ codeforces_prediction.ipynb
├─ data_cleaning.ipynb
├─ pyproject.toml             # Project metadata and base deps
├─ uv.lock                    # Lockfile (if using uv)
├─ LICENSE
└─ README.md
```

## Data and Training Artifacts
- `data_creation.py`: pulls Codeforces users via public API in batches and writes users with both `rank` and `country` to `codeforces_filtered_users.csv`.
- `enhanced_codeforces_dataset.csv`: curated dataset used during experimentation/training.
- `model.pkl` and `vectorizer.pkl`: required at runtime. The model may be:
  - A dict with keys like `rank_model` and optionally `country_model`, or
  - A 2-tuple/list `(rank_model, country_model)`, or
  - A single classifier (rank only).

At inference, the backend will load these artifacts on startup and expose the `/predict` endpoint.

## Troubleshooting
- Backend prints: `Failed to load artifacts: ...`
  - Ensure `model.pkl` and `vectorizer.pkl` exist in project root and match the training versions (e.g., scikit-learn version compatibility).
- Frontend shows connection error
  - Verify Flask is running at `http://127.0.0.1:5000` and update `backend_url` in `frontend.py` if needed.
- Missing packages when unpickling model
  - Install `scikit-learn` to match the model. If version mismatch errors occur, consider re-exporting the model with your current version or using a compatible version.

## Development
- Python: >= 3.13 (see `pyproject.toml`)
- Core libs: `flask`, `streamlit`, `numpy`, `pandas`, `requests`, `scikit-learn`

## License
This project is licensed under the terms of the license found in `LICENSE`.
