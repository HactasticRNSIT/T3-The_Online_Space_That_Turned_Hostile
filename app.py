import streamlit as st
from modules.toxicity import analyze_text

st.set_page_config(
    page_title="AI Harassment Detection System",
    layout="wide"
)

st.title("AI Harassment Detection System")

st.sidebar.title("Moderator Panel")

message = st.text_area("Enter Message")

if st.button("Analyze"):
    result = analyze_text(message)
    st.write(result)