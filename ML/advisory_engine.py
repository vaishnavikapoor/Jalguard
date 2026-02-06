def generate_advisory(row):
    if row["status"] == "NO_DATA":
        return [
            "Insufficient data received from sensors and field reports.",
            "Please restore data connectivity or submit a field report."
        ]

    advisories = []

    r_turb = row["r_turb"]
    r_rain = row["r_rain"]
    r_health = row["r_health"]
    status = row["status"]

    if r_turb >= 0.5:
        advisories.append(
            "High water turbidity risk detected. Inspect filtration units and intake points."
        )

    if r_rain >= 0.5:
        advisories.append(
            "Recent rainfall may increase contamination risk. Increase monitoring frequency."
        )

    if r_health >= 0.6:
        advisories.append(
            "Public health indicators suggest elevated risk. Use only boiled or treated water for drinking."
        )

    if len(advisories) == 0:
        advisories.append(
            "Water sources appear safe. Continue routine monitoring and standard operations."
        )

    return " ".join(advisories)
