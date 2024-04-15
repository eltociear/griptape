from abc import ABC, abstractmethod
from attr import define
from griptape.engines.rag import RagContext


@define(kw_only=True)
class BaseStage(ABC):
    @abstractmethod
    def run(self, context: RagContext) -> RagContext:
        ...
