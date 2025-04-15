import requests
import pandas as pd
import folium
from datetime import datetime
import sys

def download():
    resp = requests.get("http://www.datiopen.it/export/csv/Mappa-dei-telefoni-pubblici-in-Italia.csv")
    if resp.ok:
        data = resp.text
        f = open("input.csv", "w")
        f.write(data)
        f.close()

def createPlot(regione, dfprovincia):
    plot = dfprovincia.plot(kind="pie", y="Provincia")
    fig = plot.get_figure()
    fig.savefig("itphones_outputs/" + regione + ".png")
    fig.clear()

def ageToColor(year, m, M):
    colors = ["darkgreen", "green", "orange", "red"]
    curryear = datetime.now().year
    deltatot = M - m
    delta = M - year
    age = round(min((delta / deltatot) * 3, 3))
    return colors[age]

def isInBounds(loc, bounds):
    lat = loc[0]
    lon = loc[1]
    ul = bounds[0]
    lr = bounds[1]
    return lat < ul[0] and lat > lr[0] and lon > ul[1] and lon < lr[1]

print("Downloading data")
download()

print("Reloading data into pandas")
df = pd.read_csv("input.csv", sep=";")
regioni = df["Regione"].unique()

print("Creating plots")
for reg in regioni:
    dfregione = df[df["Regione"] == reg]
    dfprovincia = dfregione.groupby("Provincia")["Provincia"].count()
    createPlot(reg, dfprovincia)

print("Checking for bounds")
if len(sys.argv) == 5:
    bounds = [ sys.argv[1:3], sys.argv[3:5] ]
    bounds = [[ float(x) for x in bounds[0]], [ float(x) for x in bounds[1]] ]
    print("Bounds are: ", bounds)
else:
    # Whole Italy
    bounds = [[46.62115209225544, 5.669698244577547], [36.04096044837196, 21.97861416589663]]

# Create the map with Folium API
themap = folium.Map(zoom_start=10)
themap.fit_bounds(bounds)

# Create list of locations
locations = list(zip(df["Latitudine"], df["Longitudine"]))

#Compute min and max distribution of insertion years
m = df["Anno inserimento"].min()
M = df["Anno inserimento"].max()

# loop over locations to filter on bounds and colorize
print("Rendering map")
for i in range(len(locations)):
    loc = locations[i]
    if isInBounds(loc, bounds):
        color = ageToColor(df["Anno inserimento"][i], m, M)
        icon = folium.Icon(color=color, fill_color=color)
        marker = folium.Marker([loc[0], loc[1]], icon=icon)
        marker.add_to(themap)

# save the map
themap.save("itphones_outputs/index.html")