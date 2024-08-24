"""
Combine all settings from settings files
"""

from pathlib import Path

from split_settings.tools import include

# Base dir
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Settings files
_settings = (
    'base',
    'database',
    'baton',
)

# Combining settings
include(*[f'{settings}.py' for settings in _settings])
