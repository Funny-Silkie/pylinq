import unittest

from pylinq import LinqSequence, OrderedLinqSequence


class OrderingTest(unittest.TestCase):
    def test_order(self) -> None:
        sequence: OrderedLinqSequence[int] = LinqSequence.from_iterable([1, 0, 5, 3, 6, 4, 7])\
            .order()
        assert sequence.to_list() == [0, 1, 3, 4, 5, 6, 7]

    def test_order_by(self) -> None:
        sequence: OrderedLinqSequence[str] = LinqSequence.from_iterable(["1", "0", "5", "3", "6", "4", "7"])\
            .order_by(lambda x: int(x))
        assert sequence.to_list() == ["0", "1", "3", "4", "5", "6", "7"]

    def test_order_descending(self) -> None:
        sequence: OrderedLinqSequence[int] = LinqSequence.from_iterable([1, 0, 5, 3, 6, 4, 7])\
            .order_descending()
        assert sequence.to_list() == [7, 6, 5, 4, 3, 1, 0]

    def test_order_by_descending(self) -> None:
        sequence: OrderedLinqSequence[str] = LinqSequence.from_iterable(["1", "0", "5", "3", "6", "4", "7"])\
            .order_by_descending(lambda x: int(x))
        assert sequence.to_list() == ["7", "6", "5", "4", "3", "1", "0"]

    def test_then_by(self) -> None:
        source: list[tuple[int, str]] = [
            (3, "Takahashi"),
            (4, "Ito"),
            (2, "Tanaka"),
            (4, "Sato"),
            (2, "Yamada"),
            (1, "Sato"),
            (3, "Kino"),
            (2, "Ando"),
        ]
        expected: list[tuple[int, str]] = [
            (1, "Sato"),
            (2, "Ando"),
            (2, "Tanaka"),
            (2, "Yamada"),
            (3, "Kino"),
            (3, "Takahashi"),
            (4, "Ito"),
            (4, "Sato"),
        ]
        sequence: OrderedLinqSequence[tuple[int, str]] = LinqSequence.from_iterable(source)\
            .order_by(lambda x: x[0])\
            .then_by(lambda x: x[1])
        assert sequence.to_list() == expected

    def test_then_by_descending(self) -> None:
        source: list[tuple[int, str]] = [
            (3, "Takahashi"),
            (4, "Ito"),
            (2, "Tanaka"),
            (4, "Sato"),
            (2, "Yamada"),
            (1, "Sato"),
            (3, "Kino"),
            (2, "Ando"),
        ]
        expected: list[tuple[int, str]] = [
            (4, "Sato"),
            (4, "Ito"),
            (3, "Takahashi"),
            (3, "Kino"),
            (2, "Yamada"),
            (2, "Tanaka"),
            (2, "Ando"),
            (1, "Sato"),
        ]
        sequence: OrderedLinqSequence[tuple[int, str]] = LinqSequence.from_iterable(source)\
            .order_by(lambda x: x[0])\
            .then_by_descending(lambda x: x[1])
        assert sequence.to_list() == expected

    def test_reverse(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable([1, 0, 5, 3, 6, 4, 7])\
            .reverse()
        assert sequence.to_list() == [7, 4, 6, 3, 5, 0, 1]
