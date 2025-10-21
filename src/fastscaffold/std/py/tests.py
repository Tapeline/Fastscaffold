from fastscaffold.std.gen import SimpleManyTemplatesRender


class SuperSimpleTestsTemplateGen(SimpleManyTemplatesRender):
    base_dir = ["..", "..", "tests"]
    templates = {
        "conftest.py": "tests/conftest.py.template",
        "factory.py": "tests/factory.py.template",
        "fakes.py": "tests/fakes.py.template",
    }
