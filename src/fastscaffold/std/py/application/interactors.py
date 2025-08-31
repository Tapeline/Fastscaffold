from typing import Any

import camelsnake
from jinja2 import Environment

from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import ArchitectureConfig, WebProjectConfig
from fastscaffold.std.gen import SimpleTemplateRender, src_in
from fastscaffold.std.helpers import with_src
from fastscaffold.std.jinja import Jinja
from fastscaffold.std.py.application.basic_user import AuthConfig
from fastscaffold.std.py.application.persistence import GatewayStore
from fastscaffold.std.py.domain import EntityStore


class _BaseInteractorGen(SimpleTemplateRender):
    requires_context = [
        *SimpleTemplateRender.requires_context,
        EntityStore,
        GatewayStore,
        AuthConfig,
    ]
    interactor_filename: str = ""

    def __init__(
        self,
        entity_name: str,
        *,
        with_auth: bool = True
    ) -> None:
        self.entity_name = entity_name
        self.module_name = camelsnake.camel_to_snake(entity_name)
        self.with_auth = with_auth

    def get_location(self, ctx: ScaffoldRunContext) -> list[str]:
        return [
            "application",
            "interactors",
            self.module_name,
            self.interactor_filename
        ]

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        entity = ctx[EntityStore].entities[self.entity_name]
        gw = ctx[GatewayStore].for_entities[self.entity_name]
        return super().get_jinja_vars(ctx) | dict(
            auth_import=ctx[AuthConfig].import_auth,
            gw_import=gw.import_line,
            entity=entity,
            with_auth=self.with_auth
        )


class CreateInteractorGen(_BaseInteractorGen):
    interactor_filename = "create.py"
    template = "interactors/create.py.template"


class ReadInteractorGen(_BaseInteractorGen):
    interactor_filename = "read.py"
    template = "interactors/read.py.template"


class UpdateInteractorGen(_BaseInteractorGen):
    interactor_filename = "update.py"
    template = "interactors/update.py.template"


class DeleteInteractorGen(_BaseInteractorGen):
    interactor_filename = "delete.py"
    template = "interactors/delete.py.template"


class ListInteractorGen(_BaseInteractorGen):
    interactor_filename = "list.py"
    template = "interactors/list.py.template"

    def __init__(self, *args, gw_list_method: str, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.gw_method = gw_list_method

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        return super().get_jinja_vars(ctx) | dict(
            gw_method=self.gw_method,
        )
