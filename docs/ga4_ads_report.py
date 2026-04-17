"""
GA4 Google Ads Campaign Report for oi.tax
Property ID: 273918863

Requirements:
    pip install requests rsa

Usage:
    python ga4_ads_report.py --key service_account.json
"""

import argparse
import base64
import json
import time
import requests
import rsa

PROPERTY_ID = "273918863"
API_URL = f"https://analyticsdata.googleapis.com/v1beta/properties/{PROPERTY_ID}:runReport"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPE = "https://www.googleapis.com/auth/analytics.readonly"

DIMENSIONS = [
    {"name": "sessionGoogleAdsCampaignName"},
    {"name": "sessionGoogleAdsMedium"},
    {"name": "sessionDefaultChannelGroup"},
    {"name": "month"},
]

METRICS = [
    {"name": "sessions"},
    {"name": "totalUsers"},
    {"name": "newUsers"},
    {"name": "bounceRate"},
    {"name": "averageSessionDuration"},
    {"name": "conversions"},
    {"name": "totalRevenue"},
]


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _make_jwt(client_email: str, private_key_pem: str) -> str:
    now = int(time.time())
    header = _b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    payload = _b64url(json.dumps({
        "iss": client_email,
        "scope": SCOPE,
        "aud": TOKEN_URL,
        "iat": now,
        "exp": now + 3600,
    }).encode())
    signing_input = f"{header}.{payload}".encode()
    # Service account keys are PKCS#8; convert to PKCS#1 DER then load
    import re, base64 as _b64
    pem_body = re.sub(r"-----[^-]+-----|\s", "", private_key_pem)
    der = _b64.b64decode(pem_body)
    # Strip PKCS#8 wrapper (30 82 ... 30 0d ... 04 82 ...) to get PKCS#1
    # Find the inner OCTET STRING containing the RSAPrivateKey
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


def run_report(token: str, start: str, end: str) -> dict:
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "dimensions": DIMENSIONS,
        "metrics": METRICS,
        "dateRanges": [{"startDate": start, "endDate": end}],
        "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}],
        "limit": 1000,
    }
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def format_report(data: dict) -> None:
    dim_headers = [h["name"] for h in data.get("dimensionHeaders", [])]
    met_headers = [h["name"] for h in data.get("metricHeaders", [])]
    headers = dim_headers + met_headers
    col_widths = [max(len(h), 12) for h in headers]

    header_line = "  ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    print(header_line)
    print("-" * len(header_line))

    for row in data.get("rows", []):
        dims = [v["value"] for v in row.get("dimensionValues", [])]
        mets = [v["value"] for v in row.get("metricValues", [])]
        values = dims + mets
        print("  ".join(str(v).ljust(w) for v, w in zip(values, col_widths)))

    print(f"\nTotal rows: {data.get('rowCount', 0)}")


def main():
    parser = argparse.ArgumentParser(description="GA4 Google Ads report for oi.tax")
    parser.add_argument("--key", required=True, help="Path to service account JSON key")
    parser.add_argument("--start", default="2025-01-01", help="Start date YYYY-MM-DD")
    parser.add_argument("--end", default="today", help="End date YYYY-MM-DD or 'today'")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    token = get_access_token(args.key)
    data = run_report(token, args.start, args.end)

    if args.json:
        rows = []
        dim_headers = [h["name"] for h in data.get("dimensionHeaders", [])]
        met_headers = [h["name"] for h in data.get("metricHeaders", [])]
        for row in data.get("rows", []):
            record = {}
            for i, h in enumerate(dim_headers):
                record[h] = row["dimensionValues"][i]["value"]
            for i, h in enumerate(met_headers):
                record[h] = row["metricValues"][i]["value"]
            rows.append(record)
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        format_report(data)


if __name__ == "__main__":
    main()
