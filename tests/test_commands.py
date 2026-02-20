from click.testing import CliRunner

from mailaka.cli import main
from mailaka.core.models import Inbox


def test_list_inboxes_empty(monkeypatch):
    runner = CliRunner()

    def fake_load(self):
        return []

    monkeypatch.setattr("mailaka.core.storage.InboxStorage.load", fake_load)
    result = runner.invoke(main, ["inboxes"])
    assert result.exit_code == 0
    assert "Aucune inbox" in result.output


def test_inbox_pagination_options(monkeypatch):
    runner = CliRunner()
    inbox = Inbox(provider="1secmail", address="a@b", login="a", domain="b")

    def fake_get_latest(self):
        return inbox

    class DummyProvider:
        def get_messages(self, inbox_arg, limit=None, offset=0):
            assert limit == 2
            assert offset == 1
            return []

    monkeypatch.setattr("mailaka.core.storage.InboxStorage.get_latest", fake_get_latest)
    monkeypatch.setattr("mailaka.core.provider.ProviderFactory.get_provider", lambda name: DummyProvider())

    result = runner.invoke(main, ["inbox", "--limit", "2", "--offset", "1"])
    assert result.exit_code == 0
