"""
SEO-Report Generator fuer oi.tax
Liest Google Search Console + GA4 und gibt einen formatierten Monatsreport aus.

Verwendung:
    python docs/seo_report.py --key /pfad/zu/fiorin-d83c6c57ee92.json [--site sc-domain:oi.tax]

Anforderungen:
    pip install requests rsa
"""

import argparse
import base64
import json
import re
import time
from datetime import date, timedelta
from urllib.parse import quote

import requests
import rsa

# --- Konfiguration ---
GA4_PROPERTY_ID = "273918863"
DEFAULT_GSC_SITE = "sc-domain:oi.tax"
LEGAL_CH_CTR_BENCHMARK = 2.5
# ---------------------

TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPES = (
    "https://www.googleapis.com/auth/analytics.readonly "
    "https://www.googleapis.com/auth/webmasters.readonly"
)


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _make_jwt(client_email: str, private_key_pem: str) -> str:
    now = int(time.time())
    header = _b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    payload = _b64url(json.dumps({
        "iss": client_email,
        "scope": SCOPES,
        "aud": TOKEN_URL,
        "iat": now,
        "exp": now + 3600,
    }).encode())
    signing_input = f"{header}.{payload}".encode()
    pem_body = re.sub(r"-----[^-]+-----|\s", "", private_key_pem)
    der = base64.b64decode(pem_body)
    idx = der.index(b"\x04\x82")
    inner_len = (der[idx + 2] << 8) | der[idx + 3]
    pkcs1_der = der[idx + 4: idx + 4 + inner_len]
    key = rsa.PrivateKey._load_pkcs1_der(pkcs1_der)
    sig = rsa.sign(signing_input, key, "SHA-256")
    return f"{header}.{payload}.{_b64url(sig)}"


def get_access_token(key_path: str) -> str:
    with open(key_path) as f:
        creds = json.load(f)
    jwt_token = _make_jwt(creds["client_email"], creds["private_key"])
    resp = requests.post(TOKEN_URL, data={
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt_token,
    }, timeout=15)
    resp.raise_for_status()
    return resp.json()["access_token"]


def _api_post(url: str, token: str, payload: dict, retries: int = 4) -> dict:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    for attempt in range(retries + 1):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            if resp.status_code in (429, 503) and attempt < retries:
                time.sleep(2 ** attempt)
                continue
            if not resp.ok:
                print(f"\nHTTP {resp.status_code} bei {url}")
                print(f"Details: {resp.text[:500]}")
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.ConnectionError:
            if attempt < retries:
                time.sleep(2 ** attempt)
            else:
                raise


def _api_get(url: str, token: str) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, timeout=30)
    if not resp.ok:
        print(f"\nHTTP {resp.status_code} bei {url}")
        print(f"Details: {resp.text[:500]}")
    resp.raise_for_status()
    return resp.json()


def list_gsc_sites(token: str) -> list:
    data = _api_get("https://searchconsole.googleapis.com/webmasters/v3/sites", token)
    return [s["siteUrl"] for s in data.get("siteEntry", [])]


def gsc_query(token: str, site_url: str, payload: dict) -> dict:
    encoded = quote(site_url, safe="")
    url = f"https://searchconsole.googleapis.com/webmasters/v3/sites/{encoded}/searchAnalytics/query"
    return _api_post(url, token, payload)


def ga4_report(token: str, payload: dict) -> dict:
    url = f"https://analyticsdata.googleapis.com/v1beta/properties/{GA4_PROPERTY_ID}:runReport"
    return _api_post(url, token, payload)


def _fmt_date(d: date) -> str:
    return d.strftime("%Y-%m-%d")


def _pct_change(new: float, old: float) -> str:
    if old == 0:
        return "n/a"
    delta = (new - old) / old * 100
    arrow = "▲" if delta >= 0 else "▼"
    return f"{arrow} {abs(delta):.1f}%"


def _pos_change(new: float, old: float) -> str:
    delta = old - new
    if delta > 0:
        return f"▲ +{delta:.1f}"
    elif delta < 0:
        return f"▼ {delta:.1f}"
    return "="


