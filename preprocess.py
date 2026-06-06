import pandas as pd

df = pd.read_csv("acn_partial.csv")

df.drop_duplicates(inplace=True)

timestamp_cols = [
    "connectionTime",
    "disconnectTime",
    "doneChargingTime"
]

for col in timestamp_cols:
    df[col] = pd.to_datetime(
        df[col],
        errors="coerce"
    )

df = df.dropna(
    subset=timestamp_cols
)

# ----------------------------------
# Duration Features
# ----------------------------------

df["session_duration_hr"] = (
    df["disconnectTime"]
    - df["connectionTime"]
).dt.total_seconds() / 3600

df["charging_duration_hr"] = (
    df["doneChargingTime"]
    - df["connectionTime"]
).dt.total_seconds() / 3600

df["idle_duration_hr"] = (
    df["disconnectTime"]
    - df["doneChargingTime"]
).dt.total_seconds() / 3600

# ----------------------------------
# Remove impossible durations
# ----------------------------------

df = df[df["session_duration_hr"] >= 0]
df = df[df["charging_duration_hr"] >= 0]
df = df[df["idle_duration_hr"] >= 0]

# ----------------------------------
# Time Features
# ----------------------------------

df["hour"] = df["connectionTime"].dt.hour
df["weekday"] = df["connectionTime"].dt.day_name()
df["month"] = df["connectionTime"].dt.month
df["date"] = df["connectionTime"].dt.normalize()

# ----------------------------------
# Summary
# ----------------------------------

print("Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

# ----------------------------------
# Save
# ----------------------------------

df.to_csv(
    "acn_clean.csv",
    index=False
)

print("\nSaved acn_clean.csv")