import streamlit as st

from modules.toxicity import analyze_text
from modules.alerts import (
    classify_alert,
    get_alert_color,
    get_alert_emoji
)

from modules.database import (
    save_moderation_event,
    get_recent_events
)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Harassment Detection System",
    layout="wide",
    page_icon="🛡️"
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("🛡️ Moderator Panel")

st.sidebar.markdown("---")

st.sidebar.markdown("### Alert Level Guide")

st.sidebar.markdown("🟢 **Low** — score < 0.4")
st.sidebar.markdown("🟡 **Moderate** — score 0.4–0.7")
st.sidebar.markdown("🔴 **High Risk** — score > 0.7")

st.sidebar.markdown("---")

st.sidebar.success("Monitoring System Active")

# -----------------------------------
# HEADER
# -----------------------------------

st.title("🛡️ AI Harassment Detection System")

st.markdown(
    """
    Real-time AI-powered moderation dashboard
    for detecting toxic and hostile digital interactions.
    """
)

st.markdown("---")

# -----------------------------------
# INPUT SECTION
# -----------------------------------

st.subheader("📝 Analyze a Message")

col1, col2 = st.columns([3, 1])

with col1:

    user_id = st.text_input(
        "User ID",
        placeholder="e.g. user_42"
    )

    message = st.text_area(
        "Message",
        placeholder="Enter message to analyze..."
    )

with col2:

    st.markdown("<br>", unsafe_allow_html=True)

    analyze_button = st.button("🔍 Analyze")

# -----------------------------------
# ANALYSIS
# -----------------------------------

if analyze_button:

    if user_id and message:

        # -------------------------------
        # TOXICITY ANALYSIS
        # -------------------------------

        result = analyze_text(message)

        toxicity_score = float(result["toxicity"])

        insult_score = float(result["insult"])

        threat_score = float(result["threat"])

        # -------------------------------
        # ALERT CLASSIFICATION
        # -------------------------------

        level = classify_alert(toxicity_score)

        emoji = get_alert_emoji(level)

        color = get_alert_color(level)

        # -------------------------------
        # SAVE TO DATABASE
        # -------------------------------

        save_moderation_event(
            user_id,
            message,
            toxicity_score,
            level
        )

        # -------------------------------
        # SUCCESS MESSAGE
        # -------------------------------

        st.success("Moderation event saved successfully!")

        # -------------------------------
        # METRICS
        # -------------------------------

        st.subheader("📊 Toxicity Analysis")

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Toxicity",
            round(toxicity_score, 2)
        )

        m2.metric(
            "Insult",
            round(insult_score, 2)
        )

        m3.metric(
            "Threat",
            round(threat_score, 2)
        )

        st.progress(toxicity_score)

        # -------------------------------
        # ALERT PANEL
        # -------------------------------

        st.markdown(
            f"""
            <div style='padding:16px;
                        border-radius:8px;
                        background-color:{color}22;
                        border-left:5px solid {color};
                        margin-top:20px;'>

            <h3>{emoji} Alert Level: {level}</h3>

            <p>
            Toxicity Score:
            <b>{toxicity_score:.2f}</b>
            </p>

            <p>
            User:
            <b>{user_id}</b>
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        # -------------------------------
        # FULL OUTPUT
        # -------------------------------

        st.markdown("---")

        st.subheader("🧠 Full AI Output")

        st.write(result)

    else:

        st.warning(
            "Please fill in both User ID and Message."
        )

# -----------------------------------
# RECENT EVENTS
# -----------------------------------

st.markdown("---")

st.subheader("📋 Recent Moderation Events")

events = get_recent_events(20)

if events:

    for e in events:

        level = e.get("alert_level", "Low")

        emoji = get_alert_emoji(level)

        color = get_alert_color(level)

        st.markdown(
            f"""
            <div style='margin-bottom:8px;
                        padding:10px;
                        border-radius:6px;
                        background-color:{color}18;
                        border-left:4px solid {color};'>

            {emoji}
            <b>{level}</b>

            | Score:
            <b>{e['toxicity_score']:.2f}</b>

            | User:
            <code>{e['user_id']}</code>

            | <i>{str(e['timestamp'])[:19]}</i>

            <br><br>

            <span style='color:#cccccc;'>
            {e['message'][:100]}
            </span>

            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.info(
        "No moderation events yet."
    )

# -----------------------------------
# FOOTER
# -----------------------------------

st.markdown("---")

st.caption(
    "AI Harassment Detection System • Hackathon Prototype"
)