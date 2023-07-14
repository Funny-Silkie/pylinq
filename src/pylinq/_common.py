
from inspect import signature
from typing import Callable


def get_parameter_count(func: Callable) -> int:
    """関数のパラメータ数を取得します。

    Args:
        func (Callable): 対象関数

    Returns:
        int: funcにおけるパラメータの個数
    """
    return len(signature(func).parameters)
