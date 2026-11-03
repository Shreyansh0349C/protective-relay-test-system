"""
RELAYLAB X — Measurement Engine

Provides mathematically correct RMS, frequency, and phase calculations
for use with both simulated and future real hardware data.
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional


@dataclass
class MeasurementResult:
    """Container for a complete set of measurements."""
    voltage_rms: float = 0.0
    current_rms: float = 0.0
    voltage_peak: float = 0.0
    current_peak: float = 0.0
    voltage_min: float = 0.0
    current_min: float = 0.0
    voltage_max: float = 0.0
    current_max: float = 0.0
    frequency: float = 0.0
    phase_difference: float = 0.0  # Degrees
    power_apparent: float = 0.0    # VA
    power_active: float = 0.0      # W
    power_factor: float = 0.0
    is_valid: bool = False
    source: str = "SIMULATED"


class MeasurementEngine:
    """
    Performs signal measurements on sampled waveform data.

    All calculations use standard mathematical definitions:
      Vrms = sqrt(mean(v^2))     — true RMS from samples
      Vrms = Vpeak / sqrt(2)     — for pure sinusoids
    """

    def __init__(self):
        self._voltage_buffer = np.array([])
        self._current_buffer = np.array([])
        self._time_buffer = np.array([])
        self._buffer_duration = 0.1  # seconds of data to keep
        self._sample_rate = 10000.0
        self._max_buffer_samples = int(self._buffer_duration * self._sample_rate)

    def update_data(self, time_data: np.ndarray, voltage: np.ndarray, current: np.ndarray):
        """
        Append new data to the measurement buffer.
        Old data beyond buffer_duration is discarded.
        """
        if len(time_data) == 0:
            return

        self._time_buffer = np.concatenate([self._time_buffer, time_data])
        self._voltage_buffer = np.concatenate([self._voltage_buffer, voltage])
        self._current_buffer = np.concatenate([self._current_buffer, current])

        # Trim to max buffer size
        if len(self._time_buffer) > self._max_buffer_samples:
            excess = len(self._time_buffer) - self._max_buffer_samples
            self._time_buffer = self._time_buffer[excess:]
            self._voltage_buffer = self._voltage_buffer[excess:]
            self._current_buffer = self._current_buffer[excess:]

    def compute(self) -> MeasurementResult:
        """Compute all measurements from buffered data."""
        result = MeasurementResult()

        if len(self._voltage_buffer) < 10:
            return result

        result.is_valid = True
        result.source = "SIMULATED"

        # True RMS from samples: Vrms = sqrt(mean(v^2))
        result.voltage_rms = self.calculate_rms(self._voltage_buffer)
        result.current_rms = self.calculate_rms(self._current_buffer)

        # Peak measurements
        result.voltage_peak = float(np.max(np.abs(self._voltage_buffer)))
        result.current_peak = float(np.max(np.abs(self._current_buffer)))

        # Min/Max
        result.voltage_min = float(np.min(self._voltage_buffer))
        result.voltage_max = float(np.max(self._voltage_buffer))
        result.current_min = float(np.min(self._current_buffer))
        result.current_max = float(np.max(self._current_buffer))

        # Frequency from zero crossings
        result.frequency = self.calculate_frequency(
            self._voltage_buffer, self._time_buffer
        )

        # Phase difference
        result.phase_difference = self.calculate_phase_difference(
            self._voltage_buffer, self._current_buffer, self._time_buffer
        )

        # Power calculations
        if result.voltage_rms > 0 and result.current_rms > 0:
            result.power_apparent = result.voltage_rms * result.current_rms
            result.power_factor = np.cos(np.radians(result.phase_difference))
            result.power_active = result.power_apparent * result.power_factor

        return result

    @staticmethod
    def calculate_rms(signal: np.ndarray) -> float:
        """
        Calculate true RMS from sampled data.
        Vrms = sqrt(mean(v²))
        """
        if len(signal) == 0:
            return 0.0
        return float(np.sqrt(np.mean(signal ** 2)))

    @staticmethod
    def calculate_rms_sinusoidal(peak: float) -> float:
        """
        Calculate RMS for a pure sinusoidal signal.
        Vrms = Vpeak / sqrt(2)
        """
        return peak / np.sqrt(2)

    @staticmethod
    def calculate_frequency(signal: np.ndarray, time: np.ndarray) -> float:
        """
        Calculate frequency from zero crossings.
        Uses positive-going zero crossings for accuracy.
        """
        if len(signal) < 4 or len(time) < 4:
            return 0.0

        # Find positive-going zero crossings
        crossings = []
        for i in range(1, len(signal)):
            if signal[i - 1] <= 0 < signal[i]:
                # Linear interpolation for precise crossing time
                t_cross = time[i - 1] + (time[i] - time[i - 1]) * (
                    -signal[i - 1] / (signal[i] - signal[i - 1])
                )
                crossings.append(t_cross)

        if len(crossings) < 2:
            return 0.0

        # Average period from all consecutive crossing pairs
        periods = np.diff(crossings)
        if len(periods) == 0:
            return 0.0

        avg_period = np.mean(periods)
        if avg_period <= 0:
            return 0.0

        return float(1.0 / avg_period)

    @staticmethod
    def calculate_phase_difference(
        voltage: np.ndarray, current: np.ndarray, time: np.ndarray
    ) -> float:
        """
        Calculate phase difference between voltage and current signals.
        Returns result in degrees. Positive means current lags voltage.
        """
        if len(voltage) < 4 or len(current) < 4:
            return 0.0

        def find_first_crossing(signal, t):
            for i in range(1, len(signal)):
                if signal[i - 1] <= 0 < signal[i]:
                    return t[i - 1] + (t[i] - t[i - 1]) * (
                        -signal[i - 1] / (signal[i] - signal[i - 1])
                    )
            return None

        v_cross = find_first_crossing(voltage, time)
        i_cross = find_first_crossing(current, time)

        if v_cross is None or i_cross is None:
            return 0.0

        # Estimate frequency for phase calculation
        freq = MeasurementEngine.calculate_frequency(voltage, time)
        if freq <= 0:
            return 0.0

        period = 1.0 / freq
        time_diff = i_cross - v_cross

        # Normalize to [-period/2, period/2]
        while time_diff > period / 2:
            time_diff -= period
        while time_diff < -period / 2:
            time_diff += period

        phase_deg = (time_diff / period) * 360.0
        return float(phase_deg)

    def reset(self):
        """Clear all buffered data."""
        self._voltage_buffer = np.array([])
        self._current_buffer = np.array([])
        self._time_buffer = np.array([])


class CursorMeasurement:
    """Handles measurement cursor calculations."""

    def __init__(self):
        self.cursor_a_time: float = 0.0
        self.cursor_b_time: float = 0.0
        self.cursor_a_enabled: bool = False
        self.cursor_b_enabled: bool = False

    @property
    def delta_time(self) -> float:
        """Time difference between cursors."""
        return abs(self.cursor_b_time - self.cursor_a_time)

    @property
    def frequency(self) -> Optional[float]:
        """Frequency derived from cursor delta time."""
        dt = self.delta_time
        if dt > 0:
            return 1.0 / dt
        return None

    def get_value_at_cursor(
        self, time_data: np.ndarray, signal: np.ndarray, cursor_time: float
    ) -> Optional[float]:
        """Interpolate signal value at cursor position."""
        if len(time_data) == 0 or len(signal) == 0:
            return None

        if cursor_time < time_data[0] or cursor_time > time_data[-1]:
            return None

        return float(np.interp(cursor_time, time_data, signal))
