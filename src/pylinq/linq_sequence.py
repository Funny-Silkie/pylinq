from abc import ABCMeta, abstractmethod
from typing import Callable, Generator, Generic, Iterable, Iterator, Sized, overload

from .type_variants import *


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

    # Get (Multiple values)

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

    # Convert to collection

    def to_list(self) -> list[T]:
        """リストに変換します。

        Returns:
            list[T]: インスタンスの要素を格納するリストの新しいインスタンス
        """
        return list[T](self)

    @ overload
    def to_dict(self, key_selector: Callable[[T], TKey], value_selector: None = None) -> dict[TKey, T]:
        """辞書に変換します。

        Args:
            key_selector (Callable[[T], TKey]): キーを生成する関数

        Returns:
            dict[TKey, T]: インスタンスの要素を格納する辞書の新しいインスタンス
        """
        ...

    @ overload
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
