from typing import Callable, Generic, Iterator, final

from .. import LinqSequence
from ..type_variants import *


@final
class UnionSequence(LinqSequence[T], Generic[T]):
    """和集合のシーケンスを表します。
    """

    def __init__(self, first: LinqSequence[T], second: Iterable[T]) -> None:
        """UnionSequence[T]の新しいインスタンスを初期化します。

        Args:
            first (LinqSequence[T]): 読み込むシーケンス
            second (Iterable[T]): 比較集合
        """
        super().__init__()
        self.__first: LinqSequence[T] = first
        self.__second: Iterable[T] = second
        self.__set: set[T] = set[T]()
        self.__iterator: Iterator[T] | None = None
        self.__is_second: bool = False

    def _in_iteration(self) -> bool:
        return not self.__iterator is None

    def _start_iteration(self) -> None:
        self.__first._start_iteration()
        self.__iterator = iter(self.__first)

    def _stop_iteration(self) -> None:
        self.__first._stop_iteration()
        self.__iterator = None
        self.__is_second = False
        self.__set.clear()

    def _get_next(self) -> T:
        current: T
        try:
            while True:
                current = next(
                    self.__iterator  # type: ignore
                )
                if current in self.__set:
                    continue
                self.__set.add(current)
                return current
        except StopIteration:
            if self.__is_second:
                raise
        self.__is_second = True
        self.__iterator = iter(self.__second)
        return self._get_next()


@final
class UnionBySequence(LinqSequence[T], Generic[T, TKey]):
    """和集合のシーケンスを表します。
    """

    def __init__(self, first: LinqSequence[T], second: Iterable[T], key_selector: Callable[[T], TKey]) -> None:
        """UnionVySequence[T]の新しいインスタンスを初期化します。

        Args:
            first (LinqSequence[T]): 読み込むシーケンス
            second (Iterable[T]): 比較集合
            key_selector (Callable[[T], TKey]): 比較時のキーを生成する関数
        """
        super().__init__()
        self.__first: LinqSequence[T] = first
        self.__second: Iterable[T] = second
        self.__key_selector: Callable[[T], TKey] = key_selector
        self.__set: set[TKey] = set[TKey]()
        self.__iterator: Iterator[T] | None = None
        self.__is_second: bool = False

    def _in_iteration(self) -> bool:
        return not self.__iterator is None

    def _start_iteration(self) -> None:
        self.__first._start_iteration()
        self.__iterator = iter(self.__first)

    def _stop_iteration(self) -> None:
        self.__first._stop_iteration()
        self.__iterator = None
        self.__is_second = False
        self.__set.clear()

    def _get_next(self) -> T:
        current: T
        try:
            while True:
                current = next(
                    self.__iterator  # type: ignore
                )
                key: TKey = self.__key_selector(current)
                if key in self.__set:
                    continue
                self.__set.add(key)
                return current
        except StopIteration:
            if self.__is_second:
                raise
        self.__is_second = True
        self.__iterator = iter(self.__second)
        return self._get_next()


@final
class ExceptSequence(LinqSequence[T], Generic[T]):
    """差集合のシーケンスを表します。
    """

    def __init__(self, source: LinqSequence[T], target: Iterable[T]) -> None:
        """ExceptSequence[T]の新しいインスタンスを初期化します。

        Args:
            source (LinqSequence[T]): 読み込むシーケンス
            target (Iterable[T]): 比較集合
        """
        super().__init__()
        self.__source: LinqSequence[T] = source
        self.__target: Iterable[T] = target
        self.__set: set[T] = set[T]()
        self.__iterator: Iterator[T] | None = None

    def _in_iteration(self) -> bool:
        return not self.__iterator is None

    def _start_iteration(self) -> None:
        self.__source._start_iteration()
        self.__iterator = iter(self.__source)
        self.__set.update(self.__target)

    def _stop_iteration(self) -> None:
        self.__source._stop_iteration()
        self.__iterator = None
        self.__set.clear()

    def _get_next(self) -> T:
        current: T
        while True:
            current = next(
                self.__iterator  # type: ignore
            )
            if current in self.__set:
                continue
            return current


