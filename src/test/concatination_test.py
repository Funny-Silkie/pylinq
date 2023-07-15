import unittest

from pylinq import LinqSequence


class ConcatinationTest(unittest.TestCase):
    def test_concat(self) -> None:
        sequence: LinqSequence = LinqSequence.from_iterable(range(10))\
            .concat(range(10, 20))
        assert sequence.to_list() == list[int](range(20))

    def test_append(self) -> None:
        sequence: LinqSequence = LinqSequence.from_iterable(range(10))\
            .append(10)
        assert sequence.to_list() == list[int](range(11))

    def test_prepend(self) -> None:
        sequence: LinqSequence = LinqSequence.from_iterable(range(10))\
            .prepend(-1)
        assert sequence.to_list() == list[int](range(-1, 10))
