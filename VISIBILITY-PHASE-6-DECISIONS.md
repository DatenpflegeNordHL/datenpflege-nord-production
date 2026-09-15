# DatenpflegeNord — Visibility Phase 6 Decisions

Stand: 15. September 2026
Branch: `golden-visibility-phase-6-intelligence`
Validierter Ausgangspunkt: `e63dd6e28b1396ee3372a0d0e956cb3fdf0fcb5e`

## Scope und Guardrails

Phase 6 ist ausschließlich Research und Decision Intelligence. Es wurden keine neuen Produktionsseiten angelegt, keine Phase-4/5-Produktionscopy verändert, kein Deployment ausgeführt und kein Merge nach `main` vorgenommen.

Datengrundlage:

- 34 Keywords mit aktuellen DE-Metriken aus SE Ranking: Search Volume, Difficulty, CPC und Intent.
- Aktuelle SERP-Snapshots für die Pflichtcluster und die regionalen Entscheidungsthemen, überwiegend vom 15.09.2026; bei einzelnen nationalen Headterms stammen die letzten verfügbaren Provider-Snapshots aus Juli/August/Anfang September 2026.
- Lübeck-lokalisierte SERPs für Software und Web, Kiel-lokalisierte SERPs für Web und Hamburg-lokalisierte SERPs für AI.
- Bestehende Golden-Research-Dateien und die aktuellen Owner-Seiten im Repository.
- SE-Ranking-Backlinkdaten für DatenpflegeNord und ausgewählte lokale/nationale Wettbewerber.
- Direkte, read-only HTML-Prüfung ausgewählter rankender Wettbewerberseiten.

Wichtige Datenlücke: GSC ist weiterhin nicht verfügbar. Es werden keine Impressionen, Klicks, CTRs, Query-Positionen oder Indexierungsdaten aus Search Console erfunden. Alle mit `GSC REVISIT` markierten Entscheidungen müssen nach Anschluss der First-Party-Daten erneut geprüft werden.

## Executive Decision

Die nächste Sichtbarkeitsphase sollte nicht in viele zusätzliche Landingpages zerfallen. Die stärksten Chancen liegen in drei Hebeln:

1. DatenpflegeNord hat laut aktuellem SE-Ranking-Backlinkindex **0 Referring Domains**. Das ist gegenüber praktisch allen relevanten SERP-Wettbewerbern der größte siteweite Authority-Nachteil.
2. **KI-Prozessautomatisierung** zeigt einen eigenständigen nationalen Informations-/Decision-SERP gegenüber der lokalen kommerziellen KI-Seite. Ein sauber abgegrenzter Authority-Guide ist deshalb als einziger neuer Content-Owner ausreichend belegt: **BUILD**.
3. Relaunch, lokale Webbegriffe, Make-or-Buy und API/Schnittstellen brauchen überwiegend keine neuen URLs. Hier ist **EXPAND** der stärkere und risikoärmere Zug.

## 1. Keyword- und SERP-Evidence

### Software

| Keyword | Vol. | KD | Aktueller SERP-Befund | Current owner | Intent match | Content match | Ranking risk | Cannibalization | Action |
|---|---:|---:|---|---|---|---|---|---|---|
| softwareentwicklung lübeck | 110 | 34 | Local Pack + PAA; RXM, EXORD, Software and Testing; starke Job-/Studien-Pollution durch StepStone, Indeed, Heise, BA, TH/Uni | `/softwareentwicklung-luebeck/` | hoch | hoch | hoch: Local Pack + Jobs + Authority | niedrig bei einem Owner | **EXPAND CURRENT OWNER** |
| softwareentwickler lübeck | 110 | 15 | SERP noch stärker jobdominiert; Local Pack u. a. Aikonetic, novomind, EXORD | `/softwareentwicklung-luebeck/` | mittel | hoch | hoch: Suchbegriff ist semantisch doppeldeutig | hoch für separate Seite | **EXPAND CURRENT OWNER** |
| individuelle softwareentwicklung | 320 | 12 | AI Overview + PAA; nationale Leistungsseiten dominieren, u. a. Northcommit, Wilde IT, EXWE, MaibornWolff | `/softwareentwicklung-luebeck/` | hoch | hoch | mittel-hoch: nationaler Wettbewerb | hoch für zweiten Commercial Owner | **EXPAND CURRENT OWNER** |
| individualsoftware entwickeln lassen | 30 | 9 | AI Overview + PAA; Bauer+Kirch, HEC, Lise, EXWE, Sinovo; klare Decision/Commercial-Mischung | `/softwareentwicklung-luebeck/` + Kosten-Guide als Support | hoch | hoch | mittel | mittel | **EXPAND CURRENT OWNER** |
| individualsoftware beispiele | 70 | 15 | AI Overview + PAA + Images; eigene Examples-/Use-Case-Seiten ranken, u. a. Disphere, Objektkultur, DevDuck, ISAX | `/wissen/individualsoftware-kosten/` als nächster Owner | mittel | niedrig-mittel | mittel | mittel | **HOLD** — kein eigener Asset ohne verifizierbare Beispiele/Proof |
| standardsoftware vs individualsoftware | 20 | 6 | AI Overview + PAA; Vergleichsratgeber dominieren: ERP.de, Digital Experts, Operations1, Objektkultur, HEC | `/wissen/individualsoftware-kosten/` | hoch | hoch: Make-or-Buy-Matrix vorhanden | niedrig-mittel | hoch bei Split | **EXPAND CURRENT OWNER** |
| maßgeschneiderte software | 110 | 5 | AI Overview + PAA; überwiegend nationale Leistungsseiten | `/softwareentwicklung-luebeck/` | hoch | hoch | mittel | hoch bei neuer Commercial URL | **EXPAND CURRENT OWNER** |
| schnittstellenentwicklung | 110 | 6 | AI Overview + PAA; Mix aus Service- und Definitionsseiten: BEDM, Allbytes, PTC, StudySmarter, dkd | `/softwareentwicklung-luebeck/#schnittstellen` | hoch | hoch | mittel | hoch bei eigenem Service-Owner | **EXPAND CURRENT OWNER** |
| api entwicklung | 110 | 16 | AI Overview + PAA; Red Hat, Microsoft, SAP, Google/Lucidchart dominieren Info; Agenturseiten erst dahinter | `/softwareentwicklung-luebeck/#schnittstellen` | mittel-hoch | hoch | hoch: Authority-/Info-Headterm | hoch | **EXPAND CURRENT OWNER**; standalone API **HOLD** |
| api programmierung | 140 | 30 | AI Overview + PAA + Video; SAP, Wikipedia, IBM, Red Hat dominieren | `/softwareentwicklung-luebeck/#schnittstellen` | mittel | hoch | sehr hoch: informational authority | hoch | **EXPAND CURRENT OWNER**; standalone API **HOLD** |

