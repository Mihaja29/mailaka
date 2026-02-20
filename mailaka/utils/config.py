"""Configuration management for Mailaka."""

import json
from pathlib import Path
from typing import Dict, Any, Optional

from .errors import StorageError


class Config:
    """Configuration manager for Mailaka settings."""
    
    DEFAULT_CONFIG = {
        "default_provider": "1secmail",
        "auto_save": True,
        "storage_path": str(Path.home() / ".mailaka_inboxes.json"),
    }
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file. If None, uses default location.
        """
        self.config_path = config_path or Path.home() / ".mailaka_config.json"
        self._config = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Load configuration from file.
        
        Returns:
            Configuration dictionary
        """
        if not self.config_path.exists():
            return self.DEFAULT_CONFIG.copy()
        
        try:
            return json.loads(self.config_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            raise StorageError(f"Failed to load configuration: {e}")
    
    def save(self) -> None:
        """Save configuration to file."""
        try:
            self.config_path.write_text(
                json.dumps(self._config, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except OSError as e:
            raise StorageError(f"Failed to save configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self._config[key] = value
        self.save()
    
    def reset(self) -> None:
        """Reset configuration to defaults."""
        self._config = self.DEFAULT_CONFIG.copy()
        self.save()