def fetch_gsc_overview(token: str, site: str, start: str, end: str) -> dict:
    """Gesamtkennzahlen ohne Dimension-Groupierung."""
    data = gsc_query(token, site, {"startDate": start, "endDate": end, "rowLimit": 1})
    rows = data.get("rows", [])
    if not rows:
        return {"clicks": 0, "impressions": 0, "ctr": 0.0, "position": 0.0}
    r = rows[0]
    return {
        "clicks": int(r.get("clicks", 0)),
        "impressions": int(r.get("impressions", 0)),
        "ctr": round(r.get("ctr", 0) * 100, 2),
        "position": round(r.get("position", 0), 1),
    }


def fetch_gsc_queries(token: str, site: str, start: str, end: str, limit: int = 25) -> list:
    """Keywords mit Clicks/Impressions/CTR/Position."""
    data = gsc_query(token, site, {
        "startDate": start, "endDate": end,
        "dimensions": ["query"],
        "rowLimit": limit,
        "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}],
    })
    result = []
    for r in data.get("rows", []):
        result.append({
            "query": r["keys"][0],
            "clicks": int(r.get("clicks", 0)),
            "impressions": int(r.get("impressions", 0)),
            "ctr": round(r.get("ctr", 0) * 100, 2),
            "position": round(r.get("position", 0), 1),
        })
    return result


def fetch_gsc_pages(token: str, site: str, start: str, end: str, limit: int = 25) -> list:
    """Seiten mit Clicks."""
    data = gsc_query(token, site, {
        "startDate": start, "endDate": end,
        "dimensions": ["page"],
        "rowLimit": limit,
        "orderBy": [{"fieldName": "clicks", "sortOrder": "DESCENDING"}],
    })
    result = []
    for r in data.get("rows", []):
        result.append({
            "page": r["keys"][0],
            "clicks": int(r.get("clicks", 0)),
        })
    return result


def fetch_ga4_organic(token: str, start_cur: str, end_cur: str, start_prev: str, end_prev: str) -> dict:
    """Organische Sessions + Key Events fuer 2 Zeitraeume."""
    payload = {
        "dimensions": [
            {"name": "sessionDefaultChannelGroup"},
            {"name": "landingPagePlusQueryString"},
        ],
        "metrics": [
            {"name": "sessions"},
            {"name": "keyEvents"},
            {"name": "bounceRate"},
        ],
        "dateRanges": [
            {"startDate": start_cur, "endDate": end_cur, "name": "current"},
            {"startDate": start_prev, "endDate": end_prev, "name": "previous"},
        ],
        "dimensionFilter": {
            "filter": {
                "fieldName": "sessionDefaultChannelGroup",
                "stringFilter": {"matchType": "EXACT", "value": "Organic Search"},
            }
        },
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
        "limit": 20,
    }
    data = ga4_report(token, payload)
    result = {
        "current": {"sessions": 0, "key_events": 0, "bounce_rate": 0.0, "pages": []},
        "previous": {"sessions": 0, "key_events": 0, "bounce_rate": 0.0, "pages": []},
    }
    for row in data.get("rows", []):
        dims = [d["value"] for d in row.get("dimensionValues", [])]
        mets = [m["value"] for m in row.get("metricValues", [])]
        period = dims[1] if len(dims) > 1 else ""
        page = dims[0] if dims else ""
        sessions = int(float(mets[0])) if mets else 0
        key_events = int(float(mets[1])) if len(mets) > 1 else 0
        bounce = float(mets[2]) if len(mets) > 2 else 0.0

        # GA4 mit 2 dateRanges gibt date_range_0 / date_range_1 als extra Dimension
        # Alternativ: "current" / "previous" via dateRange name
        range_dim = dims[-1] if dims else ""
        if range_dim in ("current", "date_range_0"):
            result["current"]["sessions"] += sessions
            result["current"]["key_events"] += key_events
            result["current"]["bounce_rate"] = bounce
            result["current"]["pages"].append({"page": page, "sessions": sessions, "key_events": key_events})
        elif range_dim in ("previous", "date_range_1"):
            result["previous"]["sessions"] += sessions
            result["previous"]["key_events"] += key_events

    for period in ("current", "previous"):
        s = result[period]["sessions"]
        ke = result[period]["key_events"]
        result[period]["conv_rate"] = round(ke / s * 100, 2) if s > 0 else 0.0

    return result


