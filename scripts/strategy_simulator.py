import matplotlib.pyplot as plt
import numpy as np

# Base lap time + degradation model (same as before)
def generate_stint_laptimes(tire_type, stint_laps, track_temp):
    base_lap_time = {
        "soft": 90,
        "medium": 92,
        "hard": 94
    }

    degradation_factor = {
        "soft": 0.25,
        "medium": 0.18,
        "hard": 0.12
    }

    temp_sensitivity = {
        "soft": 0.04,
        "medium": 0.03,
        "hard": 0.02
    }

    base = base_lap_time[tire_type]
    degrade = degradation_factor[tire_type]
    temp_penalty = temp_sensitivity[tire_type] * (track_temp - 25)

    lap_times = []
    for lap in range(1, stint_laps + 1):
        lap_time = base + degrade * (lap ** 1.2) + temp_penalty
        lap_times.append(lap_time)
    return lap_times

# Pit stop loss (constant)
PIT_LOSS = 23.5

# Strategy simulator
def simulate_strategy(strategy, track_temp):
    total_time = 0
    stint_results = []

    for tire, laps in strategy:
        laptimes = generate_stint_laptimes(tire, laps, track_temp)
        stint_results.append((tire, laps, laptimes))
        total_time += sum(laptimes)
        total_time += PIT_LOSS
    total_time -= PIT_LOSS
    return total_time, stint_results

# Strategies
strategies = {
    "1-stop (Soft → Hard)": [("soft", 15), ("hard", 30)],
    "2-stop (Soft → Medium → Soft)": [("soft", 12), ("medium", 16), ("soft", 17)],
    "1-stop (Medium → Hard)": [("medium", 20), ("hard", 25)],
}

colors = {
    "1-stop (Soft → Hard)": "red",
    "2-stop (Soft → Medium → Soft)": "yellow",
    "1-stop (Medium → Hard)": "gray"
}

results = {}
track_temp = 32

for name, strat in strategies.items():
    total_time, stints = simulate_strategy(strat, track_temp)
    results[name] = {"total_time": total_time, "stints": stints}

# Normalize lap times to deltas from best
min_time = min([res["total_time"] for res in results.values()])

plt.figure(figsize=(10, 6))

for name, data in results.items():
    lap_counter = 1
    lap_times_all = []
    for tire, laps, laptimes in data["stints"]:
        lap_times_all.extend(laptimes)
        lap_counter += laps
    base_offset = results[name]["total_time"] - min_time
    delta_laps = [round(t - lap_times_all[0], 2) for t in lap_times_all]
    plt.plot(range(1, len(delta_laps) + 1), delta_laps, label=f"{name} (+{round(base_offset, 1)}s)", color=colors[name])

plt.title(f"DRSS Strategy Delta Plot @ {track_temp}°C")
plt.xlabel("Lap")
plt.ylabel("Lap Time Delta (s)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
