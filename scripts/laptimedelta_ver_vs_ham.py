import fastf1
from fastf1 import plotting
import matplotlib.pyplot as plt

fastf1.Cache.enable_cache('cache')  # Make sure 'cache/' exists

# Load the session
session = fastf1.get_session(2023, 'Monza', 'Q')
session.load()

# Pick fastest laps
ver_lap = session.laps.pick_driver('VER').pick_fastest()
ham_lap = session.laps.pick_driver('HAM').pick_fastest()

# Get telemetry
ver_tel = ver_lap.get_car_data().add_distance()
ham_tel = ham_lap.get_car_data().add_distance()

# Interpolate HAM telemetry to VER's distance points
ver_dist = ver_tel['Distance']
ham_interp = ham_tel.set_index('Distance').reindex(ver_dist, method='nearest').reset_index()

# Calculate delta
delta_time = ver_tel['Speed'] - ham_interp['Speed']

# Plot delta
plt.figure(figsize=(10, 5))
plt.plot(ver_dist, delta_time, label='VER - HAM (Speed Δ)', color='red')
plt.axhline(0, color='black', linestyle='--')
plt.xlabel('Distance (m)')
plt.ylabel('Speed Difference (km/h)')
plt.title('Speed Delta: Verstappen vs Hamilton - Monza Q 2023')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
