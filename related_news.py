"""Preliminary cross-border article discovery; does NOT fact-check articles."""
import re,time,threading,json,urllib.parse,urllib.request,urllib.error,math
from news_data import COUNTRIES, normalize_article
from gdelt_client import fetch_articles, GDELTError

STOP=set("the and with from after before about into over under that this said says are was were have has for its but not a an to of in on at by as is will who new live what when where why how latest update news report reports sweden sverige enligt efter från och eller med till för att som det den ett en har hade var ska kan om vid över under nya nyhet nyheter om säger sade uppger uppgift uppgifter".split())
CACHE={};LOCK=threading.Lock()

def terms(headline):
    words=re.findall(r"[^\W_]{3,}", headline.lower(),flags=re.UNICODE)
    unique=[]
    for w in words:
        if w not in STOP and w not in unique and not w.isnumeric():unique.append(w)
    return unique[:5]

def overlap(left,right):
    aa=set(terms(left));bb=set(terms(right))
    return len(aa&bb)/len(aa|bb) if aa and bb else 0

def country_code(value):
    if not value:return None
    v=re.sub('[^a-z]','',value.lower())
    for code,c in COUNTRIES.items():
        if v in (code.lower(), c['gdelt_country'].lower(),re.sub('[^a-z]','',c['english_name'].lower()),re.sub('[^a-z]','',c['name'].lower())):return code
    known={'unitedstatesofamerica':'US','russia':'RU','uk':'GB','southkorea':'KR','northkorea':'KP','czechrepublic':'CZ','turkey':'TR','vietnam':'VN'}
    return known.get(v)

def discover(headline,origin_country=None):
    if not isinstance(headline,str) or not 5<=len(headline)<=300:raise ValueError('Ogiltig rubrik.')
    seed=terms(headline)
    if len(seed)<2: return {'status':'insufficient_terms','matches':[],'reason':'Rubriken saknar tillräckligt specifika sökord. Ingen internationell koppling visas.'}
    # GDELT searches translated full text, but returned headlines remain in source language.
    # We require lexical supporting evidence in the headline before drawing a line.
    # Thus non-Latin and translated paraphrases will often be missed in this first beta.
    query=' '.join(seed[:3]);key=(headline,origin_country)
    now=time.time()
    with LOCK:
        if key in CACHE and now-CACHE[key][0]<600:return dict(CACHE[key][1],cached=True)
    try:
        articles=fetch_articles(query, timespan="72h", maxrecords=100)
    except GDELTError as exc:
        raise RuntimeError("Internationell sökning: GDELT-fel ("+exc.code+"): "+str(exc)) from exc
    matches=[];seen_country=set();seen_domain=set()
    for raw in articles:
        norm=normalize_article(raw,1)
        if not norm:continue
        code=country_code(norm['source_country'])
        if not code or code==origin_country or code in seen_country or norm['source'] in seen_domain:continue
        score=overlap(headline,norm['headline'])
        # Candidate link, never a truth score. Require at least two exact substantial shared terms.
        shared=set(terms(headline))&set(terms(norm['headline']))
        if score<0.27 or len(shared)<2:continue
        seen_country.add(code);seen_domain.add(norm['source'])
        norm['country_code']=code
        norm['country_name']=COUNTRIES[code]['name']
        norm['shared_terms']=sorted(shared)[:5]
        norm['match_type']='Preliminär rubrikmatchning – ej AI-verifierad'
        norm['match_score']=round(score,3)
        matches.append(norm)
        if len(matches)==12:break
    result={'status':'preliminary','query':query,'headline':headline,'matches':matches,'checked_articles':len(articles),
       'note':'Kopplingar baseras på sökord och rubriköverlapp. De är inte verifierade händelsesamband. Avsaknad av linjer bevisar inte att internationell rapportering saknas.',
       'limitations':'Fulltext, språköversättning, originalkällor och AI-baserad påståendejämförelse ingår ännu inte.','cached':False}
    with LOCK:CACHE[key]=(time.time(),result)
    return result
