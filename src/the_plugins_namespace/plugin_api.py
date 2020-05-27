from abc import ABC, abstractmethod
from typing import Any, Dict


class PluginApi(ABC):

    @abstractmethod
    @property
    def name(self) -> str:
        pass

    @abstractmethod
    @property
    def description(self) -> str:
        pass

    @abstractmethod
    def run(self, config: Dict[str, Any]) -> str:
        pass
