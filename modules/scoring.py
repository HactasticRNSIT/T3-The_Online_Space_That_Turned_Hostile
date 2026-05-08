def calculate_severity(toxicity, frequency=1, network_pressure=1):

    severity = (
        0.6 * toxicity +
        0.3 * frequency +
        0.1 * network_pressure
    )

    return round(min(severity, 1.0), 2)