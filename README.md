## Uživatleský manuál

Do složky k programu je nutné přiložit soubor "adresy.geojson", který lze stáhnout např. [zde](http://overpass-turbo.eu/) pro jakoukoli část Prahy. Tento soubor musí být v souřadnicovém systému WGS84 a souřadnice musí být v atributu `"coordinates"` v sekci `"geometry"`. Soubor musí obsahovat v atributu `"properties"` mít atributy `"addr:street"` a `"addr:housenumber"`.


Druhým souborem, který je potřeba přiložit, je "kontejnery.geojson", který lze stáhnout na [stránkách Geoportálu Prahy](https://www.geoportalpraha.cz/cs/data/otevrena-data/8726EF0E-0834-463B-9E5F-FE09E62D73FB). Souřadnice musí být v JTSK systému v atributu `"geometry"` -> `"coordinates"`. Zároveň musí existovat atribut `"PRISTUP"`, který říká, jestli je kontejner veřejně přístupný nebo je jen pro obyvatele domu.

Program po spuštení do obélníku dole vypíše:
- kolik celkem adres a kontejnerů kontroloval
- jaká je průměrná nejnižší vzdálenost k veřejnému koši na tříděný odpad pro danou část Prahy
- z jaké adresy je to k veřejnému koši na tříděný odpad nejdál a kolik je to metrů
- medián nejkratších vzdáleností k veřejným kontejnerům