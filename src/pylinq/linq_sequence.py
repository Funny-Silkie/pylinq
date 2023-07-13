from abc import ABCMeta, abstractmethod
from typing import Generic, Iterable, Iterator

from .type_variants import *


class LinqSequence(Generic[T], Iterator[T], metaclass=ABCMeta):
    """LINQのシーケンスを表します。
    """

    def __init__(self) -> None:
        """LinqSequence[T]の新しいインスタンスを初期化します。
        """
        self.__iterator: Iterator[T] | None = None

    def __iter__(self) -> Iterator[T]:
        if self.__iterator is not None:
            self._stop_iteration()
        return self

    def __next__(self) -> T:
        if self.__iterator is None:
            self.__iterator = iter(self._get_source())
        try:
            current: T = next(self.__iterator)
            return current
        except StopIteration:
            self._stop_iteration()
            raise

    @abstractmethod
    def _get_source(self) -> Iterable[T]:
        """列挙対象を取得します。

        Returns:
            Iterable[T]: 列挙対象
        """
        ...

    def _stop_iteration(self) -> None:
        """列挙を停止します。
        """
        self.__iterator = None

    @classmethod
    def from_iterable(cls, source: Iterable[T]) -> "LinqSequence[T]":
        """イテラブルなオブジェクトからシーケンスを生成します。

        Args:
            source (Iterable[T]): イテラブルなオブジェクト

        Returns:
            LinqSequence[T]: sourceを持つシーケンスのインスタンス
        """
        from ._sequences import FromSequence
        return FromSequence[T](source)
