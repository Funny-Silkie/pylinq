import unittest

from pylinq import LinqSequence


class ConverTest(unittest.TestCase):
    def test_list(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(5))
        assert sequence.to_list() == [0, 1, 2, 3, 4]

    def test_dict(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(5))
        expected: dict[int, str] = {
            0: '0',
            1: '1',
            2: '2',
            3: '3',
            4: '4',
        }
        assert sequence.to_dict(lambda x: x, lambda x: str(x)) == expected

    def test_set(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable([0, 1, 1, 2, 3, 4, 4, 4])
        expected: set[int] = {0, 1, 2, 3, 4}
        assert sequence.to_set() == expected
