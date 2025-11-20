from typing import Any

from camelsnake import camel_to_snake

from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import WebProjectConfig
from fastscaffold.std.gen import (
    SimpleManyTemplatesRender,
    SimpleTemplateRender,
)
from fastscaffold.std.py.application.persistence import GatewayStore
from fastscaffold.std.py.domain import EntityStore


class AlembicGen(SimpleManyTemplatesRender):
    requires_context = [
        *SimpleManyTemplatesRender.requires_context,
    ]
    base_dir = ["infrastructure", "persistence"]
    templates = {
        "migrations/env.py": "alembic/env.py.template",
        "migrations/README": "alembic/README",
        "migrations/script.py.mako": "alembic/script.py.mako",
    }

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        return super().get_jinja_vars(ctx) | dict(
            slug=ctx[WebProjectConfig].slug
        )


class SqlalchemyModelsGen(SimpleTemplateRender):
    requires_context = [
        *SimpleTemplateRender.requires_context,
        EntityStore,
    ]
    location = ["infrastructure", "persistence", "models.py"]
    template = "sqlalchemy/models.py.template"

    def __init__(self, entities: list[str]) -> None:
        self.entities = entities

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        entities = [
            ctx[EntityStore].entities[entity_name]
            for entity_name in self.entities
        ]
        return super().get_jinja_vars(ctx) | dict(entities=entities)


class TransactionManagerWasGenerated: ...


class SqlalchemyTransactionManagerGen(SimpleTemplateRender):
    requires_context = [*SimpleTemplateRender.requires_context]
    location = ["infrastructure", "persistence", "transactions.py"]
    template = "sqlalchemy/transactions.py.template"

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        return super().get_jinja_vars(ctx) | dict(
            slug=ctx[WebProjectConfig].slug
        )

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        ctx += TransactionManagerWasGenerated()


class SqlalchemySimpleGatewayImplGen(SimpleTemplateRender):
    requires_context = [
        *SimpleTemplateRender.requires_context,
        EntityStore,
        GatewayStore,
        TransactionManagerWasGenerated,
    ]
    template = "sqlalchemy/simple_gw.py.template"

    def __init__(self, entity_name: str, **options: Any) -> None:
        self.entity_name = entity_name
        self.options = options
        self.location = [
            "infrastructure",
            "persistence",
            f"{camel_to_snake(self.entity_name)}.py",
        ]

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        return super().get_jinja_vars(ctx) | dict(
            entity=ctx[EntityStore].entities[self.entity_name],
            gw=ctx[GatewayStore].for_entities[self.entity_name],
            slug=ctx[WebProjectConfig].slug,
            opt=self.options,
        )


class SqlalchemySessionGen(SimpleTemplateRender):
    location = ["infrastructure", "persistence", "database.py"]
    template = "sqlalchemy/database.py.template"


class UUIDGeneratorImplGen(SimpleTemplateRender):
    location = ["infrastructure", "identifier.py"]
    template = "sqlalchemy/identifier.py.template"


class SqlalchemySecurityGen(SimpleTemplateRender):
    location = ["infrastructure", "persistence", "auth.py"]
    template = "sqlalchemy/auth.py.template"