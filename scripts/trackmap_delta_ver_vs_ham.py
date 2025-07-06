import fastf1
import matplotlib.pyplot as plt

# Enable FastF1 cache
fastf1.Cache.enable_cache('cache')  

# Load session data
session = fastf1.get_session(2023, 'Monza', 'Q')
session.load()

print(session.laps[session.laps['Driver'] == 'SAI'][['Driver', 'LapTime', 'Deleted']])


# Get fastest laps
ver_lap = session.laps[(session.laps['Driver'] == 'VER') & (session.laps['Deleted'] == False)].pick_fastest()
sai_lap = session.laps.pick_driver('SAI').sort_values('LapTime').iloc[0]

# Get telemetry with position and time
ver_tel = ver_lap.get_telemetry().add_distance()
sai_tel = sai_lap.get_telemetry().add_distance()

# Interpolate sai to match VER by distance
sai_tel_interp = sai_tel.set_index('Distance').reindex(ver_tel['Distance'], method='nearest').reset_index()

# Time delta (positive = VER ahead)
time_delta = (sai_tel_interp['Time'] - ver_tel['Time']).dt.total_seconds()

# Define sector boundaries based on distance (you may need to adjust these values)
s1_start, s1_end = 0, 1500
s2_start, s2_end = 1500, 4000
s3_start, s3_end = 4000, len(time_delta)

# Print sector-by-sector delta sums
print("Sector 1 delta:", time_delta[s1_start:s1_end].sum())
print("Sector 2 delta:", time_delta[s2_start:s2_end].sum())
print("Sector 3 delta:", time_delta[s3_start:s3_end].sum())
print("Total delta:", time_delta.sum())


# Plot
fig, ax = plt.subplots(figsize=(10, 8))

for i in range(len(ver_tel) - 1):
    x = [ver_tel.iloc[i]['X'], ver_tel.iloc[i + 1]['X']]
    y = [ver_tel.iloc[i]['Y'], ver_tel.iloc[i + 1]['Y']]
    delta = time_delta[i]

    if delta > 0.05:
        color = 'blue'   # VER faster
    elif delta < -0.05:
        color = 'red'    # sai faster
    else:
        color = 'gray'   # Tie/similar

    ax.plot(x, y, color=color, linewidth=2.5)

# Add sector labels
sector_distances = [ver_tel['Distance'].iloc[-1] * x for x in [0.25, 0.55, 0.85]]
sector_labels = ['Sector 1', 'Sector 2', 'Sector 3']
for d, label in zip(sector_distances, sector_labels):
    sector_point = ver_tel.iloc[(ver_tel['Distance'] - d).abs().argmin()]
    ax.text(sector_point['X'], sector_point['Y'], label, fontsize=9, ha='center', va='center', bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))

# Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='blue', lw=2.5, label='Verstappen faster'),
    Line2D([0], [0], color='red', lw=2.5, label='Sainz faster'),
    Line2D([0], [0], color='gray', lw=2.5, label='Similar pace')
]
ax.legend(handles=legend_elements, loc='lower left', fontsize=8)

# Formatting
ax.set_title("Track Map Dominance: Verstappen vs Sainz (Time-Based)")
ax.set_aspect('equal')
ax.axis('off')
plt.tight_layout()
plt.show()
