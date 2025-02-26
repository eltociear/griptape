from unittest.mock import Mock
import pytest
from griptape.drivers.event_listener.local_event_listener_driver import LocalEventListenerDriver
from griptape.structures import Pipeline
from griptape.tasks import ToolkitTask, ActionsSubtask
from griptape.events import (
    StartTaskEvent,
    FinishTaskEvent,
    StartActionsSubtaskEvent,
    FinishActionsSubtaskEvent,
    StartPromptEvent,
    FinishPromptEvent,
    StartStructureRunEvent,
    FinishStructureRunEvent,
    CompletionChunkEvent,
    EventListener,
)
from tests.mocks.mock_prompt_driver import MockPromptDriver
from tests.mocks.mock_tool.tool import MockTool


class TestEventListener:
    @pytest.fixture
    def pipeline(self):
        task = ToolkitTask("test", tools=[MockTool(name="Tool1")])

        pipeline = Pipeline(prompt_driver=MockPromptDriver(stream=True))
        pipeline.add_task(task)

        task.add_subtask(ActionsSubtask("foo"))
        return pipeline

    def test_untyped_listeners(self, pipeline):
        event_handler_1 = Mock()
        event_handler_2 = Mock()

        pipeline.event_listeners = [
            EventListener(driver=LocalEventListenerDriver(handler=event_handler_1)),
            EventListener(driver=LocalEventListenerDriver(handler=event_handler_2)),
        ]
        # can't mock subtask events, so must manually call
        pipeline.tasks[0].subtasks[0].before_run()
        pipeline.tasks[0].subtasks[0].after_run()
        pipeline.run()

        assert event_handler_1.call_count == 9
        assert event_handler_2.call_count == 9

    def test_typed_listeners(self, pipeline):
        start_prompt_event_handler = Mock()
        finish_prompt_event_handler = Mock()
        start_task_event_handler = Mock()
        finish_task_event_handler = Mock()
        start_subtask_event_handler = Mock()
        finish_subtask_event_handler = Mock()
        start_structure_run_event_handler = Mock()
        finish_structure_run_event_handler = Mock()
        completion_chunk_handler = Mock()

        pipeline.event_listeners = [
            EventListener(
                driver=LocalEventListenerDriver(handler=start_prompt_event_handler), event_types=[StartPromptEvent]
            ),
            EventListener(
                driver=LocalEventListenerDriver(handler=finish_prompt_event_handler), event_types=[FinishPromptEvent]
            ),
            EventListener(
                driver=LocalEventListenerDriver(handler=start_task_event_handler), event_types=[StartTaskEvent]
            ),
            EventListener(
                driver=LocalEventListenerDriver(handler=finish_task_event_handler), event_types=[FinishTaskEvent]
            ),
            EventListener(
                driver=LocalEventListenerDriver(handler=start_subtask_event_handler),
                event_types=[StartActionsSubtaskEvent],
            ),
            EventListener(
                driver=LocalEventListenerDriver(handler=finish_subtask_event_handler),
                event_types=[FinishActionsSubtaskEvent],
            ),
            EventListener(
                driver=LocalEventListenerDriver(handler=start_structure_run_event_handler),
                event_types=[StartStructureRunEvent],
            ),
            EventListener(
                driver=LocalEventListenerDriver(handler=finish_structure_run_event_handler),
                event_types=[FinishStructureRunEvent],
            ),
            EventListener(
                driver=LocalEventListenerDriver(handler=completion_chunk_handler), event_types=[CompletionChunkEvent]
            ),
        ]

        # can't mock subtask events, so must manually call
        pipeline.tasks[0].subtasks[0].before_run()
        pipeline.tasks[0].subtasks[0].after_run()
        pipeline.run()

        start_prompt_event_handler.assert_called_once()
        finish_prompt_event_handler.assert_called_once()
        start_task_event_handler.assert_called_once()
        finish_task_event_handler.assert_called_once()
        start_subtask_event_handler.assert_called_once()
        finish_subtask_event_handler.assert_called_once()
        start_structure_run_event_handler.assert_called_once()
        finish_structure_run_event_handler.assert_called_once()
        completion_chunk_handler.assert_called_once()

    def test_add_remove_event_listener(self, pipeline):
        pipeline.event_listeners = []
        mock1 = Mock()
        mock2 = Mock()
        event_listener_1 = pipeline.add_event_listener(
            EventListener(driver=LocalEventListenerDriver(handler=mock1), event_types=[StartPromptEvent])
        )

        event_listener_2 = pipeline.add_event_listener(
            EventListener(driver=LocalEventListenerDriver(handler=mock1), event_types=[FinishPromptEvent])
        )
        event_listener_3 = pipeline.add_event_listener(
            EventListener(driver=LocalEventListenerDriver(handler=mock2), event_types=[StartPromptEvent])
        )

        event_listener_4 = pipeline.add_event_listener(EventListener(driver=LocalEventListenerDriver(handler=mock2)))

        assert len(pipeline.event_listeners) == 4

        pipeline.remove_event_listener(event_listener_1)
        pipeline.remove_event_listener(event_listener_2)
        pipeline.remove_event_listener(event_listener_3)
        pipeline.remove_event_listener(event_listener_4)
        assert len(pipeline.event_listeners) == 0
