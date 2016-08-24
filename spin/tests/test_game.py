from unittest import TestCase

from ..game import draw


class GameTestCase(TestCase):
    def test_draw(self):
        result = draw()
        self.assertTrue(isinstance(result, tuple))
        self.assertEqual(len(result), 3)
        for item in result:
            self.assertTrue(isinstance(item, int))
            self.assertTrue(item >= 0)
            self.assertTrue(item <= 2)
