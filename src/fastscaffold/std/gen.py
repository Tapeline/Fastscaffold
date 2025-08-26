import textwrap
from collections.abc import Callable

from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import ArchitectureConfig, WebProjectConfig
from fastscaffold.std.helpers import with_src


class SourceGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig
    ]

    def __init__(
        self,
        filename: str | Callable[[ScaffoldRunContext], str],
        src: str
    ) -> None:
        self.src = textwrap.dedent(src).splitlines()
        self.filename = filename

    def build(self, ctx: ScaffoldRunContext) -> None:
        if isinstance(self.filename, str):
            filename = with_src(ctx, self.filename)
        else:
            filename = self.filename(ctx)
        ctx.files[filename].lines = self.src


class AddImports(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        ArchitectureConfig
    ]

    def __init__(
        self,
        filename: str | Callable[[ScaffoldRunContext], str],
        *import_lines: str,
    ) -> None:
        self.filename = filename
        self.import_lines = import_lines

    def build(self, ctx: ScaffoldRunContext) -> None:
        if isinstance(self.filename, str):
            filename = with_src(ctx, self.filename)
        else:
            filename = self.filename(ctx)
        ctx.files[filename].lines = [
            *self.import_lines,
            *ctx.files[filename].lines
        ]


def src_in(where: str, *path: str) -> Callable[[ScaffoldRunContext], str]:
    return {
        "domain": lambda ctx: with_src(
            ctx,
            ctx[WebProjectConfig].slug,
            ctx[ArchitectureConfig].domain_pkg,
            *path
        ),
        "application": lambda ctx: with_src(
            ctx,
            ctx[WebProjectConfig].slug,
            ctx[ArchitectureConfig].application_pkg,
            *path
        ),
        "infrastructure": lambda ctx: with_src(
            ctx,
            ctx[WebProjectConfig].slug,
            ctx[ArchitectureConfig].infrastructure_pkg,
            *path
        ),
        "bootstrap": lambda ctx: with_src(
            ctx,
            ctx[WebProjectConfig].slug,
            ctx[ArchitectureConfig].bootstrap_pkg,
            *path
        ),
        "presentation": lambda ctx: with_src(
            ctx,
            ctx[WebProjectConfig].slug,
            ctx[ArchitectureConfig].presentation_pkg,
            *path
        )
    }[where]


def import_from(pkg: str) -> Callable[[ScaffoldRunContext], str]:
    return lambda ctx: f"{ctx[WebProjectConfig].slug}.{pkg}"
