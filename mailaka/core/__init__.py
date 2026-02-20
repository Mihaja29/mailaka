"""Core business logic for Mailaka."""

from .models import Inbox, Message
from .storage import InboxStorage
from .provider import ProviderFactory, Provider, ProviderError

__all__ = [
    "Inbox",
    "Message",
    "InboxStorage",
    "ProviderFactory",
    "Provider",
    "ProviderError",
]
