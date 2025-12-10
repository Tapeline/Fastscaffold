from fastscaffold.std.gen import (
    SimpleManyTemplatesRender,
    SimpleTemplateRender,
)


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
