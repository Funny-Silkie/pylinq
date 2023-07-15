import unittest

from pylinq import LinqSequence


class SetOperationTest(unittest.TestCase):
    def test_distinct(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable([0, 1, 2, 3, 4, 1, 0, 2, 3])\
            .distinct()
        assert sequence.to_list() == [0, 1, 2, 3, 4]

    def test_distinct_by(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable([0, 1, 2, 3, 4, -1, 0, 2, -3])\
            .distinct_by(lambda x: abs(x))
        assert sequence.to_list() == [0, 1, 2, 3, 4]
