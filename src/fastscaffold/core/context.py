from collections import defaultdict
from collections.abc import Iterator
from typing import Any, Never, Self, overload

from fastscaffold.core.files import ScaffoldFile


class ContextNotFoundError(Exception):
    def __init__(self, ctx_type: type[Any] | str) -> None:
        self.ctx_type = ctx_type

    def __str__(self) -> str:
        ctx_name = (
            f"<string reference> {self.ctx_type}"
            if isinstance(self.ctx_type, str)
            else self.ctx_type.__qualname__
        )
        return f"Could not find context of type {ctx_name}"


class DuplicateContextError(Exception):
    def __init__(self, ctx_type: type[Any]) -> None:
        self.ctx_type = ctx_type

    def __str__(self) -> str:
        return (
            f"Tried to add context of type {self.ctx_type.__qualname__}, "
            f"but context already existed."
        )


class ScaffoldContext:
    def __init__(self, *contexts: Any) -> None:
        self._contexts: dict[type[Any] | str, Any] = {
            type(ctx): ctx for ctx in contexts
        }

    def get_ctx[Ctx_T](
        self, typ: type[Ctx_T] | str, default: Ctx_T = Never
    ) -> Ctx_T:
        if isinstance(typ, str):
            if typ in self._contexts:
                return self._contexts[typ]
            for ctx_type in self._contexts:
                if ctx_type.__name__ == typ:
                    return self._contexts[ctx_type]
            else:
                raise ContextNotFoundError(typ)
        if typ not in self._contexts:
            if default is Never:
                raise ContextNotFoundError(typ)
            else:
                return default
        return self._contexts[typ]

    def __getitem__[Ctx_T](self, typ: type[Ctx_T] | str) -> Ctx_T:
        return self.get_ctx(typ)

    def add_ctx(self, ctx: Any) -> None:
        if type(ctx) in self._contexts:
            raise DuplicateContextError(ctx)
        self._contexts[type(ctx)] = ctx

    @overload
    def __setitem__[Ctx_T](self, key: type[Ctx_T], value: Ctx_T): ...

    @overload
    def __setitem__(self, key: str, value: Any): ...

    def __setitem__[Ctx_T](self, key: type[Ctx_T] | str, value: Ctx_T | Any):
        self._contexts[key] = value

    def __iadd__(self, ctx: Any) -> Self:
        self.add_ctx(ctx)
        return self

    def __contains__(self, item: Any) -> bool:
        return item in self._contexts

    def __iter__(self) -> Iterator[Any]:
        return iter(
            ctx for key, ctx in self._contexts.items()
            if isinstance(key, type)
        )


class DefaultFileDict(dict[str, ScaffoldFile]):
    def __getitem__(self, item: str) -> ScaffoldFile:
        if item not in self:
            self[item] = ScaffoldFile(
                path=item, lines=[], ctx=ScaffoldContext()
            )
        return super().__getitem__(item)


class ScaffoldRunContext(ScaffoldContext):
    def __init__(self, *contexts: Any):
        super().__init__(*contexts)
        self.files: dict[str, ScaffoldFile] = DefaultFileDict()
