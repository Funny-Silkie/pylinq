from typing import Callable, Generator, Generic, Iterable, Iterator

from ..type_variants import *
from ..linq_sequence import LinqSequence


class FromSequence(LinqSequence[T], Generic[T]):
    """イテラブルなオブジェクトをそのまま持つシーケンスのクラスです。
    """

    def __init__(self, source: Iterable[T]) -> None:
        """FromSequence[T]の新しいインスタンスを初期化します。

        Args:
            source (Iterable[T]): 使用するイテラブルなオブジェクト
        """
        LinqSequence[T].__init__(
            self  # type:ignore
        )
        self.__source: Iterable[T] = source

    def _get_source(self) -> Iterable[T]:
        return self.__source


class GeneratorSequence(LinqSequence[T], Generic[T]):
    """Generatorを基にしたシーケンスのクラスです。
    """

    def __init__(self, func: Callable[[*TArgs], Generator[T, None, None]], *args: *TArgs) -> None:  # type: ignore
        """GeneratorSequence[T]の新しいインスタンスを初期化します。

        Args:
            func (Callable[[*TArgs], Generator[T, None, None]]): Generatorを生成する関数
            args: funcに与える引数
        """
        self.__func: Callable[[*TArgs], Generator[T, None, None]] = func  # type: ignore
        self.__args: tuple = args
        self.__geneartor: Generator[T, None, None] | None = None

    def __iter__(self) -> Iterator[T]:
        if not self.__geneartor is None:
            self._stop_iteration()
        return self

    def __next__(self) -> T:
        if self.__geneartor is None:
            self.__geneartor = self.__func(*self.__args)
        try:
            current: T = next(self.__geneartor)
            return current
        except StopIteration:
            self._stop_iteration()
            raise

    def _stop_iteration(self) -> None:
        self.__geneartor = None

    def _get_source(self) -> Iterable[T]:
        raise TypeError()
