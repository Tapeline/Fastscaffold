from dataclasses import dataclass

from camelsnake import camel_to_snake

from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.gen import (
    SimpleManyTemplatesRender,
    SimpleTemplateRender,
)


@dataclass
class LitestarController:
    name: str
    module_name: str


@dataclass
class LitestarControllerStore:
    controllers: list[LitestarController]


class LitestarCommonsGen(SimpleManyTemplatesRender):
    """
    Generates common litestar utility files.

    Generates modules and functions to neatly deal with errors,
    OpenAPI and security definitions.

    Examples:
        ```python
        LitestarCommonsGen()
        ```
    """

    base_dir = ["presentation", "http"]
    templates = {
        "errors.py": "litestar/errors.py.template",
        "openapi.py": "litestar/openapi.py.template",
        "security.py": "litestar/security.py.template",
        "framework/errors.py": "litestar/framework/errors.py.template",
        "framework/openapi.py": "litestar/framework/openapi.py.template",
        "framework/middlewares.py": "litestar/framework/middlewares.py.template",
    }


class LitestarCommonUserEndpointsGen(SimpleTemplateRender):
    """
    Generates common litestar user endpoints.

    Requires:
        BasicAppAuthGen
        BasicAppAuthInteractorsGen
        LitestarCommonsGen

    These endpoints include:

    - login
    - logout
    - register
    - get profile

    Examples:
        ```python
        LitestarCommonUserEndpointsGen()
        ```
    """

    location = ["presentation", "http", "controllers", "user.py"]
    template = "litestar/auth_controllers.py.template"

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        if LitestarControllerStore not in ctx:
            ctx[LitestarControllerStore] = LitestarControllerStore([])
        ctx[LitestarControllerStore].controllers.append(LitestarController(
            name="AuthController",
            module_name="presentation.http.controllers.user",
        ))


class LitestarCommonCRUDGen(SimpleTemplateRender):
    """
    Generates common litestar CRUD.

    Requires:
        BasicAppAuthGen
        LitestarCommonsGen

    These endpoints may include:

    - create (c)
    - read (r)
    - update (u)
    - delete (d)
    - list (l)

    Args:
        opts: options (any combination of letters "crudl") to generate
        entity_name: existing domain entity name to generate CRUD for

    Examples:
        ```python
        LitestarCommonCRUDGen("crudl", "EntityName")
        ```
    """

    location = ["presentation", "http", "controllers", "user.py"]
    template = "litestar/crud.py.template"

    def __init__(self, opts: str, entity_name: str) -> None:
        self.opts = opts
        self.entity = entity_name

    def get_location(self, ctx: ScaffoldRunContext) -> list[str]:
        return [
            "presentation", "http", "controllers",
            camel_to_snake(self.entity) + ".py"
        ]

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        if LitestarControllerStore not in ctx:
            ctx[LitestarControllerStore] = LitestarControllerStore([])
        ctx[LitestarControllerStore].controllers.append(LitestarController(
            name=f"{self.entity}Controller",
            module_name=".".join(self.get_location(ctx)).removesuffix(".py"),
        ))

