from itertools import count
from typing import Generic, final

from .. import LinqSequence
from ..type_variants import *


@final
class EmptySequence(LinqSequence[T], Generic[T]):
    """空のシーケンスを表します。
    """

    def __init__(self) -> None:
        """EmptySequenceの新しいインスタンスを初期化します。
        """
        super().__init__()

    def _in_iteration(self) -> bool:
        return False

    def _start_iteration(self) -> None:
        pass

    def _stop_iteration(self) -> None:
        pass

    def _get_next(self) -> T:
        raise StopIteration()


@final
class RangeSequence(LinqSequence[int]):
    """指定した範囲の整数を列挙するシーケンスを表します。
    """

    def __init__(self, start: int, count: int) -> None:
        """RangeSequenceの新しいインスタンスを初期化します。

        Args:
            start (int): 開始値
            count (int): 列挙数
        """
        self.__current: int = start
        self.__start: int = start
        self.__end: int = start + count

    def _in_iteration(self) -> bool:
        return self.__current == self.__start

    def _start_iteration(self) -> None:
        pass

    def _stop_iteration(self) -> None:
        self.__current = self.__start

    def _get_next(self) -> int:
        result: int = self.__current
        self.__current += 1
        if self.__current == self.__end:
            raise StopIteration()
        return result


@final
class RepeatSequence(LinqSequence[T], Generic[T]):
    """単一の値を繰り返し出力するシーケンスを表します。
    """

    def __init__(self, value: T, count: int) -> None:
        """RepeatSequence[T]の新しいインスタンスを初期化します。

        Args:
            value (T): 列挙する値
            count (int): 列挙数
        """
        self.__index: int = 0
        self.__value: T = value
        self.__count: int = count

    def _in_iteration(self) -> bool:
        return self.__index > 0

    def _start_iteration(self) -> None:
        pass

    def _stop_iteration(self) -> None:
        self.__index = 0

    def _get_next(self) -> T:
        if self.__index == self.__count:
            raise StopIteration()
        self.__index += 1
        return self.__value
