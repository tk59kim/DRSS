import fastf1
from fastf1.plotting import setup_mpl
from matplotlib import pyplot as plt

#enable data cache (download race data one and stores it)
fastf1.Cache.enable_cache('./cache')

#Load qualifying session from Monza 2023
session = fastf1.get_session(2021,'Monza', 'Q')
session.load()

#Pick fastest laps from VER and HAM
ver = session.laps.pick_driver('VER').pick_fastest()
ham = session.laps.pick_driver('HAM').pick_fastest()

#Get telemetry data
ver_tel = ver.get_car_data().add_distance()
ham_tel = ham.get_car_data().add_distance()

#Plot speed vs distance
plt.plot(ver_tel['Distance'], ver_tel['Speed'], label='VER')
plt.plot(ham_tel['Distance'], ham_tel['Speed'], label='HAM')

plt.title("Monza 2021 Qualifying - Fastest Laps")
plt.xlabel("Distance (m)")
plt.ylabel("Speed (km/h)")
plt.legend()
plt.show()