Software-Entscheidung: Der lokale Commercial Owner ist bereits strukturell passend und besitzt eine eigene API-/Schnittstellen-Sektion. Eine zusätzliche generische API-Seite würde vor allem den internen Owner splitten, während Google bei den API-Headterms starke Definitions-/Authority-Domains bevorzugt.

### Web

| Keyword | Vol. | KD | Aktueller SERP-Befund | Current owner | Intent match | Content match | Ranking risk | Cannibalization | Action |
|---|---:|---:|---|---|---|---|---|---|---|
| webagentur lübeck | 320 | 55 | Local Pack + lokale Anbieter: foryumedia, Netzhirsch, Vicon, Popien, Jamp; werbeagentur.de als Directory | `/webentwicklung-luebeck/` | hoch | hoch | hoch: Local Pack + KD55 | sehr hoch bei zweiter Lübeck-Web-URL | **EXPAND CURRENT OWNER** |
| webentwicklung lübeck | 40 | 52 | HANSOLU, Vicon, Jamp, gradwerk, ISEO; Local Pack; leichte Job-Pollution | `/webentwicklung-luebeck/` | hoch | hoch | hoch | niedrig | **EXPAND CURRENT OWNER** |
| webdesign lübeck | 390 | 55 | Exakte lokale Leistungsseiten dominieren: Augustin, Northbay, Popien, Netzhirsch, Web Labels; starker Local Pack | `/webentwicklung-luebeck/` | hoch | hoch: Title/H1 enthalten Webdesign | sehr hoch | sehr hoch bei Split | **EXPAND CURRENT OWNER** |
| webdesigner schleswig-holstein | 170 | 27 | Statewide-Provider + Local Pack + Sortlist/Bark; u. a. Ralf Kortum, Jannis Timm, Bothe | `/webentwicklung-luebeck/` ist nur indirekter Owner | mittel | niedrig-mittel regional | mittel | mittel-hoch | **HOLD** |
| website erstellen lassen lübeck | 10 | 45 | Praktisch dieselben URLs wie `webdesign lübeck`: Augustin, Web Labels, Northbay, HANSOLU, Jamp, Popien, Netzhirsch | `/webentwicklung-luebeck/` | hoch | hoch: Phrase bereits im Hero/Projektstart | hoch | sehr hoch | **EXPAND CURRENT OWNER** |
| website relaunch | 250 | 16 | AI Overview + PAA + Images; nationale Definition-/Guide-Seiten dominieren | `/wissen/website-relaunch-checkliste/` | hoch | hoch | mittel | mittel | **EXPAND CURRENT OWNER** |
| website relaunch seo | 140 | 14 | AI Overview; Morefire, OMR, Sistrix, Seonative, Snutig, Ucentric; SEO-Guides dominieren | `/wissen/website-relaunch-checkliste/` | hoch | hoch | mittel | hoch bei neuem Guide | **EXPAND CURRENT OWNER** |
| website relaunch checkliste | 50 | 8 | AI Overview + PAA; HubSpot, Snutig, Vierviertel, Ucentric, Evergreen; Checklisten dominieren | `/wissen/website-relaunch-checkliste/` | sehr hoch | sehr hoch | mittel | niedrig | **EXPAND CURRENT OWNER** |
| website relaunch kosten | 30 | 9 | AI Overview + PAA; Kostenartikel und kombinierte Guides; Snutig/Brightsolutions ranken mit Kosten + Checkliste | `/wissen/website-relaunch-checkliste/` | hoch | mittel | niedrig-mittel | hoch bei separater Kosten-URL | **EXPAND CURRENT OWNER** |
| website relaunch projektplan | 20 | 7 | AI Overview + PAA; Webwild, OMR, Relaunch.de, Kreativkarussell, Snutig, Suxeedo; Guide/Plan-Intent | `/wissen/website-relaunch-checkliste/` | hoch | hoch | niedrig-mittel | hoch bei separatem Plan-Guide | **EXPAND CURRENT OWNER** |

