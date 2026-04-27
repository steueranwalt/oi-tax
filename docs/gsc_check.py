"""GSC-Diagnose: listet alle Properties auf die der Service Account sieht."""
import base64, json, re, time, requests, rsa

def b64url(d):
    return base64.urlsafe_b64encode(d).rstrip(b"=").decode()

def get_token(key_path):
    creds = json.load(open(key_path))
    now = int(time.time())
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
    hdr = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    pay = b64url(json.dumps({"iss": creds["client_email"], "scope": SCOPE,
                              "aud": TOKEN_URL, "iat": now, "exp": now + 3600}).encode())
    signing = f"{hdr}.{pay}".encode()
    pem_body = re.sub(r"-----[^-]+-----|\s", "", creds["private_key"])
    der = base64.b64decode(pem_body)
    idx = der.index(b"\x04\x82")
    inner = (der[idx + 2] << 8) | der[idx + 3]
    key = rsa.PrivateKey._load_pkcs1_der(der[idx + 4: idx + 4 + inner])
    sig = rsa.sign(signing, key, "SHA-256")
    jwt = f"{hdr}.{pay}.{b64url(sig)}"
    r = requests.post(TOKEN_URL, data={
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt}, timeout=15)
    r.raise_for_status()
    return r.json()["access_token"]

import sys
key = sys.argv[1] if len(sys.argv) > 1 else "fiorin-d83c6c57ee92.json"
print(f"Service Account Key: {key}")
token = get_token(key)
print("Token OK")
r = requests.get("https://searchconsole.googleapis.com/webmasters/v3/sites",
                 headers={"Authorization": f"Bearer {token}"})
print(f"Status: {r.status_code}")
print(r.text[:2000])
