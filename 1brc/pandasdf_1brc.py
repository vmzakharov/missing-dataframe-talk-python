import pandas as pd

FILE = "measurements_10.txt"

if __name__ == "__main__":
    df = pd.read_csv(
        FILE,
        sep=";",
        header=None,
        names=["Station", "Temperature"],
        engine='pyarrow'
    )

    df = df.groupby("Station").agg(["min", "mean", "max"])

    df.columns = df.columns.droplevel()

    df = df.sort_values("Station")

    for index, row in df.iterrows():
        print(f"{index}={row['min']:0.1f}/{row['mean']:0.1f}/{row['max']:0.1f}")
