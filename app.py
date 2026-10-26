
import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# Page settings
st.set_page_config(
    page_title="PhishShift - Message Risk Scanner",
    page_icon="🛡️",
    layout="wide"
)

# Load trained SMS spam model
MODEL_PATH = Path(__file__).parent / "phishshift_model.pkl"
model = joblib.load(MODEL_PATH)

# Session statistics and scan history
if "total" not in st.session_state:
    st.session_state["total"] = 0

if "spam" not in st.session_state:
    st.session_state["spam"] = 0

if "ham" not in st.session_state:
    st.session_state["ham"] = 0

if "history" not in st.session_state:
    st.session_state["history"] = []

# Custom styling
st.markdown("""
<style>
.stApp {
    background-color: #10131a;
    color: #f1f5f9;
}
h1 {
    color: #64b5f6;
}
[data-testid="stMetric"] {
    background-color: #1c2331;
    padding: 18px;
    border-radius: 12px;
}
.stButton button {
    background-color: #1976d2;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🛡️ PhishShift")
st.subheader("Message Risk Scanner")
st.write(
    "Check an SMS message for spam-related warning signs. "
    "This prototype is not a verified phishing detector."
)

# Dashboard
st.markdown("### 📊 Dashboard")
c1, c2, c3 = st.columns(3)
c1.metric("Messages Checked", st.session_state["total"])
c2.metric("Spam Predictions", st.session_state["spam"])
c3.metric("Legitimate Predictions", st.session_state["ham"])

st.divider()

# Message scanner
st.markdown("### 🔍 Scan a Message")
message = st.text_area(
    "Paste your SMS message here:",
    placeholder="Example: Congratulations! You have won a prize. Claim now...",
    height=150
)

if st.button("Scan Message", use_container_width=True):
    if not message.strip():
        st.warning("Please enter a message first.")
    else:
        prediction = model.predict([message])[0]
        st.session_state["history"].append({
    "Message": message,
    "Prediction": prediction,
    "Time": pd.Timestamp.now().strftime("%H:%M:%S")
})
        st.session_state["total"] += 1

        if prediction == "spam":
            st.session_state["spam"] += 1
            st.error("⚠️ Spam-like message detected")
            st.write(
                "The model classified this message as SMS spam. "
                "Check any links, requests for money, or requests for personal details."
            )
        else:
            st.session_state["ham"] += 1
            st.success("✅ Classified as likely legitimate")
            st.write(
                "The model classified this message as ham. "
                "This does not guarantee that the message is safe."
            )

        st.caption(
            "Research demo only: the model was trained on an SMS spam dataset, "
            "not a verified phishing dataset."
        )

st.divider()
st.caption("PhishShift | Educational cybersecurity prototype")

# Scan History
st.divider()
st.markdown("### 📜 Scan History")

if st.session_state["history"]:
    history_df = pd.DataFrame(st.session_state["history"])

    st.dataframe(history_df, use_container_width=True)

    st.download_button(
        label="📥 Download Scan History",
        data=history_df.to_csv(index=False).encode("utf-8"),
        file_name="phishshift_scan_history.csv",
        mime="text/csv"
    )
else:
    st.info("No messages scanned yet.")

# Graph Dashboard
st.subheader("📊 Message Analysis Dashboard")

# Prepare chart data from scan history
if st.session_state["history"]:
    chart_data = pd.DataFrame(st.session_state["history"])

    # Count each prediction type
    prediction_counts = chart_data["Prediction"].value_counts()

    col1, col2 = st.columns(2)

    with col1:
        st.write("### 🥧 Message Distribution")
        st.bar_chart(prediction_counts)

    with col2:
        st.write("### 📊 Scan Results")
        st.dataframe(
            prediction_counts.rename_axis("Prediction").reset_index(name="Count"),
            use_container_width=True
        )
else:
    st.info("Scan a few messages to see your charts here.")

