import unittest

from pylinq import LinqSequence


class GetMultiTest(unittest.TestCase):
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

    def test_distinct(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable([0, 1, 2, 3, 4, 1, 0, 2, 3])\
            .distinct()
        assert sequence.to_list() == [0, 1, 2, 3, 4]

    def test_distinct_by(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable([0, 1, 2, 3, 4, -1, 0, 2, -3])\
            .distinct_by(lambda x: abs(x))
        assert sequence.to_list() == [0, 1, 2, 3, 4]

    def test_skip(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(100))\
            .skip(50)
        assert sequence.to_list() == list[int](range(50, 100))

    def test_skip_last(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(100))\
            .skip_last(70)
        assert sequence.to_list() == list[int](range(30))

    def test_skip_while(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(100))\
            .skip_while(lambda x: x < 90)
        assert sequence.to_list() == list[int](range(90, 100))

    def test_take(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(100))\
            .take(20)
        assert sequence.to_list() == list[int](range(20))

    def test_take_last(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(100))\
            .take_last(20)
        assert sequence.to_list() == list[int](range(80, 100))

    def test_take_while(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(100))\
            .take_while(lambda x: x < 10)
        assert sequence.to_list() == list[int](range(10))

    def test_default_if_empty1(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(10))\
            .default_if_empty(-1)
        assert sequence.to_list() == list[int](range(10))

    def test_default_if_empty2(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(list[int]())\
            .default_if_empty(-1)
        assert sequence.to_list() == [-1]
