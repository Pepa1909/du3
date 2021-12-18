from pyproj import Transformer
import json
import math
import statistics

def vypocet_vzdalenosti(misto_jtsk, kontejner):

    """Spočítá vzdálenost adresy od kontejneru na tříděný odpad a tuto hodnotu vrátí."""

    vzdalenost_x = misto_jtsk[0]-(kontejner["geometry"]["coordinates"][0])
    vzdalenost_y = misto_jtsk[-1]-(kontejner["geometry"]["coordinates"][-1])
    vzdalenost = math.sqrt(vzdalenost_x**2 + vzdalenost_y**2)
    return vzdalenost

def urceni_nejmensi_vzdalenosti(vzdalenost, min_dist):
    
    """Kontroluje nejnižší vzdálenost, kterou pak vrátí."""

    if min_dist == None:
        min_dist = vzdalenost
    if vzdalenost < min_dist:
        min_dist = vzdalenost
    return min_dist

def kos_nejdal(nejdal, min_vzdalenost, misto, minima_vzdalenosti):

    """Vytváří seznam, ve kterém je adresa, odkud je to ke koši nejdál a zároveň vzdálenost adresy.\n
    Vrací seznam, který zbyde - v něm je největší vzdálenost i se správnou adresou."""
    
    if nejdal == None:
        nejdal = [min_vzdalenost, misto["properties"]["addr:street"], misto["properties"]["addr:housenumber"]]
    elif nejdal[0] < minima_vzdalenosti[-1]:
        nejdal = [minima_vzdalenosti[-1], misto["properties"]["addr:street"], misto["properties"]["addr:housenumber"]]
    return nejdal

try:
    # Načtení souborů a vytvoření potřebných seznamů
    with open("adresy.geojson", encoding = "utf-8") as json_adresy, open("kontejnery.geojson", encoding = "utf-8") as json_kontejnery:
        data_adresy = json.load(json_adresy)
        data_kontejnery = json.load(json_kontejnery) 

# Výjimky, které program umí poznat
except FileNotFoundError as filenotfound:
    print(f"Soubor {filenotfound.filename} nebyl nalezen.")    
    quit()  
except PermissionError as permission:
    print(f"Program nemá oprávnění ke čtení souboru {permission.filename}.")
    quit()
except json.decoder.JSONDecodeError:
    print(f"Minimálně jeden ze souborů není platný .json soubor.")
    quit()

# Vytvoření převodníku, seznamu na nejbližší koše a konstanty na nejvzdálenější koš
wgs2jtsk_prevodnik = Transformer.from_crs(4326,5514, always_xy = True)
minima = []
adresa_a_kos_nejdal = None
MAX_DISTANCE = 10000

# Projede celý seznam adres, každou přetransformuje do JTSK
for adresa in data_adresy["features"]:
    jtsk_adresa = wgs2jtsk_prevodnik.transform(*adresa["geometry"]["coordinates"])

    # Toto platí pro první kontejner počítaný z adresy
    nejmensi_vzdalenost = None
    
    # Pro každou adresu spočítá vzdálenost k nejbližšímu kontejneru na tříděný odpad, nejmenší uloží do seznamu 
    for kontejner in data_kontejnery["features"]:
        if kontejner["properties"]["PRISTUP"] == "volně":
            vzdalenost_mista_od_kontejneru = vypocet_vzdalenosti(jtsk_adresa, kontejner)
            nejmensi_vzdalenost = urceni_nejmensi_vzdalenosti(vzdalenost_mista_od_kontejneru, nejmensi_vzdalenost)   
            
    minima.append(nejmensi_vzdalenost) # Seznam minima obsahuje vzdálenosti nejbližších košů

    # Když je nové nejmenší číslo větší než MAX_DISTANCE (10 km), program se ukončí
    if minima[-1] > MAX_DISTANCE:
        print(f"Nejbližší kontejner k jedné z adres se nachází dále než {MAX_DISTANCE/1000:.2f} km, v datech bude chyba.")
        quit()

    # Určení adresy, ze které je to ke koši nejdál
    adresa_a_kos_nejdal = kos_nejdal(adresa_a_kos_nejdal, nejmensi_vzdalenost, adresa, minima) 

# Vytištění výstupu   
print(f'''
Načteno {len(data_adresy["features"])} adresních bodů.
Načteno {len(data_kontejnery["features"])} kontejnerů na tříděný odpad.

Průměrná vzdálenost ke kontejneru je {statistics.mean(minima):.0f} m.
Nejdále je to z adresy {adresa_a_kos_nejdal[-2]} {adresa_a_kos_nejdal[-1]}, vzdálenost je {max(minima):.0f} m. 
Medián vzdáleností je {statistics.median(minima):.0f} m.
''')