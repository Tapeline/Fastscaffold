from dataclasses import dataclass
from importlib.resources import read_text
from string import Template

from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import ArchitectureConfig, WebProjectConfig
from fastscaffold.std.gen import src_in
from fastscaffold.std.jinja import Jinja
from fastscaffold.std.py.application.persistence import GatewayStore
from fastscaffold.std.py.domain import EntityStore


@dataclass
class AuthConfig:
    import_auth: str


class BasicAppAuthGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig,
        EntityStore
    ]

    def __init__(
            self,
            user_entity_name: str
    ):
        self.user_entity_name = user_entity_name

    def build(self, ctx: ScaffoldRunContext) -> None:
        user_entity = ctx[EntityStore].entities[self.user_entity_name]
        mapping = {
            "user_import": user_entity.import_line,
            "user_class": user_entity.name,
            "slug": ctx[WebProjectConfig].slug
        }

        auth_file = ctx.files[src_in(
            "application", "auth", "auth.py"
        )(ctx)]
        auth_template = Template(
            read_text(
                "fastscaffold.resource", "std/auth/auth.py.template"
            )
        )
        auth_file.lines.extend(
            auth_template.substitute(mapping).splitlines()
        )

        exc_file = ctx.files[src_in(
            "application", "auth", "exception.py"
        )(ctx)]
        exc_template = Template(
            read_text(
                "fastscaffold.resource", "std/auth/exception.py.template"
            )
        )
        exc_file.lines.extend(
            exc_template.substitute(mapping).splitlines()
        )

        ctx += AuthConfig(
            import_auth=(
                f"from {ctx[WebProjectConfig].slug}"
                f".{ctx[ArchitectureConfig].application_pkg}"
                f".auth.auth import UserIdProvider"
            )
        )


class BasicAppAuthInteractorsGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig,
        EntityStore,
        GatewayStore,
    ]

    def __init__(
        self, entity_name: str,
    ) -> None:
        self.entity_name = entity_name

    def build(self, ctx: ScaffoldRunContext) -> None:
        entity = ctx[EntityStore].entities[self.entity_name]
        gw = ctx[GatewayStore].for_entities[self.entity_name]
        for template_name in (
            "login.py", "logout.py", "profile.py", "register.py"
        ):
            file = ctx.files[src_in(
                "application", "interactors", "auth", template_name
            )(ctx)]
            template = ctx[Jinja].env.get_template(
                f"interactors/auth/{template_name}.template"
            )
            result = template.render(
                slug=ctx[WebProjectConfig].slug,
                user=entity,
                user_gw=gw,
            )
