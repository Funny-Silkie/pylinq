from abc import ABCMeta, abstractmethod
from typing import Callable, Generic

from .type_variants import *
from .linq_sequence import LinqSequence


class OrderedLinqSequence(LinqSequence[T], Generic[T], metaclass=ABCMeta):
    """並び替えられたシーケンスを表します。
    """

    @abstractmethod
    def _create_oredered_sequence(self, key_selector: Callable[[T], TKey], descending: bool) -> "OrderedLinqSequence[T]":
        """二つ目のソート条件で並び替えを行います。

        Args:
            key_selector (Callable[[T], TKey]): ソートのキーを生成する関数
            descending (bool): 降順でTrue，昇順でFalse

        Returns:
            OrderedLinqSequence[T]: ソート後のシーケンス
        """
        ...

    def then_by(self, key_selector: Callable[[T], TKey]) -> "OrderedLinqSequence[T]":
        """二つ目のソート条件で並び替えを行います。

        Args:
            key_selector (Callable[[T], TKey]): ソートのキーを生成する関数

        Returns:
            OrderedLinqSequence[T]: ソート後のシーケンス
        """
        return self._create_oredered_sequence(key_selector, False)

    def then_by_descending(self, key_selector: Callable[[T], TKey]) -> "OrderedLinqSequence[T]":
        """二つ目のソート条件で逆順の並び替えを行います。

        Args:
            key_selector (Callable[[T], TKey]): ソートのキーを生成する関数

        Returns:
            OrderedLinqSequence[T]: ソート後のシーケンス
        """
        return self._create_oredered_sequence(key_selector, True)
