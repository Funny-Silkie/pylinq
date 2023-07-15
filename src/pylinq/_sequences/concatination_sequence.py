from typing import Generic, Iterator, final

from .. import LinqSequence
from ..type_variants import *


@final
class ConcatSequence(LinqSequence[T], Generic[T]):
    """結合されたシーケンスを表します。
    """

    def __init__(self, source: LinqSequence[T], after: Iterable[T]) -> None:
        """ConcatSequence[T]の新しいインスタンスを初期化します。

        Args:
            source (LinqSequence[T]): 読み込むシーケンス
            after (Iterable[T]): 結合するシーケンス
        """
        super().__init__()
        self.__source: LinqSequence[T] = source
        self.__after: Iterable[T] = after
        self.__iteartor: Iterator[T] | None = None
        self.__is_after: bool = False

    def _in_iteration(self) -> bool:
        return self.__iteartor is not None

    def _start_iteration(self) -> None:
        self.__source._start_iteration()
        self.__iteartor = iter(self.__source)
        self.__is_after = False

    def _stop_iteration(self) -> None:
        self.__iteartor = None
        self.__is_after = False

    def _get_next(self) -> T:
        try:
            return next(self.__iteartor)  # type: ignore
        except:
            if self.__is_after:
                raise
        self.__iteartor = iter(self.__after)
        self.__is_after = True
        return self._get_next()


@final
class ApPrependSequence(LinqSequence[T], Generic[T]):
    """先頭または末尾に要素を追加されたシーケンスを表します。
    """

    def __init__(self, source: LinqSequence[T], value: T, append: bool) -> None:
        """ApPrependSequence[T]の新しいインスタンスを初期化します。

        Args:
            source (LinqSequence[T]): 読み込むシーケンス
            value (T): 追加する要素
            append (bool): TrueでAppend，FalseでPrepend
        """
        super().__init__()
        self.__source: LinqSequence[T] = source
        self.__iterator: Iterator[T] | None = None
        self.__value: T = value
        self.__append: bool = append
        self.__finished: bool = False
        self.__value_returned: bool = False

    def _in_iteration(self) -> bool:
        return self.__source._in_iteration() or self.__value_returned

    def _start_iteration(self) -> None:
        self.__source._start_iteration()
        self.__iterator = iter(self.__source)

    def _stop_iteration(self) -> None:
        self.__source._stop_iteration()
        self.__iterator = None
        self.__value_returned = False
        self.__finished = False

    def _get_next(self) -> T:
        if not self.__value_returned and not self.__append:
            self.__value_returned = True
            return self.__value
        if self.__finished:
            raise StopIteration(0)

        try:
            return next(self.__iterator)  # type: ignore
        except:
            if not self.__value_returned and self.__append:
                self.__value_returned = True
                self.__finished = True
                return self.__value
            raise
