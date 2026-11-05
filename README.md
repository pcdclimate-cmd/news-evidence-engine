# News from Facts – världskarta (MVP 2.0)

**Ny version av det befintliga GitHub/Render-projektet.** Startsidan (`/`) är nu en interaktiv världskarta. Den tidigare matematiska faktagranskaren finns kvar på `/granska` och API:et `/api/analyze` fungerar som tidigare.

## Vad fungerar?
- Interaktiv världskarta med länder, zoom, dragning och sökfält.
- Klick på valfritt land. 20 valda länder har vardera två **fiktiva demonstrationsrubriker**; övriga länder visar tydligt att ingen data finns.
- `/api/countries` listar de 20 exempeländerna.
- `/api/news?country=SE` returnerar två demonstrationsposter och tydliga metadata om att de inte är verkliga nyheter.
- `/api/health` lämnar ett enklare driftsvar.
- Den befintliga faktagranskaren och testerna är bevarade.

**OBS: Inga aktuella nyheter, automatiska redaktionella rankningar, riktiga skribenter, AI-verifiering eller källkopplingar finns ännu i paketet.** Det är avsiktligt för att undvika att fabricera rubriker. Kartans globala landsgränser laddas i webbläsaren från world-atlas via jsDelivr, och Leaflet/topojson laddas via CDN. Extern internetanslutning krävs för kartan.

## Uppdatera samma hemsida på Render
1. Packa upp ZIP-filen lokalt. Öppna GitHub-repository `news-evidence-engine`.
2. Välj **Add file → Upload files**. Dra in innehållet i mappen, **inte zip-filen**. GitHub frågar om du vill ersätta befintliga filer. Vid problem kan du ändra direkt via filernas Edit-knapp eller använda GitHub Desktop.
3. Kontrollera att `index.html`, `granska.html`, `news_data.py`, `server.py`, `engine.py`, `test_engine.py`, `render.yaml`, `README.md` ligger i repositoryts rot (alternativt i samma Root Directory som redan är inställd på Render).
4. Välj **Commit changes**. Om Render har **Auto-Deploy On Commit** publiceras ändringarna automatiskt.
5. Kontrollera hemsidans startsida `/`, faktagranskaren `/granska`, samt `/api/health` och `/api/news?country=SE`.

**Viktigt:** Kommandona på Render ska vara oförändrade: Build `python -m unittest -v`, Start `python server.py`. Ändra inga API-nycklar eller andra hemligheter i repositoryt.

## Köra lokalt
Python 3.10+: `python -m unittest -v` och `python server.py`, öppna därefter `http://127.0.0.1:8765/`.

## Kartteknik och källor
Leaflet 1.9.4 (BSD-2-Clause): https://leafletjs.com/  
world-atlas / Natural Earth (public domain kartdata): https://github.com/topojson/world-atlas  
topojson-client 3: https://github.com/topojson/topojson-client

Landsgränser är en approximativ kartrepresentation; omtvistade gränser kan skilja sig från olika jurisdiktioners officiella kartor.

## Föreslagen nästa version
En separat servermodul som hämtar licensierade nyhetsflöden; deduplicering och uppdelning på händelser; per-land rankning med transparenta kriterier; spårning av artikel, författare, originalpublicering och citeringsrelation; källbaserad påståendekontroll och osäkerhet. Automatiska granskningsresultat får inte presenteras som verifierade utan validering och tydlig möjlighet till rättelse.
