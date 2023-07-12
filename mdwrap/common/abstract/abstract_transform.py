from abc import ABC, abstractmethod

from mdwrap.common.abstract.abstract_line_context import AbstractLineContext


class AbstractTransform(ABC):
    """Abstract base class for applying a tranformation to lines of text."""

    @abstractmethod
    def apply(self, *, context: AbstractLineContext) -> None:
        """Transform the lines of text."""
        raise NotImplementedError
