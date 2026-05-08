class SeverityScorer:

    def __init__(self):

        self.toxicity_weight = 0.6
        self.frequency_weight = 0.3
        self.network_weight = 0.1

    def calculate_severity(
        self,
        toxicity_score,
        frequency_score=0,
        network_pressure=0
    ):

        severity_score = (
            (toxicity_score * self.toxicity_weight)
            + (frequency_score * self.frequency_weight)
            + (network_pressure * self.network_weight)
        )

        severity_score = max(0, min(severity_score, 1))

        severity_label = self.get_severity_label(
            severity_score
        )

        return {
            "severity_score": round(severity_score, 3),
            "severity_label": severity_label
        }

    def get_severity_label(self, score):

        if score >= 0.85:
            return "CRITICAL"

        elif score >= 0.65:
            return "HIGH"

        elif score >= 0.4:
            return "MEDIUM"

        elif score >= 0.2:
            return "LOW"

        return "SAFE"


if __name__ == "__main__":

    scorer = SeverityScorer()

    result = scorer.calculate_severity(
        toxicity_score=0.92,
        frequency_score=0.6,
        network_pressure=0.4
    )

    print(result)