import pandas as pd

# Load cleaned ACN data
df = pd.read_csv("acn_clean.csv")

# --------------------------------------------------
# Remove unnecessary columns
# --------------------------------------------------

drop_cols = [
    "_id",
    "sessionID",
    "timezone",
    "userInputs",
    "userID"
]

existing_cols = [col for col in drop_cols if col in df.columns]

df.drop(columns=existing_cols, inplace=True)

# --------------------------------------------------
# Remove invalid records
# --------------------------------------------------

df = df[df["charging_duration_hr"] >= 0]
df = df[df["idle_duration_hr"] >= 0]

# Keep only realistic session lengths
df = df[df["session_duration_hr"] <= 24]

# --------------------------------------------------
# Feature Engineering
# --------------------------------------------------

# Charging intensity
df["energy_per_hour"] = (
    df["kWhDelivered"]
    / (df["charging_duration_hr"] + 0.01)
)

# Idle behavior
df["idle_ratio"] = (
    df["idle_duration_hr"]
    / (df["session_duration_hr"] + 0.01)
)

# Weekend indicator
df["weekend"] = (
    df["weekday"].isin(
        ["Saturday", "Sunday"]
    )
).astype(int)

# Peak-hour indicator
# NOTE:
# Replace with EDA-derived hours later if needed
df["peak_hour"] = (
    df["hour"].between(14, 18)
).astype(int)

# --------------------------------------------------
# Final sanity checks
# --------------------------------------------------

print("\nDataset Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())

# --------------------------------------------------
# Save
# --------------------------------------------------

df.to_csv(
    "acn_features.csv",
    index=False
)

print("\nSaved: acn_features.csv")