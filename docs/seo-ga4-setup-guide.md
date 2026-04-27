# SEO-Auswertung & GA4-Setup — Anleitung für neue Websites

Erstellt auf Basis der Einrichtung für oi.tax (April 2026).
Gilt für statische HTML-Sites mit direktem gtag.js (kein Google Tag Manager).

---

## Teil 1: Monatliche SEO-Auswertung

### 1.1 Google Search Console — Daten exportieren

**Gesamtkennzahlen:**
1. search.google.com/search-console → Property auswählen
2. Linkes Menü → **„Leistung"** → **„Suchergebnisse"**
3. **„Datum"** → **„Vergleichen"** → **„Vorherige Periode"**
4. Zeitraum: **Letzte 28 Tage**
5. Alle 4 Kacheln aktivieren: Klicks, Impressionen, CTR, Position
6. Zahlen notieren (aktuell + Vorperiode)

**Keywords nach Clicks:**
- Tab **„Abfragen"** → Sortierung: Klicks absteigend → Top 10 notieren

**Positions-Gewinner/-Verlierer:**
- Tab „Abfragen", Vergleichsmodus aktiv
- Spalte „Position" → Differenz → aufsteigend (Gewinner) / absteigend (Verlierer)

**Seiten mit Clicks-Änderungen:**
- Tab **„Seiten"** → Spalte „Differenz Klicks"

**Export:** Oben rechts → „Exportieren" → Google Sheets

---

### 1.2 Google Analytics GA4 — Daten exportieren

**Organic Sessions:**
1. analytics.google.com → Property auswählen
2. Berichte → **„Akquisition"** → **„Traffic-Akquisition"**
3. Vergleich aktivieren (letzte 28 Tage vs. vorherige 28 Tage)
4. Zeile **„Organic Search"** → Sessions notieren

**Conversion Rate (nur wenn Key Events eingerichtet):**
- Gleiche Tabelle → Spalte „Schlüsselereignisse" bei Organic Search

**Top Landingpages Organic:**
1. Berichte → **„Engagement"** → **„Landingpages"**
2. Filter hinzufügen → „Sitzungs-Standardkanal-Gruppe" = „Organic Search"
3. Top 5 URLs + Sessions + Absprungrate notieren

---

### 1.3 SEO-Report erstellen

Vorlage für den monatlichen Report (Zielgruppe: Kanzleiinhaber, 5 Minuten lesbar):

```
## SEO-Report [Website] — [Monat Jahr]
Zeitraum: [Datum] vs. [Datum]

### 1. Kennzahlen-Übersicht
| Kennzahl          | Aktuell | Vormonat | Veränderung |
|-------------------|---------|----------|-------------|
| Klicks            |         |          | ▲▼ %        |
| Impressionen      |         |          | ▲▼ %        |
| Ø CTR             |         |          | ▲▼ %        |
| Ø Position        |         |          | ▲▼          |
| Organic Sessions  |         |          | ▲▼ %        |
| Conversion Rate   |         |          | ▲▼ %        |

### 2. Drei Wins diesen Monat
- [Keyword X] von Position Y auf Z — konkrete Clicks-Auswirkung
- ...

### 3. Drei Probleme mit Massnahmen
Problem | Warum relevant | Was tun

### 4. Priorität nächsten Monat
„Priorität: [Massnahme] — weil [Begründung]."

### 5. Keyword-Radar (Position 11–20)
Keywords nahe Seite 1 + konkrete Seitenempfehlung

### Gesamteinschätzung
Trend positiv / neutral / negativ — ein Satz Begründung.
```

