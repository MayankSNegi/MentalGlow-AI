import pandas as pd
import numpy as np
from pathlib import Path

SRC = Path("app/data/universal_raw.csv")
DST = Path("app/data/cleaned_dataset.csv")

df = pd.read_csv(SRC)

# 🧹 Remove accidental unnamed/empty columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
print("✅ Loaded:", SRC, "rows:", len(df))

# Keep/ensure needed columns exist
needed = [
    "age","gender","city","relationship_status",
    "sleep_hours","exercise_frequency","screen_time_hours","diet_quality",
    "stress_level","anxiety_level","mood","motivation_level","concentration_level",
    "social_support","social_interaction_frequency","work_stress","is_student","is_employed",
    "household_responsibility","open_to_therapy","aware_of_mental_health",
    "mental_health_risk"
]
for c in needed:
    if c not in df.columns:
        df[c] = np.nan

# Clip numeric ranges
clip_ranges = {
    "age": (10, 100),
    "sleep_hours": (0, 12),
    "exercise_frequency": (0, 7),
    "screen_time_hours": (0, 16),
    "diet_quality": (1, 5),
    "stress_level": (1, 5),
    "anxiety_level": (1, 5),
    "motivation_level": (1, 5),
    "concentration_level": (1, 5),
    "social_support": (1, 5),
    "social_interaction_frequency": (0, 7),
    "work_stress": (1, 5),
    "household_responsibility": (1, 5),
}
for col, (lo, hi) in clip_ranges.items():
    df[col] = pd.to_numeric(df[col], errors="coerce").clip(lo, hi)
    df[col] = df[col].fillna(df[col].median())

# Binary coercions
for b in ["is_student","is_employed","open_to_therapy","aware_of_mental_health"]:
    df[b] = pd.to_numeric(df[b], errors="coerce").fillna(0).clip(0,1).astype(int)

# Normalize categoricals
df["gender"] = df["gender"].astype(str).str.strip().str.lower().replace(
    {"m":"male","f":"female","man":"male","woman":"female","femake":"female"}
)
df["mood"] = df["mood"].astype(str).str.lower().replace(
    {"positive":"high","happy":"high","negative":"low","sad":"low"}
)
df["relationship_status"] = df["relationship_status"].astype(str).str.strip().str.lower()
df["city"] = df["city"].astype(str).str.strip().str.lower()

# Target fallback if absent
if "mental_health_risk" not in df.columns or df["mental_health_risk"].isna().all():
    df["mental_health_risk"] = ((df["stress_level"] >= 4) | (df["anxiety_level"] >= 4)).astype(int)

# One-hot encode categoricals
cat_cols = ["gender","relationship_status","mood","city"]
df = pd.get_dummies(df, columns=cat_cols, drop_first=False)

DST.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(DST, index=False)
print("✅ Saved cleaned dataset →", DST, "rows:", len(df))
