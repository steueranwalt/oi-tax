#!/usr/bin/env python3
"""
GA4 Tracking Setup — statische HTML-Sites
Wendet Consent Mode v2, Cookie-Banner, Lead-Tracking und Satisfaction-Signals
auf alle HTML-Dateien eines Repos an.

Verwendung:
  python3 setup_tracking.py --ga4-id G-XXXXXXXXXX --lang de
  python3 setup_tracking.py --ga4-id G-XXXXXXXXXX --lang en --privacy-link privacy.html

Bekannte Properties:
  oi.tax                   G-QP9TCQ7FG9
  steueranwaltskanzlei.com G-BL2S0EVD0Z
  steueranwalt-hamburg.de  G-LR90VG7QE2
  steueranwalt-zuerich.ch  G-15W7GJH219
"""

import os, re, argparse

# --- Argumente -----------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument('--ga4-id', required=True, help='GA4 Property ID, z.B. G-XXXXXXXXXX')
parser.add_argument('--lang', default='de', choices=['de', 'en'], help='Hauptsprache (de/en)')
parser.add_argument('--privacy-link', default=None, help='Pfad zur Datenschutzseite')
parser.add_argument('--base-dir', default='.', help='Root-Verzeichnis des Repos')
args = parser.parse_args()

GA4_ID       = args.ga4_id
MAIN_LANG    = args.lang
BASE_DIR     = os.path.abspath(args.base_dir)

# Datenschutz-Link automatisch erkennen oder aus Argument übernehmen
PRIVACY_FALLBACK = args.privacy_link or ('datenschutz.html' if MAIN_LANG == 'de' else 'privacy.html')


# --- Snippets ------------------------------------------------------------

def gtag_snippet(ga4_id):
    return f'''<!-- Google tag (gtag.js) with Consent Mode v2 -->
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent', 'default', {{
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    wait_for_update: 500
  }});
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={ga4_id}"></script>
<script>
  gtag('js', new Date());
  gtag('config', '{ga4_id}');
  if (localStorage.getItem('oi_consent') === 'granted') {{
    gtag('consent', 'update', {{ analytics_storage: 'granted' }});
  }}
</script>'''


def banner_snippet(lang, privacy_link):
    if lang == 'de':
        return f'''<div id="oi-consent" style="display:none;position:fixed;bottom:0;left:0;right:0;background:#1a1a1a;border-top:1px solid #333;padding:1rem 1.5rem;align-items:center;justify-content:space-between;gap:1rem;z-index:9999;flex-wrap:wrap;">
  <p style="margin:0;color:#f2f2f2;font-size:0.875rem;">Diese Website verwendet Google Analytics zur anonymen Nutzungsanalyse. <a href="{privacy_link}" style="color:#ff3500;">Datenschutz</a></p>
  <div style="display:flex;gap:0.75rem;flex-shrink:0;">
    <button onclick="oiDenyConsent()" style="background:transparent;border:1px solid #666;color:#f2f2f2;padding:0.5rem 1rem;cursor:pointer;font-size:0.875rem;border-radius:4px;">Ablehnen</button>
    <button onclick="oiGrantConsent()" style="background:#ff3500;border:none;color:#fff;padding:0.5rem 1rem;cursor:pointer;font-size:0.875rem;border-radius:4px;font-weight:600;">Akzeptieren</button>
  </div>
</div>'''
    else:
        return f'''<div id="oi-consent" style="display:none;position:fixed;bottom:0;left:0;right:0;background:#1a1a1a;border-top:1px solid #333;padding:1rem 1.5rem;align-items:center;justify-content:space-between;gap:1rem;z-index:9999;flex-wrap:wrap;">
  <p style="margin:0;color:#f2f2f2;font-size:0.875rem;">This site uses Google Analytics to understand usage anonymously. <a href="{privacy_link}" style="color:#ff3500;">Privacy policy</a></p>
  <div style="display:flex;gap:0.75rem;flex-shrink:0;">
    <button onclick="oiDenyConsent()" style="background:transparent;border:1px solid #666;color:#f2f2f2;padding:0.5rem 1rem;cursor:pointer;font-size:0.875rem;border-radius:4px;">Decline</button>
    <button onclick="oiGrantConsent()" style="background:#ff3500;border:none;color:#fff;padding:0.5rem 1rem;cursor:pointer;font-size:0.875rem;border-radius:4px;font-weight:600;">Accept</button>
  </div>
</div>'''


