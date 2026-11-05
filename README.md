# News from Facts v4.1 – stabilare GDELT-hantering

Denna uppdatering ändrar inte kartan eller artikelmatchningens metod. Den korrigerar hur nyhetsleverantörens fel hanteras.

- Gemensam begränsning av anrop från landsnyheter och internationell sökning.
- Ett försiktigt återförsök vid överbelastning (HTTP 429/5xx) och nätverksfel.
- JSON-kontroll och tydligare felkoder i API-svar.
- Tidigare hämtade landsnyheter visas om tillgängliga vid ett tillfälligt leverantörsfel.
- Inga nyheter hittas på om GDELT inte svarar.

## Installera

Packa upp ZIP-filen. Kopiera samtliga projektfiler till din lokala `news-evidence-engine`-mapp via Windows Utforskaren. Välj *Ersätt filerna på målet*. Använd GitHub Desktop för **Commit to main → Push origin**. Render publicerar därefter ändringen.

## Kontroll

- `/api/health` ska visa `4.1-gdelt-stability`.
- `/api/news?country=SE` ska visa två verkliga artiklar, en tom lista, eller ett mer specifikt fel (`rate_limited`, `network_error`, `invalid_response` eller HTTP-fel).
- Kör `python -m unittest discover -v` lokalt.

Observera att programmet inte kan garantera tillgänglighet hos GDELT. GDELT DOC 2.0 är en extern gratistjänst; fler nyhetskällor och schemalagd cache behöver byggas för stabil produktion.
