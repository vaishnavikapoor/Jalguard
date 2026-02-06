import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)


N_DAYS = 60
VILLAGES = ["V1", "V2", "V3"]

START_DATE = datetime(2025, 1, 1)

SOURCES = ["pond", "river", "handpump"]


def generate_rainfall():
    # most days low rain, sometimes heavy
    if np.random.rand() < 0.15:
        return np.random.uniform(20, 60)  # heavy rain
    else:
        return np.random.uniform(0, 8)

def generate_ph(prev_ph):
    drift = np.random.normal(0, 0.05)
    ph = prev_ph + drift
    return float(np.clip(ph, 6.0, 8.8))

def generate_orp():
    return float(np.clip(np.random.normal(350, 40), 200, 500))

def generate_report_text(d, v, f, source):
    templates = [
        "Today {d} people have loose motions and {v} are vomiting after using {s} water.",
        "{d} persons reported diarrhea and {v} vomiting today. Water source was {s}.",
        "Field worker noticed {d} diarrhea cases and {f} fever cases in the village. Source: {s}.",
        "There are {d} loose motion cases, {v} vomiting cases and {f} fever cases today after drinking {s} water."
    ]
    t = random.choice(templates)
    return t.format(d=d, v=v, f=f, s=source)


rows = []

for village in VILLAGES:

    prev_ph = np.random.uniform(6.5, 7.8)

    turbidity_history = [3, 3]  # for lag
    diarrhea_history = [0, 0]

    for day in range(N_DAYS):

        date = START_DATE + timedelta(days=day)

        rainfall = generate_rainfall()

        # turbidity depends on recent rainfall
        recent_rain = rainfall + 0.7 * turbidity_history[-1]
        turbidity = np.clip(
            2 + 0.12 * recent_rain + np.random.normal(0, 1),
            1, 30
        )

        ph = generate_ph(prev_ph)
        orp = generate_orp()


        past_turbidity = turbidity_history[-2]

        base_risk = max(0, (past_turbidity - 5) / 10)

        diarrhea = np.random.poisson(1 + 6 * base_risk)
        vomiting = np.random.poisson(0.5 + 3 * base_risk)
        fever = np.random.poisson(0.5 + 2 * base_risk)

        source = random.choice(SOURCES)

        report_text = generate_report_text(
            diarrhea, vomiting, fever, source
        )

        rows.append({
            "village_id": village,
            "date": date.date(),
            "ph": round(ph, 2),
            "turbidity": round(float(turbidity), 2),
            "orp": round(orp, 1),
            "rainfall": round(rainfall, 1),
            "true_diarrhea": int(diarrhea),
            "true_vomiting": int(vomiting),
            "true_fever": int(fever),
            "report_text": report_text
        })

        turbidity_history.append(turbidity)
        diarrhea_history.append(diarrhea)
        prev_ph = ph

df = pd.DataFrame(rows)
df.to_csv("data/synthetic_village_water_data.csv", index=False)

print(df.head())
