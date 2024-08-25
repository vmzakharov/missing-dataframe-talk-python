import pandas as pd
import time

FILE = "measurements_10.txt"

def print_time(message, begin_time, end_time):
    delta_ms = int((end_time - begin_time) * 1000)
    print(f"{message}: {delta_ms} ms")


if __name__ == "__main__":
    start_time = time.monotonic()

    df = pd.read_csv(
        FILE,
        sep=";",
        header=None,
        names=["Station", "Temperature"],
        engine='pyarrow'
    )

    load_time = time.monotonic()

    print_time("Loaded", start_time, load_time)

    df = df.groupby("Station").agg(["min", "mean", "max"])

    df.columns = df.columns.droplevel()

    df = df.sort_values("Station")

    end_time = time.monotonic()

    print_time("Aggregated", load_time, end_time)

    for index, row in df.iterrows():
        print(f"{index}={row['min']:0.1f}/{row['mean']:0.1f}/{row['max']:0.1f}")
