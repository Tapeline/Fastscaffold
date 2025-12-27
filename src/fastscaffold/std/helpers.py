from os.path import commonprefix
from pathlib import Path

import inflect

from fastscaffold.core.context import ScaffoldRunContext
from fastscaffold.std.configs import WebProjectConfig


def with_src(ctx: ScaffoldRunContext, *path: str) -> str:
    return str(Path(ctx[WebProjectConfig].src, *path))


eng = inflect.engine()


def plural(s: str) -> str:
    plural_lwc = eng.plural(s.lower(), 2)
    common_prefix = commonprefix([plural_lwc, s.lower()])
    return s[:len(common_prefix)] + plural_lwc[len(common_prefix):]
