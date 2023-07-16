from abc import ABCMeta, abstractmethod
from typing import Callable, Generic

from .type_variants import *
from .linq_sequence import LinqSequence


class OrderedLinqSequence(LinqSequence[T], Generic[T], metaclass=ABCMeta):
    """並び替えられたシーケンスを表します。
    """

    @abstractmethod
    def _create_oredered_sequence(self, key_selector: Callable[[T], TKey], descending: bool) -> "OrderedLinqSequence[T]":
        ...

    def then_by(self, key_selector: Callable[[T], TKey]) -> "OrderedLinqSequence[T]":
        return self._create_oredered_sequence(key_selector, False)

    def then_by_descending(self, key_selector: Callable[[T], TKey]) -> "OrderedLinqSequence[T]":
        return self._create_oredered_sequence(key_selector, True)
