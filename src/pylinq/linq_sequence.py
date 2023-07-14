from abc import ABCMeta, abstractmethod
from typing import Callable, Generator, Generic, Iterable, Iterator, overload

from .type_variants import *


class LinqSequence(Generic[T], Iterator[T], metaclass=ABCMeta):
    """LINQのシーケンスを表します。
    """

    def __init__(self) -> None:
        """LinqSequence[T]の新しいインスタンスを初期化します。
        """
        pass

    def __iter__(self) -> Iterator[T]:
        if self._in_iteration() is not None:
            self._stop_iteration()
        return self

    def __next__(self) -> T:
        if not self._in_iteration():
            self._start_iteration()
        try:
            current: T = self._get_next()
            return current
        except StopIteration:
            self._stop_iteration()
            raise

    @abstractmethod
    def _in_iteration(self) -> bool:
        """インスタンスが列挙中かどうかを取得します。

        Returns:
            bool: インスタンスが列挙中の場合はTrue，それ以外でFalse
        """
        ...

    @abstractmethod
    def _start_iteration(self) -> None:
        """列挙を開始します。
        """
        ...

    @abstractmethod
    def _stop_iteration(self) -> None:
        """列挙を停止します。
        """
        ...

    @abstractmethod
    def _get_next(self) -> T:
        """次に列挙する値を取得します。

        Returns:
            T: 次に列挙する値
        """
        ...

    # From

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

    @classmethod
    def from_generator(cls, func: Callable[*TArgs, Generator[T, None, None]], *args: *TArgs) -> "LinqSequence[T]":  # type: ignore
        """Generatorからシーケンスを生成します。

        Args:
            func (Callable[[*TArgs], Generator[T, None, None]]): Generatorを生成する関数
            args: funcに与える引数

        Returns:
            LinqSequence[T]: funcによるGeneratorを持つシーケンスのインスタンス
        """
        from ._sequences import GeneratorSequence
        return GeneratorSequence[T](func, *args)
