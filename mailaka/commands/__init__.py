"""Command modules for Mailaka CLI."""

from .new import new
from .inbox import inbox
from .read import read
from .delete import delete
from .attachments import attachments
from .download import download
from .status import status
from .list_inboxes import list_inboxes

__all__ = [
    "new",
    "inbox",
    "read",
    "delete",
    "attachments",
    "download",
    "status",
    "list_inboxes",
]
