from abc import ABC, abstractmethod
from typing import Any


class BaseProcess(ABC):
    @abstractmethod
    def process(self, *args: Any, **kwargs: Any) -> Any:
        pass
