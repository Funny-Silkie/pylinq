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
