"""Transparent, deliberately uncalibrated evidence scoring engine."""
import math
from urllib.parse import urlparse

STRENGTH_LR = {1: 1.2, 2: 1.5, 3: 2.0, 4: 3.0, 5: 5.0}
SOURCE_FACTOR = {"primary": 1.0, "secondary": 0.75, "unknown": 0.5}


def analyze(payload):
    if not isinstance(payload, dict):
        raise ValueError("Indata måste vara ett objekt.")
    claim = str(payload.get("claim", "")).strip()
    if len(claim) < 5 or len(claim) > 2000:
        raise ValueError("Påståendet måste vara 5–2000 tecken.")
    evidence = payload.get("evidence", [])
    if not isinstance(evidence, list) or len(evidence) > 100:
        raise ValueError("Max 100 belägg per analys.")
    groups = {}
    parsed = []
    for i, ev in enumerate(evidence):
        if not isinstance(ev, dict):
            raise ValueError(f"Belägg {i + 1} är felaktigt.")
        description = str(ev.get("description", "")).strip()
        group = str(ev.get("group", "")).strip().lower()
        direction = ev.get("direction")
        source_type = ev.get("source_type", "unknown")
        strength = ev.get("strength")
        url = str(ev.get("url", "")).strip()
        if not description or len(description) > 1000 or not group or len(group) > 150:
            raise ValueError(f"Belägg {i + 1} saknar beskrivning eller källgrupp.")
        if direction not in ("support", "refute") or source_type not in SOURCE_FACTOR or type(strength) is not int or strength not in STRENGTH_LR:
            raise ValueError(f"Belägg {i + 1} har ogiltig klassificering.")
        if url and (urlparse(url).scheme not in ("https", "http") or not urlparse(url).netloc):
            raise ValueError(f"Belägg {i + 1} har en ogiltig käll-URL.")
        log_weight = math.log(STRENGTH_LR[strength]) * SOURCE_FACTOR[source_type]
        if direction == "refute":
            log_weight = -log_weight
        item = {"description": description, "group": group, "direction": direction,
                "source_type": source_type, "strength": strength, "url": url,
                "log_weight": round(log_weight, 4), "counted": False}
        parsed.append(item)
        groups.setdefault(group, []).append(i)
    # Within each origin group, pick the strongest absolute piece of evidence;
    # the other items are displayed but not treated as independent confirmations.
    selected = []
    for group, indices in groups.items():
        chosen = max(indices, key=lambda j: abs(parsed[j]["log_weight"]))
        parsed[chosen]["counted"] = True
        selected.append(chosen)
    log_odds = sum(parsed[j]["log_weight"] for j in selected)
    index = 100 / (1 + math.exp(-max(-30, min(30, log_odds))))
    if not selected:
        verdict = "Otillräckligt underlag"
    elif any(parsed[j]["direction"] == "support" for j in selected) and any(parsed[j]["direction"] == "refute" for j in selected) and abs(log_odds) < 0.7:
        verdict = "Motstridiga belägg"
    elif log_odds >= 1.1:
        verdict = "Starkare stöd"
    elif log_odds <= -1.1:
        verdict = "Starkare motbevis"
    else:
        verdict = "Otillräckligt underlag"
    return {"claim": claim, "verdict": verdict,
            "evidence_index": round(index, 1) if selected else None,
            "log_evidence": round(log_odds, 4), "source_groups": len(groups),
            "evidence_count": len(parsed), "counted_count": len(selected),
            "evidence": parsed,
            "disclaimer": "Evidensindex är en okalibrerad modellpoäng, inte sannolikheten att påståendet är sant. Källor och styrkor är manuellt klassificerade."}
