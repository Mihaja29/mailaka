"""Storage management for inboxes."""

import json
from pathlib import Path
from typing import List, Optional

from .models import Inbox
from ..utils.errors import StorageError


class InboxStorage:
    """Manages persistent storage of inboxes."""
    
    def __init__(self, storage_path: Optional[Path] = None):
        """Initialize storage manager.
        
        Args:
            storage_path: Path to storage file. If None, uses default location.
        """
        self.storage_path = storage_path or Path.home() / ".mailaka_inboxes.json"
    
    def load(self) -> List[Inbox]:
        """Load all inboxes from storage.
        
        Returns:
            List of Inbox objects
            
        Raises:
            StorageError: If loading fails
        """
        if not self.storage_path.exists():
            return []
        
        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            return [Inbox.from_dict(item) for item in data]
        except (json.JSONDecodeError, OSError) as e:
            raise StorageError(f"Failed to load inboxes: {e}")
    
    def save(self, inboxes: List[Inbox]) -> None:
        """Save inboxes to storage.
        
        Args:
            inboxes: List of Inbox objects to save
            
        Raises:
            StorageError: If saving fails
        """
        try:
            data = [inbox.to_dict() for inbox in inboxes]
            self.storage_path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except OSError as e:
            raise StorageError(f"Failed to save inboxes: {e}")
    
    def add(self, inbox: Inbox) -> None:
        """Add an inbox to storage.
        
        Args:
            inbox: Inbox object to add
        """
        inboxes = self.load()
        inboxes.append(inbox)
        self.save(inboxes)
    
    def get_latest(self) -> Optional[Inbox]:
        """Get the most recently added inbox.
        
        Returns:
            Latest Inbox object or None if no inboxes exist
        """
        inboxes = self.load()
        return inboxes[-1] if inboxes else None
    
    def clear(self) -> None:
        """Clear all stored inboxes."""
        self.save([])
