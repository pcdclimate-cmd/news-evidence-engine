"""Live GDELT DOC search. Article listings are discovery, not fact-checking."""
import json, time, threading, urllib.parse, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone

COUNTRIES={c["code"]:c for c in json.loads((Path(__file__).parent / "countries.json").read_text(encoding="utf-8"))}
CACHE={}
CACHE_TTL=1800
LOCK=threading.Lock()
LAST_REQUEST=[0.0]
API="https://api.gdeltproject.org/api/v2/doc/doc"

def normalize_article(item, rank):
    link=item.get("url", "")
    parts=urllib.parse.urlsplit(link)
    if parts.scheme not in ("http","https") or not parts.hostname:return None
    title=(item.get("title") or "").strip()
    if not title:return None
    domain=item.get("domain") or parts.hostname
    return {"rank":rank,"headline":title[:300],"url":link,"source":domain,
            "language":item.get("language"),"source_country":item.get("sourcecountry"),
            "seen_at":item.get("seendate"),"author":None,"status":"Inte faktagranskad"}

def get_news(code):
    code=code.upper()
    if code not in COUNTRIES:raise ValueError("Okänd landskod")
    now=time.time()
    with LOCK:
        cached=CACHE.get(code)
        if cached and now-cached[0]<CACHE_TTL:return dict(cached[1],cached=True)
        # Gentle global pacing, avoid bursts toward GDELT. Do not hold the lock during network calls.
        delay=max(0,6-(now-LAST_REQUEST[0]))
        LAST_REQUEST[0]=now+delay
    if delay:time.sleep(delay)
    country=COUNTRIES[code]
    params={"query":"sourcecountry:"+country["gdelt_country"],"mode":"ArtList",
            "format":"json","timespan":"24h","maxrecords":"50","sort":"DateDesc"}
    req=urllib.request.Request(API+"?"+urllib.parse.urlencode(params),headers={"User-Agent":"NewsFromFacts/3.0 (research prototype)","Accept":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=15) as response:
            raw=response.read(2_000_000)
            payload=json.loads(raw)
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,ValueError) as exc:
        with LOCK:
            stale=CACHE.get(code)
        if stale:return dict(stale[1],cached=True,stale=True,warning="GDELT svarar inte just nu; visar tidigare hämtade artiklar.")
        raise RuntimeError("Nyhetsleverantören GDELT svarade inte. Försök igen senare.") from exc
    articles=payload.get("articles",[])
    seen=set();stories=[];domains=set()
    for a in articles:
        normalized=normalize_article(a,len(stories)+1)
        if not normalized:continue
        key=(normalized["url"].split('?')[0]).lower()
        if key in seen or normalized["source"] in domains:continue
        seen.add(key);domains.add(normalized["source"]);stories.append(normalized)
        if len(stories)>=2:break
    result={"country_code":code,"country":country["name"],"mode":"live",
      "source":"GDELT DOC 2.0","retrieved_at":datetime.now(timezone.utc).isoformat(),
      "methodology":"De två senaste tillgängliga artiklarna från olika publicistdomäner i GDELT:s senaste 24 timmar. Inte en rankning av de viktigaste nyheterna och inte faktagranskade.",
      "stories":stories,"cached":False}
    with LOCK:CACHE[code]=(time.time(),result)
    return result
