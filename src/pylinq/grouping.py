from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Generic, Sized

from .linq_sequence import LinqSequence
from .type_variants import *


class Grouping(LinqSequence[T], Generic[TKey, T], metaclass=ABCMeta):
    """キーを基にグループ化されたシーケンスを表します。
    """
    @abstractproperty
    def key(self) -> TKey:
        """キーを取得します。
        """
        ...


class Lookup(LinqSequence[Grouping[TKey, TValue]], Generic[TKey, TValue], Sized, metaclass=ABCMeta):
    """1つ以上の値がマップされたキーのシーケンスを表します。
    """

    @abstractmethod
    def contains_key(self, key: TKey) -> bool:
        """指定したキーが格納されているかどうかを検証します。

        Args:
            key (TKey): 検証するキー

        Returns:
            bool: keyが格納されていたらTrue，それ以外でFalse
        """
        ...

    @abstractmethod
    def __getitem__(self, key: TKey) -> LinqSequence[TValue]:
        """キーに対応するGrouping[TKey, T]のインスタンスを取得します。

        Args:
            key (TKey): 検索するキー

        Returns:
            LinqSequence[TValue]: keyに対応するGrouping[TKey, T]のインスタンス
        """
        ...
