import time

FILE = "D:\\projects\\1brc\\measurements_100MM.txt"
MIN = 0
MAX = 1
SUM = 2
COUNT = 3

if __name__ == "__main__":
    start_time = time.monotonic()
    stats_by_station = {}

    with open(FILE, 'r') as file:
        for line in file:
            station, temperature_as_string = line.strip().split(';')
            temperature = float(temperature_as_string)

            if station in stats_by_station:
                current_stats = stats_by_station[station]
                stats_by_station[station] = (
                    min(current_stats[MIN], temperature),
                    max(current_stats[MAX], temperature),
                    current_stats[SUM] + temperature,
                    current_stats[COUNT] + 1
                )
            else:
                stats_by_station[station] = (temperature, temperature, temperature, 1)

    end_time = time.monotonic()
    print(f"Done: {end_time - start_time:.2f}s")

    for station, stats in sorted(stats_by_station.items()):
        print(f"{station}={stats[MIN]:0.1f}/{stats[SUM]/stats[COUNT]:0.1f}/{stats[MAX]:0.1f}")


# def print_stats(stats):
#     formatted = ", ".join(
#         [
#             f"{k}={v['min']}/{v['sum']/v['count']:.1f}/{v['max']}"
#             for k, v in sorted(stats.items(), key=lambda x: x[0])
#         ]
#     )
#     print("{" + formatted + "}")