@final
class ExceptBySequence(LinqSequence[T], Generic[T, TKey]):
    """差集合のシーケンスを表します。
    """

    def __init__(self, source: LinqSequence[T], target: Iterable[T], key_selector: Callable[[T], TKey]) -> None:
        """ExceptBySequence[T]の新しいインスタンスを初期化します。

        Args:
            source (LinqSequence[T]): 読み込むシーケンス
            target (Iterable[T]): 比較集合
            key_selector (Callable[[T], TKey]): 比較時のキーを生成する関数
        """
        super().__init__()
        self.__source: LinqSequence[T] = source
        self.__target: Iterable[T] = target
        self.__key_selector: Callable[[T], TKey] = key_selector
        self.__set: set[TKey] = set[TKey]()
        self.__iterator: Iterator[T] | None = None

    def _in_iteration(self) -> bool:
        return not self.__iterator is None

    def _start_iteration(self) -> None:
        self.__source._start_iteration()
        self.__iterator = iter(self.__source)
        self.__set.update(map(self.__key_selector, self.__target))

    def _stop_iteration(self) -> None:
        self.__source._stop_iteration()
        self.__iterator = None
        self.__set.clear()

    def _get_next(self) -> T:
        current: T
        while True:
            current = next(
                self.__iterator  # type: ignore
            )
            key: TKey = self.__key_selector(current)
            if key in self.__set:
                continue
            return current


@final
class InterceptSequence(LinqSequence[T], Generic[T]):
    """積集合のシーケンスを表します。
    """

    def __init__(self, source: LinqSequence[T], target: Iterable[T]) -> None:
        """InterceptSequence[T]の新しいインスタンスを初期化します。

        Args:
            source (LinqSequence[T]): 読み込むシーケンス
            target (Iterable[T]): 比較集合
        """
        super().__init__()
        self.__source: LinqSequence[T] = source
        self.__target: Iterable[T] = target
        self.__set: set[T] = set[T]()
        self.__iterator: Iterator[T] | None = None

    def _in_iteration(self) -> bool:
        return not self.__iterator is None

    def _start_iteration(self) -> None:
        self.__source._start_iteration()
        self.__iterator = iter(self.__source)
        self.__set.update(self.__target)

    def _stop_iteration(self) -> None:
        self.__source._stop_iteration()
        self.__iterator = None
        self.__set.clear()

    def _get_next(self) -> T:
        current: T
        while True:
            current = next(
                self.__iterator  # type: ignore
            )
            if not current in self.__set:
                continue
            return current


@final
class InterceptBySequence(LinqSequence[T], Generic[T, TKey]):
    """積集合のシーケンスを表します。
    """

    def __init__(self, source: LinqSequence[T], target: Iterable[T], key_selector: Callable[[T], TKey]) -> None:
        """InterceptBySequence[T]の新しいインスタンスを初期化します。

        Args:
            source (LinqSequence[T]): 読み込むシーケンス
            target (Iterable[T]): 比較集合
            key_selector (Callable[[T], TKey]): 比較時のキーを生成する関数
        """
        super().__init__()
        self.__source: LinqSequence[T] = source
        self.__target: Iterable[T] = target
        self.__key_selector: Callable[[T], TKey] = key_selector
        self.__set: set[TKey] = set[TKey]()
        self.__iterator: Iterator[T] | None = None

    def _in_iteration(self) -> bool:
        return not self.__iterator is None

    def _start_iteration(self) -> None:
        self.__source._start_iteration()
        self.__iterator = iter(self.__source)
        self.__set.update(map(self.__key_selector, self.__target))

    def _stop_iteration(self) -> None:
        self.__source._stop_iteration()
        self.__iterator = None
        self.__set.clear()

    def _get_next(self) -> T:
        current: T
        while True:
            current = next(
                self.__iterator  # type: ignore
            )
            key: TKey = self.__key_selector(current)
            if not key in self.__set:
                continue
            return current
