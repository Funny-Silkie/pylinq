from typing import Callable, Generic, final

from .. import LinqSequence
from ..type_variants import *


@final
class WhereSequence(LinqSequence[T], Generic[T]):
    """絞り込みを行うシーケンスを表します。
    """

    def __init__(self, source: LinqSequence[T], match: Callable[[T, int], bool]) -> None:
        """WhereSequence[T]の新しいインスタンスを初期化します。

        Args:
            source (LinqSequence[T]): 読み込むシーケンス
            match (Callable[[T, int], bool]): 絞り込み関数
        """
        super().__init__()
        self.__index: int = 0
        self.__match: Callable[[T, int], bool] = match
        self.__source: LinqSequence[T] = source

    def _in_iteration(self) -> bool:
        return self.__source._in_iteration()

    def _start_iteration(self) -> None:
        self.__source._start_iteration()

    def _stop_iteration(self) -> None:
        self.__source._stop_iteration()
        self.__index = 0

    def _get_next(self) -> T:
        while True:
            current: T = next(self.__source)
            i: int = self.__index
            self.__index += 1
            if self.__match(current, i):
                return current
