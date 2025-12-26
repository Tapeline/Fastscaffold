from dataclasses import dataclass
from typing import Any

import camelsnake
from jinja2 import Environment

from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import WebProjectConfig
from fastscaffold.std.gen import SimpleTemplateRender, src_in
from fastscaffold.std.helpers import with_src
from fastscaffold.std.jinja import Jinja
from fastscaffold.std.py.application.basic_user import AuthConfig
from fastscaffold.std.py.application.persistence import GatewayStore
from fastscaffold.std.py.domain import EntityStore


@dataclass
class GeneratedInteractor:
    name: str
    module_name: str


@dataclass
class InteractorStore:
    interactors: list[GeneratedInteractor]


class _BaseInteractorGen(SimpleTemplateRender):
    requires_context = [
        *SimpleTemplateRender.requires_context,
        EntityStore,
        GatewayStore,
        AuthConfig,
    ]
    interactor_filename: str = ""
    interactor_name_template: str = ""

    def __init__(
        self,
        entity_name: str,
        *,
        with_auth: bool = True,
        name: str | None = None,
    ) -> None:
        self.entity_name = entity_name
        self.module_name = camelsnake.camel_to_snake(entity_name)
        self.with_auth = with_auth
        self.name = name or self.interactor_name_template.format(entity_name)

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
            with_auth=self.with_auth,
            name=self.name
        )

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        if InteractorStore not in ctx:
            ctx[InteractorStore] = InteractorStore([])
        if self.name:
            ctx[InteractorStore].interactors.append(
                GeneratedInteractor(
                    self.name,
                    f"application."
                    f"interactors."
                    f"{self.module_name}."
                    f"{self.interactor_filename.removesuffix('.py')}"
                )
            )


class CreateInteractorGen(_BaseInteractorGen):
    interactor_filename = "create.py"
    template = "interactors/create.py.template"


class ReadInteractorGen(_BaseInteractorGen):
    interactor_filename = "read.py"
    interactor_name_template = "Read{0}"
    template = "interactors/read.py.template"


class UpdateInteractorGen(_BaseInteractorGen):
    interactor_filename = "update.py"
    interactor_name_template = "Update{0}"
    template = "interactors/update.py.template"


class DeleteInteractorGen(_BaseInteractorGen):
    interactor_filename = "delete.py"
    interactor_name_template = "Delete{0}"
    template = "interactors/delete.py.template"


class ListInteractorGen(_BaseInteractorGen):
    interactor_filename = "list.py"
    interactor_name_template = "List{0}"
    template = "interactors/list.py.template"

    def __init__(self, *args, gw_list_method: str, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.gw_method = gw_list_method

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        return super().get_jinja_vars(ctx) | dict(
            gw_method=self.gw_method,
        )
