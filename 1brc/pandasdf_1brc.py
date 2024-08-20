import pandas as pd
import time

MEASUREMENT_FILE = "D:\\projects\\1brc\\measurements_10.txt"

if __name__ == "__main__":
    start_time = time.monotonic()

    df = pd.read_csv(
        MEASUREMENT_FILE,
        sep=";",
        header=None,
        names=["Station", "Temperature"],
        engine='pyarrow'
    )

    load_time = time.monotonic()

    print(f"Loaded: {load_time - start_time:.2f}s")

    df = df.groupby("Station").agg(["min", "mean", "max"])
    print(df)
    df.columns = df.columns.droplevel()

    df = df.sort_values("Station")

    end_time = time.monotonic()
    print(f"Done: {end_time - start_time:.2f}s")

    for index, row in df.iterrows():
        print(f"{index}={row['min']:0.1f}/{row['mean']:0.1f}/{row['max']:0.1f}")
