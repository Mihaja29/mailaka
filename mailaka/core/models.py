"""Data models for Mailaka."""

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any


@dataclass
class Inbox:
    """Represents an ephemeral email inbox."""
    
    provider: str
    address: str
    login: Optional[str] = None
    domain: Optional[str] = None
    token: Optional[str] = None
    password: Optional[str] = None
    account_id: Optional[str] = None
    comment: Optional[str] = None  # Note modifiable par l'utilisateur
    inbox_type: Optional[str] = "temp"  # "temp" (15min) ou "longterm"
    created_at: Optional[str] = None    # ISO datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert inbox to dictionary.
        
        Returns:
            Dictionary representation of inbox
        """
        data = asdict(self)
        # Remove None values
        return {k: v for k, v in data.items() if v is not None}
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Inbox":
        """Create inbox from dictionary.
        
        Args:
            data: Dictionary containing inbox data
            
        Returns:
            Inbox instance
        """
        return cls(**data)


@dataclass
class Message:
    """Represents an email message."""
    
    id: str
    sender: str
    subject: str
    body: Optional[str] = None
    date: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary.
        
        Returns:
            Dictionary representation of message
        """
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create message from dictionary.
        
        Args:
            data: Dictionary containing message data
            
        Returns:
            Message instance
        """
        return cls(**data)
