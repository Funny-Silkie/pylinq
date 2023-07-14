from collections import deque
from typing import Callable, Generic, Iterator, final

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


@final
class TakeSequence(LinqSequence[T], Generic[T]):
    """先頭から指定した個数の要素を列挙するシーケンスを表します。
    """

    def __init__(self, source: LinqSequence[T], count: int) -> None:
        """TakeSequence[T]の新しいインスタンスを初期化します。

        Args:
            source (LinqSequence[T]): 読み込むシーケンス
            count (int): 取得する要素数
        """
        super().__init__()
        self.__source: LinqSequence[T] = source
        self.__index: int = 0
        self.__count: int = count

    def _in_iteration(self) -> bool:
        return self.__index > 0

    def _start_iteration(self) -> None:
        self.__source._start_iteration()

    def _stop_iteration(self) -> None:
        self.__source._stop_iteration()
        self.__index = 0

    def _get_next(self) -> T:
        if self.__index == self.__count:
            raise StopIteration()
        self.__index += 1
        return next(self.__source)


@final
class TakeLastSequence(LinqSequence[T], Generic[T]):
    """末尾から指定した個数の要素を列挙するシーケンスを表します。
    """

    def __init__(self, source: LinqSequence[T], count: int) -> None:
        """TakeLastSequence[T]の新しいインスタンスを初期化します。

        Args:
            source (LinqSequence[T]): 読み込むシーケンス
            count (int): 取得する要素数
        """
        super().__init__()
        self.__source: LinqSequence[T] = source
        self.__iterator: Iterator[T] | None = None
        self.__count: int = count

    def _in_iteration(self) -> bool:
        return not self.__iterator is None

    def _start_iteration(self) -> None:
        queue: deque = deque[T](self.__source, maxlen=self.__count)
        self.__iterator = iter(queue)

    def _stop_iteration(self) -> None:
        self.__iterator = None

    def _get_next(self) -> T:
        return next(self.__iterator)  # type: ignore


@final
class TakeWhileSequence(LinqSequence[T], Generic[T]):
    """指定した条件を満たす間列挙を続けるシーケンスを表します。
    """

    def __init__(self, source: LinqSequence[T], match: Callable[[T, int], bool]) -> None:
        super().__init__()
        self.__index: int = 0
        self.__match: Callable[[T, int], bool] = match
        self.__source: LinqSequence[T] = source

    def _in_iteration(self) -> bool:
        return self.__index > 0

    def _start_iteration(self) -> None:
        self.__source._start_iteration()

    def _stop_iteration(self) -> None:
        self.__source._stop_iteration()
        self.__index = 0

    def _get_next(self) -> T:
        result: T = next(self.__source)
        if not self.__match(result, self.__index):
            raise StopIteration()
        self.__index += 1
        return result
