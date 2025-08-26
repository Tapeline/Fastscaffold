from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from fastscaffold.core.context import ScaffoldContext


@dataclass
class ScaffoldFile:
    path: str
    lines: list[str]
    ctx: "ScaffoldContext"

    def __post_init__(self):
        self.ctx[FileAssembler] = DefaultFileAssembler()


class FileAssembler(Protocol):
    @abstractmethod
    def assemble_file(self, file: ScaffoldFile) -> str:
        raise NotImplementedError


class DefaultFileAssembler(FileAssembler):
    def assemble_file(self, file: ScaffoldFile) -> str:
        return "\n".join(file.lines)
