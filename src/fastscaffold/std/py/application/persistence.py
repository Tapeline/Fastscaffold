from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable

from camelsnake import camel_to_snake

from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import WebProjectConfig
from fastscaffold.std.gen import SimpleTemplateRender, import_from
from fastscaffold.std.py.domain import EntityStore

from src.fastscaffold.misc.merger import merge_all


@dataclass
class GeneratedGateway:
    import_line: str
    name: str


@dataclass
class GatewayStore:
    for_entities: dict[str, GeneratedGateway]


class UoWInterfaceGen(SimpleTemplateRender):
    location = ["application", "persistence", "uow.py"]
    template = "application/uow.py.template"


class PaginationDTOGen(SimpleTemplateRender):
    location = ["application", "pagination.py"]
    template = "application/pagination.py.template"


class GatewayInterfaceGen(SimpleTemplateRender):
    requires_context = [
        *SimpleTemplateRender.requires_context,
        EntityStore,
    ]
    template = "application/gateway.py.template"

    def __init__(
        self,
        entity_name: str,
        *include: dict[str, Any],
        gen_exceptions: bool = False,
    ):
        self.entity_name = entity_name
        self.location = [
            "application",
            "persistence",
            f"{camel_to_snake(entity_name)}.py",
        ]
        self.gen_exceptions = gen_exceptions
        self.include = merge_all({}, *include)

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        return super().get_jinja_vars(ctx) | dict(
            entity=ctx[EntityStore].entities[self.entity_name],
            gen_exceptions=self.gen_exceptions,
            import_from=import_from,
            include=self.include,
        )

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        if GatewayStore not in ctx:
            ctx += GatewayStore({})
        ctx[GatewayStore].for_entities[self.entity_name] = GeneratedGateway(
            import_line=(
                f"from {ctx[WebProjectConfig].slug}"
                f".application.persistence"
                f".{camel_to_snake(self.entity_name)} import {self.entity_name}Gateway"
            ),
            name=f"{self.entity_name}Gateway",
        )

    @staticmethod
    def add_get_by_id() -> dict[str, Any]:
        return {"add_get_by_id": True}

    @staticmethod
    def add_delete_by_id() -> dict[str, Any]:
        return {"add_delete_by_id": True}

    @staticmethod
    def add_save() -> dict[str, Any]:
        return {"add_save": True}

    @classmethod
    def add_get_paginated_filtered(
        cls, name: str, **kwargs
    ) -> dict[str, Any]:
        return {
            "add_get_paginated_filtered": {
                "name": name,
                "args": ", ".join(f"{arg}: {typ}" for arg, typ in kwargs.items())
            }
        }

    @classmethod
    def add_get_filtered(
        cls, name: str, **kwargs
    ) -> dict[str, Any]:
        return {
            "add_get_filtered": {
                "name": name,
                "args": ", ".join(f"{arg}: {typ}" for arg, typ in kwargs.items())
            }
        }


class UUIDGeneratorInterfaceGen(SimpleTemplateRender):
    location = ["application", "identifier.py"]
    template = "application/identifier.py.template"
