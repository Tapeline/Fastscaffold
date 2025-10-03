import textwrap
from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any, ClassVar

from fastscaffold.core.component import ScaffoldComponent
from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import WebProjectConfig
from fastscaffold.std.helpers import with_src
from fastscaffold.std.jinja import Jinja


class SourceGen(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
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


class SimpleTemplateRender(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        Jinja
    ]
    location: list[str] = []
    template: str = ""
    replace_file: bool = False

    def get_location(self, ctx: ScaffoldRunContext) -> list[str]:
        return self.location

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        return dict(
            web_project=ctx[WebProjectConfig],
            slug=ctx[WebProjectConfig].slug
        )

    def before_build(self, ctx: ScaffoldRunContext) -> None:
        ...

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        ...

    def build(self, ctx: ScaffoldRunContext) -> None:
        self.before_build(ctx)
        jinja_vars = self.get_jinja_vars(ctx)
        template = ctx[Jinja].env.get_template(self.template)
        result = template.render(**jinja_vars)
        file = ctx.files[src_in(*self.get_location(ctx))(ctx)]
        if self.replace_file:
            file.lines.clear()
        file.lines.extend(result.splitlines())
        self.after_build(ctx)


class SimpleManyTemplatesRender(ScaffoldComponent):
    requires_context = [
        WebProjectConfig,
        Jinja
    ]
    base_dir: ClassVar[list[str]] = []
    templates: ClassVar[dict[str, str]] = {}
    replace_files: bool = False

    def get_base_dir(self, ctx: ScaffoldRunContext) -> list[str]:
        return self.base_dir

    def get_jinja_vars(self, ctx: ScaffoldRunContext) -> dict[str, Any]:
        return dict(
            web_project=ctx[WebProjectConfig],
            slug=ctx[WebProjectConfig].slug
        )

    def before_build(self, ctx: ScaffoldRunContext) -> None:
        ...

    def after_build(self, ctx: ScaffoldRunContext) -> None:
        ...

    def build(self, ctx: ScaffoldRunContext) -> None:
        self.before_build(ctx)
        jinja_vars = self.get_jinja_vars(ctx)
        for template_dst, template_src in self.templates.items():
            template = ctx[Jinja].env.get_template(template_src)
            result = template.render(**jinja_vars)
            file = ctx.files[src_in(
                *self.get_base_dir(ctx),
                template_dst
            )(ctx)]
            if self.replace_files:
                file.lines.clear()
            file.lines.extend(result.splitlines())
        self.after_build(ctx)


def src_in(where: str, *path: str) -> Callable[[ScaffoldRunContext], str]:
    return {
        "domain": lambda ctx: with_src(
            ctx,
            ctx[WebProjectConfig].slug,
            "domain",
            *path
        ),
        "application": lambda ctx: with_src(
            ctx,
            ctx[WebProjectConfig].slug,
            "application",
            *path
        ),
        "infrastructure": lambda ctx: with_src(
            ctx,
            ctx[WebProjectConfig].slug,
            "infrastructure",
            *path
        ),
        "bootstrap": lambda ctx: with_src(
            ctx,
            ctx[WebProjectConfig].slug,
            "bootstrap",
            *path
        ),
        "presentation": lambda ctx: with_src(
            ctx,
            ctx[WebProjectConfig].slug,
            "presentation",
            *path
        )
    }.get(
        where,
        lambda ctx: with_src(
            ctx,
            ctx[WebProjectConfig].slug,
            where,
            *path
        )
    )


def import_from(pkg: str) -> Callable[[ScaffoldRunContext], str]:
    return lambda ctx: f"{ctx[WebProjectConfig].slug}.{pkg}"
