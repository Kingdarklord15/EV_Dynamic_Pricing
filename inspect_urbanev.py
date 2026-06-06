import pandas as pd

files = [
    "urbanev/volume.csv",
    "urbanev/occupancy.csv",
    "urbanev/duration.csv",
    "urbanev/price.csv",
    "urbanev/time.csv",
    "urbanev/stations.csv",
    "urbanev/information.csv"
]

for file in files:

    print("\n" + "=" * 60)
    print(file)

    df = pd.read_csv(file)

    print("Shape:", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicates:")
    print(df.duplicated().sum())

    print("\nHead:")
    print(df.head())