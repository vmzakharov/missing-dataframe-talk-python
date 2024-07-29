import pandas as pd
import time

if __name__ == "__main__":
    start_time = time.time()

    df = pd.read_csv(
        "D:\\projects\\1brc\\" + "measurements_10.txt",
        sep=";",
        header=None,
        names=["station", "measure"],
        engine='pyarrow'
    )

    df = df.groupby("station").agg(["min", "max", "mean"])

    df.columns = df.columns.droplevel()

    df = df.sort_values("station")

    end_time = time.time()

    print(f"Done: {end_time - start_time:.2f}s")

    for index, row in df.iterrows():
        print(f"{index}={row['min']:0.1f}/{row['mean']:0.1f}/{row['max']:0.1f}")
