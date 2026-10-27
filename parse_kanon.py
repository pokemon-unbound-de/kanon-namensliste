#!/usr/bin/env python3
"""Kanon-Namensliste: offizielle deutsche + englische Namen für
Pokémon, Attacken, Fähigkeiten und Items (Hauptspiele, Gen 1–9 +
aktuelle Gen-10-Zusätze).

Quellen (je Zeile in der CSV verlinkt; Snapshots unter cache/):
- Pokémon:   PokéWiki "Pokémon-Liste"
             https://www.pokewiki.de/Pok%C3%A9mon-Liste
- Attacken:  Bulbapedia "List of moves in other languages" (EN + DE,
             Main + Z-Moves + G-Max), DE der Main-Liste cross-checked
             gegen PokéWiki "Attacken-Liste"
             https://bulbapedia.bulbagarden.net/wiki/List_of_moves_in_other_languages
             https://www.pokewiki.de/Attacken-Liste
- Fähigkeiten: PokéWiki "Fähigkeiten-Liste" (self-contained, DE + EN)
             https://www.pokewiki.de/F%C3%A4higkeiten-Liste
- Items:     Bulbapedia "List of items in other languages" (EN + DE)
             https://bulbapedia.bulbagarden.net/wiki/List_of_items_in_other_languages

Ausgabe: kanon_namen.csv  Spalten: typ;en;de;quelle
(typ = pokémon | attacke | fähigkeit | item)

Spin-off-Attacken (Mystery Dungeon / Shadow) sind NICHT enthalten —
Basis sind die Hauptspiele. Namen sind keine Spieltexte → öffentlich.

Wiedervorgang:  python3 parse_kanon.py   (deterministisch, ohne Netz)
"""
import csv
import html as htmllib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache"

BP_BASE = "https://bulbapedia.bulbagarden.net/wiki/"
PW_BASE = "https://www.pokewiki.de/"

CJK_RE = re.compile(r"[\u3000-\u9fff\uf900-\ufaff\U00020000-\U0003ffff]")
TAG_RE = re.compile(r"<[^>]+>")
TD_RE = re.compile(r"<td([^>]*)>(.*?)</td>", re.S)
H3_RE = re.compile(
    r'<h3><span class="mw-headline" id="([^"]+)">.*?</span></h3>')
EN_LINK_RE = re.compile(r'<a href="/wiki/([^"?]+)"[^>]*>(.*?)</a>', re.S)


def has_cjk(s: str) -> bool:
    return bool(CJK_RE.search(s))


def read(path) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def wikitext_of(name: str) -> str:
    with open(CACHE / name, encoding="utf-8") as fh:
        return json.load(fh)["parse"]["wikitext"]["*"]


