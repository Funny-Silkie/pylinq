from typing import Generic, Iterable, Iterator

from ..type_variants import *
from ..linq_sequence import LinqSequence


class FromSequence(LinqSequence[T], Generic[T]):
    """イテラブルなオブジェクトをそのまま持つシーケンスのクラスです。
    """

    def __init__(self, source: Iterable[T]) -> None:
        """FromSequence[T]の新しいインスタンスを初期化します。

        Args:
            source (Iterable[T]): 使用するイテラブルなオブジェクト
        """
        LinqSequence[T].__init__(
            self  # type:ignore
        )
        self.__source: Iterable[T] = source

    def _get_source(self) -> Iterable[T]:
        return self.__source
