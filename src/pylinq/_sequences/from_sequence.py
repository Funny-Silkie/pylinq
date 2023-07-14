from typing import Callable, Generator, Generic, Iterable, Iterator

from .. import LinqSequence
from ..type_variants import *


class FromSequence(LinqSequence[T], Generic[T]):
    """イテラブルなオブジェクトをそのまま持つシーケンスのクラスです。
    """

    def __init__(self, source: Iterable[T]) -> None:
        """FromSequence[T]の新しいインスタンスを初期化します。

        Args:
            source (Iterable[T]): 使用するイテラブルなオブジェクト
        """
        super().__init__()
        self.__iterator: Iterator[T] | None = None
        self.__source: Iterable[T] = source

    def _in_iteration(self) -> bool:
        return not self.__iterator is None

    def _start_iteration(self) -> None:
        self.__iterator = iter(self.__source)

    def _stop_iteration(self) -> None:
        self.__iterator = None

    def _get_next(self) -> T:
        return next(self.__iterator)  # type: ignore


class GeneratorSequence(LinqSequence[T], Generic[T]):
    """Generatorを基にしたシーケンスのクラスです。
    """

    def __init__(self, func: Callable[[*TArgs], Generator[T, None, None]], *args: *TArgs) -> None:  # type: ignore
        """GeneratorSequence[T]の新しいインスタンスを初期化します。

        Args:
            func (Callable[[*TArgs], Generator[T, None, None]]): Generatorを生成する関数
            args: funcに与える引数
        """
        super().__init__()
        self.__func: Callable[[*TArgs], Generator[T, None, None]] = func  # type: ignore
        self.__args: tuple = args
        self.__geneartor: Generator[T, None, None] | None = None

    def _in_iteration(self) -> bool:
        return not self.__geneartor is None

    def _start_iteration(self) -> None:
        self.__geneartor = self.__func(*self.__args)

    def _stop_iteration(self) -> None:
        self.__geneartor = None

    def _get_next(self) -> T:
        return next(self.__geneartor)  # type: ignore
