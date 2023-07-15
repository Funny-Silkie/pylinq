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
