"""
RELAYLAB X — Test Configuration Page

Allows configuration of voltage reference, current reference,
phase difference, and test control.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QDoubleSpinBox, QGroupBox, QGridLayout, QFrame,
    QMessageBox, QSizePolicy
)
from app.ui.theme import Theme
from app.core.simulation import SimulationEngine


class TestConfigPage(QWidget):
    """Test configuration and control page."""

    test_started = Signal()
    test_stopped = Signal()

    def __init__(self, simulation_engine: SimulationEngine, parent=None):
        super().__init__(parent)
        self._sim_engine = simulation_engine
        self._test_running = False
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(20)

        # Title
        title = QLabel("TEST CONFIGURATION")
        title.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: 20px;
            font-weight: 700;
            letter-spacing: 2px;
        """)
        layout.addWidget(title)

        subtitle = QLabel("Configure output parameters for the simulated test system")
        subtitle.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(subtitle)

        # Simulation mode banner
        sim_banner = QFrame()
        sim_banner.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.STATUS_WARNING}15;
                border: 1px solid {Theme.STATUS_WARNING}40;
                border-radius: 6px;
                padding: 8px;
            }}
        """)
        sim_banner_layout = QHBoxLayout(sim_banner)
        sim_icon = QLabel("⚡")
        sim_icon.setStyleSheet("font-size: 16px;")
        sim_banner_layout.addWidget(sim_icon)
        sim_text = QLabel("SIMULATION MODE — No real hardware output. All values are simulated.")
        sim_text.setStyleSheet(f"color: {Theme.STATUS_WARNING}; font-weight: 600;")
        sim_banner_layout.addWidget(sim_text)
        sim_banner_layout.addStretch()
        layout.addWidget(sim_banner)

        # Configuration cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        # Voltage card
        v_card = self._create_card("VOLTAGE OUTPUT", Theme.VOLTAGE_BLUE)
        v_layout = QGridLayout()

        v_layout.addWidget(self._dim_label("Reference (RMS)"), 0, 0)
        self.voltage_spin = QDoubleSpinBox()
        self.voltage_spin.setRange(0.0, 400.0)
        self.voltage_spin.setValue(230.0)
        self.voltage_spin.setSuffix(" V")
        self.voltage_spin.setDecimals(1)
        self.voltage_spin.setSingleStep(10.0)
        v_layout.addWidget(self.voltage_spin, 0, 1)

        v_layout.addWidget(self._dim_label("Peak Voltage"), 1, 0)
        self.vpeak_label = QLabel("325.3 V")
        self.vpeak_label.setStyleSheet(f"color: {Theme.VOLTAGE_BLUE}; font-weight: 600; font-family: 'SF Mono', monospace;")
        v_layout.addWidget(self.vpeak_label, 1, 1)

        v_layout.addWidget(self._dim_label("Range"), 2, 0)
        v_layout.addWidget(self._dim_label("0 – 400 V RMS"), 2, 1)

        v_card.layout().addLayout(v_layout)
        cards_layout.addWidget(v_card)

        # Current card
        i_card = self._create_card("CURRENT OUTPUT", Theme.CURRENT_AMBER)
        i_layout = QGridLayout()

        i_layout.addWidget(self._dim_label("Reference (RMS)"), 0, 0)
        self.current_spin = QDoubleSpinBox()
        self.current_spin.setRange(0.0, 40.0)
        self.current_spin.setValue(10.0)
        self.current_spin.setSuffix(" A")
        self.current_spin.setDecimals(2)
        self.current_spin.setSingleStep(1.0)
        i_layout.addWidget(self.current_spin, 0, 1)

        i_layout.addWidget(self._dim_label("Peak Current"), 1, 0)
        self.ipeak_label = QLabel("14.14 A")
        self.ipeak_label.setStyleSheet(f"color: {Theme.CURRENT_AMBER}; font-weight: 600; font-family: 'SF Mono', monospace;")
        i_layout.addWidget(self.ipeak_label, 1, 1)

        i_layout.addWidget(self._dim_label("Range"), 2, 0)
        i_layout.addWidget(self._dim_label("0 – 40 A RMS"), 2, 1)

        i_card.layout().addLayout(i_layout)
        cards_layout.addWidget(i_card)

        # Phase / Frequency card
        pf_card = self._create_card("WAVEFORM PARAMETERS", Theme.TEXT_SECONDARY)
        pf_layout = QGridLayout()

        pf_layout.addWidget(self._dim_label("Frequency"), 0, 0)
        self.freq_label = QLabel("50.0 Hz (Fixed — Phase 1)")
        self.freq_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; font-weight: 600; font-family: 'SF Mono', monospace;")
        pf_layout.addWidget(self.freq_label, 0, 1)

        pf_layout.addWidget(self._dim_label("Phase Difference"), 1, 0)
        self.phase_spin = QDoubleSpinBox()
        self.phase_spin.setRange(-180.0, 180.0)
        self.phase_spin.setValue(0.0)
        self.phase_spin.setSuffix(" °")
        self.phase_spin.setDecimals(1)
        self.phase_spin.setSingleStep(5.0)
        pf_layout.addWidget(self.phase_spin, 1, 1)

        pf_layout.addWidget(self._dim_label("Power Factor"), 2, 0)
        self.pf_label = QLabel("1.000")
        self.pf_label.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; font-weight: 600; font-family: 'SF Mono', monospace;")
        pf_layout.addWidget(self.pf_label, 2, 1)

        pf_card.layout().addLayout(pf_layout)
        cards_layout.addWidget(pf_card)

        layout.addLayout(cards_layout)

        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(12)

        self.apply_btn = QPushButton("✔ Apply Settings")
        self.apply_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.VOLTAGE_BLUE_GLOW};
                color: {Theme.TEXT_PRIMARY};
                border: 1px solid {Theme.VOLTAGE_BLUE};
                border-radius: 6px;
                padding: 12px 32px;
                font-size: 14px;
                font-weight: 700;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background-color: {Theme.VOLTAGE_BLUE_DIM};
            }}
        """)
        self.apply_btn.clicked.connect(self._apply_settings)
        action_layout.addWidget(self.apply_btn)

        self.start_btn = QPushButton("▶ Start Test")
        self.start_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.STATUS_OK}20;
                color: {Theme.STATUS_OK};
                border: 1px solid {Theme.STATUS_OK};
                border-radius: 6px;
                padding: 12px 32px;
                font-size: 14px;
                font-weight: 700;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background-color: {Theme.STATUS_OK}40;
            }}
        """)
        self.start_btn.clicked.connect(self._toggle_test)
        action_layout.addWidget(self.start_btn)

        self.reset_btn = QPushButton("↺ Reset Defaults")
        self.reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.BG_LIGHT};
                color: {Theme.TEXT_SECONDARY};
                border: 1px solid {Theme.BORDER_LIGHT};
                border-radius: 6px;
                padding: 12px 32px;
                font-size: 14px;
                font-weight: 500;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background-color: {Theme.BG_LIGHTER};
            }}
        """)
        self.reset_btn.clicked.connect(self._reset_defaults)
        action_layout.addWidget(self.reset_btn)

        action_layout.addStretch()
        layout.addLayout(action_layout)

        # Confirmation area
        self.confirm_label = QLabel("")
        self.confirm_label.setStyleSheet(f"color: {Theme.STATUS_OK}; font-size: 13px; font-weight: 500;")
        layout.addWidget(self.confirm_label)

        layout.addStretch()

        # Connect live update signals
        self.voltage_spin.valueChanged.connect(self._update_peak_displays)
        self.current_spin.valueChanged.connect(self._update_peak_displays)
        self.phase_spin.valueChanged.connect(self._update_pf_display)

    def _create_card(self, title: str, accent_color: str) -> QFrame:
        card = QFrame()
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_MEDIUM};
                border: 1px solid {Theme.BORDER_DARK};
                border-radius: 8px;
                border-top: 3px solid {accent_color};
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 12, 16, 16)
        card_layout.setSpacing(12)

        lbl = QLabel(title)
        lbl.setStyleSheet(f"""
            color: {accent_color};
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
        """)
        card_layout.addWidget(lbl)

        return card

    def _dim_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 12px;")
        return lbl

    def _update_peak_displays(self):
        import numpy as np
        vpeak = self.voltage_spin.value() * np.sqrt(2)
        ipeak = self.current_spin.value() * np.sqrt(2)
        self.vpeak_label.setText(f"{vpeak:.1f} V")
        self.ipeak_label.setText(f"{ipeak:.2f} A")

    def _update_pf_display(self):
        import numpy as np
        pf = np.cos(np.radians(self.phase_spin.value()))
        self.pf_label.setText(f"{pf:.3f}")

    def _apply_settings(self):
        """Apply current settings to the simulation engine."""
        self._sim_engine.set_voltage(self.voltage_spin.value())
        self._sim_engine.set_current(self.current_spin.value())
        self._sim_engine.set_phase_difference(self.phase_spin.value())

        self.confirm_label.setText(
            f"✔ Settings applied to simulator: "
            f"{self.voltage_spin.value():.1f} V, "
            f"{self.current_spin.value():.2f} A, "
            f"Δφ = {self.phase_spin.value():.1f}°"
        )
        self.confirm_label.setStyleSheet(f"color: {Theme.STATUS_OK}; font-size: 13px; font-weight: 500;")

        if self._sim_engine.is_running():
            self._sim_engine.restart()

    def _toggle_test(self):
        if self._test_running:
            self._sim_engine.stop()
            self._test_running = False
            self.start_btn.setText("▶ Start Test")
            self.start_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Theme.STATUS_OK}20;
                    color: {Theme.STATUS_OK};
                    border: 1px solid {Theme.STATUS_OK};
                    border-radius: 6px;
                    padding: 12px 32px;
                    font-size: 14px;
                    font-weight: 700;
                    min-height: 40px;
                }}
                QPushButton:hover {{
                    background-color: {Theme.STATUS_OK}40;
                }}
            """)
            self.confirm_label.setText("⏹ Test stopped")
            self.test_stopped.emit()
        else:
            self._apply_settings()
            self._sim_engine.start()
            self._test_running = True
            self.start_btn.setText("⏹ Stop Test")
            self.start_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Theme.STATUS_ERROR}20;
                    color: {Theme.STATUS_ERROR};
                    border: 1px solid {Theme.STATUS_ERROR};
                    border-radius: 6px;
                    padding: 12px 32px;
                    font-size: 14px;
                    font-weight: 700;
                    min-height: 40px;
                }}
                QPushButton:hover {{
                    background-color: {Theme.STATUS_ERROR}40;
                }}
            """)
            self.confirm_label.setText("▶ Test started [SIMULATED]")
            self.test_started.emit()

    def _reset_defaults(self):
        self.voltage_spin.setValue(230.0)
        self.current_spin.setValue(10.0)
        self.phase_spin.setValue(0.0)
        self._update_peak_displays()
        self._update_pf_display()
        self.confirm_label.setText("↺ Settings reset to defaults")
        self.confirm_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 13px; font-weight: 500;")
