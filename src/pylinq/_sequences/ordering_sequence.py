from typing import Callable, Generic

from .. import LinqSequence, OrderedLinqSequence
from ..type_variants import *


class OrderedLinqSequenceImpl(OrderedLinqSequence[T], Generic[T, TKey]):
    """OrderedLinqSequenceの実装です。
    """

    def __init__(self, source: LinqSequence[T], key_selector: Callable[[T], TKey], descending: bool, parent: "OrderedLinqSequence[T] | None") -> None:
        super().__init__()
        self.__source: LinqSequence[T] = source
        self.__key_selector: Callable[[T], TKey] = key_selector
        self.__descending: bool = descending
        self.__parent: OrderedLinqSequence[T] | None = parent
        self.__iterated: list[T] = list[T]()
        self.__keys: list[tuple[TKey, int]] = list[tuple[TKey, int]]()
        self.__index_selector: Callable[[int], int]
        self.__index: int = 0

    def __index_selector_ascending(self, value: int) -> int:
        """昇順列挙時のインデックスの導出する関数です。

        Args:
            value (int): 通常インデックス

        Returns:
            int: 昇順インデックス
        """
        return value

    def __index_selector_descending(self, value: int) -> int:
        """降順列挙時のインデックスの導出する関数です。

        Args:
            value (int): 通常インデックス

        Returns:
            int: 降順インデックス
        """
        return len(self.__keys) - value - 1

    def _in_iteration(self) -> bool:
        return self.__index > 0

    def _start_iteration(self) -> None:
        values: list[T] = self.__iterated
        values.extend(self.__source.to_list())
        keys: list[tuple[TKey, int]] = self.__keys
        keys.extend(map(lambda x: (self.__key_selector(x), 0), values))
        for i in range(len(values)):
            keys[i] = (keys[i][0], i)

        keys.sort(key=lambda x: x[0])  # type:ignore

        self.__index_selector = self.__index_selector_descending if self.__descending else self.__index_selector_ascending

    def _stop_iteration(self) -> None:
        self.__index = 0
        self.__iterated.clear()
        self.__keys.clear()

    def _get_next(self) -> T:
        if self.__index == len(self.__keys):
            raise StopIteration()
        i: int = self.__index_selector(self.__index)
        self.__index += 1
        return self.__iterated[self.__keys[i][1]]

    def _create_oredered_sequence(self, key_selector: Callable[[T], T2], descending: bool) -> OrderedLinqSequence[T]:
        return OrderedLinqSequenceImpl[T, tuple[TKey, T2]](self.__source, lambda x: (self.__key_selector(x), key_selector(x)), descending, self)
