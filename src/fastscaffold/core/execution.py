from collections.abc import Callable
from typing import Any

from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.core.files import FileAssembler


class RequiredContextNotFound(Exception):
    def __init__(self, component: ScaffoldComponent, ctx: type[Any]) -> None:
        self.component = component
        self.ctx = ctx

    def __str__(self) -> str:
        return (
            f"Component {self.component} required context of type "
            f"{self.ctx.__qualname__}, but it wasn't found"
        )


class ScaffoldExecutor:
    def __init__(self) -> None:
        self.ctx = ScaffoldRunContext()
        self.components = []

    def run(
        self,
        scaffold_setup: Callable[
            [ScaffoldRunContext], list[ScaffoldComponent]
        ]
    ) -> dict[str, str]:
        self.components = scaffold_setup(self.ctx)
        for component in self.components:
            self._assert_component_can_run(component)
            component.build(self.ctx)
        return self._assemble_files()

    def _assert_component_can_run(self, component: ScaffoldComponent) -> None:
        for required_ctx in component.requires_context:
            if required_ctx not in self.ctx:
                raise RequiredContextNotFound(component, required_ctx)

    def _assemble_files(self) -> dict[str, str]:
        return {
            filename: file.ctx[FileAssembler].assemble_file(file)
            for filename, file in self.ctx.files.items()
        }
