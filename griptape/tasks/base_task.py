from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from concurrent import futures
from enum import Enum
from typing import TYPE_CHECKING, Any, Optional
from collections.abc import Sequence

from attr import define, field, Factory

from griptape.events import StartTaskEvent, FinishTaskEvent
from griptape.artifacts import ErrorArtifact

if TYPE_CHECKING:
    from griptape.artifacts import BaseArtifact
    from griptape.structures import Structure
    from griptape.memory.meta import BaseMetaEntry


@define
class BaseTask(ABC):
    class State(Enum):
        PENDING = 1
        EXECUTING = 2
        FINISHED = 3

    id: str = field(default=Factory(lambda: uuid.uuid4().hex), kw_only=True)
    state: State = field(default=State.PENDING, kw_only=True)
    parent_ids: list[str] = field(factory=list, kw_only=True)
    child_ids: list[str] = field(factory=list, kw_only=True)
    max_meta_memory_entries: Optional[int] = field(default=20, kw_only=True)

    output: Optional[BaseArtifact] = field(default=None, init=False)
    structure: Optional[Structure] = field(default=None, init=False)
    context: dict[str, Any] = field(factory=dict, kw_only=True)
    futures_executor: futures.Executor = field(default=Factory(lambda: futures.ThreadPoolExecutor()), kw_only=True)

    @property
    @abstractmethod
    def input(self) -> BaseArtifact | tuple[BaseArtifact, ...] | tuple[BaseArtifact, Sequence[BaseArtifact]]:
        ...

    @property
    def parents(self) -> list[BaseTask]:
        return [self.structure.find_task(parent_id) for parent_id in self.parent_ids]

    @property
    def children(self) -> list[BaseTask]:
        return [self.structure.find_task(child_id) for child_id in self.child_ids]

    @property
    def meta_memories(self) -> list[BaseMetaEntry]:
        if self.structure and self.structure.meta_memory:
            if self.max_meta_memory_entries:
                return self.structure.meta_memory.entries[: self.max_meta_memory_entries]
            else:
                return self.structure.meta_memory.entries
        else:
            return []

    def __str__(self) -> str:
        return str(self.output.value)

    def preprocess(self, structure: Structure) -> BaseTask:
        self.structure = structure

        return self

    def is_pending(self) -> bool:
        return self.state == BaseTask.State.PENDING

    def is_finished(self) -> bool:
        return self.state == BaseTask.State.FINISHED

    def is_executing(self) -> bool:
        return self.state == BaseTask.State.EXECUTING

    def before_run(self) -> None:
        if self.structure:
            self.structure.publish_event(
                StartTaskEvent(
                    task_id=self.id,
                    task_parent_ids=self.parent_ids,
                    task_child_ids=self.child_ids,
                    task_input=self.input,
                    task_output=self.output,
                )
            )

    def after_run(self) -> None:
        if self.structure:
            self.structure.publish_event(
                FinishTaskEvent(
                    task_id=self.id,
                    task_parent_ids=self.parent_ids,
                    task_child_ids=self.child_ids,
                    task_input=self.input,
                    task_output=self.output,
                )
            )

    def execute(self) -> Optional[BaseArtifact]:
        try:
            self.state = BaseTask.State.EXECUTING

            self.before_run()

            self.output = self.run()

            self.after_run()
        except Exception as e:
            self.structure.logger.error(f"{self.__class__.__name__} {self.id}\n{e}", exc_info=True)

            self.output = ErrorArtifact(str(e), exception=e)
        finally:
            self.state = BaseTask.State.FINISHED

            return self.output

    def can_execute(self) -> bool:
        return self.state == BaseTask.State.PENDING and all(parent.is_finished() for parent in self.parents)

    def reset(self) -> BaseTask:
        self.state = BaseTask.State.PENDING
        self.output = None

        return self

    @abstractmethod
    def run(self) -> BaseArtifact:
        ...

    @property
    def full_context(self) -> dict[str, Any]:
        if self.structure:
            structure_context = self.structure.context(self)

            structure_context.update(self.context)

            return structure_context
        else:
            return {}