Web-Entscheidung: Für Lübeck zeigen `webdesign`, `webagentur`, `webentwicklung` und `website erstellen lassen` weitgehend dieselbe Anbietergruppe. Das ist starke Anti-Split-Evidenz. Der aktuelle Owner enthält bereits Webdesign, Webentwicklung, Website-erstellen-lassen, Relaunch, Kostenfaktoren, technische SEO-Basis und Projektvorbereitung.

### KI / Automation

| Keyword | Vol. | KD | Aktueller SERP-Befund | Current owner | Intent match | Content match | Ranking risk | Cannibalization | Action |
|---|---:|---:|---|---|---|---|---|---|---|
| ki automatisierung | 920 | 54 | AI Overview + PAA + Video; IHK, Salesforce, Fraunhofer, KUKA, IBM, ServiceNow; starke Enterprise-/Definition-Authority | `/ki-automatisierung-luebeck/` | mittel: national informational vs local commercial | mittel-hoch | sehr hoch | hoch, wenn neuer Guide zu breit wird | **HOLD** als Headterm; über Process-Authority unterstützen |
| ki automation | 260 | 42 | Sehr ähnlich zu `ki automatisierung`: AIO/PAA, IHK, Salesforce, Fraunhofer, Enterprise-Anbieter | `/ki-automatisierung-luebeck/` | mittel | mittel-hoch | sehr hoch | hoch | **HOLD** als eigener Owner |
| ki prozessautomatisierung | 90 | 26 | Eigenständiger AIO/PAA-SERP: Future AI Solutions, d.velop, Haufe, IPH, Informatica, INNEO, Fraunhofer | `/ki-automatisierung-luebeck/` nur Commercial Owner | hoch für Thema, aber Intent-Separation vorhanden | Commercial-Seite deckt Basis, nicht Authority-Tiefe | mittel-hoch | kontrollierbar durch klare Rollen | **BUILD SUPPORTING AUTHORITY PAGE** |
| prozessautomatisierung ki | 30 | 7 | AIO + PAA + Video; Zenetti, IPH, Future AI, Informatica, BankingHub, Springer | `/ki-automatisierung-luebeck/` | hoch | mittel-hoch | mittel | kontrollierbar | **BUILD SUPPORTING AUTHORITY PAGE** |
| ki automatisierung für unternehmen | 40 | 45 | AIO + PAA; IHK, Salesforce, KI-Company, Fraunhofer, IBM; Info/Commercial-Mix | `/ki-automatisierung-luebeck/` | hoch | hoch | hoch | mittel | **EXPAND CURRENT OWNER** + Authority intern verlinken |
| intelligente automatisierung | 90 | 10 | AIO + PAA; IBM, PTC, CGI, AWS, OTRS, Oracle; Definition/Enterprise-Authority dominiert | `/ki-automatisierung-luebeck/` | mittel | mittel | hoch trotz niedriger KD | hoch bei Glossar-Klon | **HOLD** |
| ki workflow automatisierung | 20 | 19 | Keyword-Metrik vorhanden; der SERP-Provider lieferte für den exakten Term keinen belastbaren Result-Snapshot. Kein SERP erfunden. Nachbarcluster zeigt AIO/PAA/Guide-Mix. | `/ki-automatisierung-luebeck/` | hoch | hoch | unbekannt-mittel | mittel | **HOLD** als eigener Owner; im Process-Guide mitführen |
| n8n automatisierung | 110 | 16 | Aktueller Google-SERP: AI Overview + PAA + Reviews + Related Searches + Images + Videos; IONOS, n8n.io, BPC, Fabian Stegmaier, HCO, n8n-Agentur; Info/Tool/Commercial-Mix | `/ki-automatisierung-luebeck/` | hoch | hoch | mittel | hoch bei zusätzlicher n8n-Service-URL | **HOLD** standalone; keine city-spezifischen n8n-Seiten |

KI-Entscheidung: `KI-Prozessautomatisierung` ist ausreichend getrennt vom lokalen Commercial Owner, **wenn** der neue Asset als nationaler Decision-/Implementation-Guide gebaut wird und nicht als zweite Leistungsseite. `KI Automatisierung` selbst ist trotz hohen Volumens kein sinnvoller isolierter Headterm-Build: zu breit, KD54 und stark von Enterprise-/Definition-Authority besetzt.

## 2. SERP Features und Intent-Zusammenfassung

| Cluster | Local Pack | PAA | AI Overview | Images/Video | Directory/Pollution | Dominanter Page Type |
|---|---|---|---|---|---|---|
| Lübeck Software | ja | ja | im lokalisierten Snapshot nicht dominant | Video vorhanden | sehr starke Jobs/Studium + lokale Directories | lokale Service-Seiten + Jobs |
| Lübeck Web | stark | teilweise | nicht primärer lokaler Hebel | nicht dominant | einzelne Directories | exakte lokale Service-Seiten |
| Individualsoftware national | nein | stark | häufig | Images bei Beispiele | Wikipedia/Scholarly punktuell | Service + Decision/Comparison Guides |
| API/Schnittstellen | nein | stark | häufig | Video bei API Programmierung | wenig | Definitions-/Authority + Service-Mix |
| Relaunch | nein | stark | häufig | Images punktuell | gering | Authority Guides/Checklists |
| KI/Automation | nein | stark | sehr häufig | Video häufig | Kurse/Training punktuell | Definition/Enterprise + Decision Guides |
| n8n | nein | ja | ja | Images + Videos | Bücher/Tutorials punktuell | Tool, Guides, Examples, Services |

