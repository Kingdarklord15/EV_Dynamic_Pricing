import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("urbanev_merged.csv")

df["datetime"] = pd.to_datetime(df["datetime"])

df["hour"] = df["datetime"].dt.hour
df["weekday"] = df["datetime"].dt.dayofweek


plt.figure(figsize=(8,5))
df["volume"].hist(bins=50)

plt.title("Demand Volume Distribution")
plt.xlabel("Volume")
plt.ylabel("Frequency")

plt.show()

hourly = df.groupby("hour")["volume"].mean()

plt.figure(figsize=(10,5))
hourly.plot()

plt.title("Average Demand by Hour")
plt.xlabel("Hour")
plt.ylabel("Average Volume")

plt.show()
hourly_occ = df.groupby("hour")["occupancy"].mean()

plt.figure(figsize=(10,5))
hourly_occ.plot()

plt.title("Average Occupancy by Hour")
plt.xlabel("Hour")
plt.ylabel("Occupancy")

plt.show()

hourly_price = df.groupby("hour")["price"].mean()

plt.figure(figsize=(10,5))
hourly_price.plot()

plt.title("Average Price by Hour")
plt.xlabel("Hour")
plt.ylabel("Price")

plt.show()

weekday_demand = df.groupby("weekday")["volume"].mean()

plt.figure(figsize=(8,5))
weekday_demand.plot(kind="bar")

plt.title("Demand by Weekday")
plt.xlabel("Day")
plt.ylabel("Average Volume")

plt.show()

top_grids = (
    df.groupby("grid")["volume"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

print(top_grids)


sample = df.sample(10000)

plt.figure(figsize=(8,5))
plt.scatter(
    sample["price"],
    sample["volume"],
    alpha=0.3
)

plt.xlabel("Price")
plt.ylabel("Volume")
plt.title("Price vs Demand")

plt.show()