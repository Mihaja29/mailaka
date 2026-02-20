"""Custom exception classes for Mailaka."""


class MailakaError(Exception):
    """Base exception for Mailaka errors."""
    pass


class ProviderError(MailakaError):
    """Exception raised when a provider API fails."""
    pass


class StorageError(MailakaError):
    """Exception raised when storage operations fail."""
    pass
