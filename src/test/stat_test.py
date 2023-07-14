import unittest

from pylinq import LinqSequence


class StatTest(unittest.TestCase):
    def test_count1(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(10))
        assert sequence.count() == 10

    def test_count2(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(10))
        assert sequence.count(lambda x: x % 3 == 0) == 4

    def test_max_by1(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["1", "2", "3", "4", "5"])
        actual: str | None = sequence.max_by(lambda x: int(x))
        assert actual is not None
        assert actual == "5"

    def test_max_by2(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(list[str]())
        actual: str | None = sequence.max_by(lambda x: int(x))
        assert actual is None

    def test_min_by1(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["1", "2", "3", "4", "5"])
        actual: str | None = sequence.min_by(lambda x: int(x))
        assert actual is not None
        assert actual == "1"

    def test_min_by2(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(list[str]())
        actual: str | None = sequence.min_by(lambda x: int(x))
        assert actual is None

    def test_sum(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["1", "2", "3", "4", "5"])
        assert sequence.sum(lambda x: int(x)) == 15

    def test_average(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["1", "2", "3", "4", "5"])
        assert sequence.average(lambda x: int(x)) == 3

    def test_accumulate1(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["1", "2", "3", "4", "5"])
        assert sequence.aggregate(0, lambda accumulate, current: accumulate + int(current)) == 15

    def test_accumulate2(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["1", "2", "3", "4", "5"])
        assert sequence.aggregate(0, lambda accumulate, current: accumulate + int(current), lambda x: x / sequence.count()) == 3
