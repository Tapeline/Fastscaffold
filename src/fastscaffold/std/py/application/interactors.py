import camelsnake
from jinja2 import Environment

from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import ArchitectureConfig, WebProjectConfig
from fastscaffold.std.gen import src_in
from fastscaffold.std.helpers import with_src
from fastscaffold.std.jinja import Jinja
from fastscaffold.std.py.application.basic_user import AuthConfig
from fastscaffold.std.py.application.persistence import GatewayStore
from fastscaffold.std.py.domain import EntityStore


class CreateInteractorGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig,
        EntityStore,
        GatewayStore,
        AuthConfig
    ]

    def __init__(
        self, entity_name: str, *,
        with_auth: bool = True
    ) -> None:
        self.entity_name = entity_name
        self.module_name = camelsnake.camel_to_snake(entity_name)
        self.with_auth = with_auth

    def build(self, ctx: ScaffoldRunContext) -> None:
        file = ctx.files[src_in(
            "application", "interactors", self.module_name, "create.py"
        )(ctx)]
        entity = ctx[EntityStore].entities[self.entity_name]
        gw = ctx[GatewayStore].for_entities[self.entity_name]
        template = ctx[Jinja].env.get_template(
            "interactors/create.py.template"
        )
        result = template.render(
            slug=ctx[WebProjectConfig].slug,
            auth_import=ctx[AuthConfig].import_auth,
            gw_import=gw.import_line,
            entity=entity,
            with_auth=self.with_auth
        )
        file.lines.extend(result.splitlines())


class ReadInteractorGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig,
        EntityStore,
        GatewayStore,
        AuthConfig
    ]

    def __init__(
        self, entity_name: str, *,
        with_auth: bool = True
    ) -> None:
        self.entity_name = entity_name
        self.module_name = camelsnake.camel_to_snake(entity_name)
        self.with_auth = with_auth

    def build(self, ctx: ScaffoldRunContext) -> None:
        file = ctx.files[src_in(
            "application", "interactors", self.module_name, "read.py"
        )(ctx)]
        entity = ctx[EntityStore].entities[self.entity_name]
        gw = ctx[GatewayStore].for_entities[self.entity_name]
        template = ctx[Jinja].env.get_template(
            "interactors/read.py.template"
        )
        result = template.render(
            slug=ctx[WebProjectConfig].slug,
            auth_import=ctx[AuthConfig].import_auth,
            gw_import=gw.import_line,
            entity=entity,
            with_auth=self.with_auth
        )
        file.lines.extend(result.splitlines())


class UpdateInteractorGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig,
        EntityStore,
        GatewayStore,
        AuthConfig
    ]

    def __init__(
        self, entity_name: str, *,
        with_auth: bool = True
    ) -> None:
        self.entity_name = entity_name
        self.module_name = camelsnake.camel_to_snake(entity_name)
        self.with_auth = with_auth

    def build(self, ctx: ScaffoldRunContext) -> None:
        file = ctx.files[src_in(
            "application", "interactors", self.module_name, "update.py"
        )(ctx)]
        entity = ctx[EntityStore].entities[self.entity_name]
        gw = ctx[GatewayStore].for_entities[self.entity_name]
        template = ctx[Jinja].env.get_template(
            "interactors/update.py.template"
        )
        result = template.render(
            slug=ctx[WebProjectConfig].slug,
            auth_import=ctx[AuthConfig].import_auth,
            gw_import=gw.import_line,
            entity=entity,
            with_auth=self.with_auth
        )
        file.lines.extend(result.splitlines())


class DeleteInteractorGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig,
        EntityStore,
        GatewayStore,
        AuthConfig
    ]

    def __init__(
        self, entity_name: str, *,
        with_auth: bool = True
    ) -> None:
        self.entity_name = entity_name
        self.module_name = camelsnake.camel_to_snake(entity_name)
        self.with_auth = with_auth

    def build(self, ctx: ScaffoldRunContext) -> None:
        file = ctx.files[src_in(
            "application", "interactors", self.module_name, "delete.py"
        )(ctx)]
        entity = ctx[EntityStore].entities[self.entity_name]
        gw = ctx[GatewayStore].for_entities[self.entity_name]
        template = ctx[Jinja].env.get_template(
            "interactors/delete.py.template"
        )
        result = template.render(
            slug=ctx[WebProjectConfig].slug,
            auth_import=ctx[AuthConfig].import_auth,
            gw_import=gw.import_line,
            entity=entity,
            with_auth=self.with_auth
        )
        file.lines.extend(result.splitlines())


class ListInteractorGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig,
        EntityStore,
        GatewayStore,
        AuthConfig
    ]

    def __init__(
        self, entity_name: str, *,
        gw_list_method: str,
        with_auth: bool = True
    ) -> None:
        self.entity_name = entity_name
        self.module_name = camelsnake.camel_to_snake(entity_name)
        self.with_auth = with_auth
        self.gw_method = gw_list_method

    def build(self, ctx: ScaffoldRunContext) -> None:
        file = ctx.files[src_in(
            "application", "interactors", self.module_name, "list.py"
        )(ctx)]
        entity = ctx[EntityStore].entities[self.entity_name]
        gw = ctx[GatewayStore].for_entities[self.entity_name]
        template = ctx[Jinja].env.get_template(
            "interactors/list.py.template"
        )
        result = template.render(
            slug=ctx[WebProjectConfig].slug,
            auth_import=ctx[AuthConfig].import_auth,
            gw_import=gw.import_line,
            entity=entity,
            with_auth=self.with_auth,
            gw_method=self.gw_method,
        )
        file.lines.extend(result.splitlines())
