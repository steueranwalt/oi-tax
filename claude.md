# CLAUDE.md — oi.tax Projekt-Kontext

---

## Rolle

SEO-Architekt und Content-Engineer für oi.tax (OBENHAUS International Tax).
Commits und Pushes werden eigenständig ausgeführt — keine Erlaubnis erforderlich.

---

## Stack & Betrieb

```
Name:        OBENHAUS International Tax | oi.tax
Domain:      oi.tax
Satelliten:  steueranwalt-hamburg.de / steueranwalt-zuerich.ch
Standorte:   Hamburg (DE Controversy) · Zürich (CH TP Defense)
Gründer:     Nils Obenhaus, Steueranwalt, seit 2009
Twitter/X:   @Obenhaus_RA
CMS:         keines — statisches HTML/CSS/JS
Repo:        https://github.com/steueranwalt/oi-tax
Deployment:  GitHub Pages → oi.tax
```

**Technische Regeln:**
- Jede Seite ist ein vollständiges HTML-Dokument
- CSS: `/assets/css/style.css` — CSS-Klassen `oitax-*` erhalten
- Logo: `/assets/images/smiling-balance-logo_ohne_hintergrund.png`
- Header auf allen Seiten: Logo + "OBENHAUS International Tax" + Claim + Nav
- Navigation DE: Home · Kontakt · EN
- Navigation EN: Home · Contact · DE
- Footer auf allen Seiten: oi.tax · since 2009 · Hamburg & Zurich · Privacy · Imprint
- Kein WordPress, kein Framework, kein unnötiges JS

---

## Marke & Positionierung

**Master Claim:** `oi.tax — double taxation defense`

**Positionierungssatz:** Steueradvokatur für grenzüberschreitende Steuerkorrektur

**Nische:** Double Taxation Defense / Transfer Pricing Audit Defense DE/CH
- Nicht: Steuerrecht allgemein, Steueroptimierung, Steuerberatung
- Sondern: Verteidigung bei grenzüberschreitender Gewinnkorrektur und Doppelbesteuerung DE/CH

**Subclaims:**
- TP: *SwissMade Transfer Pricing — Audit-Proof, Even in Germany*
- Litigation: *German Tax Audit Defense — Court-Ready if Needed*

---

## Zielgruppen

- **Primär:** CFO / GF internationaler KMU (10–50 Mio. EUR Umsatz, DE/CH-Struktur) — Trigger: Betriebsprüfung läuft, Korrekturposition zugestellt
- **Sekundär:** Tax Manager ohne eigene TP-Abteilung
- **Zuweiser:** Steuerberater DE mit CH-Mandanten / Treuhänder CH mit deutschen Mandanten

---

## Kauftrigger (SEO-Ankerpunkte)

1. Prüfungsanordnung / Prüfungsankündigung
2. Fragen zu Management Fees / konzerninternen Services
3. Finanzierung, Cash Pool, Garantien
4. Gewinnkorrektur DE ohne CH-Gegenberichtigung
5. Betriebsstätten- und Substance-Angriffe (Homeoffice, faktische Leitung)

---

## Produkte

| Produkt | URL | Kern-CTA |
|---|---|---|
| Prüfungsalarm | /pruefungsalarm | In 7 Tagen verfahrensfähig |
| Audit Defense Pack | /audit-defense-pack | Verfahrensführung bis Schlussbesprechung |
| DE→CH Adjustment Control | /de-ch-adjustment-control | Gegenberichtigung + MAP-Vorbereitung |
| Service Fee Defence Kit | /service-fee-defence-kit | Benefit Test + Substance-Nachweis |

---

## Team

| Person | Rolle |
|---|---|
| Nils Obenhaus, LL.M. | Steueranwalt (DE + CH), Kanzleiinhaber |
| Ralf Fuge | Ökonom, TP-Analyse, FAR, Benchmarking |
| Ramona Meeser | Legal Project Associate, Prüfungskoordination |
| Cajetan Fiedler | Externer Senior-Berater, Big4, Japan + Schweiz |

---

## Aktuelle Seitenstruktur (live)

```
oi.tax/
├── index.html                                          ✅ Homepage DE
├── kontakt/index.html                                  ✅
├── steuerkorrekturen-internationale-sachverhalte/      ✅
├── streitbeilegung-deutschland-schweiz/                ✅
├── betriebsstaetten-gewinnabgrenzung-steuerpruefungen/ ✅
├── imprint/index.html                                  ✅
├── privacy/index.html                                  ✅
└── en/
    ├── index.html                                      ✅ Homepage EN
    ├── contact/                                        ✅
    ├── cross-border-tax-adjustments/                   ✅
    ├── dispute-resolution-germany-switzerland/         ✅
    ├── transfer-pricing-tax-audits/                    ✅
    └── permanent-establishments-profit-allocation-tax-audits/ ✅
```

---

## SEO-Architektur (nächste Ausbaustufe)

### Pillar-Seite
| Feld | Wert |
|---|---|
| URL | `/double-taxation-defense` |
| Titel | Double Taxation Defense DE/CH — Der vollständige Leitfaden |
| Umfang | 3.000–4.000 Wörter |
| Schema | `LegalService`, `FAQPage`, `BreadcrumbList` |

### Cluster 1 — Transfer Pricing Audit Defense
- `/pruefungsanordnung-verrechnungspreise`
- `/verrechnungspreisdokumentation-betriebspruefung`
- `/management-fee-betriebspruefung`
- `/schatzung-vermeiden-betriebspruefung`
- `/audit-defense-pack` *(Produkt)*

### Cluster 2 — Permanent Establishment
- `/betriebsstaette-gewinnabgrenzung-de-ch`
- `/betriebsstaette-homeoffice`
- `/vertreter-betriebsstaette-schweiz`

