from typing import Callable, Generic, final

from .. import LinqSequence
from ..type_variants import *


@final
class SelectSequence(LinqSequence[TResult], Generic[T, TResult]):
    """要素の変換を行うシーケンスを表します。
    """

    def __init__(self, source: LinqSequence[T], selector: Callable[[T, int], TResult]) -> None:
        """SelectSequence[T, TResult]の新しいインスタンスを初期化します。

        Args:
            source (LinqSequence[T]): 読み込むシーケンス
            selector (Callable[[T, int], TResult]): 要素の変換を行う関数
        """
        super().__init__()
        self.__index: int = 0
        self.__source: LinqSequence[T] = source
        self.__selector: Callable[[T, int], TResult] = selector

    def _in_iteration(self) -> bool:
        return self.__source._in_iteration()

    def _start_iteration(self) -> None:
        self.__source._start_iteration()

    def _stop_iteration(self) -> None:
        self.__source._stop_iteration()
        self.__index = 0

    def _get_next(self) -> TResult:
        i: int = self.__index
        self.__index += 1
        return self.__selector(next(self.__source), i)
