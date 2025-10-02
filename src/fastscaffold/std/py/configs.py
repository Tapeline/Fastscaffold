from fastscaffold.std.gen import (
    SimpleManyTemplatesRender,
    SimpleTemplateRender,
)


class PyprojectGen(SimpleTemplateRender):
    location = ["..", "..", "pyproject.toml"]
    template = "configs/pyproject.toml.template"


class PyQAConfigsGen(SimpleManyTemplatesRender):
    base_dir = ["..", ".."]
    templates = {
        ".coveragerc": "configs/.coveragerc.template",
        ".flake8": "configs/.flake8.template",
        "mypy.ini": "configs/mypy.ini.template",
        "pytest.ini": "configs/pytest.ini.template",
        "ruff.toml": "configs/ruff.toml.template",
    }