def clean_cell(raw: str) -> str:
    """HTML-Zelle -> Text (Tags weg, Entities, Trim, Renaming-Asterisk)."""
    txt = TAG_RE.sub("", raw)
    txt = htmllib.unescape(txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    # Renaming-Anmerkung: "Klaps*" -> "Klaps"
    txt = txt.rstrip("*").strip()
    return txt


# --------------------------------------------------------------------------
# Bulbapedia-HTML-Tabellen (robust: Zellen per <td>, DE via lang="de")
# --------------------------------------------------------------------------

def parse_bp_tables(html: str) -> list[tuple[str, list[dict]]]:
    """Alle roundy-Tabelle als (section, rows). section = letzte h3-
    Headline vor der Tabelle ("" vor der ersten)."""
    headings = [(m.start(), m.group(1)) for m in H3_RE.finditer(html)]
    tables = []
    for m in re.finditer(r'<table class="roundy sortable"', html):
        end = html.find("</table>", m.start())
        if end < 0:
            continue
        body = html[m.start():end]
        section = ""
        for pos, hid in headings:
            if pos < m.start():
                section = hid
        tables.append((section, body))

    out = []
    for section, body in tables:
        rows = []
        for tr in re.finditer(r"<tr[^>]*>(.*?)</tr>", body, re.S):
            cells = TD_RE.findall(tr.group(1))
            if len(cells) < 8:
                continue  # Kopfzeile (th) oder Kurzzeile
            # EN-Zelle: erste Zelle mit Artikel-Link (keine File:-Links)
            en_title = en_text = ""
            de_text = ""
            for attrs, raw in cells:
                if "lang=" in attrs and 'lang="de"' in attrs:
                    de_text = clean_cell(raw)
                if not en_title:
                    for lm in EN_LINK_RE.finditer(raw):
                        title = lm.group(1)
                        if title.startswith("File:"):
                            continue
                        en_title = title
                        en_text = clean_cell(lm.group(2))
                        break
            rows.append({"en_title": en_title, "en": en_text,
                         "de": de_text, "index": clean_cell(cells[0][1])})
        out.append((section, rows))
    return out


def main_rows_of(tables) -> list[dict]:
    """Main-Tabelle = erste Tabelle der Seite."""
    return tables[0][1] if tables else []


# --------------------------------------------------------------------------
# PokéWiki (wikitext)
# --------------------------------------------------------------------------

def parse_pokedex() -> list[dict]:
    wt = wikitext_of("pokedex.json")
    start = wt.find("{|")
    end = wt.find("|}", start)
    table = wt[start:end]
    rows = []
    for row in table.split("|-")[1:]:
        fields = [f.strip() for f in row.split("||")]
        if len(fields) < 9:
            continue
        m = re.search(r"(\d{4})", fields[0])
        if not m:
            continue  # Mystery-Pokémon ohne Nummer (Braubel)
        de_link = re.search(r"\[\[([^\]|]+)", fields[2])
        if not de_link:
            print(f"! Pokémon Nr {m.group(1)}: kein DE-Link: {fields[2]!r}",
                  file=sys.stderr)
            continue
        en = fields[3].strip()
        rows.append({"num": int(m.group(1)), "de": de_link.group(1).strip(),
                     "link": de_link.group(1).strip(), "en": en})
    return rows


def parse_attacken() -> dict[str, dict]:
    """PokéWiki Attacken-Liste: Zeilen starten mit '||' -> Index in
    fields[1], Link in fields[2]. Z-Move-Zeilen (622, 624, ...) tragen
    den Namen mit rowspan='2'; die zweite Zeile (623, 625, ...) enthält
    nur ein Typ-Icon und wird übersprungen."""
    wt = wikitext_of("page_Attacken-Liste.json")
    start = wt.find("{|")
    end = wt.find("|}", start)
    table = wt[start:end]
    out: dict[str, dict] = {}
    for row in table.split("|-")[1:]:
        fields = [f.strip() for f in row.split("||")]
        if len(fields) < 3:
            continue
        m = re.fullmatch(r"\d{1,3}", fields[1])
        if not m:
            continue
        de_link = re.search(r"\[\[([^\]|]+)", fields[2])
        if not de_link:
            continue  # rowspan-Zweiteile der Z-Move-Zeilen
        out[m.group(0)] = {"de": de_link.group(1).strip(),
                           "link": de_link.group(1).strip()}
    return out


def parse_fähigkeiten() -> list[dict]:
    """PokéWiki Fähigkeiten-Liste: self-contained (DE + EN + Link).
    Die Nummerierung hat Lücken (267, 302–304, 314, 317); 313 Einträge
    bis Index 319."""
    wt = wikitext_of("page_Fähigkeiten-Liste.json")
    out = []
    for row in re.split(r"\|-(?:style=[^\n]*)?", wt):
        fields = [f.strip() for f in row.split("||")]
        if len(fields) < 3:
            continue
        m = re.search(r"(\d{3})", fields[0])
        if not m:
            continue
        de_link = re.search(r"\[\[([^\]|]+)", fields[1])
        if not de_link:
            print(f"! Fähigkeit {fields[0]}: kein Link: {fields[1]!r}",
                  file=sys.stderr)
            continue
        de = de_link.group(1).strip()
        # Disambiguierungs-Suffix im Artikel-Titel (z. B. "Sandsturm
        # (Fähigkeit)" gegen die Attacke "Sandsturm") aus dem Namen
        # streichen; der Link/URL behält ihn (zeigt auf den Artikel).
        de = re.sub(r"\s*\(Fähigkeit\)$", "", de)
        out.append({"num": int(m.group(1)), "de": de,
                    "en": fields[2].strip(),
                    "link": de_link.group(1).strip()})
    return out


# --------------------------------------------------------------------------
# Merge + Ausgabe
# --------------------------------------------------------------------------

def main() -> int:
    pokedex = parse_pokedex()
    attacken = parse_attacken()
    faehigkeiten = parse_fähigkeiten()

    moves_tables = parse_bp_tables(read(CACHE / "bp_moves.html"))
    items_tables = parse_bp_tables(read(CACHE / "bp_items.html"))
    bp_moves_main = main_rows_of(moves_tables)
    bp_zmoves = [r for s, rows in moves_tables if s == "Z-Moves" for r in rows]
    bp_gmax = [r for s, rows in moves_tables if s == "G-Max_Moves" for r in rows]
    bp_items = [r for _s, rows in items_tables for r in rows]

    rows: list[list[str]] = []
    problems: list[str] = []
    stats = Counter()

    # -- Pokémon (PokéWiki: DE + EN + Link)
    for p in pokedex:
        rows.append(["pokémon", p["en"], p["de"],
                     PW_BASE + quote(p["link"], safe="")])
    stats["pokémon"] = len(rows)

    # -- Attacken Main (Bulbapedia-Index ↔ PokéWiki-Index)
    pw_num = {int(k): v for k, v in attacken.items()}
    for r in bp_moves_main:
        if not r["index"].isdigit() or not r["en"]:
            problems.append(f"attacke main: unklare Zeile: {r!r}")
            continue
        num = int(r["index"])
        stats["attacke"] += 1
        if not r["de"] or r["de"] == "—":
            problems.append(f"attacke {num} ({r['en']}): kein DE-Name in Bulbapedia")
            continue
        pw = pw_num.get(num)
        if pw:
            url = PW_BASE + quote(pw["link"], safe="")
            de = pw["de"]
            if pw["de"].rstrip("*") != r["de"]:
                problems.append(f"attacke {num}: DE-Abweichung "
                                f"(PokéWiki {pw['de']!r} vs. "
                                f"Bulbapedia {r['de']!r})")
        else:
            # neuere Attacke ohne PokéWiki-Artikel -> Bulbapedia als Quelle
            url = BP_BASE + quote(r["en_title"], safe="")
            de = r["de"]
        if has_cjk(de):
            problems.append(f"attacke {num}: CJK in DE {de!r}")
            continue
        rows.append(["attacke", r["en"], de, url])

    # -- Attacken Z-Moves (PokéWiki 622/624/... via Bulbapedia-Index "X/Y")
    for r in bp_zmoves:
        key = r["index"].split("/")[0].strip()
        if not key.isdigit() or not r["en"]:
            problems.append(f"z-move: unklarer Index: {r!r}")
            continue
        if not r["de"] or has_cjk(r["de"]):
            problems.append(f"z-move {key} ({r['en']}): kein DE in Bulbapedia")
            continue
        stats["attacke_zg"] += 1
        pw = attacken.get(key)
        if pw:
            de = pw["de"]
            url = PW_BASE + quote(pw["link"], safe="")
            if de != r["de"]:
                problems.append(f"z-move {key}: DE-Abweichung "
                                f"(PokéWiki {de!r} vs. Bulbapedia {r['de']!r})")
        else:
            de = r["de"]
            url = BP_BASE + quote(r["en_title"], safe="")
        rows.append(["attacke", r["en"], de, url])

    # -- Attacken G-Max (nur Bulbapedia, Indexe sind '???')
    for r in bp_gmax:
        if not r["en"] or not r["de"] or has_cjk(r["de"]):
            problems.append(f"g-max: übersprungen: {r!r}")
            continue
        stats["attacke_zg"] += 1
        rows.append(["attacke", r["en"], r["de"],
                     BP_BASE + quote(r["en_title"], safe="")])

    # -- Fähigkeiten (PokéWiki, self-contained)
    for f in faehigkeiten:
        if not f["en"] or has_cjk(f["de"]):
            problems.append(f"fähigkeit {f['num']} ({f['de']}): ungültig")
            continue
        rows.append(["fähigkeit", f["en"], f["de"],
                     PW_BASE + quote(f["link"], safe="")])
    stats["fähigkeit"] = len(faehigkeiten)

    # -- Items (Bulbapedia: EN + DE + Link)
    seen_en: set[str] = set()
    for r in bp_items:
        if not r["en"] or not r["de"] or r["de"] == "—":
            if r["en"]:
                stats["items_gekippt"] += 1
            continue
        if r["en"] in seen_en:
            problems.append(f"item: doppelte EN-Zeile {r['en']!r}")
            continue
        if has_cjk(r["en"]) or has_cjk(r["de"]):
            problems.append(f"item: CJK in {r['en']!r}/{r['de']!r}")
            continue
        seen_en.add(r["en"])
        rows.append(["item", r["en"], r["de"],
                     BP_BASE + quote(r["en_title"], safe="")])
    stats["item"] = len(seen_en)

    rows.sort(key=lambda r: (r[0], r[2].casefold(), r[1].casefold()))
    out_csv = ROOT / "kanon_namen.csv"
    with open(out_csv, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        w.writerow(["typ", "en", "de", "quelle"])
        w.writerows(rows)

    # -- Report
    counts: Counter = Counter(r[0] for r in rows)
    print(f"→ {out_csv}")
    print(f"  Zeilen: {len(rows)} | " +
          " | ".join(f"{k}: {v}" for k, v in sorted(counts.items())))
    print(f"  (Attacken davon Z-Moves/G-Max: {stats['attacke_zg']}, "
          f"Items ohne DE/ungültig: {stats['items_gekippt']})")

    de_map: dict[tuple[str, str], list[str]] = defaultdict(list)
    for r in rows:
        de_map[(r[0], r[2].casefold())].append(r[1])
    dups = {k: sorted(set(v)) for k, v in de_map.items() if len(set(v)) > 1}
    print(f"  DE-Namen mit >1 EN (gleicher Typ): {len(dups)}")
    for k, v in sorted(dups.items()):
        print(f"    {k[0]}: {k[1]!r} -> {v}")

    print(f"  Probleme: {len(problems)}")
    for p in problems[:30]:
        print(f"    {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