Featured Snippets waren in den ausgewerteten aktuellen Kern-Snapshots kein stabil dominierendes Feature. Bei den nationalen Informationsclustern haben AI Overview und PAA sichtbar die frühere Answer-Box-Rolle übernommen.

Die lokalen Provider-Snapshots lieferten Local-Pack-Namen, aber keine konsistent verifizierbaren Review-Counts für alle Anbieter. Deshalb werden keine Review-Zahlen erfunden oder aus uneinheitlichen Drittquellen zusammengerechnet.

## 3. Competitor Classification

### LOCAL DIRECT

- Web Lübeck: Augustin Marketing, Northbay Digital & Design, Popien Webdesign, Netzhirsch, foryumedia, Vicon, Jamp, HANSOLU, ISEO, Web Labels.
- Software Lübeck: RXM Solutions, EXORD, Software and Testing, Aikonetic; Local Pack enthält außerdem wechselnde lokale/regionale Anbieter.
- Kiel Web: Webagentur Kiel, secondlayer, Websiteandmore, Pixelwerft, Seiten-Werk, HGD Media, Augustin Marketing Kiel-Seite.
- Hamburg AI: KI-Helden, Next Strategy AI/Adence, Bluebatch, Ziya und weitere Hamburg-spezifische Anbieter.

### NATIONAL DIRECT

- Individualsoftware: Northcommit, EXWE, HEC, Bauer + Kirch, MaibornWolff, Lise, Sinovo.
- Schnittstellen/API: BEDM, Allbytes, PTC Solutions, Webfactory, Blueshoe.
- KI: Future AI Solutions, KI-Company, n8n-Agentur und weitere spezialisierte Automation-Anbieter.

### AUTHORITY / CONTENT

- KI: Salesforce, IBM, AWS, Oracle, Fraunhofer IAO, Haufe, d.velop, Informatica.
- API: Red Hat, Microsoft, SAP, Google Cloud, IBM.
- Relaunch: OMR, Sistrix, HubSpot, Evergreen, Suxeedo, Morefire.
- Individualsoftware: ERP.de, Operations1, Objektkultur, ISAX sowie Wikipedia bei Definitions-/Examples-Intent.

### DIRECTORY / PLATFORM

Feedbax, Sortlist, werbeagentur.de, Bark, Gelbe Seiten, Das Telefonbuch, Das Örtliche, ProvenExpert/OMR Reviews je nach Query und Funktion.

### IRRELEVANT SERP POLLUTION

StepStone, Indeed, Heise Jobs, Arbeitsagentur, LinkedIn Jobs, Meinestadt, Kimeta, Hochschul-/Studienseiten und einzelne Kurs-/Buchresultate, wenn die Query eigentlich einen Dienstleister sucht.

## 4. Page-Level Competitor Review

| Page | Stärken im Ranking/Conversion | Proof/Trust | Pricing/Process | Schema/Structure | Gap für DatenpflegeNord |
|---|---|---|---|---|---|
| Augustin Marketing — `/webdesign-luebeck/` | Exact-local Title/H1, sehr aggressive Conversion-CTAs, lokale Positionierung, viele Feature-Sektionen, FAQ | große Referenzgalerie, Testimonials, sichtbare Google-/ProvenExpert-Signale, lokale Standortsektion, zusätzliche Zertifizierungsclaims | kein pauschaler Preis im geprüften Ausschnitt; klare kostenlose Erstberatung | WebPage/Breadcrumb/WebSite/Organization; umfangreiche Entity-Daten | DPN ist technischer/präziser, hat aber sichtbar weniger externen Proof und keine vergleichbare Referenz-/Review-Dichte |
| RXM — `/software-entwicklung/software-entwicklung-luebeck/` | Exact-local Title, breite Software-/API-/KI-Abdeckung, FAQ, Projektstart-CTA | Kundenbewertungen und „Ausgewählte Projekte“ | Entwicklungsprozess in Schritten; Kosten werden nach Scope/Komplexität erklärt | FAQPage im HTML nachgewiesen | DPN besitzt die stärkere Make-or-Buy-/Scope-Decision-Logik, RXM zeigt mehr klassische Projekt-/Kunden-Proof-Elemente |
| Future AI Solutions — `/leistungen/prozessautomatisierung/` | Exact `KI Prozessautomatisierung` Title/H1, Nutzenargumentation, Prozessanalyse → Integration → Rollout, klare CTA | sichtbare Nutzen-/Produktivitätsclaims; im geprüften Ausschnitt keine gleich starke technische Fehler-/Freigabelogik | kostenloses Strategiegespräch; keine belastbare Preislogik im Ausschnitt | saubere H1/H2-Service-Struktur | DPN kann sich mit überprüfbaren Prozessgrenzen, Human-in-the-loop, Fehlerfällen, Rule-vs-KI-Matrix und technischen Beispielen differenzieren |
| Snutig — `/blogbeitrage/website-relaunch-checkliste-kosten/` | Ein URL-Asset bündelt Checkliste, Projektplan, Kosten, SEO, GEO, FAQ und Case Study | konkrete Case-Study-Struktur und externe Quellen | 12-Schritte-Prozess und konkrete Kostenrahmen | starke Content-Hierarchie; interne Links in Web/SEO-Cluster | Belegt, dass ein starker Relaunch-Guide mehrere Longtails gemeinsam besitzen kann; DPN sollte nicht in Kosten/SEO/Projektplan splitten |
| DPN current Relaunch guide | URL-Decision-Matrix, 36-Punkte-Checkliste, technische Release-/Canonical-/Postlaunch-Abnahme | authored/dated TechArticle, reproduzierbare technische Checks | keine Fake-Preise; noch keine explizite Kostenfaktoren-/Projektplan-Sektion | TechArticle/WebPage/Breadcrumb + Organization | Beste Differenzierung ist technische Abnahme + interaktive Checkliste; fehlend sind explizite Kostenfaktoren, Phasenplan und SEO-Migrations-Kurzantworten |

