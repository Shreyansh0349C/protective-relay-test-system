"""
RELAYLAB X — Measurements Page

Detailed measurement display with live RMS, frequency, phase,
power, and min/max readings.
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QFrame,
    QSizePolicy
)
from app.ui.theme import Theme
from app.core.measurements import MeasurementResult


class MeasurementTile(QFrame):
    """A single measurement readout tile."""

    def __init__(self, title: str, unit: str, color: str = Theme.TEXT_PRIMARY, parent=None):
        super().__init__(parent)
        self._unit = unit
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_MEDIUM};
                border: 1px solid {Theme.BORDER_DARK};
                border-radius: 8px;
                border-top: 3px solid {color};
            }}
        """)
        self.setMinimumHeight(100)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)

        lbl = QLabel(title)
        lbl.setStyleSheet(f"color: {color}; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(lbl)

        self.value_label = QLabel("---")
        self.value_label.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: 28px;
            font-weight: 700;
            font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
        """)
        layout.addWidget(self.value_label)

        self.unit_label = QLabel(unit)
        self.unit_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 11px;")
        layout.addWidget(self.unit_label)

    def set_value(self, value: str):
        self.value_label.setText(value)


class MeasurementsPage(QWidget):
    """Detailed measurements display page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_result = MeasurementResult()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(20)

        # Title
        title = QLabel("MEASUREMENTS")
        title.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; font-size: 20px; font-weight: 700; letter-spacing: 2px;")
        layout.addWidget(title)

        subtitle = QLabel("Real-time signal measurements from simulated data")
        subtitle.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(subtitle)

        # Data source indicator
        self.source_label = QLabel("⚡ Source: SIMULATED")
        self.source_label.setStyleSheet(f"color: {Theme.STATUS_WARNING}; font-size: 11px; font-weight: 600;")
        layout.addWidget(self.source_label)

        # Voltage measurements
        v_title = QLabel("VOLTAGE CHANNEL")
        v_title.setStyleSheet(f"color: {Theme.VOLTAGE_BLUE}; font-size: 12px; font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(v_title)

        v_grid = QHBoxLayout()
        v_grid.setSpacing(12)
        self.v_rms = MeasurementTile("V RMS", "V", Theme.VOLTAGE_BLUE)
        self.v_peak = MeasurementTile("V PEAK", "V", Theme.VOLTAGE_BLUE)
        self.v_min = MeasurementTile("V MIN", "V", Theme.VOLTAGE_BLUE_DIM)
        self.v_max = MeasurementTile("V MAX", "V", Theme.VOLTAGE_BLUE_DIM)
        v_grid.addWidget(self.v_rms)
        v_grid.addWidget(self.v_peak)
        v_grid.addWidget(self.v_min)
        v_grid.addWidget(self.v_max)
        layout.addLayout(v_grid)

        # Current measurements
        i_title = QLabel("CURRENT CHANNEL")
        i_title.setStyleSheet(f"color: {Theme.CURRENT_AMBER}; font-size: 12px; font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(i_title)

        i_grid = QHBoxLayout()
        i_grid.setSpacing(12)
        self.i_rms = MeasurementTile("I RMS", "A", Theme.CURRENT_AMBER)
        self.i_peak = MeasurementTile("I PEAK", "A", Theme.CURRENT_AMBER)
        self.i_min = MeasurementTile("I MIN", "A", Theme.CURRENT_AMBER_DIM)
        self.i_max = MeasurementTile("I MAX", "A", Theme.CURRENT_AMBER_DIM)
        i_grid.addWidget(self.i_rms)
        i_grid.addWidget(self.i_peak)
        i_grid.addWidget(self.i_min)
        i_grid.addWidget(self.i_max)
        layout.addLayout(i_grid)

        # System measurements
        s_title = QLabel("SYSTEM")
        s_title.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 12px; font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(s_title)

        s_grid = QHBoxLayout()
        s_grid.setSpacing(12)
        self.freq = MeasurementTile("FREQUENCY", "Hz", Theme.STATUS_INFO)
        self.phase = MeasurementTile("PHASE DIFF", "°", Theme.STATUS_INFO)
        self.power_s = MeasurementTile("APPARENT PWR", "VA", Theme.TEXT_SECONDARY)
        self.power_p = MeasurementTile("ACTIVE PWR", "W", Theme.TEXT_SECONDARY)
        self.pf = MeasurementTile("POWER FACTOR", "", Theme.TEXT_SECONDARY)
        s_grid.addWidget(self.freq)
        s_grid.addWidget(self.phase)
        s_grid.addWidget(self.power_s)
        s_grid.addWidget(self.power_p)
        s_grid.addWidget(self.pf)
        layout.addLayout(s_grid)

        layout.addStretch()

    def update_measurements(self, result: MeasurementResult):
        """Update all measurement displays with new data."""
        self._last_result = result

        if not result.is_valid:
            return

        self.v_rms.set_value(f"{result.voltage_rms:.2f}")
        self.v_peak.set_value(f"{result.voltage_peak:.2f}")
        self.v_min.set_value(f"{result.voltage_min:.2f}")
        self.v_max.set_value(f"{result.voltage_max:.2f}")

        self.i_rms.set_value(f"{result.current_rms:.3f}")
        self.i_peak.set_value(f"{result.current_peak:.3f}")
        self.i_min.set_value(f"{result.current_min:.3f}")
        self.i_max.set_value(f"{result.current_max:.3f}")

        self.freq.set_value(f"{result.frequency:.2f}")
        self.phase.set_value(f"{result.phase_difference:.2f}")
        self.power_s.set_value(f"{result.power_apparent:.1f}")
        self.power_p.set_value(f"{result.power_active:.1f}")
        self.pf.set_value(f"{result.power_factor:.3f}")

        self.source_label.setText(f"⚡ Source: {result.source}")
