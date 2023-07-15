import unittest

from pylinq import Grouping, LinqSequence, Lookup
from test.entries import Person


class GroupingTest(unittest.TestCase):
    def test_to_look_up1(self) -> None:
        source: list[Person] = [
            Person(1, "Sato"),
            Person(2, "Tanaka"),
            Person(3, "Takahashi"),
            Person(4, "Sato"),
            Person(5, "Ito"),
        ]
        sequence: Lookup[str, Person] = LinqSequence.from_iterable(source)\
            .to_look_up(lambda x: x.name)
        assert sequence.count() == 4
        assert sequence["Sato"].element_at(0).id == 1
        assert sequence["Sato"].element_at(1).id == 4
        assert sequence["Tanaka"].element_at(0).id == 2
        assert sequence["Takahashi"].element_at(0).id == 3
        assert sequence["Ito"].element_at(0).id == 5
        assert sequence["404"].count() == 0

    def test_to_look_up2(self) -> None:
        source: list[Person] = [
            Person(1, "Sato"),
            Person(2, "Tanaka"),
            Person(3, "Takahashi"),
            Person(4, "Sato"),
            Person(5, "Ito"),
        ]
        sequence: Lookup[str, int] = LinqSequence.from_iterable(source)\
            .to_look_up(lambda x: x.name, lambda x: x.id)
        assert sequence.count() == 4
        assert sequence["Sato"].element_at(0) == 1
        assert sequence["Sato"].element_at(1) == 4
        assert sequence["Tanaka"].element_at(0) == 2
        assert sequence["Takahashi"].element_at(0) == 3
        assert sequence["Ito"].element_at(0) == 5
        assert sequence["404"].count() == 0

    def test_group_by1(self) -> None:
        source: list[Person] = [
            Person(1, "Sato"),
            Person(2, "Tanaka"),
            Person(3, "Takahashi"),
            Person(4, "Sato"),
            Person(5, "Ito"),
        ]
        sequence: LinqSequence[Grouping[str, Person]] = LinqSequence.from_iterable(source)\
            .group_by(lambda x: x.name)
        assert sequence.count() == 4
        assert sequence.single(lambda x: x.key == "Sato").element_at(0).id == 1
        assert sequence.single(lambda x: x.key == "Sato").element_at(1).id == 4
        assert sequence.single(lambda x: x.key == "Tanaka").element_at(0).id == 2
        assert sequence.single(lambda x: x.key == "Takahashi").element_at(0).id == 3
        assert sequence.single(lambda x: x.key == "Ito").element_at(0).id == 5

    def test_group_by2(self) -> None:
        source: list[Person] = [
            Person(1, "Sato"),
            Person(2, "Tanaka"),
            Person(3, "Takahashi"),
            Person(4, "Sato"),
            Person(5, "Ito"),
        ]
        sequence: LinqSequence[Grouping[str, int]] = LinqSequence.from_iterable(source)\
            .group_by(lambda x: x.name, lambda x: x.id)
        assert sequence.count() == 4
        assert sequence.single(lambda x: x.key == "Sato").element_at(0) == 1
        assert sequence.single(lambda x: x.key == "Sato").element_at(1) == 4
        assert sequence.single(lambda x: x.key == "Tanaka").element_at(0) == 2
        assert sequence.single(lambda x: x.key == "Takahashi").element_at(0) == 3
        assert sequence.single(lambda x: x.key == "Ito").element_at(0) == 5

    def test_group_by3(self) -> None:
        source: list[Person] = [
            Person(1, "Sato"),
            Person(2, "Tanaka"),
            Person(3, "Takahashi"),
            Person(4, "Sato"),
            Person(5, "Ito"),
        ]
        sequence: LinqSequence[tuple[str, list[Person]]] = LinqSequence.from_iterable(source)\
            .group_by(lambda x: x.name, None, lambda x, y: (x, y.to_list()))
        assert sequence.count() == 4
        assert sequence.single(lambda x: x[0] == "Sato")[1][0].id == 1
        assert sequence.single(lambda x: x[0] == "Sato")[1][1].id == 4
        assert sequence.single(lambda x: x[0] == "Tanaka")[1][0].id == 2
        assert sequence.single(lambda x: x[0] == "Takahashi")[1][0].id == 3
        assert sequence.single(lambda x: x[0] == "Ito")[1][0].id == 5

    def test_group_by4(self) -> None:
        source: list[Person] = [
            Person(1, "Sato"),
            Person(2, "Tanaka"),
            Person(3, "Takahashi"),
            Person(4, "Sato"),
            Person(5, "Ito"),
        ]
        sequence: LinqSequence[tuple[str, list[int]]] = LinqSequence.from_iterable(source)\
            .group_by(lambda x: x.name, lambda x: x.id, lambda x, y: (x, y.to_list()))
        assert sequence.count() == 4
        assert sequence.single(lambda x: x[0] == "Sato")[1] == [1, 4]
        assert sequence.single(lambda x: x[0] == "Tanaka")[1] == [2]
        assert sequence.single(lambda x: x[0] == "Takahashi")[1] == [3]
        assert sequence.single(lambda x: x[0] == "Ito")[1] == [5]
