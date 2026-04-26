# SEO-Monatsroutine — 4 Websites

Websites: oi.tax · steueranwaltskanzlei.com · steueranwalt-hamburg.de · steueranwalt-zuerich.ch
Zeitaufwand: ca. 45 Minuten pro Monat
Turnus: Jeden 1. des Monats

---

## Schritt 1: Daten holen (15 Min.)

Öffne 4 Browser-Tabs parallel — je einen pro Property.

### Google Search Console

| Property | URL |
|---|---|
| oi.tax | search.google.com/search-console → oi.tax |
| steueranwaltskanzlei.com | search.google.com/search-console → steueranwaltskanzlei.com |
| steueranwalt-hamburg.de | search.google.com/search-console → steueranwalt-hamburg.de |
| steueranwalt-zuerich.ch | search.google.com/search-console → steueranwalt-zuerich.ch |

Pro Tab: Leistung → Suchergebnisse → Datum → Vergleichen → Vorherige 28 Tage → Exportieren → Google Sheets

### Google Analytics GA4

| Property | ID |
|---|---|
| oi.tax | G-QP9TCQ7FG9 |
| steueranwaltskanzlei.com | G-BL2S0EVD0Z |
| steueranwalt-hamburg.de | G-LR90VG7QE2 |
| steueranwalt-zuerich.ch | G-15W7GJH219 |

Pro Tab: Berichte → Akquisition → Traffic-Akquisition → Vergleich aktivieren → Zeile „Organic Search" ablesen

---

## Schritt 2: Master-Tabelle ausfüllen (10 Min.)

| Kennzahl | oi.tax | steueranwaltskanzlei.com | steueranwalt-hamburg.de | steueranwalt-zuerich.ch |
|---|---|---|---|---|
| GSC Klicks aktuell | | | | |
| GSC Klicks Vormonat | | | | |
| Veränderung % | | | | |
| Impressionen aktuell | | | | |
| Impressionen Vormonat | | | | |
| Veränderung % | | | | |
| Ø CTR aktuell | | | | |
| Ø Position aktuell | | | | |
| GA4 Organic Sessions aktuell | | | | |
| GA4 Organic Sessions Vormonat | | | | |
| Conversion Rate (generate_lead) | | | | |
| quick_exit-Anteil (falls >20 %) | | | | |

---

## Schritt 3: Pro-Site-Analyse (15 Min. — je 4 Min. pro Site)

Für jede Site folgende Fragen beantworten:

**1. Gibt es eine klare Bewegung in eine Richtung?**
- Klicks +/- mehr als 15 % → Ursache suchen (neues Keyword, Verlust, saisonaler Effekt)

**2. Welches Keyword hat sich am stärksten verändert?**
- GSC → Abfragen → Differenz sortieren → Top-Mover notieren

**3. Gibt es eine Seite mit hohem quick_exit-Anteil?**
- GA4 → Engagement → Ereignisse → quick_exit → nach page aufschlüsseln

**4. Gibt es ein Keyword nahe Seite 1 (Position 8–20)?**
- GSC → Abfragen → Position 8–20 filtern → Kandidaten notieren

---

## Schritt 4: Massnahmen priorisieren (5 Min.)

Verwende diese Prioritätslogik:

```
1. DRINGEND: Klick-Verlust > 25 % auf einer Site → sofort Ursache suchen
2. HOCH:     quick_exit > 20 % auf einer wichtigen Seite → Inhalt überarbeiten
3. MITTEL:   Keyword auf Position 8–15 → gezielter Content-Push möglich
4. NIEDRIG:  CTR < 1 % bei Position < 10 → Snippet (Title/Description) optimieren
```

Maximal 1 Massnahme pro Site pro Monat — nicht mehr.

---

## Schritt 5: Monatsnotiz speichern

Vorlage (als Kommentar in den jeweiligen GitHub-Repos oder als Datei):

```
Datum: [Monat Jahr]
Site: [URL]

Klicks: [X] ([+/-]% vs. Vormonat)
Impressionen: [X] ([+/-]%)
Ø CTR: [X]%
Ø Position: [X]
Organic Sessions: [X]
Conversions (generate_lead): [X]

Auffälligste Bewegung: [Keyword / Seite]
Massnahme diesen Monat: [was wird getan]
Ergebnis prüfen am: [nächster Monat]
```

---

## Kennzahlen-Referenz

| Kennzahl | Gut | Verbesserungsbedarf |
|---|---|---|
| CTR (Legal CH/DE) | > 2,5 % | < 1,5 % |
| Ø Position Ziel-Keywords | < 10 | > 20 |
| quick_exit-Anteil | < 10 % | > 20 % |
| scroll_depth 75 % | > 30 % der Besucher | < 15 % |
| time_on_page 60s | > 40 % der Besucher | < 20 % |
| Organic Sessions Monat | wächst | sinkt 2+ Monate |

---

## GA4-Satisfaction-Signals auswerten

Einmal pro Quartal — nicht monatlich nötig.

1. GA4 → Berichte → Engagement → Ereignisse
2. Ereignis `scroll_depth` anklicken → nach Parameter `page` aufschlüsseln
3. Ereignis `quick_exit` anklicken → nach Parameter `page` aufschlüsseln
4. Ereignis `time_on_page` (seconds=120) → nach `page` aufschlüsseln

**Interpretation:**

| Kombination | Bedeutung | Massnahme |
|---|---|---|
| Hoher quick_exit, wenig scroll_depth | Inhalt passt nicht zur Suchabsicht | Title/H1/Intro überarbeiten |
| Hoher scroll_depth, kein generate_lead | Inhalt überzeugt, CTA fehlt | CTA sichtbarer platzieren |
| Viel time_on_page, wenig internal_nav | Sackgasse — kein Weiterklicken | Interne Links ergänzen |
| Viel internal_nav, wenig generate_lead | Nutzer sucht noch — zu früh für Kontakt | Informationsarchitektur prüfen |

---

## Setup-Script für neue Sites

Das Script `docs/setup_tracking.py` auf das Root-Verzeichnis eines Repos anwenden:

```bash
# Im Root des jeweiligen Repos ausführen:
python3 /pfad/zu/setup_tracking.py --ga4-id G-XXXXXXXXXX --lang de
```

Optionen:
- `--ga4-id` : GA4 Property ID der Site
- `--lang` : Hauptsprache (`de` oder `en`) für Cookie-Banner-Text
- `--privacy-link` : Pfad zur Datenschutzseite (Standard: `datenschutz.html`)

---

## Schnell-Checkliste Monatsbeginn

- [ ] 4x GSC-Export → Google Sheets
- [ ] 4x GA4 Organic Sessions notieren
- [ ] Master-Tabelle ausfüllen
- [ ] Pro Site: eine Auffälligkeit benennen
- [ ] Pro Site: eine Massnahme festlegen (oder explizit: keine nötig)
- [ ] Monatsnotiz in Repo/Datei speichern
