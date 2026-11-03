"""
RELAYLAB X — Simulation Engine

Generates accurate 50 Hz voltage and current sine waves for prototype testing.
All data is clearly marked as SIMULATED.

This module runs a background thread that continuously produces sampled
waveform data and delivers it to the GUI without blocking the main thread.
"""

import numpy as np
from PySide6.QtCore import QObject, Signal, QThread, QMutex, QMutexLocker
import time


class SimulationConfig:
    """Configuration for the simulation engine."""

    def __init__(self):
        self.voltage_amplitude: float = 325.27  # Peak voltage (230 Vrms * sqrt(2))
        self.current_amplitude: float = 14.14   # Peak current (10 Arms * sqrt(2))
        self.frequency: float = 50.0            # Hz (fixed for Phase 1)
        self.phase_difference: float = 0.0      # Radians between V and I
        self.sample_rate: float = 10000.0       # Samples per second
        self.noise_level: float = 0.002         # Noise as fraction of amplitude
        self.running: bool = False
        self.voltage_enabled: bool = True
        self.current_enabled: bool = True

    @property
    def voltage_rms(self) -> float:
        """Calculate expected RMS voltage."""
        return self.voltage_amplitude / np.sqrt(2)

    @property
    def current_rms(self) -> float:
        """Calculate expected RMS current."""
        return self.current_amplitude / np.sqrt(2)

    def set_voltage_rms(self, vrms: float):
        """Set voltage by RMS value (0-400 V)."""
        vrms = np.clip(vrms, 0.0, 400.0)
        self.voltage_amplitude = vrms * np.sqrt(2)

    def set_current_rms(self, irms: float):
        """Set current by RMS value (0-40 A)."""
        irms = np.clip(irms, 0.0, 40.0)
        self.current_amplitude = irms * np.sqrt(2)


class SimulationWorker(QObject):
    """
    Background worker that generates continuous waveform data.
    Runs in a separate QThread to avoid blocking the GUI.
    """

    # Emits (time_array, voltage_array, current_array)
    data_ready = Signal(np.ndarray, np.ndarray, np.ndarray)
    status_changed = Signal(str)

    def __init__(self, config: SimulationConfig):
        super().__init__()
        self._config = config
        self._mutex = QMutex()
        self._running = False
        self._time_offset = 0.0
        self._update_interval = 0.033  # ~30 fps update rate

    @property
    def config(self) -> SimulationConfig:
        return self._config

    def start_simulation(self):
        """Start generating waveform data."""
        with QMutexLocker(self._mutex):
            self._running = True
            self._time_offset = 0.0
        self.status_changed.emit("RUNNING [SIMULATED]")
        self._run_loop()

    def stop_simulation(self):
        """Stop generating waveform data."""
        with QMutexLocker(self._mutex):
            self._running = False
        self.status_changed.emit("STOPPED")

    def is_running(self) -> bool:
        with QMutexLocker(self._mutex):
            return self._running

    def _run_loop(self):
        """Main simulation loop — generates data at configured update rate."""
        while True:
            with QMutexLocker(self._mutex):
                if not self._running:
                    break

            # Generate one frame of waveform data
            samples_per_frame = int(self._config.sample_rate * self._update_interval)
            omega = 2.0 * np.pi * self._config.frequency

            # Create time array for this frame
            t = np.linspace(
                self._time_offset,
                self._time_offset + self._update_interval,
                samples_per_frame,
                endpoint=False
            )

            # Generate voltage waveform
            voltage = np.zeros(samples_per_frame)
            if self._config.voltage_enabled:
                voltage = self._config.voltage_amplitude * np.sin(omega * t)
                if self._config.noise_level > 0:
                    voltage += np.random.normal(
                        0,
                        self._config.noise_level * self._config.voltage_amplitude,
                        samples_per_frame
                    )

            # Generate current waveform
            current = np.zeros(samples_per_frame)
            if self._config.current_enabled:
                current = self._config.current_amplitude * np.sin(
                    omega * t - self._config.phase_difference
                )
                if self._config.noise_level > 0:
                    current += np.random.normal(
                        0,
                        self._config.noise_level * self._config.current_amplitude,
                        samples_per_frame
                    )

            # Advance time offset for continuity
            self._time_offset += self._update_interval

            # Emit data
            self.data_ready.emit(t, voltage, current)

            # Sleep for update interval
            time.sleep(self._update_interval)


class SimulationEngine(QObject):
    """
    High-level simulation engine that manages the worker thread.

    Usage:
        engine = SimulationEngine()
        engine.data_ready.connect(my_handler)
        engine.start()
        ...
        engine.stop()
    """

    data_ready = Signal(np.ndarray, np.ndarray, np.ndarray)
    status_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = SimulationConfig()
        self._worker = None
        self._thread = None

    def start(self):
        """Start the simulation in a background thread."""
        if self._thread is not None and self._thread.isRunning():
            return

        self._thread = QThread()
        self._worker = SimulationWorker(self.config)
        self._worker.moveToThread(self._thread)

        # Connect signals
        self._worker.data_ready.connect(self.data_ready.emit)
        self._worker.status_changed.connect(self.status_changed.emit)
        self._thread.started.connect(self._worker.start_simulation)

        self.config.running = True
        self._thread.start()

    def stop(self):
        """Stop the simulation and clean up the thread."""
        if self._worker:
            self._worker.stop_simulation()
        if self._thread:
            self._thread.quit()
            self._thread.wait(2000)
        self.config.running = False
        self.status_changed.emit("STOPPED")

    def restart(self):
        """Restart the simulation with current config."""
        self.stop()
        self.start()

    def set_voltage(self, vrms: float):
        """Set voltage amplitude by RMS value."""
        self.config.set_voltage_rms(vrms)

    def set_current(self, irms: float):
        """Set current amplitude by RMS value."""
        self.config.set_current_rms(irms)

    def set_phase_difference(self, degrees: float):
        """Set phase difference in degrees."""
        self.config.phase_difference = np.radians(degrees)

    def is_running(self) -> bool:
        """Check if simulation is currently running."""
        return self._worker is not None and self._worker.is_running()

    def cleanup(self):
        """Clean up resources on application exit."""
        self.stop()
        if self._thread:
            self._thread.deleteLater()
            self._thread = None
