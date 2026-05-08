# modules/alerts.py

def classify_alert(toxicity_score: float) -> str:
    """
    Classify alert level based on toxicity score.
    < 0.4  -> Low
    0.4-0.7 -> Moderate
    > 0.7  -> High Risk
    """
    if toxicity_score < 0.4:
        return "Low"
    elif toxicity_score <= 0.7:
        return "Moderate"
    else:
        return "High Risk"

def get_alert_color(level: str) -> str:
    colors = {
        "Low": "green",
        "Moderate": "orange",
        "High Risk": "red"
    }
    return colors.get(level, "gray")

def get_alert_emoji(level: str) -> str:
    emojis = {
        "Low": "🟢",
        "Moderate": "🟡",
        "High Risk": "🔴"
    }
    return emojis.get(level, "⚪")