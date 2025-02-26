from unittest.mock import Mock
from pytest import fixture
from tests.mocks.mock_event import MockEvent
from griptape.drivers.event_listener.webhook_event_listener_driver import WebhookEventListenerDriver


class TestWebhookEventListenerDriver:
    @fixture(autouse=True)
    def mock_post(self, mocker):
        mock_post = mocker.patch("requests.post")
        mock_post.return_value = Mock(status_code=201)

        return mock_post

    def test_init(self):
        assert WebhookEventListenerDriver(webhook_url="")

    def test_try_publish_event(self, mock_post):
        driver = WebhookEventListenerDriver(webhook_url="foo bar", headers={"Authorization": "Bearer foo bar"})
        event = MockEvent()
        driver.try_publish_event(event=event)

        mock_post.assert_called_once_with(
            url="foo bar", json={"event": event.to_dict()}, headers={"Authorization": "Bearer foo bar"}
        )