Keine Wettbewerberclaims werden übernommen. Prozent-, Preis-, Review- oder Zertifizierungsbehauptungen der Konkurrenz sind nur Musterbeobachtungen und keine Vorlage für DatenpflegeNord.

## 5. Unique-Value Gap

| Cluster | Was Ranking-Seiten häufiger liefern | Was DatenpflegeNord glaubwürdig besser/eigenständiger liefern kann |
|---|---|---|
| Local Web | Referenzen, Reviews, lokale Standort-/Team-Signale, aggressive Conversion | technischer Relaunch-/Release-Prozess, nachvollziehbare Abnahme, SEO-/Canonical-/Redirect-Kompetenz, Web↔API↔Software-Verknüpfung |
| Local Software | Projekte/Kundenlogos, breite Technologie-Listen, FAQ | Make-or-Buy-Matrix, Scope-Check, Fehler-/Betriebsfragen, API-Entscheidungslogik, keine erfundenen Festpreise |
| KI-Prozessautomatisierung | Definition, Benefits, generische Use Cases, teilweise starke Enterprise Authority | Decision Matrix „Regel/n8n/KI/Agent“, Human Approval, Fehlerpfade, Rechte/API-Grenzen, prüfbare Workflow-Beispiele und Diagramme |
| Individualsoftware | Beispiele/Case Studies und Vergleichsartikel | vorhandener interaktiver Scope-Check + Make-or-Buy; echte Beispiele erst ergänzen, wenn sie verifizierbar sind |
| Relaunch | Kostenrahmen, Projektplan, SEO-Guide, Cases | bereits bessere technische URL-/Release-Abnahme; durch Kostenfaktoren + Phasenplan + SEO-Kurzantworten zu einem vollständigen Decision Asset ausbauen |
| API/Schnittstellen | Definitionscontent und generische Best Practices | reale Integrationsplanung: Quelle/Ziel, Rechte, Limits, Retry/Deduplizierung, Fehlerbehandlung, Ownership; bestehender Software-Owner ist dafür ausreichend |
| n8n | Tutorials, Templates, Toolerklärung, Beispiele | Entscheidung, wann n8n genügt und wann Custom Code/KI sinnvoll ist; Betrieb, Fehler, Freigaben, APIs; keine Stadt-Doorways nötig |

## 6. Specific Page Decisions

### KI authority — `/wissen/ki-prozessautomatisierung/`

**Decision: BUILD**

Alle fünf Gates sind erfüllt:

- Distinct intent: national informational/decision vs lokaler Commercial Owner.
- Demand: 90 Vol. für `ki prozessautomatisierung`, zusätzliche 30 für `prozessautomatisierung ki` plus angrenzende Workflow-/Company-Queries.
- SERP separation: Process-spezifische Pages/Guides ranken; das Set unterscheidet sich sichtbar vom breiten `ki automatisierung`-SERP.
- Unique value: DPN besitzt bereits belastbare technische Differenzierung in Rule-vs-KI, n8n, APIs, Human Approval und Fehlerfällen; der Authority Asset kann diese als tiefen Entscheidungs-/Implementierungsrahmen ausarbeiten.
- Anti-cannibalization: der neue Guide bleibt national informational und verlinkt auf `/ki-automatisierung-luebeck/` als lokalen Commercial Owner. Keine zweite „KI Agentur Lübeck“-Leistungsseite.

Pflicht-Brief für Phase 7: Definition → Eignungscheck → Regel/n8n/KI/Agent-Vergleich → Beispielworkflow/Diagramm → Fehler-/Freigabematrix → Integrations-/Rechte-Check → Implementierungsphasen → klare Grenzen → CTA zum lokalen Commercial Owner. Keine generischen „KI spart X %“-Claims ohne eigene Evidenz.

**GSC REVISIT:** nach Indexierung Query-Separation und interne Kannibalisierung anhand First-Party-Daten prüfen.

### Individualsoftware second authority

- `Standardsoftware vs Individualsoftware`: **EXPAND** `/wissen/individualsoftware-kosten/`. Die vorhandene Make-or-Buy-Matrix ist bereits exakt der richtige Owner.
- `Individualsoftware Beispiele`: **HOLD** als standalone Asset. Der Examples-SERP ist eigenständig, aber ein generischer Beispiele-Artikel ohne echte/verifizierbare Beispiele würde keinen belastbaren Unique Value schaffen. Bestehenden Guide höchstens um klar als Entscheidungsszenarien bezeichnete, nicht als Kundenfälle ausgegebene Beispiele ergänzen.

**GSC REVISIT:** prüfen, ob der Kosten-Guide bereits Impressionen für Vergleichs-/Examples-Queries erhält, bevor ein späterer Split erwogen wird.

### Relaunch expansion

**Decision: EXPAND** `/wissen/website-relaunch-checkliste/`.

`website relaunch seo`, `website relaunch kosten`, `website relaunch projektplan` und `website relaunch checkliste` überlappen SERP-seitig stark. Snutig demonstriert aktuell sogar auf einer einzelnen URL, dass Checkliste + Kosten + SEO + Projektplan zusammen ranken können. DPN besitzt bereits den stärksten technischen Kern und sollte ergänzen:

