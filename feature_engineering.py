import pandas as pd
import numpy as np

df = pd.read_csv("urbanev_merged.csv")

info = pd.read_csv("urbanev/information.csv")

info = info[
    [
        "grid",
        "count",
        "fast_count",
        "slow_count",
        "CBD"
    ]
]

df = df.merge(
    info,
    on="grid",
    how="left"
)

df["datetime"] = pd.to_datetime(df["datetime"])

df["hour"] = df["datetime"].dt.hour
df["weekday"] = df["datetime"].dt.dayofweek
df["month"] = df["datetime"].dt.month

df["utilization"] = (
    df["occupancy"] /
    df["count"].replace(0, np.nan)
)

df.replace(
    [np.inf, -np.inf],
    np.nan,
    inplace=True
)

print("Shape:", df.shape)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

df.to_csv(
    "urbanev_features.csv",
    index=False
)

print("\nSaved urbanev_features.csv")