from dataclasses import dataclass

from fastscaffold.core.files import FileAssembler, ScaffoldFile
from fastscaffold.std.gen import SimpleTemplateRender


class DataCommonsGen(SimpleTemplateRender):
    location = ["data_commons.py"]
    template = "data_commons.py.template"
