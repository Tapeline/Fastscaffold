from typing import Any, override


class UnmergeableError(Exception):
    def __init__(self, base: Any, obj: Any) -> None:
        self.base = base
        self.obj = obj

    @override
    def __str__(self) -> str:
        return f"Cannot merge {self.obj} into {self.base}"


def merge[T](base: T, obj: T) -> T:
    if isinstance(base, list) and isinstance(obj, list):
        return base + obj
    if isinstance(base, set) and isinstance(obj, set):
        return base | obj
    if isinstance(base, dict) and isinstance(obj, dict):
        return base | obj
    if isinstance(base, tuple) and isinstance(obj, tuple):
        return base + obj
    raise UnmergeableError(base, obj)


def merge_all[T](base: T, *objs: T) -> T:
    for obj in objs:
        base = merge(base, obj)
    return base
