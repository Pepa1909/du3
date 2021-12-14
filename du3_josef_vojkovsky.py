from pyproj import Transformer
import json
import math
import statistics
with open("adresy.geojson", encoding="utf-8") as adresy, open("kontejnery.geojson",encoding="utf-8") as kontejnery:
    data_adresy = json.load(adresy)
    ulice = data_adresy["features"][0]["properties"]["addr:street"]
    cislo_domu = data_adresy["features"][0]["properties"]["addr:housenumber"]
    wgs2jtsk = Transformer.from_crs(4326,5514, always_xy=True)
    data_kontejnery = json.load(kontejnery) 
    vzdalenosti = []
    minima = []
    for adresa in data_adresy["features"]:
        jtsk_adresa = wgs2jtsk.transform(*adresa["geometry"]["coordinates"])
        for kontejner in data_kontejnery["features"]:
            vzdalenost_x = jtsk_adresa[0]-(kontejner["geometry"]["coordinates"][0])
            vzdalenost_y = jtsk_adresa[-1]-(kontejner["geometry"]["coordinates"][-1])
            vzdalenost = math.sqrt(vzdalenost_x**2+vzdalenost_y**2)
            vzdalenosti.append(vzdalenost)
            if vzdalenosti[-1] < vzdalenosti[0]:
                vzdalenosti.remove(vzdalenosti[0])
            elif len(vzdalenosti) > 1:
                vzdalenosti.remove(vzdalenosti[-1])
        minima.append(vzdalenosti[0])
        vzdalenosti=[]
    print(f'''načteno {len(data_kontejnery["features"])} kontejnerů a {len(data_adresy["features"])} adres.
    
    průměrná vzdálenost je {statistics.mean(minima)} a nejmenší vzdálenost je {min(minima)} na adrese {ulice} {cislo_domu}''')
            