- kompakte SEO-Migrations-Kurzantworten,
- explizite Projektphasen mit Verantwortlichkeiten/Abnahme,
- Kostenfaktoren statt erfundener Festpreise,
- „wann Relaunch, wann Modernisierung“-Decision,
- GSC/Postlaunch-Monitoring als First-Party-Gate, sobald verfügbar.

Keine separaten `/website-relaunch-kosten/`, `/website-relaunch-seo/` oder `/website-relaunch-projektplan/` Assets.

### Standalone API page

**Decision: HOLD**.

`api entwicklung` und vor allem `api programmierung` sind stark informationell und von Red Hat/Microsoft/SAP/IBM/Google/Wikipedia geprägt. Der existierende Software-Owner deckt API-Entwicklung, API-Programmierung, Webhooks, Datenaustausch, Limits, Rechte und Fehlerfälle bereits explizit ab. `schnittstellenentwicklung` ist kommerzieller, aber ebenfalls sauber im bestehenden Owner untergebracht.

### Generic Systemintegration page

**Decision: REJECT**.

Zu breit, geringe semantische Präzision und unnötige Überlappung mit Software/API/Automation. Ein neuer generischer Owner würde die vorhandene Architektur verschlechtern.

### City-specific n8n pages

**Decision: REJECT**.

Der belastbare nationale `n8n automatisierung`-SERP zeigt Tool-/Guide-/Service-Intent, aber keine Evidenz, die Stadt-Doorways rechtfertigt. Die vorhandene Lübeck-KI-Seite kann n8n kommerziell mitführen. Stadtmodifizierte n8n-Seiten hätten derzeit Doorway- und Thin-Content-Risiko.

## 7. Local Web / Software Gap

### Lübeck Web

Stärkste lokale SERP-Gegner: Augustin Marketing, Netzhirsch, Northbay, Popien, HANSOLU, Vicon, Jamp, foryumedia, Web Labels/ISEO je nach Query.

Was Google sichtbar belohnt:

- exakte lokale Leistungsrelevanz,
- Local Pack/Business Profile Präsenz,
- Referenzen/Case Studies,
- Review-/Trust-Signale,
- klarer lokaler Standort-/Marktbezug,
- kommerzielle CTA-Führung.

DPNs Copy-Fit ist inzwischen gut: `/webentwicklung-luebeck/` nennt im Title/H1 Webdesign + Webentwicklung, enthält `Website erstellen lassen`, Relaunch, Kostenfaktoren und Webagentur/Webdesigner-Sprache. Die nächste Lücke ist deshalb **nicht** eine zweite Lübeck-Landingpage, sondern verifizierbarer Proof und externe Authority.

### Lübeck Software

`softwareentwicklung lübeck` besitzt echten Local-Service-Intent, wird aber massiv durch Jobs/Studium verwässert. Local Pack sowie RXM/EXORD/Software and Testing zeigen die kommerzielle Chance. `softwareentwickler lübeck` ist noch stärker joblastig und sollte nur als unterstützende Semantik betrachtet werden, nicht als eigener Page Owner.

## 8. Regional Expansion

| Region candidate | Evidence | Doorway/Entity gate | Regional decision |
|---|---|---|---|
| Kiel Web | `webdesign kiel` 390/KD32, `webagentur kiel` 320, `webentwicklung kiel` 30; Exact-local Pages + Local Pack dominieren | echte Service-Area plausibel, aber einzigartige Kiel-Proof-/Content-Basis noch nicht belegt; keine Stadt-Kopie zulässig | **BUILD LATER** |
| Hamburg AI | `ki agentur hamburg` 70/KD12, `ki beratung hamburg` 70/KD9; Dedicated-local Pages + Directories + Local Pack | Service-Area/Entity-Wahrheit und Issue #13 machen aggressive Expansion aktuell zu riskant | **HOLD** |
| Schleswig-Holstein Web | `webdesigner schleswig-holstein` 170/KD27, `webdesign schleswig-holstein` 110/KD28; statewide Provider + Directories | eigener regionaler Nutzen gegenüber Lübeck/Kiel noch nicht ausreichend belegt | **HOLD** |

Kiel ist die stärkste spätere Regionalchance, aber nur mit eigener regionaler Substanz: tatsächlicher Service-Prozess, regional passende Proof-Elemente und eindeutige Differenzierung. Eine umbenannte Lübeck-Seite wäre **REJECT**.

**GSC REVISIT:** regionale Impressionen/Queries und reale Nachfrage aus Schleswig-Holstein/Kiel/Hamburg vor Veröffentlichung einbeziehen.

## 9. Backlink / Authority Gap

Aktueller SE-Ranking-Index:

| Domain | Referring domains | Relevanz |
|---|---:|---|
| datenpflege-nord.de | **0** | größter siteweiter Gap |
| software-and-testing.de | 37 | lokaler Software-Minimalbenchmark |
| exord.de | 127 | lokaler Software-Wettbewerber |
| northbayco.de | 135 | lokaler Web-Wettbewerber |
| augustin-marketing.de | 176 | lokaler Web-Wettbewerber; Backlinkzahl selbst stark sitewide/noisy |
| rxm.de | 248 | lokaler Software-Wettbewerber |
| iseo.de | 396 | lokaler Digital-/Softwareanbieter |
| netzhirsch.de | 460 | lokaler Web-Wettbewerber |
| vicon.de | 482 | lokaler Web-Wettbewerber |
| jamp.de | 590 | lokaler Web-Wettbewerber |
| more-fire.com | 1,340 | nationaler Relaunch/SEO-Authority-Wettbewerber |
| d-velop.de | 2,742 | nationaler KI-/Process-Authority-Wettbewerber |

