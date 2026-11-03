"""Tests for the measurement engine."""

import pytest
import numpy as np
from app.core.measurements import MeasurementEngine, CursorMeasurement


class TestRMSCalculation:
    """Test RMS calculation accuracy."""

    def test_sine_wave_rms(self):
        amplitude = 325.27
        t = np.linspace(0, 0.1, 10000, endpoint=False)
        signal = amplitude * np.sin(2 * np.pi * 50 * t)

        rms = MeasurementEngine.calculate_rms(signal)
        expected = amplitude / np.sqrt(2)
        assert abs(rms - expected) < 1.0

    def test_sinusoidal_rms_formula(self):
        peak = 325.27
        rms = MeasurementEngine.calculate_rms_sinusoidal(peak)
        assert abs(rms - 230.0) < 0.2

    def test_dc_signal_rms(self):
        signal = np.full(1000, 5.0)
        rms = MeasurementEngine.calculate_rms(signal)
        assert abs(rms - 5.0) < 0.001

    def test_zero_signal_rms(self):
        signal = np.zeros(1000)
        rms = MeasurementEngine.calculate_rms(signal)
        assert rms == 0.0

    def test_empty_signal_rms(self):
        signal = np.array([])
        rms = MeasurementEngine.calculate_rms(signal)
        assert rms == 0.0


class TestFrequencyCalculation:
    """Test frequency measurement."""

    def test_50hz_frequency(self):
        t = np.linspace(0, 0.1, 10000, endpoint=False)
        signal = np.sin(2 * np.pi * 50 * t)

        freq = MeasurementEngine.calculate_frequency(signal, t)
        assert abs(freq - 50.0) < 0.5


class TestPhaseDifference:
    """Test phase difference calculation."""

    def test_zero_phase(self):
        t = np.linspace(0, 0.1, 10000, endpoint=False)
        v = np.sin(2 * np.pi * 50 * t)
        i = np.sin(2 * np.pi * 50 * t)

        phase = MeasurementEngine.calculate_phase_difference(v, i, t)
        assert abs(phase) < 2.0


class TestCursorMeasurement:
    """Test cursor measurement calculations."""

    def test_delta_time(self):
        cursor = CursorMeasurement()
        cursor.cursor_a_time = 0.005
        cursor.cursor_b_time = 0.025
        assert abs(cursor.delta_time - 0.020) < 1e-10

    def test_cursor_frequency(self):
        cursor = CursorMeasurement()
        cursor.cursor_a_time = 0.0
        cursor.cursor_b_time = 0.020
        freq = cursor.frequency
        assert freq is not None
        assert abs(freq - 50.0) < 0.01