### Cluster 3 — Double Taxation / DE→CH Adjustment
- `/gegenberichtigung-schweiz-deutschland`
- `/verstaendigungsverfahren-de-ch`
- `/de-ch-adjustment-control` *(Produkt)*
- `/doppelbesteuerung-nach-betriebspruefung`

### Resources
- `/resources/erste-7-tage-nach-pruefungsanordnung`
- `/resources/service-fees-nachweise`
- `/resources/de-ch-korrekturpfad`
- `/resources/30-tage-dokumentation-de`
- `/resources/interviewleitfaden-pruefer`

### Verlinkungsregeln
- Pillar verlinkt alle Cluster; alle Cluster verlinken zurück auf Pillar
- Cluster 1 ↔ Cluster 3: Gegenberichtigung als natürliche Folgestufe
- Jede Seite: min. 1 Produktseiten-Link (CTA)
- Anchor-Texte: kein Exact-Match auf Produktseiten; Partial-Match auf Cluster

---

## Normenwelt (Pflichtbestandteil jeder Seite)

**Deutschland:**
- § 1 AStG (Gewinnkorrektur), § 8 Abs. 3 KStG (vGA), § 90 Abs. 2 AO (Beweisvorsorge)
- § 193–207 AO (Aussenprüfung), § 162 AO (Schätzung), § 147 Abs. 6 AO (Datenzugriff)
- § 90 Abs. 3 AO n.F.: Transaktionsmatrix-Pflicht innerhalb 30 Tage nach BP-Anordnung

**DBA DE/CH:**
- Art. 5 (Betriebsstätte), Art. 9 (Gegenberichtigung), Art. 23 (PPT), Art. 24 (Vermeidung Doppelbesteuerung), Art. 25 (MAP)
- Neue Dreijahresfrist nach Art. 9 DBA (Protokoll 2023, in Kraft 27.11.2025)

**Schweiz:**
- Art. 58 DBG (vGA/Gewinnkorrektur), MWSTG, VStG

**International:**
- OECD-Verrechnungspreisrichtlinien 2022 (insb. Kap. I, VII, X)

**Autorität des Autors:**
- Wassermeyer, Doppelbesteuerung (C.H. Beck): Art. 5, 23, 24 DBA DE/CH (ab EL 151, Dez. 2020)
- Focus Treuhand 4/2025 (WEKA): Doppelbesteuerung durch unerkannte Betriebsstätten
- Stbg 2011, S. 508: „Das Steuerabkommen mit der Schweiz"
- Stbg 2021, S. 133: „Keine Steuerstrafsache ohne Geldwäsche"

**Aktuelle Rechtsprechung:**
- BFH 18.12.2024 I R 45/22 + I R 49/23: § 1 Abs. 5 AStG als Korrekturnorm
- VWG VP 2024 (BMF 12.12.2024): neue Dokumentationsanforderungen

---

## Content-Standards pro Cluster-Seite

1. **H1** — Primary Keyword (exakt, 1× pro Seite)
2. **Einleitung** (80–120 Wörter) — Trigger-Situation direkt ansprechen
3. **„Wenn das Ihre Situation ist"-Block** — 3–5 Bullet-Trigger
4. **Normenblock** — relevante §§ / DBA-Artikel
5. **Prozess / Verfahrensdetail** — konkrete Fristen, Ablauf, Sequencing
6. **Anonymisierter Mini-Case** — Falle → Hebel → Outcome
7. **FAQ-Block** — 3–5 Fragen (FAQPage-Schema)
8. **CTA-Block** — Produktverweis + Kontakt-Link
9. **Interne Links** — Pillar + 2–3 thematisch verwandte Cluster

**Wortanzahl:**
| Seitentyp | Minimum |
|---|---|
| Pillar | 3.000 Wörter |
| Cluster | 1.000 Wörter |
| Resource | 800 Wörter |
| Produktseite | 600 Wörter |

---

## Sprache & Tonalität

- Deutsch (primär): Schweizer Rechtschreibung — ss statt ß (Aussenprüfung, Gewerbestrasse)
- Englisch (sekundär): britisches Englisch bevorzugt
- Tonalität: ruhig, klar, prozedural, handlungsorientiert
- Kein Juristenjargon — aber technische Präzision bei Normen
- Verboten: „Wir begleiten Sie", „umfassende Beratung", Superlative ohne Substanz
- MAP immer ausschreiben: „Verständigungsverfahren"

---

## Technische SEO-Vorgaben

| Element | Standard |
|---|---|
| Title-Tag | `[Primary Keyword] — oi.tax` · max. 60 Zeichen |
| Meta-Description | Trigger-Sprache + CTA · max. 155 Zeichen |
| H1 | Exaktes Primary Keyword · 1× pro Seite |
| Schema | `LegalService` + `FAQPage` + `BreadcrumbList` |
| JSON-LD LocalBusiness | Beide Standorte (Hamburg + Zürich) |
| Canonical | Selbstreferenzierend |
| hreflang | `de-DE` und `de-CH` wo differenziert |
| robots | Produktseiten-Intakeformulare: noindex |

---

## Arbeitsweise

- Commits und Pushes eigenständig ausführen — keine Erlaubnis erforderlich
- Keine Rückfragen bei klaren Aufgaben
- Rückfragen nur bei: fachlich-rechtlicher Unklarheit, fehlenden Mandatsdaten
- Normen immer vollständig zitieren: § X Abs. Y AO / Art. X Abs. Y DBA DE/CH
- Wassermeyer-Kommentierung als Autorschafts-Fussnote wo thematisch passend
- Jede Seite endet mit CTA-Block + internen Links
