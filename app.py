import streamlit as st
import plotly.express as px
import pandas as pd

from modules.toxicity import analyze_text
from modules.scoring import calculate_severity

# -----------------------------------
# TEMPORARY PLACEHOLDERS
# Device 2 will replace these later
# -----------------------------------

def capture_screen():
    return "data/sample.png"


def extract_text(path):
    return "You are pathetic and useless"


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Harassment Detection System",
    layout="wide"
)

# -----------------------------------
# HEADER
# -----------------------------------

st.title("AI Harassment Detection System")

st.markdown(
    """
    ### Real-Time AI Moderation Dashboard

    This system monitors digital conversations,
    detects hostile interactions,
    analyzes toxicity levels,
    and alerts moderators in real time.
    """
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("Moderator Dashboard")

st.sidebar.success("Monitoring System Active")

st.sidebar.metric(
    "Monitoring Status",
    "LIVE"
)

st.sidebar.metric(
    "Messages Scanned",
    128
)

st.sidebar.metric(
    "High Risk Alerts",
    5
)

st.sidebar.info(
    "Real-time toxicity monitoring system"
)

# -----------------------------------
# MAIN DASHBOARD METRICS
# -----------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Messages Processed",
    128
)

col2.metric(
    "Critical Alerts",
    5
)

col3.metric(
    "Threat Level",
    "HIGH"
)

st.divider()

# -----------------------------------
# MONITORING BUTTON
# -----------------------------------

if st.button("Start Monitoring"):

    # Capture screen
    image_path = capture_screen()

    # Extract text
    extracted_text = extract_text(image_path)

    # -----------------------------------
    # DETECTED TEXT
    # -----------------------------------

    st.subheader("Detected Text")

    st.write(extracted_text)

    st.divider()

    # -----------------------------------
    # TOXICITY ANALYSIS
    # -----------------------------------

    result = analyze_text(extracted_text)

    toxicity_score = result['toxicity']

    severity = calculate_severity(toxicity_score)

    st.subheader("Toxicity Analysis")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Toxicity",
        round(result['toxicity'], 2)
    )

    col2.metric(
        "Insult",
        round(result['insult'], 2)
    )

    col3.metric(
        "Threat",
        round(result['threat'], 2)
    )

    # -----------------------------------
    # PROGRESS BAR
    # -----------------------------------

    st.progress(float(toxicity_score))

    # -----------------------------------
    # SEVERITY SCORE
    # -----------------------------------

    st.metric(
        "Severity Score",
        severity
    )

    # -----------------------------------
    # THREAT STATUS
    # -----------------------------------

    if severity > 0.7:

        st.error(
            "🔴 HIGH RISK TOXIC CONTENT DETECTED"
        )

    elif severity > 0.4:

        st.warning(
            "🟠 MODERATE TOXICITY DETECTED"
        )

    else:

        st.success(
            "🟢 LOW RISK CONTENT"
        )

    st.divider()

    # -----------------------------------
    # ANALYTICS CHART
    # -----------------------------------

    st.subheader("Live Moderation Analytics")

    df = pd.DataFrame({
        "Category": [
            "Toxicity",
            "Insult",
            "Threat"
        ],
        "Score": [
            result['toxicity'],
            result['insult'],
            result['threat']
        ]
    })

    fig = px.bar(
        df,
        x="Category",
        y="Score",
        title="Toxicity Breakdown"
    )

    st.plotly_chart(fig)

    st.divider()

    # -----------------------------------
    # ALERT FEED
    # -----------------------------------

    st.subheader("Recent Moderation Alerts")

    st.write("⚠ Toxic language detected")
    st.write("⚠ Harassment pattern identified")
    st.write("⚠ Negative sentiment escalation")

    st.divider()

    # -----------------------------------
    # RAW OUTPUT
    # -----------------------------------

    st.subheader("Full Analysis Output")

    st.write(result)

# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(
    "AI Harassment Detection System • Hackathon Prototype"
)