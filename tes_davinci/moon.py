import ephem
import datetime
import numpy as np

def moon_elevation(lat, lon, time):
    obs = ephem.Observer()
    obs.lat = np.radians(lat)
    obs.lon = np.radians(lon)
    obs.date = time
    moon = ephem.Moon()
    moon.compute(obs)
    return np.degrees(moon.alt)

lat = np.random.uniform(-90, 90, size=1)
lon = np.random.uniform(-180, 180, size=1)
time = datetime.datetime.now()

print(moon_elevation(lat, lon, time))