"""Testy bez bazy danych: sprawdzają budowę SQL i logikę wyboru trybu.

Uruchomienie (z katalogu api/):  python -m unittest discover -s tests -t .
Dopasowanie na prawdziwych danych sprawdza się ręcznie - patrz tests/smoke_queries.md.
"""
import re
import unicodedata
import unittest

from app.search_filters import build_filters, text_condition, text_order
from app.sql_helpers import SearchTerm, max_typos, resolve_ids


class FakeDb:
    """Udaje połączenie: unaccent(lower()) liczy w Pythonie, słownik zawiera 'pszenica'."""

    def __init__(self, dictionary=None):
        self.dictionary = dictionary or {}
        self.queries = []

    def execute(self, sql, params=None):
        self.queries.append((sql, params))
        return self

    def fetchone(self):
        sql, params = self.queries[-1]
        if sql.startswith("SELECT unaccent(lower("):
            text = params[0].lower().replace("ł", "l")
            text = "".join(
                c for c in unicodedata.normalize("NFKD", text)
                if not unicodedata.combining(c)
            )
            return {"t": text}
        raise AssertionError(sql)

    def fetchall(self):
        sql, params = self.queries[-1]
        if "WHERE unaccent(lower(name)) = unaccent(lower(" in sql:
            return [{"id": i} for n, i in self.dictionary.items() if n == params[0].lower()]
        return []


def placeholders(sql):
    return set(re.findall(r"%\((\w+)\)s", sql))


class MaxTyposTest(unittest.TestCase):
    def test_never_more_than_two(self):
        self.assertTrue(all(max_typos(n) <= 2 for n in range(1, 200)))

    def test_short_queries_get_one_typo(self):
        self.assertEqual(max_typos(3), 1)
        self.assertEqual(max_typos(5), 1)

    def test_long_queries_get_two_typos(self):
        self.assertEqual(max_typos(6), 2)
        self.assertEqual(max_typos(7), 2)  # "Amitsar" -> Amistar (WF-02, kryterium 1)


class SearchTermTest(unittest.TestCase):
    def test_normalizes_case_diacritics_and_spaces(self):
        term = SearchTerm.from_raw(FakeDb(), "  PSZENŻYTO   ozime ")
        self.assertEqual(term.text, "pszenzyto ozime")

    def test_empty_gives_none(self):
        for raw in (None, "", "   "):
            self.assertIsNone(SearchTerm.from_raw(FakeDb(), raw))

    def test_long_query_is_truncated(self):
        term = SearchTerm.from_raw(FakeDb(), "a" * 500)
        self.assertEqual(len(term.text), 100)


class SqlShapeTest(unittest.TestCase):
    def test_strict_mode_has_no_fuzzy_functions(self):
        sql = text_condition("strict") + text_order("strict")
        self.assertNotIn("levenshtein", sql)
        self.assertNotIn("similarity", sql)

    def test_fuzzy_mode_uses_levenshtein(self):
        self.assertIn("levenshtein_less_equal", text_condition("fuzzy"))

    def test_all_placeholders_have_values(self):
        db = FakeDb({"pszenica": 1, "mszyce": 2, "fungicyd": 3})
        term = SearchTerm.from_raw(db, "Amistar")
        for mode in ("strict", "fuzzy"):
            where, params = build_filters(
                db, term=term, crops=["pszenica"], pests=["mszyce"],
                product_types=["fungicyd"], role="amateur", mode=mode,
            )
            full = where + text_order(mode)
            self.assertLessEqual(placeholders(full), set(params), mode)

    def test_no_text_means_no_text_condition(self):
        where, params = build_filters(
            FakeDb(), term=None, crops=None, pests=None, product_types=None,
            role="professional",
        )
        self.assertEqual(where, "TRUE")
        self.assertEqual(params, {})

    def test_amateur_role_filters_amateur_products(self):
        where, _ = build_filters(
            FakeDb(), term=None, crops=None, pests=None, product_types=None,
            role="amateur",
        )
        self.assertIn("p.for_amateurs", where)

    def test_crop_and_pest_share_one_usage(self):
        db = FakeDb({"ziemniak": 1, "stonka ziemniaczana": 2})
        where, _ = build_filters(
            db, term=None, crops=["ziemniak"], pests=["stonka ziemniaczana"],
            product_types=None, role="professional",
        )
        self.assertEqual(where.count("FROM usage u"), 1)  # WF-04: to samo zastosowanie


class ResolveIdsTest(unittest.TestCase):
    def test_exact_name_does_not_run_fuzzy(self):
        db = FakeDb({"pszenica": 7})
        self.assertEqual(resolve_ids(db, "crop", ["pszenica"]), [7])
        self.assertFalse(any("levenshtein" in q[0] for q in db.queries))


if __name__ == "__main__":
    unittest.main()