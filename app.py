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

import streamlit as st
from modules.alerts import classify_alert, get_alert_color, get_alert_emoji
from modules.database import save_moderation_event, get_recent_events

st.set_page_config(
    page_title="AI Harassment Detection System",
    layout="wide",
    page_icon="🛡️"
)

# --- Sidebar ---
st.sidebar.title("🛡️ Moderator Panel")
st.sidebar.markdown("---")
st.sidebar.markdown("**Alert Level Guide**")
st.sidebar.markdown("🟢 **Low** — score < 0.4")
st.sidebar.markdown("🟡 **Moderate** — score 0.4–0.7")
st.sidebar.markdown("🔴 **High Risk** — score > 0.7")

# --- Header ---
st.title("🛡️ AI Harassment Detection System")
st.markdown("Real-time toxic content detection and moderation dashboard.")
st.markdown("---")

# --- Input Section ---
st.subheader("📝 Analyze a Message")
col1, col2 = st.columns([3, 1])

with col1:
    user_id = st.text_input("User ID", placeholder="e.g. user_42")
    message = st.text_area("Message", placeholder="Enter message to analyze...")

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    # Simulated score input (Device 3 will replace this with real Detoxify score)
    toxicity_score = st.slider("Toxicity Score (from Device 3)", 0.0, 1.0, 0.5, step=0.01)

if st.button("🔍 Analyze & Save"):
    if user_id and message:
        level = classify_alert(toxicity_score)
        emoji = get_alert_emoji(level)
        color = get_alert_color(level)

        save_moderation_event(user_id, message, toxicity_score, level)

        st.success(f"Event saved to MongoDB!")
        st.markdown(
            f"<div style='padding:16px; border-radius:8px; background-color:{color}22; "
            f"border-left: 5px solid {color};'>"
            f"<b>{emoji} Alert Level: {level}</b><br>"
            f"Score: <b>{toxicity_score:.2f}</b><br>"
            f"User: <b>{user_id}</b>"
            f"</div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("Please fill in both User ID and Message.")

st.markdown("---")

# --- Recent Events Table ---
st.subheader("📋 Recent Moderation Events")

events = get_recent_events(20)
if events:
    for e in events:
        level = e.get("alert_level", "Low")
        emoji = get_alert_emoji(level)
        color = get_alert_color(level)
        st.markdown(
            f"<div style='margin-bottom:8px; padding:10px; border-radius:6px; "
            f"background-color:{color}18; border-left:4px solid {color};'>"
            f"{emoji} <b>{level}</b> | Score: <b>{e['toxicity_score']:.2f}</b> | "
            f"User: <code>{e['user_id']}</code> | "
            f"<i>{str(e['timestamp'])[:19]}</i><br>"
            f"<span style='color:#ccc;'>{e['message'][:100]}</span>"
            f"</div>",
            unsafe_allow_html=True
        )
else:
    st.info("No moderation events yet. Analyze a message to get started.")    