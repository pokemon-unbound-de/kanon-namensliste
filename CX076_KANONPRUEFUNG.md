# CX076 – elf angefragte Namen, 03.11.2026

Vier aktuelle Itemnamen korrigiert; vier Fähigkeiten sind bereits unter ihrem
Gen-IX-Namen korrekt; drei weitere Namen waren unverändert richtig.
Alle3273 Identitäten bleiben erhalten. Kein ROM, keine Slotentscheidung.

## Einzelergebnis

| EN | Vor diesem Nachtrag | Ergebnis | Gelesener Namensbeleg |
|---|---|---|---|
| Brine | Lake | unverändert | [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Brine_(move)#In_other_languages) |
| Lunge | Anfallen | unverändert | [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Lunge_(move)#In_other_languages) |
| Twisted Spoon | Krümmlöffel | aktuell Krummlöffel abIV; historische FormII–III separat erhalten | [Bulbapedia, Revision4636355](https://bulbapedia.bulbagarden.net/w/index.php?title=Twisted_Spoon&oldid=4636355) |
| Mega Bracelet | Mega-Armreife | Grundname Mega-Armreif; keine historische Umbenennung behauptet | [Bulbapedia, Revision4551311](https://bulbapedia.bulbagarden.net/w/index.php?title=Mega_Bracelet&oldid=4551311) |
| Wacan Berry | Kerzalberre | Kerzalbeere; Schreibfehler nicht als Alias aufnehmen | [Bulbapedia, Revision4635181](https://bulbapedia.bulbagarden.net/w/index.php?title=Wacan_Berry&oldid=4635181) |
| Lagging Tail | Schwerschwf. | aktuell Schwerschweif abVII; historische FormIV–VI separat | [Bulbapedia, Revision4590199](https://bulbapedia.bulbagarden.net/w/index.php?title=Lagging_Tail&oldid=4590199) |
| Own Tempo | Gleichmut | aktuell unverändert; Tempomacher ist die FormIII–VIII | [Bulbapedia, Revision4534274](https://bulbapedia.bulbagarden.net/w/index.php?title=Own_Tempo_(Ability)&oldid=4534274) |
| Poison Heal | Giftheilung | aktuell unverändert; Aufheber ist die FormIV–VIII | [Bulbapedia, Revision4547772](https://bulbapedia.bulbagarden.net/w/index.php?title=Poison_Heal_(Ability)&oldid=4547772) |
| Tangled Feet | Taumelschritt | aktuell unverändert; Fußangel ist die FormIV–VIII | [Bulbapedia, Revision4634073](https://bulbapedia.bulbagarden.net/w/index.php?title=Tangled_Feet_(Ability)&oldid=4634073) |
| Symbiosis | Symbiose | aktuell unverändert; Nutznießer historischVI–VIII, Quellenunterschied unten | [Bisafans: Gen-IX-Umbenennungen](https://www.bisafans.de/spiele/editionen/karmesin-purpur/aenderungen.php) |
| Mime Jr. | Pantimimi | unverändert | [Bulbapedia](https://bulbapedia.bulbagarden.net/wiki/Mime_Jr._(Pok%C3%A9mon)#In_other_languages) |

## Quellenlimit und wichtiger Unterschied bei Symbiosis

Alle elf angefragten PokéWiki-Einleitungsseiten wurden erneut versucht und
antworteten HTTP403. **Null gelesene PokéWiki-Einleitungssätze**, kein erfundener
Wortlaut und keine vorgetäuschte formale Erfüllung dieses Abnahmekriteriums.
Die obigen Einzelseiten/Sprachtabellen wurden als Alternativbelege gelesen.

Die gelesene Bulbapedia-Sprachtabelle zu Symbiosis nennt nur Nutznießer ohne
Generationsmarkierung. Das ist kein Beleg gegen einen neueren Namen:
Der vorhandene PokéWiki-Fähigkeitenlisten-Snapshot führt Symbiose für EN
Symbiosis; die zusätzlich gelesene deutsche Gen-IX-Änderungsliste von Bisafans
belegt die Umbenennung ausdrücklich und ebenso die drei anderen Fähigkeiten.
Deshalb wird Symbiose nicht zu Nutznießer zurückgesetzt. Der alte Name bleibt
mit Generationenbereich erhalten. Kein Quellenmehrheitsentscheid und kein
Französisch-/Deutsch-Tausch aus bloßer Namensgleichheit.

Die Quellenbefunde ersetzen weder die gewünschte Einleitungssatz-Abnahme
durch Nevio/I3 noch den Test, welcher offizielle Name in einen konkreten
ROM-Slot passt. Die Projektregel bleibt: neuester passender offizieller Name,
sonst passende ältere offizielle Form; keine automatische ROM-Umbenennung.

## Umsetzung und Prüfung

`generation_names.json` ergänzt sechs belegte zeitliche Namenspaare; zusammen
mit den drei vorhandenen Paaren stehen neun historische Aliase separat.
`name_corrections.json` korrigiert zwei konkrete Quellschreibungen ohne
Aliasbehauptung. Der Offlinegenerator wendet beides identitätsgenau an und
bricht bei fehlenden/doppelten Identitäten oder unbekannter Schreibweise ab.
Ein erneuter Generatorlauf kann die vier Korrekturen nicht wieder verlieren.

Acht Tests prüfen u.a. alle elf aktuellen Namen, Alias-/Tippfehlertrennung,
Idempotenz, unbekannte Quellformen und unveränderte fremde Identitäten.
CSV-Zeilenenden bleiben wie bisher CRLF; die Änderung führt keinen neuen
Zeilenendenstil ein. Eigene QA, keine unabhängige Abnahme oder Liveintegration.
