from pyproj import Transformer
import json
with open("adresy.geojson", encoding="utf-8") as file:
    data = json.load(file)
    souradnice_x = data["features"][0]["geometry"]["coordinates"][0]
    souradnice_y = data["features"][0]["geometry"]["coordinates"][-1]
    ulice = data["features"][0]["properties"]["addr:street"]
    cislo_domu = data["features"][0]["properties"]["addr:housenumber"]
    wgs2jtsk = Transformer.from_crs(4326,5514, always_xy=True)
    out = wgs2jtsk.transform(souradnice_x, souradnice_y)
    print(ulice, cislo_domu, out)  
