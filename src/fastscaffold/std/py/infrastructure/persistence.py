from importlib.resources import read_text
from typing import Any

from camelsnake import camel_to_snake

from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import ArchitectureConfig, WebProjectConfig
from fastscaffold.std.gen import SimpleTemplateRender, src_in
from fastscaffold.std.jinja import Jinja
from fastscaffold.std.py.application.persistence import GatewayStore
from fastscaffold.std.py.domain import EntityStore


class AlembicGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig,
    ]

    def build(self, ctx: ScaffoldRunContext) -> None:
        file = ctx.files[src_in(
            "infrastructure", "persistence", "migrations", "env.py"
        )(ctx)]
        template = ctx[Jinja].env.get_template(
            f"alembic/env.py.template"
        )
        result = template.render(slug=ctx[WebProjectConfig].slug)
        file.lines.extend(result.splitlines())
        for template_name in ("README", "script.py.mako"):
            file = ctx.files[src_in(
                "infrastructure", "persistence", "migrations", template_name
            )(ctx)]
            file.lines.extend(read_text(
                "fastscaffold.resource", f"std/alembic/{template_name}"
            ).splitlines())


class SqlalchemyModelsGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig,
        EntityStore
    ]

    def __init__(self, entities: list):
        self.entities = entities

    def build(self, ctx: ScaffoldRunContext) -> None:
        entities = [
            ctx[EntityStore].entities[entity_name]
            for entity_name in self.entities
        ]
        file = ctx.files[src_in(
            "infrastructure", "persistence", "models.py"
        )(ctx)]
        template = ctx[Jinja].env.get_template(
            "sqlalchemy/models.py.template"
        )
        result = template.render(entities=entities)
        file.lines.extend(result.splitlines())


class UoWWasGenerated: ...


class SqlalchemyUoWGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig,
    ]

    def build(self, ctx: ScaffoldRunContext) -> None:
        file = ctx.files[src_in(
            "infrastructure", "persistence", "uow.py"
        )(ctx)]
        template = ctx[Jinja].env.get_template(
            "sqlalchemy/uow.py.template"
        )
        result = template.render(slug=ctx[WebProjectConfig].slug)
        file.lines.extend(result.splitlines())
        ctx += UoWWasGenerated()


class SqlalchemySimpleGatewayImplGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig,
        EntityStore,
        GatewayStore,
        UoWWasGenerated
    ]

    def __init__(
        self,
        entity_name: str,
        **options: Any
    ) -> None:
        self.entity_name = entity_name
        self.options = options

    def build(self, ctx: ScaffoldRunContext) -> None:
        file = ctx.files[src_in(
            "infrastructure",
            "persistence",
            camel_to_snake(self.entity_name) + ".py"
        )(ctx)]
        template = ctx[Jinja].env.get_template(
            "sqlalchemy/simple_gw.py.template"
        )
        result = template.render(
            entity=ctx[EntityStore].entities[self.entity_name],
            gw=ctx[GatewayStore].for_entities[self.entity_name],
            slug=ctx[WebProjectConfig].slug,
            opt=self.options
        )
        file.lines.extend(result.splitlines())


class SqlalchemySessionGen(SimpleTemplateRender):
    location = ["infrastructure", "persistence", "database.py"]
    template = "sqlalchemy/database.py.template"


class UUIDGeneratorImplGen(SimpleTemplateRender):
    location = ["infrastructure", "identifier.py"]
    template = "sqlalchemy/identifier.py.template"


class SqlalchemySecurityGen(SimpleTemplateRender):
    location = ["infrastructure", "persistence", "auth.py"]
    template = "sqlalchemy/auth.py.template"
