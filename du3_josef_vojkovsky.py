from pyproj import Transformer
import json
import math
with open("adresy.geojson", encoding="utf-8") as adresy, open("kontejnery.geojson",encoding="utf-8") as kontejnery:
    data_adresy = json.load(adresy)
    souradnice = data_adresy["features"][0]["geometry"]["coordinates"]
    ulice = data_adresy["features"][0]["properties"]["addr:street"]
    cislo_domu = data_adresy["features"][0]["properties"]["addr:housenumber"]
    wgs2jtsk = Transformer.from_crs(4326,5514, always_xy=True)
    out = wgs2jtsk.transform(*souradnice)
    data_kontejnery = json.load(kontejnery) 
    list_kont=[]
    for kontejner in data_kontejnery["features"]:
        list_kont.append(kontejner["geometry"]["coordinates"])
    list_adres=[]
    for adresa in data_adresy["features"]:
        jtsk_adresa = wgs2jtsk.transform(*adresa["geometry"]["coordinates"])
        list_adres.append(jtsk_adresa)
    print(list_adres[0][0],list_adres[0][-1])
    print(list_kont[0][0],list_kont[0][-1])
        # vzdalenost_x = list_adres[0][0]-(list_kont[0][0])
        # vzdalenost_y = list_adres[0][-1]-( list_kont[0][-1])
        # print(math.sqrt(vzdalenost_x**2+vzdalenost_y**2))
        # list_adres = []
