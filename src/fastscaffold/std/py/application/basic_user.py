from dataclasses import dataclass
from typing import Any

from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import WebProjectConfig
from fastscaffold.std.gen import SimpleManyTemplatesRender
from fastscaffold.std.py.application.persistence import GatewayStore
from fastscaffold.std.py.domain import EntityStore


@dataclass
class AuthConfig:
    import_auth: str


class BasicAppAuthGen(SimpleManyTemplatesRender):
    requires_context = [
        *SimpleManyTemplatesRender.requires_context,
        EntityStore,
    ]
    base_dir = ["application", "auth"]
    templates = {
        "auth.py": "auth/auth.py.template",
        "exceptions.py": "auth/exceptions.py.template"
    }

    def __init__(self, user_entity_name: str):
        self.user_entity_name = user_entity_name

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        user_entity = ctx[EntityStore].entities[self.user_entity_name]
        return super().get_jinja_vars(ctx) | {
            "user_import": user_entity.import_line,
            "user_class": user_entity.name,
            "slug": ctx[WebProjectConfig].slug
        }

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        ctx += AuthConfig(
            import_auth=(
                f"from {ctx[WebProjectConfig].slug}"
                f".application.auth.auth import UserIdProvider"
            )
        )


class BasicAppAuthInteractorsGen(SimpleManyTemplatesRender):
    requires_context = [
        *SimpleManyTemplatesRender.requires_context,
        EntityStore, GatewayStore,
    ]
    base_dir = ["application", "interactors", "auth"]
    templates = {
        "login.py": "interactors/auth/login.py.template",
        "logout.py": "interactors/auth/logout.py.template",
        "profile.py": "interactors/auth/profile.py.template",
        "register.py": "interactors/auth/register.py.template",
    }

    def __init__(self, entity_name: str) -> None:
        self.entity_name = entity_name

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        entity = ctx[EntityStore].entities[self.entity_name]
        gw = ctx[GatewayStore].for_entities[self.entity_name]
        return super().get_jinja_vars(ctx) | dict(
            user=entity,
            user_gw=gw,
        )
