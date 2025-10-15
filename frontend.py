import streamlit as st
import requests

# =========================
# 🌟 PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Codeforces Rank & Country Predictor",
    page_icon="⚙️",
    layout="wide",
)

# =========================
# 🎨 HEADER
# =========================
st.markdown(
    """
    <style>
    .main-title {
        font-size: 38px;
        font-weight: 700;
        text-align: center;
        color: #2F80ED;
        margin-bottom: 10px;
    }
    .sub-text {
        text-align: center;
        color: #555;
        font-size: 17px;
        margin-bottom: 30px;
    }
    .stTextArea textarea {
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 15px;
        background-color: #f8f9fa;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="main-title">⚙️ Codeforces Rank & Country Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Upload or paste your source code to predict your rank and country 🚀</p>', unsafe_allow_html=True)

# =========================
# 🔗 BACKEND URL
# =========================
backend_url = "http://127.0.0.1:5000/predict"  # Flask backend URL

# =========================
# 📤 FILE UPLOAD OR TEXT
# =========================
col1, col2 = st.columns([2, 1])

with col1:
    upload_option = st.radio("Choose Input Method:", ["🧾 Paste Code", "📂 Upload File"], horizontal=True)

    code_input = ""
    if upload_option == "🧾 Paste Code":
        code_input = st.text_area("💻 Paste your C++ or Python code below:", height=320)
    else:
        uploaded_file = st.file_uploader("📁 Upload a source code file (.cpp, .py, .txt)", type=["cpp", "py", "txt"])
        if uploaded_file is not None:
            code_input = uploaded_file.read().decode("utf-8")
            st.code(code_input, language="cpp")

with col2:
    st.info(
        """
        ### 💡 Tips
        - Supports `.cpp`, `.py`, and `.txt` files  
        - Make sure your backend (Flask) is running  
        - Click **Predict** to see model output  
        """
    )

# =========================
# 🔍 PREDICTION
# =========================
st.markdown("---")
predict_button = st.button("🚀 Predict My Rank & Country", use_container_width=True)

if predict_button:
    if not code_input.strip():
        st.warning("⚠️ Please provide source code input!")
    else:
        with st.spinner("Predicting... Please wait ⏳"):
            try:
                response = requests.post(backend_url, json={"source_code": code_input})
                result = response.json()

                if "error" in result:
                    st.error(f"❌ {result['error']}")
                else:
                    st.success("✅ Prediction Successful!")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("🏅 Predicted Rank", result["rank"])
                    with col2:
                        st.metric("🌍 Predicted Country", result["country"])

                    # Optional: show highlighted source code
                    st.markdown("### 🧩 Source Code Preview")
                    st.code(code_input, language="cpp")

            except Exception as e:
                st.error(f"🚫 Failed to connect to backend: {e}")

# =========================
# ⚙️ FOOTER
# =========================
st.markdown(
    """
    <hr>
    <p style='text-align:center;color:gray;'>
    Made with ❤️ by <b>Mohammed Bilal</b> | Powered by Streamlit & Flask
    </p>
    """,
    unsafe_allow_html=True
)
