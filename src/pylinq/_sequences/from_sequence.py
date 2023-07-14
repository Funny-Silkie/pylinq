from typing import Callable, Generator, Generic, Iterable, Iterator, Sized, final

from .. import LinqSequence
from ..type_variants import *


class FromSequence(LinqSequence[T], Generic[T]):
    """イテラブルなオブジェクトをそのまま持つシーケンスのクラスです。
    """

    def __init__(self, source: Iterable[T]) -> None:
        """FromSequence[T]の新しいインスタンスを初期化します。

        Args:
            source (Iterable[T]): 使用するイテラブルなオブジェクト
        """
        super().__init__()
        self.__iterator: Iterator[T] | None = None
        self._source: Iterable[T] = source

    def _in_iteration(self) -> bool:
        return not self.__iterator is None

    def _start_iteration(self) -> None:
        self.__iterator = iter(self._source)

    def _stop_iteration(self) -> None:
        self.__iterator = None

    def _get_next(self) -> T:
        return next(self.__iterator)  # type: ignore


class SizedFromSequence(FromSequence[T], Sized, Generic[T]):
    """サイズ付きのイテラブルなオブジェクトをそのまま持つシーケンスのクラスです。
    """

    def __init__(self, source: Iterable[T]) -> None:
        """SizedSequence[T]の新しいインスタンスを初期化します。

        Args:
            source (Iterable[T]): 使用するイテラブルなオブジェクト
        """
        super().__init__(source)

    def __len__(self) -> int:
        return len(self._source)  # type: ignore


@final
class DictSequence(LinqSequence[tuple[TKey, TValue]], Sized, Generic[TKey, TValue]):
    """辞書をそのまま持つシーケンスのクラスです。
    """

    def __init__(self, source: dict[TKey, TValue]) -> None:
        """DictSequence[TKey, TValue]の新しいインスタンスを初期化します。

        Args:
            source (dict[TKey, TValue]): 使用する辞書
        """
        super().__init__()
        self.__iterator: Iterator[TKey] | None = None
        self.__source: dict[TKey, TValue] = source

    def _in_iteration(self) -> bool:
        return not self.__iterator is None

    def _start_iteration(self) -> None:
        self.__iterator = iter(self.__source)

    def _stop_iteration(self) -> None:
        self.__iterator = None

    def _get_next(self) -> tuple[TKey, TValue]:
        key: TKey = next(self.__iterator)  # type: ignore
        return (key, self.__source[key])

    def __len__(self) -> int:
        return len(self.__source)


class GeneratorSequence(LinqSequence[T], Generic[T]):
    """Generatorを基にしたシーケンスのクラスです。
    """

    def __init__(self, func: Callable[[*TArgs], Generator[T, None, None]], *args: *TArgs) -> None:  # type: ignore
        """GeneratorSequence[T]の新しいインスタンスを初期化します。

        Args:
            func (Callable[[*TArgs], Generator[T, None, None]]): Generatorを生成する関数
            args: funcに与える引数
        """
        super().__init__()
        self.__func: Callable[[*TArgs], Generator[T, None, None]] = func  # type: ignore
        self.__args: tuple = args
        self.__geneartor: Generator[T, None, None] | None = None

    def _in_iteration(self) -> bool:
        return not self.__geneartor is None

    def _start_iteration(self) -> None:
        self.__geneartor = self.__func(*self.__args)

    def _stop_iteration(self) -> None:
        self.__geneartor = None

    def _get_next(self) -> T:
        return next(self.__geneartor)  # type: ignore
