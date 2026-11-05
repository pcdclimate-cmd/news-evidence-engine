"""Shared, rate-conscious GDELT DOC 2.0 client.

No keys. Does not manufacture articles when the provider is unavailable.
"""
import json
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.gdeltproject.org/api/v2/doc/doc"
_LOCK = threading.Lock()
_NEXT_SLOT = 0.0
_INTERVAL_SECONDS = 6.0

class GDELTError(RuntimeError):
    def __init__(self, detail, code="upstream_error"):
        super().__init__(detail)
        self.code = code


def _pace():
    global _NEXT_SLOT
    with _LOCK:
        now = time.monotonic()
        slot = max(now, _NEXT_SLOT)
        _NEXT_SLOT = slot + _INTERVAL_SECONDS
    delay = slot - now
    if delay > 0:
        time.sleep(delay)


def fetch_articles(query, *, timespan="24h", maxrecords=50, sort="DateDesc"):
    params = {
        "query": query, "mode": "ArtList", "format": "json", "timespan": timespan,
        "maxrecords": str(maxrecords), "sort": sort,
    }
    url = API + "?" + urllib.parse.urlencode(params)
    last = None
    for attempt in range(2):
        _pace()
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; NewsFromFacts/4.1; research)",
                     "Accept": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                body = response.read(3_000_000)
                content_type = response.headers.get("Content-Type", "")
            if "json" not in content_type.lower() and not body.lstrip().startswith(b"{"):
                raise GDELTError("GDELT returnerade ett svar som inte var JSON.", "invalid_response")
            payload = json.loads(body)
            if not isinstance(payload, dict) or not isinstance(payload.get("articles", []), list):
                raise GDELTError("GDELT returnerade oväntad datastruktur.", "invalid_response")
            return payload["articles"] if "articles" in payload else []
        except urllib.error.HTTPError as exc:
            code = "rate_limited" if exc.code == 429 else "upstream_http"
            last = GDELTError(f"GDELT HTTP {exc.code}.", code)
            if attempt == 0 and (exc.code == 429 or exc.code in (500, 502, 503, 504)):
                try:
                    retry_after = min(20, max(6, int(exc.headers.get("Retry-After", "6"))))
                except (ValueError, TypeError):
                    retry_after = 6
                time.sleep(retry_after)
                continue
            break
        except (urllib.error.URLError, TimeoutError) as exc:
            last = GDELTError(f"GDELT nätverksfel eller tidsgräns: {type(exc).__name__}.", "network_error")
            if attempt == 0:
                continue
            break
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            last = GDELTError("GDELT returnerade ogiltig JSON.", "invalid_response")
            break
        except GDELTError as exc:
            last = exc
            break
    raise last or GDELTError("Okänt GDELT-fel.")
