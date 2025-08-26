from importlib.resources import read_text

from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import ArchitectureConfig, WebProjectConfig
from fastscaffold.std.gen import src_in
from fastscaffold.std.jinja import Jinja
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


class SqlalchemyUoWGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig,
    ]

    def __init__(self, entities: list):
        self.entities = entities

    def build(self, ctx: ScaffoldRunContext) -> None:
        file = ctx.files[src_in(
            "infrastructure", "persistence", "uow.py"
        )(ctx)]
        template = ctx[Jinja].env.get_template(
            "sqlalchemy/uow.py.template"
        )
        result = template.render(slug=ctx[WebProjectConfig].slug)
        file.lines.extend(result.splitlines())
