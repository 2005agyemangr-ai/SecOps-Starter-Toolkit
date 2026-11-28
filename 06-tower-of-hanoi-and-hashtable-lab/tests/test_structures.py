import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from structures import HashTable, solve_hanoi


class TestStructures(unittest.TestCase):
    def test_hashtable_crud(self) -> None:
        ht = HashTable(size=8)
        ht.put("course", "INF 213")
        ht.put("course", "INF 215")
        self.assertEqual(ht.get("course"), "INF 215")
        self.assertIsNone(ht.get("missing"))
        self.assertTrue(ht.delete("course"))
        self.assertFalse(ht.delete("course"))

    def test_hanoi_moves(self) -> None:
        moves = solve_hanoi(3, "A", "B", "C")
        self.assertEqual(len(moves), 7)
        self.assertEqual(moves[0], ("A", "C"))
        self.assertEqual(moves[-1], ("A", "C"))


if __name__ == "__main__":
    unittest.main()
