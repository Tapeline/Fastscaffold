from fastscaffold.std.gen import (
    SimpleManyTemplatesRender,
    SimpleTemplateRender,
)


class LitestarCommonsGen(SimpleManyTemplatesRender):
    base_dir = ["presentation", "http"]
    templates = {
        "errors.py": "litestar/errors.py.template",
        "openapi.py": "litestar/openapi.py.template",
        "security.py": "litestar/security.py.template",
        "framework/errors.py": "litestar/framework/errors.py.template",
        "framework/openapi.py": "litestar/framework/openapi.py.template",
    }


class LitestarCommonUserEndpointsGen(SimpleTemplateRender):
    location = ["presentation", "http", "controllers", "user.py"]
    template = "litestar/auth_controllers.py.template"
