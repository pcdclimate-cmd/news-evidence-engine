# News from Facts v4.0 – Automatic cross-border discovery (beta)

## What users see

Click a country, then click **Visa kopplingar på kartan** on a news card. No URL entry required. The server queries GDELT for potentially related articles, filters candidates conservatively on common words in the *headlines*, and draws dotted connections to their publisher countries. Clicking another country or article resets the connections.

## Important limitations

- This first beta is **NOT an AI fact checker**, nor does it calculate article truthfulness.
- It compares headlines, not article bodies; cross-language links will often be missed and matches may be false positives.
- Geographic lines show **publisher country**, not location of the reported event or origin of the claim.
- No matches does not mean no coverage. GDELT coverage is incomplete and rate limited.
- Next steps: structured event clustering, multilingual full-text comparisons, provenance tracing, claim-by-claim contradiction assessment and calibrated evidence scoring, with editorial review.
- GDELT API response time is variable; do not promise instant completion. Loading starts immediately on click.

## Deployment

Upload files into the existing GitHub repository and deploy the latest commit in Render. Start command: `python server.py`. Health check: `/api/health` gives `4.0-links-beta`.

## Validation

`python -m unittest discover -v`
