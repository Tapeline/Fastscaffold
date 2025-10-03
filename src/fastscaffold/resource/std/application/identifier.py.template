import uuid
from abc import abstractmethod
from typing import Protocol


class UUIDGenerator(Protocol):
    """UUID generator."""

    @abstractmethod
    def __call__(self) -> uuid.UUID:
        """Generate a UUID."""
