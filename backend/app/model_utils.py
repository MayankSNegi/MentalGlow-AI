import joblib
import pandas as pd
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "models" / "mental_health_model.pkl"
model = joblib.load(MODEL_PATH)

def preprocess(payload: dict) -> pd.DataFrame:
    row = {
        # Basic Demographics
        "age": payload["age"],
        "sleep_hours": payload["sleep_hours"],
        "exercise_frequency": payload["exercise_frequency"],
        "screen_time_hours": payload["screen_time_hours"],
        "diet_quality": payload["diet_quality"],

        # Emotional & Mental Health
        "stress_level": payload["stress_level"],
        "anxiety_level": payload["anxiety_level"],
        "motivation_level": payload["motivation_level"],
        "concentration_level": payload["concentration_level"],

        # Social & Work/Study
        "social_support": payload["social_support"],
        "social_interaction_frequency": payload["social_interaction_frequency"],
        "work_stress": payload["work_stress"],
        "is_student": payload["is_student"],
        "is_employed": payload["is_employed"],

        # Household
        "household_responsibility": payload["household_responsibility"],

        # Awareness
        "open_to_therapy": payload["open_to_therapy"],
        "aware_of_mental_health": payload["aware_of_mental_health"],
    }

    # One-hot encode categorical
    row[f"gender_{payload['gender']}"] = 1
    row[f"mood_{payload['mood']}"] = 1
    row[f"relationship_status_{payload['relationship_status']}"] = 1
    row[f"city_{payload['city'].strip().lower()}"] = 1  # switched to city

    df = pd.DataFrame([row])

    # Align to model features (add missing = 0)
    for col in model.feature_names_in_:
        if col not in df.columns:
            df[col] = 0

    return df[model.feature_names_in_]
