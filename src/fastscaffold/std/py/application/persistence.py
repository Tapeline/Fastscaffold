import textwrap
from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

import camelsnake

from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.core.files import ScaffoldFile
from fastscaffold.std.configs import ArchitectureConfig, WebProjectConfig
from fastscaffold.std.gen import import_from, src_in
from fastscaffold.std.py.domain import EntityStore


@dataclass
class GeneratedGateway:
    import_line: str
    name: str


@dataclass
class GatewayStore:
    for_entities: dict[str, GeneratedGateway]


class UoWInterfaceGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig
    ]

    def build(self, ctx: ScaffoldRunContext) -> None:
        file = ctx.files[src_in(
            "application", "persistence", "uow.py"
        )(ctx)]
        file.lines = [
            "from abc import abstractmethod"
            "from typing import Protocol",
            "",
            "",
            "class UoW(Protocol):",
            '    """A unit of work."""',
            "",
            "    @abstractmethod",
            "    async def __aenter__(self) -> None:",
            '        """Init UoW."""',
            "",
            "    @abstractmethod",
            "    async def __aexit__(",
            "            self,",
            "            exc_type: type[Exception],",
            "            exc_val: Exception,",
            "            exc_tb: Any",
            "    ) -> None:",
            '        """Rollback or commit."""',
            ""
        ]


class PaginationDTOGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig
    ]

    def build(self, ctx: ScaffoldRunContext) -> None:
        file = ctx.files[src_in(
            "application", "pagination.py"
        )(ctx)]
        file.lines.extend([
            "from dataclasses import dataclass",
            "",
            "",
            "@dataclass(frozen=True, slots=True)",
            "class PaginationParams:",
            "    page: int",
            "    page_size: int",
            ""
        ])


class GatewayInterfaceGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig,
        EntityStore,
    ]

    def __init__(
        self,
        entity_name: str,
        *include,
        gen_exceptions: bool = False,
    ):
        self.entity_name = entity_name
        self.include = include
        self.filename = camelsnake.camel_to_snake(entity_name)
        self.gen_exceptions = gen_exceptions

    def build(self, ctx: ScaffoldRunContext) -> None:
        file = ctx.files[src_in(
            "application", "persistence", self.filename + ".py"
        )(ctx)]
        entity = ctx[EntityStore].entities[self.entity_name]
        exceptions = []
        if self.gen_exceptions:
            exceptions.extend([
                f"class {entity.name}NotFound(Exception):",
                '    """Raised when entity with such id is not found."""',
                "",
                f"    def __init__(self, uid: {self.entity_name}Id) -> None:",
                '        """Init and set uid."""',
                "        self.id = uid",
                "",
                "",
            ])
        file.lines.extend([
            "from abc import abstractmethod",
            "from collections.abc import Sequence",
            "from typing import Protocol",
            "",
            entity.import_line,
            f"from {import_from("application.pagination")(ctx)} "
            f"import PaginationParams",
            "",
            "",
            *exceptions,
            f"class {self.entity_name}Gateway(Protocol):",
            f'    """Access to {self.filename.replace("_", " ")}s."""',
            "",
        ])
        for method in self.include:
            method(self, file, ctx)
        if GatewayStore not in ctx:
            ctx += GatewayStore({})
        ctx[GatewayStore].for_entities[self.entity_name] = GeneratedGateway(
            import_line=(
                f"from {ctx[WebProjectConfig].slug}"
                f".{ctx[ArchitectureConfig].application_pkg}"
                f".{self.filename} import {self.entity_name}Gateway"
            ),
            name=f"{self.entity_name}Gateway"
        )

    def add_get_by_id(
        self, file: ScaffoldFile, ctx: ScaffoldRunContext
    ) -> None:
        file.lines.extend([
            "    @abstractmethod",
            f"    async def get_by_id(self, uid: {self.entity_name}Id)"
            f" -> {self.entity_name}:",
            '        """Get by id."""',
            "        raise NotImplementedError",
            ""
        ])

    def add_delete_by_id(
        self, file: ScaffoldFile, ctx: ScaffoldRunContext
    ) -> None:
        file.lines.extend([
            "    @abstractmethod",
            f"    async def delete_by_id(self, uid: {self.entity_name}Id)"
            f" -> {self.entity_name}:",
            '        """Delete by id."""',
            "        raise NotImplementedError",
            ""
        ])

    def add_save(
        self, file: ScaffoldFile, ctx: ScaffoldRunContext
    ) -> None:
        file.lines.extend([
            "    @abstractmethod",
            f"    async def save(self, entity: {self.entity_name}) -> None:",
            '        """Save entity."""',
            "        raise NotImplementedError",
            ""
        ])

    @classmethod
    def add_get_paginated_filtered(
        cls, name: str, **kwargs
    ) -> Callable[..., None]:
        def generator(
            self: cls, file: ScaffoldFile, ctx: ScaffoldRunContext
        ) -> None:
            kwargs["paginate"] = "PaginationParams"
            args = ", ".join(f"{arg}: {typ}" for arg, typ in kwargs.items())
            file.lines.extend([
                "    @abstractmethod",
                f"    async def {name}(self, {args})"
                f" -> Sequence[{self.entity_name}]:",
                '        """Get filtered and paginated."""',
                "        raise NotImplementedError",
                ""
            ])
        return generator

    @classmethod
    def add_get_filtered(
        cls, name: str, **kwargs
    ) -> Callable[..., None]:
        def generator(
            self: Self, file: ScaffoldFile, ctx: ScaffoldRunContext
        ) -> None:
            args = ", ".join(f"{arg}: {typ}" for arg, typ in kwargs.items())
            file.lines.extend([
                "    @abstractmethod",
                f"    async def {name}(self, {args})"
                f" -> Sequence[{self.entity_name}]:",
                '        """Get filtered."""',
                "        raise NotImplementedError",
                ""
            ])
        return generator


class UUIDGeneratorInterfaceGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig
    ]

    def build(self, ctx: ScaffoldRunContext) -> None:
        file = ctx.files[src_in(
            "application", "identifier.py"
        )(ctx)]
        file.lines.extend([
            "class UUIDGenerator(Protocol):",
            '    """UUID generator."""',
            "",
            "    @abstractmethod",
            "    def __call__(self) -> uuid.UUID:",
            '        """Generate a UUID."""',
            "",
        ])
