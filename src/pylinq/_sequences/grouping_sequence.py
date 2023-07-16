from typing import Generic, Hashable, Iterator, Sized, final

from .. import Grouping, LinqSequence, Lookup
from ..type_variants import *


@final
class GroupingImpl(Grouping[TKey, T], Sized, Hashable, Generic[TKey, T]):
    """Grouping[TKey, T]の実装です。
    """
    @property
    def key(self) -> TKey:
        return self.__key

    def __init__(self, key: TKey) -> None:
        """GroupingImpl[TKey, T]の新しいインスタンスを初期化します。

        Args:
            key (TKey): キー
        """
        super().__init__()
        self.__key: TKey = key
        self.__values: list[T] = list[T]()
        self.__iterator: Iterator[T] | None = None

    def add(self, value: T) -> None:
        """値を追加します。

        Args:
            value (T): 追加する値
        """
        self.__values.append(value)

    def _in_iteration(self) -> bool:
        return not self.__iterator is None

    def _start_iteration(self) -> None:
        self.__iterator = iter(self.__values)

    def _stop_iteration(self) -> None:
        self.__iterator = None

    def _get_next(self) -> T:
        return next(self.__iterator)  # type: ignore

    def __len__(self) -> int:
        return len(self.__values)

    def __hash__(self) -> int:
        return hash(self.key)


class LookupImpl(Lookup[TKey, TValue], Generic[TKey, TValue]):
    """Lookup[TKey, TValue]の実装です。
    """

    def __init__(self) -> None:
        """LookupImpl[TKey, TValue]の新しいインスタンスを初期化します。
        """
        super().__init__()
        self.__source: dict[TKey, GroupingImpl[TKey, TValue]] = dict[TKey, GroupingImpl[TKey, TValue]]()
        self.__key_iterator: Iterator[TKey] | None = None

    def contains_key(self, key: TKey) -> bool:
        return key in self.__source

    def get_or_add_grouping(self, key: TKey) -> GroupingImpl[TKey, TValue]:
        """キーに基づくGroupingのインスタンスを取得します。
        存在しない場合は生成して追加します。

        Args:
            key (TKey): キー

        Returns:
            GroupingImpl[TKey, TValue]: keyに基づく存在するまたは生成されたインスタンス
        """
        if key in self.__source:
            return self.__source[key]
        result = GroupingImpl[TKey, TValue](key)
        self.__source[key] = result
        return result

    def get_grouping(self, key: TKey) -> GroupingImpl[TKey, TValue] | None:
        """キーに基づくGroupingのインスタンスを取得します。

        Args:
            key (TKey): キー

        Returns:
            GroupingImpl[TKey, TValue] | None: keyに基づくインスタンス。存在しない場合はNone
        """
        if key in self.__source:
            return self.__source[key]
        return None

    def _in_iteration(self) -> bool:
        return not self.__key_iterator is None

    def _start_iteration(self) -> None:
        self.__key_iterator = iter(self.__source)

    def _stop_iteration(self) -> None:
        self.__key_iterator = None

    def _get_next(self) -> Grouping[TKey, TValue]:
        key: TKey = next(
            self.__key_iterator  # type: ignore
        )
        return self.__source[key]

    def __getitem__(self, key: TKey) -> LinqSequence[TValue]:
        return self.__source.get(key, LinqSequence[TValue].empty())

    def __len__(self) -> int:
        return len(self.__source)
