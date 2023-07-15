import unittest

from pylinq import LinqSequence


class CheckSequenceTest(unittest.TestCase):
    def test_sequence_equal(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(10))
        assert sequence.sequence_equal([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
