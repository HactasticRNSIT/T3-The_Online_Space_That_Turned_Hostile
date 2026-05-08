from detoxify import Detoxify
import re


class ToxicityEngine:

    def __init__(self):

        self.model = Detoxify("original")

    def clean_text(self, text):

        text = text.lower()

        text = re.sub(r"http\S+", "", text)

        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

        text = re.sub(r"\s+", " ", text).strip()

        return text

    def analyze_text(self, text):

        if not text:
            return {
                "success": False,
                "error": "Empty text"
            }

        cleaned_text = self.clean_text(text)

        results = self.model.predict(cleaned_text)

        toxicity_score = float(results["toxicity"])

        insult_score = float(results["insult"])

        threat_score = float(results["threat"])

        severe_toxicity = float(results["severe_toxicity"])

        identity_attack = float(results["identity_attack"])

        overall_score = max(
            toxicity_score,
            insult_score,
            threat_score,
            severe_toxicity,
            identity_attack
        )

        return {
            "success": True,
            "original_text": text,
            "cleaned_text": cleaned_text,
            "toxicity_score": round(overall_score, 3),
            "categories": {
                key: round(float(value), 3)
                for key, value in results.items()
            }
        }


# -----------------------------------
# GLOBAL ENGINE INSTANCE
# -----------------------------------

engine = ToxicityEngine()


# -----------------------------------
# COMPATIBILITY FUNCTION FOR app.py
# -----------------------------------

def analyze_text(text):

    result = engine.analyze_text(text)

    if not result["success"]:

        return {
            "toxicity": 0,
            "insult": 0,
            "threat": 0
        }

    categories = result["categories"]

    return {
        "toxicity": categories.get("toxicity", 0),
        "insult": categories.get("insult", 0),
        "threat": categories.get("threat", 0)
    }


# -----------------------------------
# TESTING
# -----------------------------------

if __name__ == "__main__":

    sample = "You are useless and disgusting"

    result = analyze_text(sample)

    print(result)