import unittest

from pylinq import LinqSequence


class GetSingleTest(unittest.TestCase):
    def test_element_at(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(10))
        assert sequence.element_at(3) == 3

    def test_element_at_or_default1(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(10))
        assert sequence.element_at_or_default(3, -1) == 3

    def test_element_at_or_default2(self) -> None:
        sequence: LinqSequence[int] = LinqSequence.from_iterable(range(10))
        assert sequence.element_at_or_default(100, -1) == -1

    def test_first1(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A", "B", "C"])
        assert sequence.first() == "A"

    def test_first2(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A", "AA", "AAA", "AAAA", "AAAAA"])
        assert sequence.first(lambda x: len(x) % 2 == 0) == "AA"

    def test_first_or_default1(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A", "B", "C"])
        assert sequence.first_or_default("Z") == "A"

    def test_first_or_default2(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable([])
        assert sequence.first_or_default("Z") == "Z"

    def test_first_or_default3(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A", "AA", "AAA", "AAAA", "AAAAA"])
        assert sequence.first_or_default("Z", lambda x: len(x) % 2 == 0) == "AA"

    def test_first_or_default4(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A", "AA", "AAA", "AAAA", "AAAAA"])
        assert sequence.first_or_default("Z", lambda x: len(x) == 100) == "Z"

    def test_last1(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A", "B", "C"])
        assert sequence.last() == "C"

    def test_last2(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A", "AA", "AAA", "AAAA", "AAAAA"])
        assert sequence.last(lambda x: len(x) % 2 == 0) == "AAAA"

    def test_last_or_default1(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A", "B", "C"])
        assert sequence.last_or_default("Z") == "C"

    def test_last_or_default2(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable([])
        assert sequence.last_or_default("Z") == "Z"

    def test_last_or_default3(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A", "AA", "AAA", "AAAA", "AAAAA"])
        assert sequence.last_or_default("Z", lambda x: len(x) % 2 == 0) == "AAAA"

    def test_last_or_default4(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A", "AA", "AAA", "AAAA", "AAAAA"])
        assert sequence.last_or_default("Z", lambda x: len(x) == 100) == "Z"

    def test_single1(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A"])
        assert sequence.single() == "A"

    def test_single2(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A", "AA", "AAA", "AAAA", "AAAAA"])
        assert sequence.single(lambda x: len(x) == 2) == "AA"

    def test_single_or_default1(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A"])
        assert sequence.single_or_default("Z") == "A"

    def test_single_or_default2(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable([])
        assert sequence.single_or_default("Z") == "Z"

    def test_single_or_default3(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A", "AA", "AAA", "AAAA", "AAAAA"])
        assert sequence.single_or_default("Z", lambda x: len(x) == 2) == "AA"

    def test_single_or_default4(self) -> None:
        sequence: LinqSequence[str] = LinqSequence.from_iterable(["A", "AA", "AAA", "AAAA", "AAAAA"])
        assert sequence.single_or_default("Z", lambda x: len(x) == 100) == "Z"