**Format-Regeln:**
- Kein ß (Schweizer Rechtschreibung: ss statt ß)
- Zahlen immer mit Kontext (z.B. „CTR 3 % — Branchenschnitt Legal CH: ~2,5 %")
- Keine Agentur-Floskeln

---

## Teil 2: GA4-Tracking einrichten

### 2.0 Übersicht — alle Events

| Event | Auslöser | Parameter | Zweck |
|---|---|---|---|
| `generate_lead` | Klick IncaMail / Telefon | `method`: incamail / phone_ch / phone_de | Conversion-Messung |
| `scroll_depth` | Scroll 25 / 50 / 75 % | `depth`, `page` | Inhalt gelesen? |
| `time_on_page` | 30s / 60s / 120s aktiv | `seconds`, `page` | Echte Beschäftigung |
| `internal_nav` | Klick auf internen Link | `destination` | Weiterexploration |
| `quick_exit` | <15s ohne Interaktion (von Google/Bing) | `page` | Pogo-Stick-Proxy |

### 2.1 Consent Mode v2 — Code-Änderung

Ersetze den bestehenden gtag-Snippet im `<head>` jeder HTML-Seite:

**Alt:**
```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

**Neu (Consent Mode v2):**
```html
<!-- Google tag (gtag.js) with Consent Mode v2 -->
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('consent', 'default', {
    analytics_storage: 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    wait_for_update: 500
  });
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
  if (localStorage.getItem('oi_consent') === 'granted') {
    gtag('consent', 'update', { analytics_storage: 'granted' });
  }
</script>
```

> `G-XXXXXXXXXX` mit der echten GA4 Property ID ersetzen.

---

### 2.2 Telefon-Klicks tracken

Tel-Links um `data-lead`-Attribut ergänzen:

```html
<!-- Vorher -->
<a href="tel:+41441234567">+41 44 123 45 67</a>

<!-- Nachher -->
<a href="tel:+41441234567" data-lead="phone_ch">+41 44 123 45 67</a>
```

Schema für `data-lead`-Werte:
- `phone_ch` — Schweizer Nummer
- `phone_de` — Deutsche Nummer
- `incamail` — verschlüsseltes Kontaktformular
- `contact_form` — Standard-Kontaktformular

---

### 2.3 Event-Listener + Consent-Funktionen

Folgenden Script-Block vor `</body>` einfügen (ersetzt den einfachen generate_lead-Listener):

```html
<script>
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
</script>
```

---

### 2.4 Cookie-Banner

Direkt vor `</body>` einfügen. Farben an das jeweilige Site-Design anpassen (`#2a2a2a`, `#ff3500` etc.):

**Deutsch:**
```html
<div id="oi-consent" style="display:none;position:fixed;bottom:0;left:0;right:0;background:#2a2a2a;border-top:1px solid #4a4a4a;padding:1rem 1.5rem;align-items:center;justify-content:space-between;gap:1rem;z-index:9999;flex-wrap:wrap;">
  <p style="margin:0;color:#f2f2f2;font-size:0.875rem;">Diese Website verwendet Google Analytics zur anonymen Nutzungsanalyse. <a href="/privacy/" style="color:#ff3500;">Datenschutz</a></p>
  <div style="display:flex;gap:0.75rem;flex-shrink:0;">
    <button onclick="oiDenyConsent()" style="background:transparent;border:1px solid #7a7a7a;color:#f2f2f2;padding:0.5rem 1rem;cursor:pointer;font-size:0.875rem;border-radius:4px;">Ablehnen</button>
    <button onclick="oiGrantConsent()" style="background:#ff3500;border:none;color:#fff;padding:0.5rem 1rem;cursor:pointer;font-size:0.875rem;border-radius:4px;font-weight:600;">Akzeptieren</button>
  </div>
</div>
```

**Englisch:**
```html
<div id="oi-consent" style="display:none;position:fixed;bottom:0;left:0;right:0;background:#2a2a2a;border-top:1px solid #4a4a4a;padding:1rem 1.5rem;align-items:center;justify-content:space-between;gap:1rem;z-index:9999;flex-wrap:wrap;">
  <p style="margin:0;color:#f2f2f2;font-size:0.875rem;">This site uses Google Analytics to understand usage anonymously. <a href="/privacy/" style="color:#ff3500;">Privacy policy</a></p>
  <div style="display:flex;gap:0.75rem;flex-shrink:0;">
    <button onclick="oiDenyConsent()" style="background:transparent;border:1px solid #7a7a7a;color:#f2f2f2;padding:0.5rem 1rem;cursor:pointer;font-size:0.875rem;border-radius:4px;">Decline</button>
    <button onclick="oiGrantConsent()" style="background:#ff3500;border:none;color:#fff;padding:0.5rem 1rem;cursor:pointer;font-size:0.875rem;border-radius:4px;font-weight:600;">Accept</button>
  </div>
</div>
```

> Link `/privacy/` durch den tatsächlichen Datenschutz-Pfad der jeweiligen Site ersetzen.

---

### 2.5 Satisfaction Signals — User-Zufriedenheit messen

Google wertet zunehmend aus, ob Inhalte die Suchabsicht befriedigen. Direkte Rankingfaktoren sind diese Signale nicht — aber Seiten mit starkem Engagement halten Positionen stabiler und erholen sich nach Updates schneller.

**Wichtige Hinweise:**
- `time_on_page` misst Zeit ab Seitenload, nicht aktive Lesezeit (Tab-Wechsel werden nicht herausgefiltert)
- `quick_exit` feuert nur bei organischen Besuchern (Referrer enthält google. oder bing.)
- `internal_nav` erfasst Klicks auf relative Links (`href` beginnt mit `/` oder endet mit `.html`)

Folgenden Script-Block vor `</body>` einfügen (kombiniert mit Consent- und Lead-Tracking):

```html
<script>
  /* Lead + consent + satisfaction signals */
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
  /* Satisfaction signals */
  (function () {
    var path = location.pathname;

    // Scroll depth: 25 %, 50 %, 75 %
    var marks = { 25: false, 50: false, 75: false };
    window.addEventListener('scroll', function () {
      var pct = (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight * 100;
      [25, 50, 75].forEach(function (m) {
        if (!marks[m] && pct >= m) { marks[m] = true; gtag('event', 'scroll_depth', { depth: m, page: path }); }
      });
    }, { passive: true });

    // Time on page: 30 s, 60 s, 120 s
    [30, 60, 120].forEach(function (s) {
      setTimeout(function () { gtag('event', 'time_on_page', { seconds: s, page: path }); }, s * 1000);
    });

    // Internal navigation
    document.querySelectorAll('a[href^="/"], a[href^="./"], a[href$=".html"]').forEach(function (a) {
      if (!a.dataset.lead) {
        a.addEventListener('click', function () { gtag('event', 'internal_nav', { destination: a.getAttribute('href') }); });
      }
    });

    // Quick-exit proxy (pogo-stick): organischer Besucher, keine Interaktion in 15 s
    if (/google\.|bing\./.test(document.referrer)) {
      var engaged = false;
      ['scroll', 'click', 'keydown'].forEach(function (ev) {
        document.addEventListener(ev, function () { engaged = true; }, { once: true, passive: true });
      });
      setTimeout(function () { if (!engaged) gtag('event', 'quick_exit', { page: path }); }, 15000);
    }
  }());
</script>
```

**Auswertung in GA4:**
- Berichte → Engagement → Ereignisse → nach Ereignisname filtern
- Vergleich: Seiten mit hohem `scroll_depth`-75%-Anteil vs. Seiten mit hohem `quick_exit`-Anteil
- Seiten mit vielen `quick_exit`-Events → Inhalt oder Meta-Description überarbeiten
- Seiten mit `time_on_page` 120s → Inhalt funktioniert, für interne Verlinkung priorisieren

---

1. analytics.google.com → Property auswählen
2. Links unten: **Zahnrad-Icon** (Verwaltung)
3. Spalte „Property" → **„Datenanzeige"** → **„Ereignisse"**
4. Event `generate_lead` suchen → **Stern anklicken** → als Schlüsselereignis markieren

> Das Event erscheint in der Liste erst nach dem ersten echten Klick auf einen getrackten Link. Falls es noch nicht sichtbar ist: Auf der Website einmal auf den Kontakt-Button klicken, dann 24h warten.

**Nach der Aktivierung sichtbar in:**
- Berichte → Akquisition → Traffic-Akquisition → Spalte „Schlüsselereignisse"
- Aufgeteilt nach `method`: `incamail`, `phone_ch`, `phone_de`

---

## Checkliste neue Website

- [ ] GA4 Property erstellt, Tracking-Code eingebunden
- [ ] Consent Mode v2 Snippet ersetzt (alle HTML-Seiten)
- [ ] `data-lead`-Attribute auf allen Kontakt-Links gesetzt
- [ ] Event-Listener + Consent-Funktionen eingefügt
- [ ] Cookie-Banner eingefügt (Sprache beachten)
- [ ] Datenschutz-Link im Banner korrekt gesetzt
- [ ] Ersten Klick auf Kontakt-Button ausgelöst (Event testen)
- [ ] GA4 Admin → `generate_lead` als Schlüsselereignis markiert
- [ ] Search Console Property erstellt und verifiziert
- [ ] Search Console mit GA4 Property verknüpft (Admin → Search Console-Verknüpfungen)