Die Rohanzahl ist kein Qualitätsziel. Stichproben bei Wettbewerbern enthalten auch SEO-Müll, Rank-/Article-Farmen und sitewide Links. Diese Kategorien werden ausdrücklich ausgeschlossen.

Priorisierte, brand-safe Opportunity-Kategorien:

1. echte technische/open-source Proof-Quellen: GitHub-Projekte, Projektdokumentation, relevante Tool-/Vendor-Ökosysteme, sofern real und öffentlich belegbar;
2. redaktionelle Fachbeiträge/Interviews/Case-Referenzen, bei denen DPN tatsächlich technische Substanz liefert;
3. lokale Tech-/Hochschul-/Community-Verbindungen nur bei echter Beziehung oder Beitrag; EXORD zeigt z. B. hochwertige Uni-Lübeck-/DigitalOcean-Kategorien im Linkprofil;
4. seriöse Branchen-/Professional-Profile mit Referral-Potenzial;
5. lokale Business Citations erst nach sauberer Entity-Wahrheit und ohne Massenverzeichnis-Strategie.

Nicht zulässig: bezahlte Spamverzeichnisse, PBNs, irrelevante Bulk-Citations, Linktauschprogramme, gekaufte Article-Farm-Links.

Issue #13 begrenzt aggressive externe Entity-/Profilexpansion. Brand-safe Content-/Tech-Authority ist erlaubt.

## 10. AI Search / GEO

Die nationalen KI-, API-, Individualsoftware- und Relaunch-SERPs zeigen häufig Google AI Overview + PAA. Der aktuelle n8n-SERP zeigt zusätzlich, dass Google im AI-Modus sowohl die Originalquelle `n8n.io` als auch erklärende Guides, Praxisanbieter und Videos als Quellen zieht.

Extractability-Gaps für DPN:

- kurze Definition direkt unter H1/H2,
- echte Vergleichsmatrizen statt Marketingabsätze,
- nummerierte Implementierungs-/Entscheidungsschritte,
- klar beschriftete technische Beispiele,
- Failure-/Approval-Kriterien,
- Kostenfaktoren statt Scheingenauigkeit,
- sichtbare Autor-/Stand-Angaben und nachvollziehbare Aktualität,
- interne Links zwischen Commercial Owner und Authority Owner mit klarer Aufgabenverteilung.

Keine „AI-SEO“-Sonderfeatures erfinden. Die vorhandenen HTML-Inhalte, Tabellen, strukturierte Antworten, Autoren-/Stand-Signale und belegbaren technischen Details sind der Hebel.

## 11. PHASE 6 DECISION TABLE

| Cluster | Search volume | Difficulty | Intent | SERP type | Current owner | Competitor strength | Unique-value gap | Cannibalization risk | Business fit | Decision | Priority |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Lübeck Software Core | 110 + 110 | 34 / 15 | Local + Commercial, job-mixed | Local Pack + service + jobs | `/softwareentwicklung-luebeck/` | high | Proof/authority > copy | low if one owner | very high | **EXPAND** | P1 |
| Individualsoftware Commercial | 320 + 110 + 30 | 12 / 5 / 9 | Commercial/Decision | national service + AIO/PAA | `/softwareentwicklung-luebeck/` | medium-high | technical decision depth | high if split | very high | **EXPAND** | P1 |
| Standard vs Individual | 20 | 6 | Informational decision | comparison guides + AIO/PAA | `/wissen/individualsoftware-kosten/` | medium | matrix already exists | high if split | high | **EXPAND** | P2 |
| Individualsoftware Beispiele | 70 | 15 | Informational/examples | example pages + AIO/PAA/Images | cost guide is nearest owner | medium | verified examples/cases missing | medium | high | **HOLD** | P3 |
| API / Schnittstellen | 110 + 110 + 140 | 6 / 16 / 30 | Mixed Info/Commercial | AIO/PAA; authority + service | `/softwareentwicklung-luebeck/#schnittstellen` | high | practical integration/error model | high | high | **EXPAND** | P2 |
| Standalone API page | same cluster | same | mixed | authority-heavy | none needed | high | insufficient URL-level separation | very high | medium-high | **HOLD** | P3 |
| Lübeck Web Commercial | 390 + 320 + 40 + 10 | 55 / 55 / 52 / 45 | Local + Commercial | exact-local pages + Local Pack | `/webentwicklung-luebeck/` | very high | external proof/local authority | very high if split | very high | **EXPAND** | P1 |
| Relaunch Authority | 250 + 140 + 50 + 30 + 20 | 16 / 14 / 8 / 9 / 7 | Informational/Decision | AIO/PAA + guides/checklists | `/wissen/website-relaunch-checkliste/` | high | costs + phase plan + concise SEO layer | high if split | high | **EXPAND** | P1 |
| KI-Prozessautomatisierung Authority | 90 + 30 supporting | 26 / 7 | Informational/Decision | AIO/PAA; process guides + service | new supporting authority owner | medium-high | decision matrix + technical controls | medium, manageable | very high | **BUILD** | P1 |
| Broad KI Automation Headterms | 920 + 260 | 54 / 42 | broad informational | AIO/PAA/video; enterprise authority | `/ki-automatisierung-luebeck/` commercial only | very high | no reason to clone definitions | high | high | **HOLD** | P3 |
| n8n Automation standalone | 110 | 16 | Info/Tool/Commercial | AIO/PAA/video/images/guides/services | `/ki-automatisierung-luebeck/` | medium-high | decision/ops angle available | high | high | **HOLD** | P2 |
| City-specific n8n | no reliable city volume | n/a | unproven local | no local evidence proving doorway need | current KI owner | n/a | no unique city value | very high | medium | **REJECT** | P4 |
| Kiel Web | 390 + 320 + 30 | 32 / 0* / 20 | Local + Commercial | exact-local pages + Local Pack | none | high | unique Kiel proof required | high | high | **HOLD** | P2 deferred |
| Schleswig-Holstein Web | 170 + 110 | 27 / 28 | Regional + Commercial | statewide providers + Local Pack/directories | Lübeck owner only indirectly | medium | unique regional proposition missing | medium-high | high | **HOLD** | P3 |
| Hamburg AI | 70 + 70 | 12 / 9 | Local + Commercial | exact-local pages + directories + Local Pack | none | medium-high | service-area/entity proof missing | high | high | **HOLD** | P3 |
| Generic Systemintegration | not prioritized | n/a | broad/ambiguous | overlaps software/integration | software owner already | mixed | no unique owner role | very high | medium | **REJECT** | P4 |

