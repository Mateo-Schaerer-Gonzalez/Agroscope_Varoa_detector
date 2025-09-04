import os
from typing import Union, Optional


class Settings:
    """Settings class that reads and parses settings from a text file."""
    
    def __init__(self, folder_path: str):
        """
        Initialize Settings by loading from settings.txt in the given folder.
        
        Args:
            folder_path (str): Path to the folder containing settings.txt
        """
        self.folder_path = folder_path
        self.settings_data = {}
        self._load_settings()
    
    def _load_settings(self):
        """Load settings from a text file using the get_settings function."""
        settings_content = get_settings(self.folder_path)
        self._parse_settings(settings_content)
    
    def _parse_settings(self, content: str):
        """Parse the settings content into a dictionary."""
        self.settings_data = {}
        
        for line in content.strip().split('\n'):
            line = line.strip()
            if line and '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Try to convert to appropriate type
                self.settings_data[key] = self._convert_value(value)
    
    def _convert_value(self, value: str) -> Union[int, float, str]:
        """Convert string value to appropriate type (int, float, or str)."""
        # Try int first
        try:
            return int(value)
        except ValueError:
            pass
        
        # Try float
        try:
            return float(value)
        except ValueError:
            pass
        
        # Return as string
        return value
    
    def get(self, key: str, default=None):
        """
        Get a setting value by key.
        
        Args:
            key (str): The setting key
            default: Default value if key not found
            
        Returns:
            The setting value or default
        """
        return self.settings_data.get(key, default)
    
    def __getitem__(self, key: str):
        """Allow dictionary-style access to settings."""
        return self.settings_data[key]
    
    def __contains__(self, key: str):
        """Allow 'in' operator to check if key exists."""
        return key in self.settings_data
    
    def keys(self):
        """Return all setting keys."""
        return self.settings_data.keys()
    
    def values(self):
        """Return all setting values."""
        return self.settings_data.values()
    
    def items(self):
        """Return all setting key-value pairs."""
        return self.settings_data.items()
    
    # Specific property accessors for common settings
    @property
    def recording_count(self) -> int:
        """Get recording count setting."""
        return self.get('recording_count', 1)
    
    @property
    def recording_timeout(self) -> int:
        """Get recording timeout setting."""
        return self.get('recording_timeout', 1)
    
    @property
    def vent_time(self) -> int:
        """Get vent time setting."""
        return self.get('vent_time', 20)
    
    @property
    def led1_time(self) -> int:
        """Get LED1 time setting."""
        return self.get('led1_time', 20)
    
    @property
    def led2_time(self) -> int:
        """Get LED2 time setting."""
        return self.get('led2_time', 20)
    
    @property
    def frame_count(self) -> int:
        """Get frame count setting."""
        return self.get('frame_count', 30)
    
    @property
    def fps(self) -> int:
        """Get FPS setting."""
        return self.get('fps', 30)
    
    @property
    def vent(self) -> int:
        """Get vent setting."""
        return self.get('vent', 255)
    
    @property
    def led1(self) -> int:
        """Get LED1 setting."""
        return self.get('led1', 255)
    
    @property
    def led2(self) -> int:
        """Get LED2 setting."""
        return self.get('led2', 255)
    
    def __str__(self):
        """String representation of settings."""
        lines = [f"{key}={value}" for key, value in sorted(self.settings_data.items())]
        return '\n'.join(lines)
    
    def __repr__(self):
        """Representation of settings object."""
        return f"Settings(folder_path='{self.folder_path}', keys={list(self.settings_data.keys())})"


def get_settings(folder_path):
    """Load settings from a text file."""
    settings_file = os.path.join(folder_path, ".settings.txt")
    if not os.path.exists(settings_file):
        raise FileNotFoundError(f"Settings file not found: {settings_file}")

    with open(settings_file, "r") as f:
        settings = f.read()

    return settings

