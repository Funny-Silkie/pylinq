from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING, Callable, Generator, Generic, Iterable, Iterator, Sized, overload

from .type_variants import *
if TYPE_CHECKING:
    from .grouping import Grouping, Lookup


class LinqSequence(Generic[T], Iterator[T], metaclass=ABCMeta):
    """LINQのシーケンスを表します。
    """

    def __init__(self) -> None:
        """LinqSequence[T]の新しいインスタンスを初期化します。
        """
        pass

    def __iter__(self) -> Iterator[T]:
        if self._in_iteration() is not None:
            self._stop_iteration()
        return self

    def __next__(self) -> T:
        if not self._in_iteration():
            self._start_iteration()
        try:
            current: T = self._get_next()
            return current
        except StopIteration:
            self._stop_iteration()
            raise

    @abstractmethod
    def _in_iteration(self) -> bool:
        """インスタンスが列挙中かどうかを取得します。

        Returns:
            bool: インスタンスが列挙中の場合はTrue，それ以外でFalse
        """
        ...

    @abstractmethod
    def _start_iteration(self) -> None:
        """列挙を開始します。
        """
        ...

    @abstractmethod
    def _stop_iteration(self) -> None:
        """列挙を停止します。
        """
        ...

    @abstractmethod
    def _get_next(self) -> T:
        """次に列挙する値を取得します。

        Returns:
            T: 次に列挙する値
        """
        ...

    # From

    @classmethod
    def from_iterable(cls, source: Iterable[T]) -> "LinqSequence[T]":
        """イテラブルなオブジェクトからシーケンスを生成します。

        Args:
            source (Iterable[T]): イテラブルなオブジェクト

        Returns:
            LinqSequence[T]: sourceを持つシーケンスのインスタンス
        """
        from ._sequences import FromSequence, SizedFromSequence
        if isinstance(source, Sized):
            return SizedFromSequence[T](source)
        return FromSequence[T](source)

    @classmethod
    def from_dict(cls, source: dict[TKey, TValue]) -> "LinqSequence[tuple[TKey, TValue]]":
        """辞書からシーケンスを生成します。

        Args:
            source (dict[TKey, TValue]): 辞書

        Returns:
            LinqSequence[tuple[TKey, TValue]]: sourceを持つシーケンスのインスタンス
        """
        from ._sequences import DictSequence
        return DictSequence[TKey, TValue](source)

    @classmethod
    def from_generator(cls, func: Callable[*TArgs, Generator[T, None, None]], *args: *TArgs) -> "LinqSequence[T]":  # type: ignore
        """Generatorからシーケンスを生成します。

        Args:
            func (Callable[[*TArgs], Generator[T, None, None]]): Generatorを生成する関数
            args: funcに与える引数

        Returns:
            LinqSequence[T]: funcによるGeneratorを持つシーケンスのインスタンス
        """
        from ._sequences import GeneratorSequence
        return GeneratorSequence[T](func, *args)

    # Create

    @classmethod
    def empty(cls) -> "LinqSequence[T]":
        """空のシーケンスを取得します。

        Returns:
            LinqSequence[T]: 空のシーケンス
        """
        from ._sequences import EmptySequence
        return EmptySequence[T]()

    @classmethod
    def range(cls, start: int, count: int) -> "LinqSequence[int]":
        """指定した範囲の整数を列挙するシーケンスを生成します。

        Args:
            start (int): 開始値
            count (int): 列挙する個数

        Raises:
            ValueError: countが0未満

        Returns:
            LinqSequence[int]: 指定した範囲の整数を列挙するシーケンス
        """
        from ._sequences import RangeSequence
        if count < 0:
            raise ValueError("parameter 'count' must be 0 or positive value")
        if count == 0:
            return LinqSequence[int].empty()
        return RangeSequence(start, count)

    @classmethod
    def repeat(cls, value: T, count: int) -> "LinqSequence[T]":
        """単一の値を繰り返し列挙するシーケンスを生成します。

        Args:
            value (T): 列挙する値
            count (int): 列挙する個数

        Raises:
            ValueError: countが0未満

        Returns:
            LinqSequence[T]: 単一の値を繰り返し列挙するシーケンス
        """
        from ._sequences import RepeatSequence
        if count < 0:
            raise ValueError("parameter 'count' must be 0 or positive value")
        if count == 0:
            return cls.empty()
        return RepeatSequence(value, count)

    def default_if_empty(self, default: T) -> "LinqSequence[T]":
        """シーケンスが空の場合に既定値を一つ与えるシーケンスを取得します。

        Args:
            default (T): シーケンスが空の場合の既定値

        Returns:
            LinqSequence[T]: シーケンスが空の場合に既定値を一つ与えるシーケンス
        """

        def inner(source: LinqSequence[T], default: T) -> Generator[T, None, None]:
            iterator: Iterator[T] = iter(source)
            try:
                yield next(iterator)
            except StopIteration:
                yield default
            while True:
                try:
                    yield next(iterator)
                except StopIteration:
                    return

        return self.from_generator(inner, self, default)

    # Concatination

    def concat(self, iterable: Iterable[T]) -> "LinqSequence[T]":
        """末尾にシーケンスを結合します。

        Args:
            iterable (Iterable[T]): 末尾に結合するシーケンス

        Returns:
            LinqSequence[T]: 結合のシーケンス
        """
        from ._sequences import ConcatSequence
        return ConcatSequence[T](self, iterable)

    def append(self, value: T) -> "LinqSequence[T]":
        """シーケンスの末尾に要素を追加します。

        Args:
            value (T): 追加する要素

        Returns:
            LinqSequence[T]: 追加後のシーケンス
        """
        from ._sequences import ApPrependSequence
        return ApPrependSequence[T](self, value, True)

    def prepend(self, value: T) -> "LinqSequence[T]":
        """シーケンスの先頭に要素を追加します。

        Args:
            value (T): 追加する要素

        Returns:
            LinqSequence[T]: 追加後のシーケンス
        """
        from ._sequences import ApPrependSequence
        return ApPrependSequence[T](self, value, False)

    # Get (Single value)

    def element_at(self, index: int) -> T:
        """指定したインデックスの要素を取得します。

        Args:
            index (int): 検索インデックス

        Raises:
            ValueError: indexが0未満
            IndexError: indexが要素数以上

        Returns:
            T: indexに対応する要素
        """
        if index < 0:
            raise ValueError("parameter 'index' must be 0 or positive value")
        i: int = 0
        for current in self:
            if i == index:
                return current
            i += 1
        raise IndexError()

    def element_at_or_default(self, index: int, default: T) -> T:
        """指定したインデックスの要素を取得します。

        Args:
            index (int): 検索インデックス
            default (T): 要素が見つからない場合の既定値

        Raises:
            ValueError: indexが0未満

        Returns:
            T: indexに対応する要素，見つからない場合はdefault
        """
        if index < 0:
            raise ValueError("parameter 'index' must be 0 or positive value")
        i: int = 0
        for current in self:
            if i == index:
                return current
            i += 1
        return default

    @overload
    def first(self, match: None = None) -> T:
        """先頭の要素を取得します。

        Raises:
            ValueError: シーケンスが空

        Returns:
            T: 先頭の要素
        """
        ...

    @overload
    def first(self, match: Callable[[T], bool]) -> T:
        """条件に適合する先頭の要素を取得します。

        Args:
            match (Callable[[T], bool]): 要素の条件

        Raises:
            ValueError: 条件に適合する先頭の要素が存在しない

        Returns:
            T: matchに適合する末尾の要素
        """
        ...

    def first(self, match: Callable[[T], bool] | None = None) -> T:
        iterator: Iterator[T] = iter(self)
        if match is None:
            try:
                return next(iterator)
            except StopIteration:
                raise ValueError("sequence is empty")
        for current in self:
            if match(current):
                return current
        raise ValueError("the element which matches the condition is not found")

    @overload
    def first_or_default(self, default: T, match: None = None) -> T:
        """先頭の要素を取得します。

        Args:
            default (T): 要素が見つからない場合の既定値

        Returns:
            T: 先頭の要素，見つからない場合はdefault
        """
        ...

    @overload
    def first_or_default(self, default: T, match: Callable[[T], bool]) -> T:
        """条件に適合する先頭の要素を取得します。

        Args:
            default (T): 要素が見つからない場合の既定値
            match (Callable[[T], bool]): 要素の条件

        Returns:
            T: matchに適合する先頭の要素，見つからない場合はdefault
        """
        ...

    def first_or_default(self, default: T, match: Callable[[T], bool] | None = None) -> T:
        iterator: Iterator[T] = iter(self)
        if match is None:
            try:
                return next(iterator)
            except StopIteration:
                return default
        for current in self:
            if match(current):
                return current
        return default

    @overload
    def last(self, match: None = None) -> T:
        """末尾の要素を取得します。

        Raises:
            ValueError: シーケンスが空

        Returns:
            T: 末尾の要素
        """
        ...

    @overload
    def last(self, match: Callable[[T], bool]) -> T:
        """条件に適合する末尾の要素を取得します。

        Args:
            match (Callable[[T], bool]): 要素の条件

        Raises:
            ValueError: 条件に適合する末尾の要素が存在しない

        Returns:
            T: matchに適合する末尾の要素
        """
        ...

    def last(self, match: Callable[[T], bool] | None = None) -> T:
        iterator: Iterator[T] = iter(self)
        result: T
        if match is None:
            try:
                result = next(iterator)
            except StopIteration:
                raise ValueError("sequence is empty")
            while True:
                try:
                    result = next(iterator)
                except StopIteration:
                    return result
        found: bool = False
        for current in self:
            if match(current):
                result = current
                found = True
        if found:
            return result
        raise ValueError("the element which matches the condition is not found")

    @overload
    def last_or_default(self, default: T, match: None = None) -> T:
        """末尾の要素を取得します。

        Args:
            default (T): 要素が見つからない場合の既定値

        Returns:
            T: 末尾の要素，見つからない場合はdefault
        """
        ...

    @overload
    def last_or_default(self, default: T, match: Callable[[T], bool]) -> T:
        """条件に適合する末尾の要素を取得します。

        Args:
            default (T): 要素が見つからない場合の既定値
            match (Callable[[T], bool]): 要素の条件

        Returns:
            T: matchに適合する末尾の要素，見つからない場合はdefault
        """
        ...

    def last_or_default(self, default: T, match: Callable[[T], bool] | None = None) -> T:
        iterator: Iterator[T] = iter(self)
        result: T
        if match is None:
            try:
                result = next(iterator)
            except StopIteration:
                return default
            while True:
                try:
                    result = next(iterator)
                except StopIteration:
                    return result
        found: bool = False
        for current in self:
            if match(current):
                result = current
                found = True
        if found:
            return result
        return default

    @overload
    def single(self, match: None = None) -> T:
        """単一の要素を取得します。

        Raises:
            ValueError: シーケンスが空または2つ以上の要素を持つ

        Returns:
            T: 単一の要素
        """
        ...

    @overload
    def single(self, match: Callable[[T], bool]) -> T:
        """条件に適合する単一の要素を取得します。

        Args:
            match (Callable[[T], bool]): 要素の条件

        Raises:
            ValueError: 条件に適合する単一の要素が存在しないまたは2つ以上存在する

        Returns:
            T: matchに適合する単一の要素
        """
        ...

    def single(self, match: Callable[[T], bool] | None = None) -> T:
        iterator: Iterator[T] = iter(self)
        result: T
        if match is None:
            try:
                result = next(iterator)
            except StopIteration:
                raise ValueError("sequence is empty")
            try:
                next(iterator)
                raise ValueError("sequence has more than one elements")
            except StopIteration:
                return result
        found: bool = False
        for current in self:
            if match(current):
                if found:
                    raise ValueError("more than one elements which meet the condition are found")
                result = current
                found = True
        if found:
            return result
        raise ValueError("the element which matches the condition is not found")

    @overload
    def single_or_default(self, default: T, match:  None = None) -> T:
        """条件に適合する単一の要素を取得します。

        Args:
            default (T): シーケンスが空の場合の既定値

        Raises:
            ValueError: シーケンスに要素が2つ以上存在する

        Returns:
            T: 単一の要素，見つからない場合はdefault
        """
        ...

    @overload
    def single_or_default(self, default: T, match: Callable[[T], bool]) -> T:
        """条件に適合する単一の要素を取得します。

        Args:
            default (T): 要素が見つからない場合の既定値
            match (Callable[[T], bool]): 要素の条件

        Raises:
            ValueError: 条件に適合する要素が2つ以上存在する

        Returns:
            T: matchに適合する単一の要素，見つからない場合はdefault
        """
        ...

    def single_or_default(self, default: T, match: Callable[[T], bool] | None = None) -> T:
        iterator: Iterator[T] = iter(self)
        result: T
        if match is None:
            try:
                result = next(iterator)
            except StopIteration:
                return default
            try:
                next(iterator)
                raise ValueError("sequence has more than one elements")
            except StopIteration:
                return result
        found: bool = False
        for current in self:
            if match(current):
                if found:
                    raise ValueError("more than one elements which meet the condition are found")
                result = current
                found = True
        if found:
            return result
        return default

    # Filtering

    @overload
    def where(self, match: Callable[[T], bool]) -> "LinqSequence[T]":
        """要素の絞り込みを行います。

        Args:
            match (Callable[[T], bool]): 要素に基づく絞り込み関数

        Returns:
            LinqSequence[T]: 絞り込み後のシーケンス
        """
        ...

    @overload
    def where(self, match: Callable[[T, int], bool]) -> "LinqSequence[T]":
        """要素の絞り込みを行います。

        Args:
            match (Callable[[T, int], bool]): 要素とインデックスに基づく絞り込み関数

        Returns:
            LinqSequence[T]: 絞り込み後のシーケンス
        """
        ...

    def where(self, match: Callable[[T], bool] | Callable[[T, int], bool]) -> "LinqSequence[T]":
        from ._sequences import WhereSequence
        from ._common import get_parameter_count
        if get_parameter_count(match) == 1:
            match1: Callable[[T], bool] = match  # type: ignore
            return WhereSequence[T](self, lambda x, _: match1(x))
        match2: Callable[[T, int], bool] = match  # type: ignore
        return WhereSequence[T](self, match2)

    def of_type(self, target: type[TResult]) -> "LinqSequence[TResult]":
        """指定した型で絞り込みを行います。

        Args:
            target (type[TResult]): 絞り込む型

        Returns:
            LinqSequence[TResult]: 絞り込み後のシーケンス
        """
        result: LinqSequence[TResult] = self.where(lambda x: isinstance(x, target))  # type: ignore
        return result

    # Grouping

    @overload
    def to_look_up(self, key_selector: Callable[[T], TKey], value_selector: None = None) -> "Lookup[TKey, T]":
        """Lookup[TKey, T]に変換します。

        Args:
            key_selector (Callable[[T], TKey]): キーを生成する関数

        Returns:
            Lookup[TKey, T]: 生成されたLookup[TKey, T]のインスタンス
        """
        ...

    @overload
    def to_look_up(self, key_selector: Callable[[T], TKey], value_selector: Callable[[T], TValue]) -> "Lookup[TKey, TValue]":
        """Lookup[TKey, TValue]に変換します。

        Args:
            key_selector (Callable[[T], TKey]): キーを生成する関数
            value_selector (Callable[[T], TValue]): 値を生成する関数

        Returns:
            Lookup[TKey, TValue]: 生成されたLookup[TKey, TValue]のインスタンス
        """
        ...

    def to_look_up(self, key_selector: Callable[[T], TKey], value_selector: Callable[[T], TValue] | None = None) -> "Lookup[TKey, T] | Lookup[TKey, TValue]":
        from ._sequences import GroupingImpl, LookupImpl
        result: LookupImpl[TKey, T] | LookupImpl[TKey, TValue]
        current_key: TKey
        if value_selector is None:
            result = LookupImpl[TKey, T]()
            for current in self:
                current_key = key_selector(current)
                grouping1: GroupingImpl[TKey, T] = result.get_or_add_grouping(current_key)
                grouping1.add(current)
            return result

        result = LookupImpl[TKey, TValue]()
        for current in self:
            current_key = key_selector(current)
            grouping2: GroupingImpl[TKey, TValue] = result.get_or_add_grouping(current_key)
            grouping2.add(value_selector(current))
        return result

    @overload
    def group_by(self, key_selector: Callable[[T], TKey], element_selector: None = None) -> "LinqSequence[Grouping[TKey, T]]":
        """グループ化を行います。

        Args:
            key_selector (Callable[[T], TKey]): 要素からキーを選択する関数

        Returns:
            LinqSequence[Grouping[TKey, T]]: グループ化後のシーケンス
        """
        ...

    @overload
    def group_by(self, key_selector: Callable[[T], TKey], element_selector: Callable[[T], T2]) -> "LinqSequence[Grouping[TKey, T2]]":
        """グループ化を行います。

        Args:
            key_selector (Callable[[T], TKey]): 要素からキーを選択する関数
            element_selector (Callable[[T], T2]): 要素を変換する関数

        Returns:
            LinqSequence[Grouping[TKey, T2]]: グループ化後のシーケンス
        """
        ...

    @overload
    def group_by(self, key_selector: Callable[[T], TKey], element_selector: None, result_selector: "Callable[[TKey, LinqSequence[T]], TResult]") -> "LinqSequence[TResult]":
        """グループ化を行います。

        Args:
            key_selector (Callable[[T], TKey]): 要素からキーを選択する関数
            element_selector None: 必ずNoneにすること
            result_selector (Callable[[TKey, LinqSequence[T]], TResult]): キーとグループ化された要素を最終的に変換する関数

        Returns:
            LinqSequence[TResult]: グループ化後のシーケンス
        """
        ...

    @overload
    def group_by(self, key_selector: Callable[[T], TKey], element_selector: Callable[[T], T2], result_selector: "Callable[[TKey, LinqSequence[T2]], TResult]") -> "LinqSequence[TResult]":
        """グループ化を行います。

        Args:
            key_selector (Callable[[T], TKey]): 要素からキーを選択する関数
            element_selector (Callable[[T], T2]): 要素を変換する関数
            result_selector (Callable[[TKey, LinqSequence[T2]], TResult]): キーとグループ化された要素を最終的に変換する関数

        Returns:
            LinqSequence[TResult]: グループ化後のシーケンス
        """
        ...

    def group_by(
        self,
        key_selector: Callable[[T], TKey],
        element_selector: Callable[[T], T2] | None = None,
        result_selector: "Callable[[TKey, LinqSequence[T]], TResult] | Callable[[TKey, LinqSequence[T2]], TResult] | None" = None
    ) -> "LinqSequence[Grouping[TKey, T]] | LinqSequence[Grouping[TKey, T2]] | LinqSequence[TResult]":
        if not TYPE_CHECKING:
            from .grouping import Grouping, Lookup

        if result_selector is None:
            # group_by(self, key_selector: Callable[[T], TKey]) -> "LinqSequence[Grouping[TKey, T]]"
            if element_selector is None:
                def inner1(source: LinqSequence[T], key_selector: Callable[[T], TKey]) -> Generator[Grouping[TKey, T], None, None]:
                    look_up: Lookup[TKey, T] = source.to_look_up(key_selector)
                    yield from look_up

                return LinqSequence[Grouping[TKey, T]].from_generator(inner1, self, key_selector)
            # group_by(self, key_selector: Callable[[T], TKey], element_selector: Callable[[T], T2]) -> "LinqSequence[Grouping[TKey, T2]]":
            else:
                def inner2(source: LinqSequence[T], key_selector: Callable[[T], TKey], element_selector: Callable[[T], T2]) -> Generator[Grouping[TKey, T2], None, None]:
                    look_up: Lookup[TKey, T2] = source.to_look_up(key_selector, element_selector)
                    yield from look_up

                return LinqSequence[Grouping[TKey, T2]].from_generator(inner2, self, key_selector, element_selector)
        else:
            # group_by(self, key_selector: Callable[[T], TKey], result_selector: Callable[[TKey, LinqSequence[T]], TResult]) -> "LinqSequence[TResult]":
            if element_selector is None:
                def inner3(source: LinqSequence[T], key_selector: Callable[[T], TKey], result_selector: Callable[[TKey, LinqSequence[T]], TResult]) -> Generator[TResult, None, None]:
                    look_up: Lookup[TKey, T] = source.to_look_up(key_selector)
                    for current in look_up:
                        yield result_selector(current.key, current)

                return LinqSequence[TResult].from_generator(inner3, self, key_selector, result_selector)
            # group_by(self, key_selector: Callable[[T], TKey], element_selector: Callable[[T], T2], result_selector: Callable[[TKey, LinqSequence[T2]], TResult]) -> "LinqSequence[TResult]":
            else:
                def inner4(source: LinqSequence[T], key_selector: Callable[[T], TKey], element_selector: Callable[[T], T2], result_selector: Callable[[TKey, LinqSequence[T2]], TResult]) -> Generator[TResult, None, None]:
                    look_up: Lookup[TKey, T2] = source.to_look_up(key_selector, element_selector)
                    for current in look_up:
                        yield result_selector(current.key, current)

                return LinqSequence[TResult].from_generator(inner4, self, key_selector, element_selector, result_selector)

    # Set operation

    def distinct(self) -> "LinqSequence[T]":
        """一意の要素からなるシーケンスに変換します。

        Returns:
            LinqSequence[T]: 一意の要素からなるシーケンス
        """
        def inner(source: LinqSequence[T]) -> Generator[T, None, None]:
            already_iterated = set[T]()
            for current in source:
                if current in already_iterated:
                    continue
                yield current
                already_iterated.add(current)
        return self.from_generator(inner, self)

    def distinct_by(self, key_selector: Callable[[T], TKey]) -> "LinqSequence[T]":
        """一意の要素からなるシーケンスに変換します。

        Args:
            key_selector (Callable[[T], TKey]): 要素の比較に用いる値を導出する関数

        Returns:
            LinqSequence[T]: 一意の要素からなるシーケンス
        """
        def inner(source: LinqSequence[T], key_selector: Callable[[T], TKey]) -> Generator[T, None, None]:
            already_iterated = set[TKey]()
            for current in source:
                key: TKey = key_selector(current)
                if key in already_iterated:
                    continue
                yield current
                already_iterated.add(key)
        return self.from_generator(inner, self, key_selector)

    # Partitioning

    def skip(self, count: int) -> "LinqSequence[T]":
        """先頭から指定した要素数をスキップするシーケンスを取得します。

        Args:
            count (int): スキップする要素数

        Returns:
            LinqSequence[T]: スキップ後のシーケンス
        """
        def inner(source: LinqSequence[T], count: int) -> Generator[T, None, None]:
            iterator: Iterator[T] = iter(source)
            try:
                for _ in range(count):
                    next(iterator)
                while True:
                    yield next(iterator)
            except StopIteration:
                return

        return self.from_generator(inner, self, count)

    def skip_last(self, count: int) -> "LinqSequence[T]":
        """末尾から指定した要素数をスキップするシーケンスを取得します。

        Args:
            count (int): スキップする要素数

        Returns:
            LinqSequence[T]: スキップ後のシーケンス
        """
        def inner(source: LinqSequence[T], count: int) -> Generator[T, None, None]:
            elements = source.to_list()
            yield from LinqSequence.from_iterable(elements).take(len(elements) - count)

        return self.from_generator(inner, self, count)

    @overload
    def skip_while(self, match: Callable[[T], bool]) -> "LinqSequence[T]":
        """指定した条件の間要素をスキップするシーケンスを取得します。

        Args:
            match (Callable[[T], bool]): 要素に基づくスキップの継続条件

        Returns:
            LinqSequence[T]: スキップ後のシーケンス
        """
        ...

    @overload
    def skip_while(self, match: Callable[[T, int], bool]) -> "LinqSequence[T]":
        """指定した条件の間要素をスキップするシーケンスを取得します。

        Args:
            match (Callable[[T, int], bool]): 要素とインデックスに基づくスキップの継続条件

        Returns:
            LinqSequence[T]: スキップ後のシーケンス
        """
        ...

    def skip_while(self, match: Callable[[T], bool] | Callable[[T, int], bool]) -> "LinqSequence[T]":
        from ._common import get_parameter_count

        def inner(source: LinqSequence[T], match: Callable[[T, int], bool]) -> Generator[T, None, None]:
            iterator: Iterator[T] = iter(source)
            try:
                index: int = 0
                while True:
                    current: T = next(iterator)
                    if not match(current, index):
                        yield current
                        break
                    index += 1
                while True:
                    yield next(iterator)
            except StopIteration:
                return

        if get_parameter_count(match) == 1:
            match1: Callable[[T], bool] = match  # type: ignore
            return self.from_generator(inner, self, lambda x, _: match1(x))
        match2: Callable[[T, int], bool] = match  # type: ignore
        return self.from_generator(inner, self, match2)

    def take(self, count: int) -> "LinqSequence[T]":
        """先頭から指定した個数分要素を取得します。

        Args:
            count (int): 取得する要素数

        Returns:
            LinqSequence[T]: 指定した個数分の要素を持つシーケンス
        """
        from ._sequences import TakeSequence
        if count <= 0:
            return self.empty()
        return TakeSequence[T](self, count)

    def take_last(self, count: int) -> "LinqSequence[T]":
        """末尾から指定した個数分要素を取得します。

        Args:
            count (int): 取得する要素数

        Returns:
            LinqSequence[T]: 指定した個数分の要素を持つシーケンス
        """
        from ._sequences import TakeLastSequence
        if count <= 0:
            return self.empty()
        return TakeLastSequence[T](self, count)

    @overload
    def take_while(self, match: Callable[[T], bool]) -> "LinqSequence[T]":
        """指定した条件の間列挙を続けるシーケンスを取得します。

        Args:
            match (Callable[[T], bool]): 要素に基づく列挙の継続条件

        Returns:
            LinqSequence[T]: 指定した条件の間列挙を続けるシーケンス
        """
        ...

    @overload
    def take_while(self, match: Callable[[T, int], bool]) -> "LinqSequence[T]":
        """指定した条件の間列挙を続けるシーケンスを取得します。

        Args:
            match (Callable[[T, int], bool]): 要素とインデックスに基づく列挙の継続条件

        Returns:
            LinqSequence[T]: 指定した条件の間列挙を続けるシーケンス
        """
        ...

    def take_while(self, match: Callable[[T], bool] | Callable[[T, int], bool]) -> "LinqSequence[T]":
        from ._common import get_parameter_count
        from ._sequences import TakeWhileSequence

        if get_parameter_count(match) == 1:
            match1: Callable[[T], bool] = match  # type: ignore
            return TakeWhileSequence[T](self, lambda x, _: match1(x))
        match2: Callable[[T, int], bool] = match  # type: ignore
        return TakeWhileSequence[T](self, match2)

    # Projection
    @overload
    def select(self, selector: Callable[[T], TResult]) -> "LinqSequence[TResult]":
        """要素の変換を行います。

        Args:
            selector (Callable[[T], TResult]): 要素を基に変換を行う関数

        Returns:
            LinqSequence[TResult]: 変換後のシーケンス
        """
        ...

    @overload
    def select(self, selector: Callable[[T, int], TResult]) -> "LinqSequence[TResult]":
        """要素の変換を行います。

        Args:
            selector (Callable[[T, int], TResult]): 要素とインデックスを基に変換を行う関数

        Returns:
            LinqSequence[TResult]: 変換後のシーケンス
        """
        ...

    def select(self, selector: Callable[[T], TResult] | Callable[[T, int], TResult]) -> "LinqSequence[TResult]":
        from ._common import get_parameter_count
        from ._sequences import SelectSequence
        if get_parameter_count(selector) == 1:
            selector1: Callable[[T], TResult] = selector  # type:ignore
            return SelectSequence[T, TResult](self, lambda x, _: selector1(x))
        selector2: Callable[[T, int], TResult] = selector  # type:ignore
        return SelectSequence[T, TResult](self, selector2)

    @overload
    def select_many(self, collection_selector: Callable[[T], Iterable[T2]], result_selector: None = None) -> "LinqSequence[T2]":
        """シーケンスを平坦化します。

        Args:
            collection_selector (Callable[[T], Iterable[T2]]): 要素を基にコレクションを導出する関数

        Returns:
            LinqSequence[T2]: 平坦化後のシーケンス
        """
        ...

    @overload
    def select_many(self, collection_selector: Callable[[T, int], Iterable[T2]], result_selector: None = None) -> "LinqSequence[T2]":
        """シーケンスを平坦化します。

        Args:
            collection_selector (Callable[[T, int], Iterable[T2]]): 要素とインデックスを基にコレクションを導出する関数

        Returns:
            LinqSequence[T2]: 平坦化後のシーケンス
        """
        ...

    @overload
    def select_many(self, collection_selector: Callable[[T], Iterable[T2]], result_selector: Callable[[T2], TResult]) -> "LinqSequence[TResult]":
        """シーケンスを平坦化します。

        Args:
            collection_selector (Callable[[T], Iterable[T2]]): 要素を基にコレクションを導出する関数
            result_selector (Callable[[T2], TResult]): コレクションの要素を変換する関数

        Returns:
            LinqSequence[TResult]: 平坦化後のシーケンス
        """
        ...

    @overload
    def select_many(self, collection_selector: Callable[[T, int], Iterable[T2]], result_selector: Callable[[T2], TResult]) -> "LinqSequence[TResult]":
        """シーケンスを平坦化します。

        Args:
            collection_selector (Callable[[T, int], Iterable[T2]]): 要素とインデックスを基にコレクションを導出する関数
            result_selector (Callable[[T2], TResult]): コレクションの要素を変換する関数

        Returns:
            LinqSequence[TResult]: 平坦化後のシーケンス
        """
        ...

    def select_many(self, collection_selector: Callable[[T], Iterable[T2]] | Callable[[T, int], Iterable[T2]], result_selector: Callable[[T2], TResult] | None = None) -> "LinqSequence[T2] | LinqSequence[TResult]":
        from ._common import get_parameter_count
        c_selector1: Callable[[T], Iterable[T2]]
        c_selector2: Callable[[T, int], Iterable[T2]]
        if result_selector is None:
            # select_many(collection_selector: Callable[[T], Iterable[T2]]) -> LinqSequence[T2]
            if get_parameter_count(collection_selector) == 1:
                def inner1(source: LinqSequence[T], collection_selector: Callable[[T], Iterable[T2]]) -> Generator[T2, None, None]:
                    for current in source:
                        yield from collection_selector(current)
                c_selector1 = collection_selector  # type: ignore
                return LinqSequence[T2].from_generator(inner1, self, c_selector1)
            # select_many(collection_selector: Callable[[T, int], Iterable[T2]]) -> LinqSequence[T2]
            else:
                def inner2(source: LinqSequence[T], collection_selector: Callable[[T, int], Iterable[T2]]) -> Generator[T2, None, None]:
                    index: int = 0
                    for current in source:
                        yield from collection_selector(current, index)
                        index += 1

                c_selector2 = collection_selector  # type: ignore
                return LinqSequence[T2].from_generator(inner2, self, c_selector2)
        else:
            # select_many(collection_selector: Callable[[T], Iterable[T2]], result_selector: Callable[[T2], TResults]) -> LinqSequence[TResult]
            if get_parameter_count(collection_selector) == 1:
                def inner3(source: LinqSequence[T], collection_selector: Callable[[T], Iterable[T2]], result_selector: Callable[[T2], TResult]) -> Generator[TResult, None, None]:
                    for current in source:
                        for intermediate in collection_selector(current):
                            yield result_selector(intermediate)

                c_selector1 = collection_selector  # type: ignore
                return LinqSequence[TResult].from_generator(inner3, self, c_selector1, result_selector)
            # select_many(collection_selector: Callable[[T], Iterable[T2, int]], result_selector: Callable[[T2], TResults]) -> LinqSequence[TResult]
            else:
                def inner4(source: LinqSequence[T], collection_selector: Callable[[T, int], Iterable[T2]], result_selector: Callable[[T2], TResult]) -> Generator[TResult, None, None]:
                    index: int = 0
                    for current in source:
                        for intermediate in collection_selector(current, index):
                            yield result_selector(intermediate)
                        index += 1

                c_selector2 = collection_selector  # type: ignore
                return LinqSequence[TResult].from_generator(inner4, self, c_selector2, result_selector)

    @overload
    def zip(self, after: Iterable[T2], result_selector: None = None) -> "LinqSequence[tuple[T, T2]]":
        """シーケンスの要素同士を結合します。

        Args:
            after (Iterable[T2]): 結合するシーケンス

        Returns:
            LinqSequence[tuple[T, T2]]: 結合後のシーケンス
        """
        ...

    @overload
    def zip(self, after: Iterable[T2], result_selector: Callable[[T, T2], TResult]) -> "LinqSequence[TResult]":
        """シーケンスの要素同士を結合します。

        Args:
            after (Iterable[T2]): 結合するシーケンス
            result_selector (Callable[[T, T2], TResult]): 要素を結合する関数

        Returns:
            LinqSequence[TResult]: 結合後のシーケンス
        """
        ...

    def zip(self, after: Iterable[T2], result_selector: Callable[[T, T2], TResult] | None = None) -> "LinqSequence[tuple[T, T2]] | LinqSequence[TResult]":
        def inner(first: LinqSequence[T], second: LinqSequence[T2], result_selector: Callable[[T, T2], TResult]) -> Generator[TResult, None, None]:
            iter1: Iterator[T] = iter(first)
            iter2: Iterator[T2] = iter(second)
            while True:
                try:
                    yield result_selector(next(iter1), next(iter2))
                except StopIteration:
                    return

        if result_selector is None:
            return LinqSequence[tuple[T, T2]].from_generator(inner, self, after, lambda x, y: (x, y))
        return LinqSequence[TResult].from_generator(inner, self, after, result_selector)

    # Convert to collection

    def to_list(self) -> list[T]:
        """リストに変換します。

        Returns:
            list[T]: インスタンスの要素を格納するリストの新しいインスタンス
        """
        return list[T](self)

    @overload
    def to_dict(self, key_selector: Callable[[T], TKey], value_selector: None = None) -> dict[TKey, T]:
        """辞書に変換します。

        Args:
            key_selector (Callable[[T], TKey]): キーを生成する関数

        Returns:
            dict[TKey, T]: インスタンスの要素を格納する辞書の新しいインスタンス
        """
        ...

    @overload
    def to_dict(self, key_selector: Callable[[T], TKey], value_selector: Callable[[T], TValue]) -> dict[TKey, TValue]:
        """辞書に変換します。

        Args:
            key_selector (Callable[[T], TKey]): キーを生成する関数
            value_selector (Callable[[T], TValue]): 値を生成する関数

        Returns:
            dict[TKey, TValue]: インスタンスの要素を格納する辞書の新しいインスタンス
        """
        ...

    def to_dict(self, key_selector: Callable[[T], TKey], value_selector: Callable[[T], TValue] | None = None) -> dict[TKey, T] | dict[TKey, TValue]:
        result: dict[TKey, T] | dict[TKey, TValue]

        if value_selector is None:
            result = dict[TKey, T]()
            for current in self:
                result[key_selector(current)] = current
            return result
        else:
            result = dict[TKey, TValue]()
            for current in self:
                result[key_selector(current)] = value_selector(current)
            return result

    def to_set(self) -> set[T]:
        """集合に変換します。

        Returns:
            set[T]: インスタンスの要素を格納する集合の新しいインスタンス
        """
        return set[T](self)

    # Statistics

    @overload
    def count(self, match: None = None) -> int:
        """要素の個数を取得します。

        Returns:
            int: シーケンスの要素数
        """
        ...

    @overload
    def count(self, match: Callable[[T], bool]) -> int:
        """指定した条件に適合する要素の数を取得します。

        Args:
            match (Callable[[T], bool]): 検索する要素の条件

        Returns:
            int: matchに適合する要素の個数
        """
        ...

    def count(self, match: Callable[[T], bool] | None = None) -> int:
        result: int
        if match is None:
            if isinstance(self, Sized):
                return len(self)
            result = 0
            for _ in self:
                result += 1
            return result
        result = 0
        for current in self:
            if match(current):
                result += 1
        return result

    def max_by(self, key_selector: Callable[[T], int | bool | float]) -> T | None:
        """最大値を取る要素を取得します。

        Args:
            key_selector (Callable[[T], int  |  bool  |  float]): 要素から値を導出する関数

        Returns:
            T | None: 最大値を取る要素。シーケンスが空の場合はNone
        """
        result: T
        max: float
        iterator: Iterator[T] = iter(self)
        try:
            result = next(iterator)
            max = key_selector(result)
        except StopIteration:
            return None
        while True:
            try:
                current: T = next(iterator)
                value: float = key_selector(current)
                if value > max:
                    result = current
                    max = value
            except StopIteration:
                return result

    def min_by(self, key_selector: Callable[[T], int | bool | float]) -> T | None:
        """最小値を取る要素を取得します。

        Args:
            key_selector (Callable[[T], int  |  bool  |  float]): 要素から値を導出する関数

        Returns:
            T | None: 最小値を取る要素。シーケンスが空の場合はNone
        """
        result: T
        min: float
        iterator: Iterator[T] = iter(self)
        try:
            result = next(iterator)
            min = key_selector(result)
        except StopIteration:
            return None
        while True:
            try:
                current: T = next(iterator)
                value: float = key_selector(current)
                if value < min:
                    result = current
                    min = value
            except StopIteration:
                return result

    def sum(self, key_selector: Callable[[T], int | bool | float]) -> float:
        """合計値を算出します。

        Args:
            key_selector (Callable[[T], int  |  bool  |  float]): 計算する値を導出する関数

        Returns:
            float: 合計値
        """
        result: float = .0
        for current in self:
            result += key_selector(current)
        return result

    def average(self, key_selector: Callable[[T], int | bool | float]) -> float:
        """平均値を算出します。

        Args:
            key_selector (Callable[[T], int  |  bool  |  float]): 計算する値を導出する関数

        Returns:
            float: 平均値
        """
        if isinstance(self, Sized):
            return self.sum(key_selector) / len(self)

        count: int = 0
        result: float = .0
        for current in self:
            result += key_selector(current)
            count += 0
        return result / count

    @overload
    def aggregate(self, seed: TAccumulate, func: Callable[[TAccumulate, T], TAccumulate], result_selector: None = None) -> TAccumulate:
        """シーケンスにアキュムレート関数を適用します。

        Args:
            seed (TAccumulate): 初期値
            func (Callable[[TAccumulate, T], TAccumulate]): 一つ前の結果と要素から値を導出する関数

        Returns:
            TAccumulate: 累積値
        """
        ...

    @overload
    def aggregate(self, seed: TAccumulate, func: Callable[[TAccumulate, T], TAccumulate], result_selector: Callable[[TAccumulate], TResult]) -> TResult:
        """シーケンスにアキュムレート関数を適用します。

        Args:
            seed (TAccumulate): 初期値
            func (Callable[[TAccumulate, T], TAccumulate]): 一つ前の結果と要素から値を導出する関数
            result_selector (Callable[[TAccumulate], TResult]): 最終的な値を変換する関数

        Returns:
            TResult: 累積値
        """
        ...

    def aggregate(self, seed: TAccumulate, func: Callable[[TAccumulate, T], TAccumulate], result_selector: Callable[[TAccumulate], TResult] | None = None) -> TAccumulate | TResult:
        accumulate: TAccumulate = seed
        for current in self:
            accumulate = func(accumulate, current)
        if result_selector is None:
            return accumulate
        return result_selector(accumulate)
