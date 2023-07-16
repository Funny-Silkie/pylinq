import unittest

from pylinq import LinqSequence


class JoiningTest(unittest.TestCase):
    def test_join(self) -> None:
        outer: list[tuple[int, str, int]] = [
            (1, "Sato", 2),
            (2, "Tanaka", 1),
            (3, "Takahashi", 3),
            (4, "Sato", 4),
            (5, "Ito", 3),
        ]
        inner: list[tuple[int, str]] = [
            (1, "Tokyo"),
            (2, "Nagoya"),
            (3, "Osaka"),
        ]
        expected: list = [
            (1, "Sato", "Nagoya"),
            (2, "Tanaka", "Tokyo"),
            (3, "Takahashi", "Osaka"),
            (5, "Ito", "Osaka"),
        ]
        sequence: LinqSequence[tuple[int, str, str]] = LinqSequence.from_iterable(outer)\
            .join(inner, lambda x: x[2], lambda x: x[0], lambda x, y: (x[0], x[1], y[1]))
        assert sequence.to_list() == expected

    def test_group_join(self) -> None:
        outer: list[tuple[int, str]] = [
            (1, "Tokyo"),
            (2, "Nagoya"),
            (3, "Osaka"),
        ]
        inner: list[tuple[int, str, int]] = [
            (1, "Sato", 2),
            (2, "Tanaka", 1),
            (3, "Takahashi", 3),
            (4, "Sato", 4),
            (5, "Ito", 3),
        ]
        expected: list = [
            (1, "Tokyo", "Tanaka"),
            (2, "Nagoya", "Sato"),
            (3, "Osaka", "Takahashi, Ito"),
        ]

        def result_selector(outer: tuple[int, str], inner: LinqSequence[tuple[int, str, int]]) -> tuple[int, str, str]:
            return (outer[0], outer[1], str.join(", ", inner.select(lambda x: x[1])))
        sequence: LinqSequence[tuple[int, str, str]] = LinqSequence.from_iterable(outer)\
            .group_join(inner, lambda x: x[0], lambda x: x[2], result_selector)
        assert sequence.to_list() == expected
