import copy
import csv
import json
from pathlib import Path
import unittest

from parse_kanon import apply_name_corrections


class CorrectionTests(unittest.TestCase):
    def setUp(self):
        self.rules = json.loads(Path('name_corrections.json').read_text())
        self.rows = [['item', 'Wacan Berry', 'Kerzalberre', 'old'],
                     ['item', 'Mega Bracelet', 'Mega-Armreife', 'old'],
                     ['item', 'Unrelated', 'Mega-Armreife', 'unrelated']]

    def test_exact_identity_idempotence_and_no_input_mutation(self):
        before = copy.deepcopy(self.rows)
        result = apply_name_corrections(self.rows, self.rules)
        self.assertEqual(self.rows, before)
        self.assertEqual(result[0][2], 'Kerzalbeere')
        self.assertEqual(result[1][2], 'Mega-Armreif')
        self.assertEqual(result[2], self.rows[2])
        self.assertEqual(apply_name_corrections(result, self.rules), result)

    def test_missing_duplicate_and_unexpected_sources_rejected(self):
        for rows in [self.rows[1:], self.rows + [self.rows[0]],
                     [['item', 'Wacan Berry', 'unreviewed', 'old']] + self.rows[1:]]:
            with self.assertRaises(ValueError):
                apply_name_corrections(rows, self.rules)
        with self.assertRaises(ValueError):
            apply_name_corrections(self.rows, self.rules + [self.rules[0]])

    def test_eleven_reviewed_current_names_and_historical_aliases(self):
        with Path('kanon_namen.csv').open(newline='') as f:
            rows = {(r['typ'], r['en']): r['de'] for r in csv.DictReader(f, delimiter=';')}
        expected = [('attacke', 'Brine', 'Lake'), ('attacke', 'Lunge', 'Anfallen'),
                    ('item', 'Twisted Spoon', 'Krummlöffel'),
                    ('item', 'Mega Bracelet', 'Mega-Armreif'),
                    ('item', 'Wacan Berry', 'Kerzalbeere'),
                    ('item', 'Lagging Tail', 'Schwerschweif'),
                    ('fähigkeit', 'Own Tempo', 'Gleichmut'),
                    ('fähigkeit', 'Poison Heal', 'Giftheilung'),
                    ('fähigkeit', 'Tangled Feet', 'Taumelschritt'),
                    ('fähigkeit', 'Symbiosis', 'Symbiose'),
                    ('pokémon', 'Mime Jr.', 'Pantimimi')]
        for typ, en, de in expected:
            self.assertEqual(rows[typ, en], de)
        with Path('kanon_aliases.csv').open(newline='') as f:
            aliases = {(r['typ'], r['en']): r['de_alias']
                       for r in csv.DictReader(f, delimiter=';')}
        self.assertEqual(aliases['fähigkeit', 'Symbiosis'], 'Nutznießer')
        self.assertEqual(aliases['fähigkeit', 'Own Tempo'], 'Tempomacher')
        self.assertEqual(aliases['item', 'Twisted Spoon'], 'Krümmlöffel')
        self.assertNotIn(('item', 'Wacan Berry'), aliases)
        self.assertNotIn(('item', 'Mega Bracelet'), aliases)
