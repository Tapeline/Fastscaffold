from abc import abstractmethod, ABC
from typing import Any, ClassVar

from fastscaffold.core.context import ScaffoldRunContext


class ScaffoldComponent(ABC):
    requires_context: ClassVar[list[type[Any]]] = []

    @abstractmethod
    def build(self, ctx: ScaffoldRunContext) -> None:
        raise NotImplementedError


