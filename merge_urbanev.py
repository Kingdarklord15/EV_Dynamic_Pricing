import pandas as pd

# ----------------------------------
# Load files
# ----------------------------------

time_df = pd.read_csv("urbanev/time.csv")

volume_df = pd.read_csv("urbanev/volume.csv")
occupancy_df = pd.read_csv("urbanev/occupancy.csv")
duration_df = pd.read_csv("urbanev/duration.csv")
price_df = pd.read_csv("urbanev/price.csv")

# ----------------------------------
# Create datetime column
# ----------------------------------

time_df["datetime"] = pd.to_datetime(
    time_df[
        ["year", "month", "day",
         "hour", "minute", "second"]
    ]
)

# ----------------------------------
# Remove duplicate timestamp columns
# ----------------------------------

for df in [
    volume_df,
    occupancy_df,
    duration_df,
    price_df
]:
    if "timestamp" in df.columns:
        df.drop(
            columns=["timestamp"],
            inplace=True
        )

# ----------------------------------
# Wide -> Long
# ----------------------------------

volume_long = volume_df.stack().reset_index()
volume_long.columns = [
    "time_idx",
    "grid",
    "volume"
]

occupancy_long = occupancy_df.stack().reset_index()
occupancy_long.columns = [
    "time_idx",
    "grid",
    "occupancy"
]

duration_long = duration_df.stack().reset_index()
duration_long.columns = [
    "time_idx",
    "grid",
    "duration"
]

price_long = price_df.stack().reset_index()
price_long.columns = [
    "time_idx",
    "grid",
    "price"
]

# ----------------------------------
# Merge
# ----------------------------------

merged = volume_long.merge(
    occupancy_long,
    on=["time_idx", "grid"],
    how="inner"
)

merged = merged.merge(
    duration_long,
    on=["time_idx", "grid"],
    how="inner"
)

merged = merged.merge(
    price_long,
    on=["time_idx", "grid"],
    how="inner"
)

# ----------------------------------
# Add datetime
# ----------------------------------

merged["datetime"] = time_df.loc[
    merged["time_idx"],
    "datetime"
].values

# ----------------------------------
# Reorder columns
# ----------------------------------

merged = merged[
    [
        "datetime",
        "grid",
        "volume",
        "occupancy",
        "duration",
        "price"
    ]
]

# ----------------------------------
# Validation
# ----------------------------------

print("Shape:", merged.shape)

print("\nMissing Values:")
print(merged.isnull().sum())

print("\nDuplicate Rows:")
print(merged.duplicated().sum())

print("\nSummary:")
print(merged.describe())

# ----------------------------------
# Save
# ----------------------------------

merged.to_csv(
    "urbanev_merged.csv",
    index=False
)

print("\nSaved urbanev_merged.csv")