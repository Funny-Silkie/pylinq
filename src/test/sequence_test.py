import unittest

from pylinq import LinqSequence


class SequenceTest(unittest.TestCase):

    def test_from(self) -> None:
        source: list[int] = [0, 1, 2, 3, 4]
        sequence = LinqSequence[int].from_iterable(source)
        index: int = 0
        for current in sequence:
            assert current == source[index]
            index += 1
