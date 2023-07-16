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

    def test_union(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable([0, 1, 2, 3, 4])\
            .union([0, 2, 4, 6, 8])
        assert sequence.to_list() == [0, 1, 2, 3, 4, 6, 8]

    def test_union_by(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable([0, 1, 2, 3, 4])\
            .union_by([0, -2, 4, -6, 8], lambda x: abs(x))
        assert sequence.to_list() == [0, 1, 2, 3, 4, -6, 8]

    def test_excepted(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable([0, 1, 2, 3, 4])\
            .excepted([0, 2, 4, 6, 8])
        assert sequence.to_list() == [1, 3]

    def test_excepted_by(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable([0, 1, 2, 3, 4])\
            .excepted_by([0, -2, 4, -6, 8], lambda x: abs(x))
        assert sequence.to_list() == [1, 3]

    def test_intercept(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable([0, 1, 2, 3, 4])\
            .intercept([0, 2, 4, 6, 8])
        assert sequence.to_list() == [0, 2, 4]

    def test_intercept_by(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable([0, 1, 2, 3, 4])\
            .intercept_by([0, -2, 4, -6, 8], lambda x: abs(x))
        assert sequence.to_list() == [0, 2, 4]
