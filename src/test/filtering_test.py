import unittest

from pylinq import LinqSequence


class FiteringTest(unittest.TestCase):
    def test_where1(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable([0, 1, 2, 3, 4])\
            .where(lambda x: x % 2 == 0)
        assert sequence.to_list() == [0, 2, 4]

    def test_where2(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable([4, 3, 2, 1, 0])\
            .where(lambda x, y: x == y)
        assert sequence.to_list() == [2]

    def test_of_type(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable([1, "1", True, 1.0, 2, "2", None, 2.0])\
            .of_type(str)
        assert sequence.to_list() == ["1", "2"]
