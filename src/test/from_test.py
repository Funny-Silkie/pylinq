from typing import Generator
import unittest

from pylinq import LinqSequence


class FromTest(unittest.TestCase):

    def test_list(self) -> None:
        source: list[int] = [0, 1, 2, 3, 4]
        sequence: LinqSequence[int] = LinqSequence[int].from_iterable(source)
        index: int = 0
        for current in sequence:
            assert current == source[index]
            index += 1

    def test_dict(self) -> None:
        source: dict[int, str] = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4'}
        sequence: LinqSequence[tuple[int, str]] = LinqSequence.from_dict(source)

        count: int = 0
        for current in sequence:
            assert current[1] == source[current[0]]
            count += 1
        assert count == len(source)

    def test_generator(self) -> None:
        def inner(count: int) -> Generator[int, None, None]:
            for i in range(count):
                yield i
        sequence: LinqSequence[int] = LinqSequence[int].from_generator(inner, 5)
        expected: int = 0
        for current in sequence:
            assert current == expected
            expected += 1
