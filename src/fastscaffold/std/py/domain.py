import textwrap
from dataclasses import dataclass

import camelsnake

from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import ArchitectureConfig, WebProjectConfig
from fastscaffold.std.gen import src_in
from fastscaffold.std.helpers import with_src


@dataclass
class DomainEntity:
    name: str
    import_line: str
    fields: dict[str, str]


@dataclass
class EntityStore:
    entities: dict[str, DomainEntity]


class EntityGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig
    ]

    def __init__(
        self,
        *,
        name: str,
        fields: dict[str, str],
        with_id: bool,
        make_dataclass: bool = True,
        append: str = "",
        add_imports: list[str] | None = None,
        filename: str | None = None
    ) -> None:
        self.name = name
        self.fields = fields
        self.make_dataclass = make_dataclass
        self.append = textwrap.dedent(append)
        self.add_imports = add_imports or []
        self.filename = filename or camelsnake.camel_to_snake(name)
        self.with_id = with_id

    def build(self, ctx: ScaffoldRunContext) -> None:
        file = ctx.files[src_in("domain", self.filename + ".py")(ctx)]
        imports = self.add_imports
        lines = []
        if self.with_id:
            imports.append("from typing import NewType")
            imports.append("from uuid import UUID")
            lines.append(f'{self.name}Id = NewType("{self.name}Id", UUID)')
            lines.append("")
            lines.append("")
            self.fields = {"id": f"{self.name}Id", **self.fields}
        if self.make_dataclass:
            lines.append("@dataclass")
            imports.append(
                "from dataclasses import dataclass"
            )
        lines.append(f"class {self.name}:")
        for field_name, field_type in self.fields.items():
            lines.append(f"    {field_name}: {field_type}")
        if self.append:
            lines.extend(
                textwrap.indent(self.append, "    ").splitlines()
            )
        file.lines = [*imports, "", *file.lines, "", *lines, ""]
        if EntityStore not in ctx:
            ctx += EntityStore({})
        import_line = (
            f"from {ctx[WebProjectConfig].slug}"
            f".{ctx[ArchitectureConfig].domain_pkg}"
            f".{self.filename} import {self.name}"
        )
        if self.with_id:
            import_line += f", {self.name}Id"
        ctx[EntityStore].entities[self.name] = DomainEntity(
            name=self.name,
            fields=self.fields,
            import_line=import_line
        )
