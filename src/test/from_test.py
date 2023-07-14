from typing import Generator
import unittest

from pylinq import LinqSequence


class FromTest(unittest.TestCase):

    def test_from_list(self) -> None:
        source: list[int] = [0, 1, 2, 3, 4]
        sequence = LinqSequence[int].from_iterable(source)
        index: int = 0
        for current in sequence:
            assert current == source[index]
            index += 1

    def test_from_generator(self) -> None:
        def inner(count: int) -> Generator[int, None, None]:
            for i in range(count):
                yield i
        sequence = LinqSequence[int].from_generator(inner, 5)
        expected: int = 0
        for current in sequence:
            assert current == expected
            expected += 1
