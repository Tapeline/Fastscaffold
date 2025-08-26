from pathlib import Path

from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import WebProjectConfig


def with_src(ctx: ScaffoldRunContext, *path: str) -> str:
    return str(Path(ctx[WebProjectConfig].src, *path))
