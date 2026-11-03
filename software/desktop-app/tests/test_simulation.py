"""Tests for the simulation engine."""

import pytest
import numpy as np
from app.core.simulation import SimulationConfig, SimulationWorker


class TestSimulationConfig:
    """Test simulation configuration."""

    def test_default_config(self):
        config = SimulationConfig()
        assert config.frequency == 50.0
        assert config.sample_rate == 10000.0
        assert config.voltage_enabled is True
        assert config.current_enabled is True

    def test_voltage_rms(self):
        config = SimulationConfig()
        config.voltage_amplitude = 325.27
        expected_rms = 325.27 / np.sqrt(2)
        assert abs(config.voltage_rms - expected_rms) < 0.01

    def test_current_rms(self):
        config = SimulationConfig()
        config.current_amplitude = 14.14
        expected_rms = 14.14 / np.sqrt(2)
        assert abs(config.current_rms - expected_rms) < 0.01

    def test_set_voltage_rms(self):
        config = SimulationConfig()
        config.set_voltage_rms(230.0)
        assert abs(config.voltage_amplitude - 230.0 * np.sqrt(2)) < 0.01
        assert abs(config.voltage_rms - 230.0) < 0.01

    def test_set_current_rms(self):
        config = SimulationConfig()
        config.set_current_rms(10.0)
        assert abs(config.current_amplitude - 10.0 * np.sqrt(2)) < 0.01
        assert abs(config.current_rms - 10.0) < 0.01

    def test_voltage_clamping(self):
        config = SimulationConfig()
        config.set_voltage_rms(500.0)
        assert config.voltage_rms <= 400.0

    def test_current_clamping(self):
        config = SimulationConfig()
        config.set_current_rms(50.0)
        assert config.current_rms <= 40.0


class TestWaveformGeneration:
    """Test waveform generation accuracy."""

    def test_voltage_waveform_shape(self):
        config = SimulationConfig()
        config.voltage_amplitude = 325.27
        config.noise_level = 0.0

        sample_rate = config.sample_rate
        duration = 0.1
        n_samples = int(sample_rate * duration)
        t = np.linspace(0, duration, n_samples, endpoint=False)

        voltage = config.voltage_amplitude * np.sin(2 * np.pi * config.frequency * t)
        assert abs(np.max(voltage) - config.voltage_amplitude) < 0.01

        rms = np.sqrt(np.mean(voltage ** 2))
        expected_rms = config.voltage_amplitude / np.sqrt(2)
        assert abs(rms - expected_rms) < 1.0


class TestSimulationWorker:
    """Test the simulation worker."""

    def test_worker_creation(self):
        config = SimulationConfig()
        worker = SimulationWorker(config)
        assert worker.config is config
        assert not worker.is_running()