def build_report(gsc_cur, gsc_prev, queries_cur, queries_prev, pages_cur, pages_prev, ga4) -> str:
    lines = []
    add = lines.append

    add("=" * 65)
    add(f"SEO-REPORT  oi.tax  —  {date.today().strftime('%B %Y')}")
    add("=" * 65)

    # --- 1. Kennzahlen-Uebersicht ---
    add("\n### 1. KENNZAHLEN-UEBERSICHT\n")
    add(f"{'Kennzahl':<25} {'Aktuell':>10} {'Vormonat':>10} {'Veraenderung':>14}")
    add("-" * 62)

    def row(label, cur, prev, fmt="{}", higher_is_better=True, reverse=False):
        cur_s = fmt.format(cur)
        prev_s = fmt.format(prev) if prev is not None else "n/a"
        chg = _pct_change(cur, prev) if prev else "n/a"
        if reverse:
            chg = _pos_change(cur, prev) if prev else "n/a"
        return f"{label:<25} {cur_s:>10} {prev_s:>10} {chg:>14}"

    add(row("Klicks (GSC)", gsc_cur["clicks"], gsc_prev["clicks"], "{:,}"))
    add(row("Impressionen (GSC)", gsc_cur["impressions"], gsc_prev["impressions"], "{:,}"))
    add(row(f"Ø CTR (Benchmark ~{LEGAL_CH_CTR_BENCHMARK}%)", gsc_cur["ctr"], gsc_prev["ctr"], "{:.2f}%"))
    add(row("Ø Position", gsc_cur["position"], gsc_prev["position"], "{:.1f}", reverse=True))
    add(row("Organic Sessions (GA4)", ga4["current"]["sessions"], ga4["previous"]["sessions"], "{:,}"))
    add(row("Conversion Rate", ga4["current"]["conv_rate"], ga4["previous"]["conv_rate"], "{:.2f}%"))

    # --- 2. Top 10 Keywords ---
    add("\n### 2. TOP 10 KEYWORDS NACH CLICKS (aktueller Zeitraum)\n")
    add(f"{'Keyword':<40} {'Clicks':>7} {'Impr.':>7} {'CTR':>7} {'Pos.':>7}")
    add("-" * 70)
    for q in queries_cur[:10]:
        kw = q["query"][:38]
        add(f"{kw:<40} {q['clicks']:>7} {q['impressions']:>7} {q['ctr']:>6.1f}% {q['position']:>7.1f}")

    # --- 3. Positions-Gewinner & -Verlierer ---
    prev_map = {q["query"]: q for q in queries_prev}
    changes = []
    for q in queries_cur:
        if q["query"] in prev_map:
            p_prev = prev_map[q["query"]]["position"]
            delta = p_prev - q["position"]
            changes.append((q["query"], p_prev, q["position"], delta))

    winners = sorted([c for c in changes if c[3] > 0], key=lambda x: -x[3])[:5]
    losers = sorted([c for c in changes if c[3] < 0], key=lambda x: x[3])[:5]

    add("\n### 3. POSITIONEN — GROESSTE VERBESSERUNGEN\n")
    add(f"{'Keyword':<40} {'Vorher':>8} {'Jetzt':>8} {'Delta':>8}")
    add("-" * 66)
    for kw, prev_p, cur_p, delta in winners:
        add(f"{kw[:38]:<40} {prev_p:>8.1f} {cur_p:>8.1f} {'▲ +'+str(round(delta,1)):>8}")

    add("\n### 4. POSITIONEN — GROESSTE VERLUSTE\n")
    add(f"{'Keyword':<40} {'Vorher':>8} {'Jetzt':>8} {'Delta':>8}")
    add("-" * 66)
    for kw, prev_p, cur_p, delta in losers:
        add(f"{kw[:38]:<40} {prev_p:>8.1f} {cur_p:>8.1f} {'▼ '+str(round(delta,1)):>8}")

    # --- 4. Seiten mit groessten Click-Aenderungen ---
    prev_pages = {p["page"]: p["clicks"] for p in pages_prev}
    page_changes = []
    for p in pages_cur:
        prev_c = prev_pages.get(p["page"], 0)
        page_changes.append((p["page"], prev_c, p["clicks"], p["clicks"] - prev_c))
    page_changes.sort(key=lambda x: -abs(x[3]))

    add("\n### 5. SEITEN — GROESSTE CLICK-VERAENDERUNGEN\n")
    add(f"{'URL':<50} {'Vorher':>8} {'Jetzt':>8} {'Delta':>8}")
    add("-" * 76)
    for url, prev_c, cur_c, delta in page_changes[:8]:
        short = url.replace("https://oi.tax", "")[:48]
        arrow = "▲" if delta >= 0 else "▼"
        add(f"{short:<50} {prev_c:>8} {cur_c:>8} {arrow+str(abs(delta)):>8}")

    # --- 5. GA4 Top Landingpages Organic ---
    add("\n### 6. TOP ORGANIC LANDINGPAGES (GA4)\n")
    add(f"{'URL':<50} {'Sessions':>10} {'Conv.':>8}")
    add("-" * 70)
    for p in ga4["current"]["pages"][:8]:
        short = p["page"].replace("https://oi.tax", "")[:48]
        conv = round(p["key_events"] / p["sessions"] * 100, 1) if p["sessions"] > 0 else 0
        add(f"{short:<50} {p['sessions']:>10} {conv:>7.1f}%")

    # --- 6. Keyword-Radar (Pos. 11-20) ---
    radar = [q for q in queries_cur if 11 <= q["position"] <= 20]
    radar.sort(key=lambda x: x["clicks"], reverse=True)
    if radar:
        add("\n### 7. KEYWORD-RADAR (Position 11–20 — nahe Seite 1)\n")
        add(f"{'Keyword':<40} {'Pos.':>7} {'Clicks':>7} {'Impr.':>7}")
        add("-" * 63)
        for q in radar[:5]:
            add(f"{q['query'][:38]:<40} {q['position']:>7.1f} {q['clicks']:>7} {q['impressions']:>7}")

    # --- Bounce Rate ---
    br = ga4["current"].get("bounce_rate", 0)
    add(f"\nAbsprungrate Organic: {br*100:.1f}%")

    add("\n" + "=" * 65)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="SEO-Report fuer oi.tax")
    parser.add_argument("--key", required=True, help="Pfad zur Service-Account-JSON")
    parser.add_argument("--site", default=DEFAULT_GSC_SITE, help="GSC-Property (z.B. sc-domain:oi.tax)")
    parser.add_argument("--days", type=int, default=30, help="Zeitraum in Tagen (default: 30)")
    args = parser.parse_args()

    today = date.today()
    yesterday = today - timedelta(days=1)
    cur_end = _fmt_date(yesterday)
    cur_start = _fmt_date(yesterday - timedelta(days=args.days - 1))
    prev_end = _fmt_date(yesterday - timedelta(days=args.days))
    prev_start = _fmt_date(yesterday - timedelta(days=args.days * 2 - 1))

    print(f"Zeitraum aktuell:  {cur_start} bis {cur_end}")
    print(f"Zeitraum vorher:   {prev_start} bis {prev_end}")
    print("Hole Daten...", flush=True)

    token = get_access_token(args.key)

    print("  GSC verfuegbare Properties...", flush=True)
    sites = list_gsc_sites(token)
    if sites:
        print(f"  Gefunden: {sites}")
        if args.site not in sites:
            print(f"\nWARNUNG: '{args.site}' nicht in der Liste.")
            print("Verwende stattdessen: --site <eine der obigen URLs>")
            return
    else:
        print("  KEINE Properties gefunden — Service Account hat keinen GSC-Zugang.")
        print("  Bitte seo-analytics-reader@fiorin.iam.gserviceaccount.com in GSC als Nutzer eintragen.")
        return

    print("  GSC Uebersicht...", flush=True)
    gsc_cur = fetch_gsc_overview(token, args.site, cur_start, cur_end)
    gsc_prev = fetch_gsc_overview(token, args.site, prev_start, prev_end)

    print("  GSC Keywords...", flush=True)
    queries_cur = fetch_gsc_queries(token, args.site, cur_start, cur_end, limit=50)
    queries_prev = fetch_gsc_queries(token, args.site, prev_start, prev_end, limit=50)

    print("  GSC Seiten...", flush=True)
    pages_cur = fetch_gsc_pages(token, args.site, cur_start, cur_end, limit=25)
    pages_prev = fetch_gsc_pages(token, args.site, prev_start, prev_end, limit=25)

    print("  GA4 Organic Sessions...", flush=True)
    ga4 = fetch_ga4_organic(token, cur_start, cur_end, prev_start, prev_end)

    print("\n")
    print(build_report(gsc_cur, gsc_prev, queries_cur, queries_prev, pages_cur, pages_prev, ga4))


if __name__ == "__main__":
    main()
