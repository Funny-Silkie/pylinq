import unittest

from pylinq import LinqSequence


class CreateTest(unittest.TestCase):
    def test_empty(self) -> None:
        sequence: LinqSequence[int] = LinqSequence[int].empty()
        count: int = 0
        for _ in sequence:
            count += 1
        assert count == 0

    def test_range(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.range(1, 5)
        expected: int = 1
        for current in sequence:
            assert current == expected
            expected += 1

    def test_repeat(self) -> None:
        sequence: LinqSequence[str] = LinqSequence[str].repeat("aaa", 5)
        count: int = 0
        for current in sequence:
            assert current == "aaa"
            count += 1
        assert count == 5

    def test_default_if_empty1(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(10))\
            .default_if_empty(-1)
        assert sequence.to_list() == list[int](range(10))

    def test_default_if_empty2(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(list[int]())\
            .default_if_empty(-1)
        assert sequence.to_list() == [-1]
