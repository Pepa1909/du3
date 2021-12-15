from json.decoder import JSONDecodeError
from pyproj import Transformer
import json
import math
import statistics

def vypocet_vzdalenosti(misto_jtsk, kontejner):

    """Spočítá vzdálenost adresy od kontejneru na tříděný odpad a tuto hodnotu vrátí."""

    vzdalenost_x = misto_jtsk[0]-(kontejner["geometry"]["coordinates"][0])
    vzdalenost_y = misto_jtsk[-1]-(kontejner["geometry"]["coordinates"][-1])
    vzdalenost = math.sqrt(vzdalenost_x**2+vzdalenost_y**2)
    return vzdalenost

def urceni_nejmensi_vzdalenosti(list_vzdalenosti,vzdalenost):
    
    """Přidá do seznamu novou vzdálenost a následně porovná s již existující vzdáleností.\n
    Vrátí nejnižší vzdálenost adresy ke kontejneru na tříděný odpad"""

    list_vzdalenosti.append(vzdalenost)
    if list_vzdalenosti[-1] < list_vzdalenosti[0]:
        list_vzdalenosti.remove(list_vzdalenosti[0])
    elif len(list_vzdalenosti) > 1:
        list_vzdalenosti.remove(list_vzdalenosti[-1])
    nejmensi_vzdalenost = list_vzdalenosti[0]
    return nejmensi_vzdalenost

def kos_nejdal(nejdal, min_vzdalenost, misto, minima_vzdalenosti):

    """Vytváří seznam, ve kterém je adresa, odkud je to ke koši nejdál a zároveň vzdálenost adresy.\n
    Vrací seznam, který zbyde - v něm je největší vzdálenost i se správnou adresou."""
    
    if nejdal==0:
        nejdal=[min_vzdalenost, misto["properties"]["addr:street"],misto["properties"]["addr:housenumber"]]
    elif nejdal[0] < minima_vzdalenosti[-1]:
        nejdal = [minima_vzdalenosti[-1],misto["properties"]["addr:street"],misto["properties"]["addr:housenumber"]]
    return nejdal

try:
    # Načtení souborů a vytvoření všech potřebných seznamů, slovníků, převodníku a proměnné.
    with open("adresy.geojson", encoding="utf-8") as json_adresy, open("kontejnery.geojson",encoding="utf-8") as json_kontejnery:
        data_adresy = json.load(json_adresy)
        data_kontejnery = json.load(json_kontejnery) 
        wgs2jtsk_prevodnik = Transformer.from_crs(4326,5514, always_xy=True)
        vzdalenosti = []
        minima = []
        max_vzdalenost_ke_kosi = 0

        # Projede celý seznam adres, každou přetransforuje do JTSK
        for adresa in data_adresy["features"]:
            jtsk_adresa = wgs2jtsk_prevodnik.transform(*adresa["geometry"]["coordinates"])

            # Pro každou adresu spočítá vzdálenost k nejbližšímu kontejneru na tříděný odpad, nejmenší uloží do seznamu 
            for kontejner in data_kontejnery["features"]:
                if kontejner["properties"]["PRISTUP"] == "volně":
                    vzdalenost_mista_od_kontejneru = vypocet_vzdalenosti(jtsk_adresa,kontejner)
                    nejmensi_vzdalenost = urceni_nejmensi_vzdalenosti(vzdalenosti, vzdalenost_mista_od_kontejneru)
                    if nejmensi_vzdalenost > 10000:
                        print("Nejbližší kontejner k jedné z adres se nachází dále než 10 km, v datech bude chyba.")
                        quit()
            minima.append(nejmensi_vzdalenost) # Seznam minima obsahuje vzdálenosti nejbližších košů

            # Určení adresy, ze které je to ke koši nejdál, příprava seznamu na další adresu
            max_vzdalenost_ke_kosi = kos_nejdal(max_vzdalenost_ke_kosi, nejmensi_vzdalenost, adresa, minima) 
            vzdalenosti=[]

        # Vytištění výstupu   
        print(f'''
Načteno {len(data_adresy["features"])} adresních bodů.
Načteno {len(data_kontejnery["features"])} kontejnerů na tříděný odpad.
        
Průměrná vzdálenost ke kontejneru je {statistics.mean(minima):.0f} m.
Nejdále je to z adresy {max_vzdalenost_ke_kosi[-2]} {max_vzdalenost_ke_kosi[-1]}, vzdálenost je {max(minima):.0f} m. 
Medián vzdáleností je {statistics.median(minima):.0f} m.
''')

# Výjimky, které program umí poznat
except FileNotFoundError as filenotfound:
    print(f"Soubor {filenotfound.filename} nebyl nalezen.")    
    quit()  
except PermissionError as permission:
    print(f"Program nemá oprávnění ke čtení souboru {permission.filename}.")
    quit()
except JSONDecodeError:
    print(f"Minimálně jeden ze souborů je prazdný.")
    quit()
