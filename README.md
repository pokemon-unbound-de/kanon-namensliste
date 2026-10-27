# Kanon-Namensliste (offizielle DE/EN-Namen, Gen 1–9)

Offizielle deutsche und englische Namen für **Pokémon, Attacken,
Fähigkeiten und Items** der Hauptspiel-Generationen 1–9 inkl. aktueller
Zusätze (Stand 2026-10-27). Auftrag: [pokemon-unbound-de#39](https://github.com/pokemon-unbound-de/pokemon-unbound-de/issues/39).

Namen sind **keine Spieltexte** → die Liste darf öffentlich sein.

## Format

`kanon_namen.csv`, getrennt durch `;`, sortiert nach `typ`, dann `de`:

| Spalte | Bedeutung |
|---|---|
| `typ` | Zeilentyp: `pokémon` \| `attacke` \| `fähigkeit` \| `item` (kein Pokémon-Typ) |
| `en` | offizieller englischer Name |
| `de` | offizieller deutscher Name |
| `quelle` | Artikel-URL der Quelle für diese Zeile |

## Umfang (3.273 Zeilen)

| typ | Anzahl | Quelle |
|---|---|---|
| `pokémon` | 1.025 | PokéWiki „Pokémon-Liste" (Nationaler Pokédex bis #1025; „Braubel" ohne Nummer ausgelassen) |
| `attacke` | 930 | Bulbapedia „List of moves in other languages" (862 Main-Attacken, Indizes 1–920) + 35 Z-Moves + 33 G-Max-Moves; DE der Main-Liste cross-checked gegen PokéWiki „Attacken-Liste" (Quelle dort dann PokéWiki-Artikel) |
| `fähigkeit` | 313 | PokéWiki „Fähigkeiten-Liste" (self-contained, DE + EN; Nummerierung mit Lücken, bis Index 319) |
| `item` | 1.005 | Bulbapedia „List of items in other languages" (alle Hauptspiel-Items, inkl. neuerer Generationen) |

**Nicht enthalten:** Spin-off-Attacken (Mystery-Dungeon-/Shadow-Moves) —
die Basis sind die Hauptspiele. Z-Moves und G-Max-Moves sind enthalten,
da sie in Hauptspielen vorkommen.

## Quellen (Snapshot 2026-10-27)

- [PokéWiki: Pokémon-Liste](https://www.pokewiki.de/Pok%C3%A9mon-Liste) (wikitext via API)
- [PokéWiki: Attacken-Liste](https://www.pokewiki.de/Attacken-Liste) (wikitext via API)
- [PokéWiki: Fähigkeiten-Liste](https://www.pokewiki.de/F%C3%A4higkeiten-Liste) (wikitext via API)
- [Bulbapedia: List of moves in other languages](https://bulbapedia.bulbagarden.net/wiki/List_of_moves_in_other_languages) (HTML)
- [Bulbapedia: List of items in other languages](https://bulbapedia.bulbagarden.net/wiki/List_of_items_in_other_languages) (HTML)

Die genutzten Seitensnapshots liegen unter [`cache/`](cache/)
(`*.json` = PokéWiki-wikitext, `bp_*.html` = Bulbapedia-HTML).

## Bekannte Besonderheiten

- **3 DE-Namen mit zwei EN-Items** (offiziell identisch benannt, beide
  Zeilen behalten): `angel` (Fishing Rod, Old Rod), `fundsache`
  (Dropped Item, Lost Item), `steintafel` (Small Tablet, Stone Plate).
- **2 DE-Abweichungen Bulbapedia vs. PokéWiki** (Attacken 738/745):
  „Sprießomben" vs. „Sprießbomben", „Präzisionsschuss" vs.
  „Präisionsschuss" (Tippfehler). Geliefert wird der PokéWiki-Name
  (deutsche Enzyklopädie, maßgeblich für DE).
- 4 Items stehen auf der Bulbapedia-Seite doppelt (z. B. Card Key in
  zwei Sektionen) → dedupliziert. 1 Platzhalter-Zeile (`???`/`—`)
  ausgelassen.
- Renaming-Marker (`*` für alte Namen) werden gestrichen; es gilt der
  aktuelle offizielle Name.
- **Offizielle Namens-Kollisionen Attacke/Fähigkeit** (gleicher
  DE-Name für zwei offizielle Namen, `typ` unterscheidet):
  `Kraftkoloss` (Superpower / Huge Power), `Sandsturm` (Sandstorm /
  Sand Stream), `Schnüffler` (Odor Sleuth / Frisk). Die
  PokéWiki-Artikel der Fähigkeiten tragen den Titel-Suffix
  „(Fähigkeit)" (Disambiguierung) — dieser wurde aus der `de`-Spalte
  gestrichen, die `quelle`-URL verlinkt weiterhin den Artikel.

## Lizenz

Namen und Daten stammen von **PokéWiki** (pokewiki.de) und
**Bulbapedia** (bulbapedia.bulbagarden.net) und unterliegen
**CC BY-NC-SA 4.0** (PokéWiki: [Lizenzhinweis](https://www.pokewiki.de/Pok%C3%A9Wiki:Urheberrecht),
Bulbapedia: [Lizenz](https://bulbapedia.bulbagarden.net/wiki/Bulbapedia:Copyrights)):
Namensnutzung nur nicht-kommerziell, Weitergabe unter gleicher Lizenz,
Angabe der Quelle. Diese Liste und ihre Snapshots unter `cache/` sind
dementsprechend **CC BY-NC-SA 4.0**; die `quelle`-Spalte gibt die
genutzten Artikel an.

## Reproduktion

```
python3 parse_kanon.py
```

Deterministisch, offline (nur `cache/`), Python 3.9+ ohne Zusatzpakete.
Erstellt `kanon_namen.csv` neu und gibt Count-Report, DE-Duplikate und
Quell-Abweichungen aus. Bei Quellen-Update: Snapshots in `cache/`
ersetzen (URLs oben), dann neu ausführen.
