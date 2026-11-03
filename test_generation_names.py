import copy
import json
import unittest
from pathlib import Path
from parse_kanon import apply_generation_names


class GenerationNamesTest(unittest.TestCase):
    def setUp(self):
        self.rules = json.loads(Path('generation_names.json').read_text())
        self.rows = [['item', 'Choice Specs', 'Wahlglas', 'old'],
                     ['attacke', 'Glare', 'Schlangenblick', 'already current'],
                     ['item', 'Unrelated', 'Wahlglas', 'unrelated'],
                     ['item', 'Focus Band', 'Fokus-Band', 'old']]
        self.rows.extend([[r['typ'], r['en'], r['legacy_de'], 'old']
                          for r in self.rules[3:]])

    def test_current_and_legacy_are_separate_and_idempotent(self):
        before = copy.deepcopy(self.rows)
        rows, aliases = apply_generation_names(self.rows, self.rules)
        self.assertEqual(self.rows, before)
        self.assertEqual(rows[0][2], 'Wahlbrille')
        self.assertEqual(rows[1][2], 'Schlangenblick')
        self.assertEqual(rows[2], self.rows[2])
        self.assertEqual(rows[3][2], 'Fokusband')
        self.assertEqual(aliases[0][2:6], ['Wahlglas', '4-7', 'Wahlbrille', 8])
        self.assertEqual(aliases[1][2:6], ['Giftblick', '1-7', 'Schlangenblick', 8])
        self.assertEqual(aliases[2][2:6], ['Fokus-Band', '2-7', 'Fokusband', 8])
        self.assertEqual(apply_generation_names(rows, self.rules), (rows, aliases))

    def test_missing_name_rejected(self):
        with self.assertRaises(ValueError):
            apply_generation_names(self.rows[1:], self.rules)

    def test_duplicate_source_identity_rejected(self):
        with self.assertRaises(ValueError):
            apply_generation_names(self.rows + [self.rows[0]], self.rules)

    def test_duplicate_rule_rejected(self):
        with self.assertRaises(ValueError):
            apply_generation_names(self.rows, self.rules + [self.rules[0]])

    def test_unexpected_spelling_rejected(self):
        self.rows[0][2] = 'unexpected'
        with self.assertRaises(ValueError):
            apply_generation_names(self.rows, self.rules)


if __name__ == '__main__':
    unittest.main()
