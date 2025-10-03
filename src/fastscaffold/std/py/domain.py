import textwrap
from dataclasses import dataclass
from typing import Any

import camelsnake

from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import WebProjectConfig
from fastscaffold.std.gen import src_in
from fastscaffold.std.helpers import with_src

from src.fastscaffold.std.gen import SimpleTemplateRender


@dataclass
class DomainEntity:
    name: str
    import_line: str
    fields: dict[str, str]


@dataclass
class EntityStore:
    entities: dict[str, DomainEntity]


class EntityGen(SimpleTemplateRender):
    def __init__(
        self,
        *,
        name: str,
        fields: dict[str, str],
        with_id: bool,
        make_dataclass: bool = True,
        append: str = "",
        add_imports: list[str] | None = None,
    ) -> None:
        self.name = name
        self.fields = fields
        self.make_dataclass = make_dataclass
        self.append = textwrap.dedent(append)
        self.add_imports = add_imports or []
        self.filename = camelsnake.camel_to_snake(name)
        self.with_id = with_id
        self.location = ["domain", f"{self.filename}.py"]

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        return super().get_jinja_vars(ctx) | dict(
            name=self.name,
            fields=self.fields,
            with_id=self.with_id,
            make_dataclass=self.make_dataclass,
            append=self.append,
            add_imports=self.add_imports,
        )

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        if EntityStore not in ctx:
            ctx += EntityStore({})
        import_line = (
            f"from {ctx[WebProjectConfig].slug}"
            f".domain"
            f".{self.filename} import {self.name}"
        )
        if self.with_id:
            import_line += f", {self.name}Id"
        ctx[EntityStore].entities[self.name] = DomainEntity(
            name=self.name,
            fields=self.fields,
            import_line=import_line
        )