`*` KD0 for `webagentur kiel` is a provider metric and must not be interpreted as “no competition”; the actual SERP visibly contains strong local competitors.

## 12. Priority Model

Positive factors were scored 1–5 and multiplied as required: Business Fit × Intent Strength × SERP Opportunity × Unique Value × Conversion Potential. Cannibalization, Authority Requirement, Entity Risk and Maintenance Burden are then applied as penalties. The index is comparative, not a traffic forecast.

| Opportunity | Positive product | Main penalties | Relative priority |
|---|---:|---|---:|
| brand-safe referring-domain / authority acquisition | 3125 | authority effort, maintenance | 1 |
| BUILD KI-Prozessautomatisierung authority | 1600 | authority requirement, moderate cannibalization control | 2 |
| EXPAND Relaunch authority owner | 960 | national authority competition | 3 |
| EXPAND Individualsoftware decision owner | 960 | authority requirement | 4 |
| EXPAND Lübeck Web owner | 1125 | very high local authority/proof requirement | 5 |
| Kiel Web future page | 640 | local proof, doorway/entity risk | deferred |
| Schleswig-Holstein Web | 480 | regional uniqueness + authority | deferred |
| Hamburg AI | 480 | entity/service-area risk + authority | deferred |

Der niedrigere Rang des Lübeck-Web-Copy-Ausbaus trotz hoher Nachfrage ist bewusst: Der bestehende Owner trifft die Suchsprache bereits gut. Die aktuelle Lücke liegt stärker bei externem Proof/Authority als bei noch mehr Text.

## 13. Phase 7 Recommendation

### Top 3 immediate visibility actions

1. **Authority gap schließen:** brand-safe Referring Domains für bestehende Commercial-/Authority-Assets aufbauen. Fokus auf echte Tech-/Open-Source-/Editorial-/Community-Proof-Quellen. Keine aggressive Entity-Profilexpansion solange Issue #13 offen ist.
2. **BUILD `/wissen/ki-prozessautomatisierung/`:** nationaler Decision-/Implementation-Guide mit harter Rollentrennung zur lokalen Commercial KI-Seite.
3. **EXPAND `/wissen/website-relaunch-checkliste/`:** SEO-Migration, Projektplan und Kostenfaktoren in denselben starken Owner integrieren; keine drei Thin Guides erzeugen.

### Top 3 deferred actions

1. **Kiel Web — BUILD LATER:** erst nach Service-Area-/Unique-Content-/Proof-Gate und GSC-Abgleich; keine Lübeck-Kopie.
2. **Individualsoftware authority — EXPAND LATER:** Standard-vs-Individual vertiefen; standalone `Individualsoftware Beispiele` erst bei verifizierbarem Beispiel-/Case-Material neu bewerten.
3. **Hamburg AI / Schleswig-Holstein Web — HOLD:** Service-Area, Entity-Wahrheit, GSC und regionale Differenzierung zuerst belegen.

## 14. GSC-dependent Decisions

Nach GSC-Anschluss erneut prüfen:

- ob `/ki-automatisierung-luebeck/` bereits national für Process-Queries Impressionen erzeugt und wie stark der neue KI-Guide kannibalisieren könnte;
- ob `/wissen/individualsoftware-kosten/` bereits `standardsoftware vs individualsoftware` / `individualsoftware beispiele` besitzt;
- welche Relaunch-Longtails der bestehende Guide bereits abdeckt und welche Expansion die höchste Impression-to-click-Chance hat;
- welche Lübeck-Webbegriffe bereits Impressionen auf `/webentwicklung-luebeck/` bündeln;
- ob regionale Query-Signale aus Kiel, Schleswig-Holstein oder Hamburg real vorhanden sind;
- Indexierungs-/CTR-Entwicklung der Phase-5-Authority-Seiten vor weiteren URL-Splits.

GSC ist ein Revisit-Gate, aber kein Grund, vorhandene SERP-Evidenz zu ignorieren. Es bleibt die wichtigste fehlende First-Party-Schicht.

## Final Status

**No new production pages created**

**No production deployment performed**

**No merge to main performed**

**Issue #13 remains OPEN**

**Issue #10/#15 remain parked**
