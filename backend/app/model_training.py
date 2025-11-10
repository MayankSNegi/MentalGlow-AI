import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import resample

# ==== Paths ====
DATA = Path("app/data/cleaned_dataset.csv")
MODEL_OUT = Path("app/models/mental_health_model.pkl")

# ==== Load Dataset ====
df = pd.read_csv(DATA)
print(f"✅ Loaded dataset: {DATA} | Rows: {len(df)}")

# Ensure target is numeric
df["mental_health_risk"] = pd.to_numeric(df["mental_health_risk"], errors="coerce").fillna(0).astype(int)

# ==== Check balance ====
print("\nBefore balancing:")
print(df["mental_health_risk"].value_counts())

# Explicitly separate classes
df_0 = df[df["mental_health_risk"] == 0]
df_1 = df[df["mental_health_risk"] == 1]

# Upsample minority
if len(df_0) != len(df_1):
    max_class_size = max(len(df_0), len(df_1))
    df_0_upsampled = resample(df_0, replace=True, n_samples=max_class_size, random_state=42)
    df_1_upsampled = resample(df_1, replace=True, n_samples=max_class_size, random_state=42)
    df_balanced = pd.concat([df_0_upsampled, df_1_upsampled])
else:
    df_balanced = pd.concat([df_0, df_1])

df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)

print("\nAfter balancing:")
print(df_balanced["mental_health_risk"].value_counts())

# ==== Split ====
X = df_balanced.drop(columns=["mental_health_risk"])
y = df_balanced["mental_health_risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# ==== Train ====
print("\n🧠 Training RandomForestClassifier...")
model = RandomForestClassifier(
    n_estimators=400,
    max_depth=12,
    class_weight="balanced_subsample",
    random_state=42
)
model.fit(X_train, y_train)

# ==== Evaluate ====
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

print("\n✅ Training complete")
print(classification_report(y_test, y_pred))
print("ROC-AUC:", roc_auc_score(y_test, y_proba))

# ==== Save ====
MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_OUT)
print(f"✅ Saved new balanced model → {MODEL_OUT}")

# ==== Feature importances (optional insight) ====
importances = pd.Series(model.feature_importances_, index=X.columns)
print("\n🔍 Top 10 important features:")
print(importances.sort_values(ascending=False).head(10))
