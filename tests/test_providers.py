from mailaka.core.models import Inbox
from mailaka.core.provider import OneSecMailProvider, MailTmProvider, GuerrillaMailProvider


def test_1secmail_pagination_slices_locally(monkeypatch):
    provider = OneSecMailProvider()
    inbox = Inbox(provider="1secmail", address="a@b", login="a", domain="b")
    payload = [
        {"id": 1, "from": "a", "subject": "s1"},
        {"id": 2, "from": "b", "subject": "s2"},
        {"id": 3, "from": "c", "subject": "s3"},
    ]

    def fake_get_json(url, headers=None):
        return payload

    monkeypatch.setattr("mailaka.core.provider._http_get_json", fake_get_json)
    messages = provider.get_messages(inbox, limit=1, offset=1)
    assert len(messages) == 1
    assert messages[0].id == "2"


def test_guerrillamail_pagination_uses_offset(monkeypatch):
    provider = GuerrillaMailProvider()
    inbox = Inbox(provider="guerrillamail", address="x@y", token="token")

    def fake_get_json(url, headers=None):
        assert "offset=2" in url
        return {
            "list": [
                {"mail_id": "10", "mail_from": "a", "mail_subject": "s"},
            ]
        }

    monkeypatch.setattr("mailaka.core.provider._http_get_json", fake_get_json)
    messages = provider.get_messages(inbox, limit=1, offset=2)
    assert len(messages) == 1
    assert messages[0].id == "10"


def test_mailtm_get_attachments(monkeypatch):
    provider = MailTmProvider()
    inbox = Inbox(provider="mailtm", address="x@y", password="pw")

    def fake_post_json(url, data, headers=None):
        return {"token": "tok"}

    def fake_get_json(url, headers=None):
        return {
            "attachments": [
                {"id": "att-1", "filename": "file.txt"},
                {"id": "att-2", "filename": "image.png"},
            ]
        }

    monkeypatch.setattr("mailaka.core.provider._http_post_json", fake_post_json)
    monkeypatch.setattr("mailaka.core.provider._http_get_json", fake_get_json)

    attachments = provider.get_attachments(inbox, "msg-1")
    assert len(attachments) == 2
    assert attachments[0]["message_id"] == "msg-1"


def test_mailtm_delete_message(monkeypatch):
    provider = MailTmProvider()
    inbox = Inbox(provider="mailtm", address="x@y", password="pw")

    def fake_post_json(url, data, headers=None):
        return {"token": "tok"}

    class DummyResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    def fake_urlopen(request, timeout=15):
        assert request.method == "DELETE"
        return DummyResponse()

    monkeypatch.setattr("mailaka.core.provider._http_post_json", fake_post_json)
    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)

    provider.delete_message(inbox, "msg-1")