TRACKING_SCRIPT = '''<script>
  /* Lead-Tracking, Consent, Satisfaction-Signals */
  document.querySelectorAll('a[data-lead]').forEach(function(a) {
    a.addEventListener('click', function() {
      gtag('event', 'generate_lead', { method: a.dataset.lead });
    });
  });
  function oiGrantConsent() {
    localStorage.setItem('oi_consent', 'granted');
    gtag('consent', 'update', { analytics_storage: 'granted' });
    document.getElementById('oi-consent').style.display = 'none';
  }
  function oiDenyConsent() {
    localStorage.setItem('oi_consent', 'denied');
    document.getElementById('oi-consent').style.display = 'none';
  }
  if (!localStorage.getItem('oi_consent')) {
    document.getElementById('oi-consent').style.display = 'flex';
  }
  (function () {
    var path = location.pathname;
    var marks = { 25: false, 50: false, 75: false };
    window.addEventListener('scroll', function () {
      var pct = (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight * 100;
      [25, 50, 75].forEach(function (m) {
        if (!marks[m] && pct >= m) { marks[m] = true; gtag('event', 'scroll_depth', { depth: m, page: path }); }
      });
    }, { passive: true });
    [30, 60, 120].forEach(function (s) {
      setTimeout(function () { gtag('event', 'time_on_page', { seconds: s, page: path }); }, s * 1000);
    });
    document.querySelectorAll('a[href^="/"], a[href^="./"], a[href$=".html"]').forEach(function (a) {
      if (!a.dataset.lead) {
        a.addEventListener('click', function () { gtag('event', 'internal_nav', { destination: a.getAttribute('href') }); });
      }
    });
    if (/google\\.|bing\\./.test(document.referrer)) {
      var engaged = false;
      ['scroll', 'click', 'keydown'].forEach(function (ev) {
        document.addEventListener(ev, function () { engaged = true; }, { once: true, passive: true });
      });
      setTimeout(function () { if (!engaged) gtag('event', 'quick_exit', { page: path }); }, 15000);
    }
  }());
</script>'''


# --- Hilfsfunktionen -----------------------------------------------------

def detect_lang(content):
    m = re.search(r'<html[^>]*lang="([^"]*)"', content)
    return m.group(1) if m else MAIN_LANG

def detect_privacy_link(content, lang):
    m = re.search(r'href="([^"]*datenschutz[^"]*)"', content)
    if m: return m.group(1)
    m = re.search(r'href="([^"]*privacy[^"]*)"', content)
    if m: return m.group(1)
    return PRIVACY_FALLBACK

def collect_html_files(base):
    result = []
    skip_dirs = {'.git', 'assets', 'docs', 'images', 'node_modules', '.github'}
    for root, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if f.endswith('.html') and 'template' not in f.lower():
                result.append(os.path.join(root, f))
    return sorted(result)


# --- Hauptlogik ----------------------------------------------------------

def process_file(fpath, ga4_id):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    lang         = detect_lang(content)
    privacy_link = detect_privacy_link(content, lang)
    changes      = []

    # 1. GA4 + Consent Mode v2 in <head>
    if ga4_id not in content:
        content = content.replace('</head>', gtag_snippet(ga4_id) + '\n</head>', 1)
        changes.append('GA4+ConsentMode')

    # 2. Telefon-Links: data-lead hinzufügen
    before = content
    content = re.sub(
        r'(<a )([^>]*href="tel:\+41[^"]*")(?![^>]*data-lead)',
        r'\1\2 data-lead="phone_ch"', content)
    content = re.sub(
        r'(<a )([^>]*href="tel:\+49[^"]*")(?![^>]*data-lead)',
        r'\1\2 data-lead="phone_de"', content)
    if content != before:
        changes.append('phone-tracking')

    # 3. IncaMail-Links: data-lead hinzufügen
    before = content
    content = re.sub(
        r'(<a )([^>]*href="https://incamail\.com/[^"]*")(?![^>]*data-lead)',
        r'\1\2 data-lead="incamail"', content)
    if content != before:
        changes.append('incamail-tracking')

    # 4. Cookie-Banner + Tracking-Script vor </body>
    if 'oi-consent' not in content:
        banner = banner_snippet(lang, privacy_link)
        content = content.replace('</body>', banner + '\n' + TRACKING_SCRIPT + '\n</body>', 1)
        changes.append('banner+signals')

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  UPDATED ({lang}) [{", ".join(changes)}]: {os.path.relpath(fpath, BASE_DIR)}')
    else:
        print(f'  SKIP (bereits aktuell): {os.path.relpath(fpath, BASE_DIR)}')


# --- Ausführung ----------------------------------------------------------

if __name__ == '__main__':
    files = collect_html_files(BASE_DIR)
    print(f'\nGA4-Setup: {GA4_ID} | Sprache: {MAIN_LANG} | {len(files)} HTML-Dateien gefunden\n')

    for fpath in files:
        process_file(fpath, GA4_ID)

    print(f'\nFertig. Bitte testen:')
    print(f'  1. Website öffnen → Cookie-Banner muss erscheinen')
    print(f'  2. Akzeptieren → Banner verschwindet')
    print(f'  3. Auf Kontakt-Link klicken → GA4 Echtzeit → generate_lead prüfen')
    print(f'  4. GA4 Admin → Datenanzeige → Ereignisse → generate_lead als Schlüsselereignis markieren')
