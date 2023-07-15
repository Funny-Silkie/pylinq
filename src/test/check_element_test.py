from typing import Any
import unittest

from pylinq import LinqSequence


class CheckElementTest(unittest.TestCase):
    def test_any1(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(10))
        assert sequence.any()
        assert sequence.any(lambda x: x == 5)
        assert not sequence.any(lambda x: x == 15)

    def test_any2(self) -> None:
        sequence: LinqSequence[Any] = LinqSequence[Any].empty()
        assert not sequence.any()

    def test_all(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(10))
        assert sequence.all(lambda x: x < 10)
        assert not sequence.all(lambda x: x % 2 == 0)

    def test_contains(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(10))
        assert sequence.contains(3)
        assert not sequence.contains(100)
