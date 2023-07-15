import unittest

from pylinq import LinqSequence


class ProjectionTest(unittest.TestCase):
    def test_select1(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(range(5))\
            .select(lambda x: str(x))
        assert sequence.to_list() == ["0", "1", "2", "3", "4"]

    def test_select2(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(reversed(range(5)))\
            .select(lambda x, i: str(x + i))
        assert sequence.to_list() == LinqSequence.repeat("4", 5).to_list()

    def test_select_many1(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(5))\
            .select_many(lambda x: range(x * 10, x * 10 + 10))
        assert sequence.to_list() == list[int](range(50))

    def test_select_many2(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.repeat(1, 5)\
            .select_many(lambda x, i: range(x, i + 1))
        assert sequence.to_list() == [1, 1, 2, 1, 2, 3, 1, 2, 3, 4]

    def test_select_many3(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(range(5))\
            .select_many(lambda x: range(x * 10, x * 10 + 10), lambda x: str(x))
        assert sequence.to_list() == list[str](map(lambda x: str(x), range(50)))

    def test_select_many4(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.repeat(1, 5)\
            .select_many(lambda x, i: range(x, i + 1), lambda x: str(x))
        assert sequence.to_list() == ["1", "1", "2", "1", "2", "3", "1", "2", "3", "4"]

    def test_zip1(self) -> None:
        sequence: LinqSequence[tuple[int, str]] = LinqSequence.from_iterable(range(5))\
            .zip(LinqSequence.from_iterable(range(5)).select(lambda x: str(x)))

        assert sequence.to_list() == [(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4")]

    def test_zip2(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(range(5))\
            .zip(LinqSequence.from_iterable(range(5)).select(lambda x: str(x)), lambda x, y: f"{x}{y}")

        assert sequence.to_list() == ["00", "11", "22", "33", "44"]
