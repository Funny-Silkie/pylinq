import unittest

from pylinq import LinqSequence


class GetMultiTest(unittest.TestCase):
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

    def test_chunk(self) -> None:
        sequence: LinqSequence[list[int]] = LinqSequence.from_iterable(range(30))\
            .chunk(10)
        expected: list[list[int]] = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
        ]
        assert sequence.to_list() == expected
