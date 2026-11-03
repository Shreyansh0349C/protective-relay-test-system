"""
RELAYLAB X — Application Settings

Manages persistent application configuration and user preferences.
"""

import json
import os
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class OscilloscopeSettings:
    """Oscilloscope display settings."""
    voltage_scale: float = 100.0       # V/div
    current_scale: float = 5.0         # A/div
    timebase: float = 5.0              # ms/div
    voltage_offset: float = 0.0        # V
    current_offset: float = 0.0        # A
    voltage_enabled: bool = True
    current_enabled: bool = True
    grid_enabled: bool = True
    trigger_source: str = "CH1"        # CH1 or CH2
    trigger_edge: str = "rising"       # rising or falling
    trigger_level: float = 0.0         # V or A
    trigger_mode: str = "auto"         # auto, normal, single
    acquisition_mode: str = "normal"   # normal, average, peak_detect
    cursor_a_enabled: bool = False
    cursor_b_enabled: bool = False


@dataclass
class TestSettings:
    """Test configuration settings."""
    voltage_reference: float = 230.0   # V RMS
    current_reference: float = 10.0    # A RMS
    frequency: float = 50.0            # Hz (fixed Phase 1)
    phase_difference: float = 0.0      # Degrees
    test_duration: float = 0.0         # 0 = continuous


@dataclass
class CommunicationSettings:
    """Serial communication settings."""
    port: str = ""
    baud_rate: int = 115200
    data_bits: int = 8
    stop_bits: float = 1.0
    parity: str = "none"
    timeout: float = 1.0
    auto_reconnect: bool = True


@dataclass
class AppSettings:
    """Root application settings container."""
    oscilloscope: OscilloscopeSettings = field(default_factory=OscilloscopeSettings)
    test: TestSettings = field(default_factory=TestSettings)
    communication: CommunicationSettings = field(default_factory=CommunicationSettings)
    theme: str = "dark"
    fullscreen: bool = True
    simulation_mode: bool = True   # Always True in Phase 1
    last_page: str = "oscilloscope"

    # Validation limits
    VOLTAGE_MAX: float = 400.0
    CURRENT_MAX: float = 40.0
    VOLTAGE_MIN: float = 0.0
    CURRENT_MIN: float = 0.0


class SettingsManager:
    """
    Manages loading, saving, and validating application settings.
    Settings are stored as JSON in the user's config directory.
    """

    DEFAULT_CONFIG_DIR = os.path.join(
        os.path.expanduser("~"), ".relaylab"
    )
    CONFIG_FILENAME = "settings.json"

    def __init__(self, config_dir: Optional[str] = None):
        self._config_dir = config_dir or self.DEFAULT_CONFIG_DIR
        self._config_path = os.path.join(self._config_dir, self.CONFIG_FILENAME)
        self.settings = AppSettings()

    def load(self) -> AppSettings:
        """Load settings from disk, or return defaults if not found."""
        try:
            if os.path.exists(self._config_path):
                with open(self._config_path, "r") as f:
                    data = json.load(f)
                self._apply_dict(data)
        except (json.JSONDecodeError, IOError, KeyError):
            self.settings = AppSettings()
        return self.settings

    def save(self):
        """Save current settings to disk."""
        try:
            os.makedirs(self._config_dir, exist_ok=True)
            with open(self._config_path, "w") as f:
                json.dump(asdict(self.settings), f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save settings: {e}")

    def _apply_dict(self, data: dict):
        """Apply a dictionary of values to settings, with validation."""
        if "oscilloscope" in data:
            for k, v in data["oscilloscope"].items():
                if hasattr(self.settings.oscilloscope, k):
                    setattr(self.settings.oscilloscope, k, v)
        if "test" in data:
            for k, v in data["test"].items():
                if hasattr(self.settings.test, k):
                    setattr(self.settings.test, k, v)
        if "communication" in data:
            for k, v in data["communication"].items():
                if hasattr(self.settings.communication, k):
                    setattr(self.settings.communication, k, v)
        for key in ("theme", "fullscreen", "simulation_mode", "last_page"):
            if key in data:
                setattr(self.settings, key, data[key])
        self._validate()

    def _validate(self):
        """Ensure all settings are within valid ranges."""
        s = self.settings
        s.test.voltage_reference = max(s.VOLTAGE_MIN, min(s.VOLTAGE_MAX, s.test.voltage_reference))
        s.test.current_reference = max(s.CURRENT_MIN, min(s.CURRENT_MAX, s.test.current_reference))
        s.test.frequency = 50.0  # Fixed for Phase 1
        s.test.phase_difference = max(-180.0, min(180.0, s.test.phase_difference))
        s.oscilloscope.trigger_source = (
            s.oscilloscope.trigger_source
            if s.oscilloscope.trigger_source in ("CH1", "CH2")
            else "CH1"
        )
        s.oscilloscope.trigger_edge = (
            s.oscilloscope.trigger_edge
            if s.oscilloscope.trigger_edge in ("rising", "falling")
            else "rising"
        )
        s.oscilloscope.trigger_mode = (
            s.oscilloscope.trigger_mode
            if s.oscilloscope.trigger_mode in ("auto", "normal", "single")
            else "auto"
        )
        s.oscilloscope.acquisition_mode = (
            s.oscilloscope.acquisition_mode
            if s.oscilloscope.acquisition_mode in ("normal", "average", "peak_detect")
            else "normal"
        )

    def reset_to_defaults(self):
        """Reset all settings to factory defaults."""
        self.settings = AppSettings()
        self.save()
