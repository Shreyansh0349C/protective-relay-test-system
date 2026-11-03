"""
RELAYLAB X — Protection Monitoring Page

Displays simulated protection status indicators for
overcurrent, short-circuit, thermal, and controller states.
"""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGridLayout, QTextEdit, QSizePolicy
)
from datetime import datetime
from app.ui.theme import Theme
from app.communication.mock_device import MockDevice


class StatusIndicator(QFrame):
    """A protection status indicator tile."""

    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self._name = name
        self._ok = True
        self.setMinimumHeight(100)
        self.setMinimumWidth(200)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(6)

        self.name_label = QLabel(name)
        self.name_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(self.name_label)

        self.status_label = QLabel("● NORMAL")
        self.status_label.setStyleSheet(f"""
            color: {Theme.STATUS_OK};
            font-size: 16px;
            font-weight: 700;
            font-family: 'SF Mono', monospace;
        """)
        layout.addWidget(self.status_label)

        self.sim_label = QLabel("[SIMULATED]")
        self.sim_label.setStyleSheet(f"color: {Theme.TEXT_DIM}; font-size: 9px;")
        layout.addWidget(self.sim_label)

        self._set_ok(True)

    def _set_ok(self, ok: bool):
        self._ok = ok
        if ok:
            self.status_label.setText("● NORMAL")
            self.status_label.setStyleSheet(f"color: {Theme.STATUS_OK}; font-size: 16px; font-weight: 700; font-family: 'SF Mono', monospace;")
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {Theme.BG_MEDIUM};
                    border: 1px solid {Theme.STATUS_OK}30;
                    border-radius: 8px;
                    border-left: 4px solid {Theme.STATUS_OK};
                }}
            """)
        else:
            self.status_label.setText("● FAULT")
            self.status_label.setStyleSheet(f"color: {Theme.STATUS_ERROR}; font-size: 16px; font-weight: 700; font-family: 'SF Mono', monospace;")
            self.setStyleSheet(f"""
                QFrame {{
                    background-color: {Theme.STATUS_ERROR}10;
                    border: 1px solid {Theme.STATUS_ERROR}50;
                    border-radius: 8px;
                    border-left: 4px solid {Theme.STATUS_ERROR};
                }}
            """)

    def set_status(self, ok: bool, text: str = ""):
        self._set_ok(ok)
        if text:
            self.status_label.setText(f"● {text}")


class ProtectionMonitoringPage(QWidget):
    """Protection monitoring and fault status page."""

    def __init__(self, mock_device: MockDevice, parent=None):
        super().__init__(parent)
        self._mock_device = mock_device
        self._event_log = []
        self._setup_ui()
        self._connect_signals()

        # Update timer
        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self._update_status)
        self._update_timer.setInterval(500)
        self._update_timer.start()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(20)

        # Title
        title = QLabel("PROTECTION MONITORING")
        title.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; font-size: 20px; font-weight: 700; letter-spacing: 2px;")
        layout.addWidget(title)

        # Warning banner
        warn_banner = QFrame()
        warn_banner.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.STATUS_WARNING}15;
                border: 1px solid {Theme.STATUS_WARNING}40;
                border-radius: 6px;
            }}
        """)
        warn_layout = QHBoxLayout(warn_banner)
        warn_layout.setContentsMargins(12, 8, 12, 8)
        warn_icon = QLabel("⚠")
        warn_icon.setStyleSheet("font-size: 16px;")
        warn_layout.addWidget(warn_icon)
        warn_text = QLabel(
            "SIMULATED PROTECTION INDICATORS — These do not represent actual "
            "hardware protection status. Do not rely on these for safety."
        )
        warn_text.setStyleSheet(f"color: {Theme.STATUS_WARNING}; font-size: 11px; font-weight: 500;")
        warn_text.setWordWrap(True)
        warn_layout.addWidget(warn_text, stretch=1)
        layout.addWidget(warn_banner)

        # Status indicators
        indicators_layout = QHBoxLayout()
        indicators_layout.setSpacing(16)

        self.overcurrent_ind = StatusIndicator("OVERCURRENT")
        self.short_circuit_ind = StatusIndicator("SHORT CIRCUIT")
        self.thermal_ind = StatusIndicator("THERMAL")
        self.controller_ind = StatusIndicator("CONTROLLER")

        indicators_layout.addWidget(self.overcurrent_ind)
        indicators_layout.addWidget(self.short_circuit_ind)
        indicators_layout.addWidget(self.thermal_ind)
        indicators_layout.addWidget(self.controller_ind)

        layout.addLayout(indicators_layout)

        # Simulation controls (for demo/testing)
        ctrl_frame = QFrame()
        ctrl_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_MEDIUM};
                border: 1px solid {Theme.BORDER_DARK};
                border-radius: 8px;
            }}
        """)
        ctrl_layout = QVBoxLayout(ctrl_frame)
        ctrl_layout.setContentsMargins(16, 12, 16, 12)
        ctrl_layout.setSpacing(8)

        ctrl_title = QLabel("SIMULATION CONTROLS")
        ctrl_title.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        ctrl_layout.addWidget(ctrl_title)

        ctrl_desc = QLabel("Trigger simulated fault conditions for UI testing:")
        ctrl_desc.setStyleSheet(f"color: {Theme.TEXT_DIM}; font-size: 11px;")
        ctrl_layout.addWidget(ctrl_desc)

        btn_layout = QHBoxLayout()
        self.sim_oc_btn = QPushButton("Simulate Overcurrent")
        self.sim_oc_btn.setStyleSheet(self._sim_btn_style(Theme.STATUS_ERROR))
        self.sim_sc_btn = QPushButton("Simulate Short Circuit")
        self.sim_sc_btn.setStyleSheet(self._sim_btn_style(Theme.STATUS_ERROR))
        self.sim_thermal_btn = QPushButton("Simulate Thermal")
        self.sim_thermal_btn.setStyleSheet(self._sim_btn_style(Theme.STATUS_WARNING))
        self.reset_faults_btn = QPushButton("Reset All Faults")
        self.reset_faults_btn.setStyleSheet(self._sim_btn_style(Theme.STATUS_OK))

        btn_layout.addWidget(self.sim_oc_btn)
        btn_layout.addWidget(self.sim_sc_btn)
        btn_layout.addWidget(self.sim_thermal_btn)
        btn_layout.addWidget(self.reset_faults_btn)
        btn_layout.addStretch()
        ctrl_layout.addLayout(btn_layout)

        layout.addWidget(ctrl_frame)

        # Event log
        log_title = QLabel("FAULT / EVENT HISTORY")
        log_title.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 12px; font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(log_title)

        self.event_log_text = QTextEdit()
        self.event_log_text.setReadOnly(True)
        self.event_log_text.setMaximumHeight(200)
        self.event_log_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Theme.BG_DARKEST};
                color: {Theme.TEXT_SECONDARY};
                border: 1px solid {Theme.BORDER_DARK};
                border-radius: 6px;
                font-family: 'SF Mono', monospace;
                font-size: 11px;
                padding: 8px;
            }}
        """)
        self.event_log_text.setPlaceholderText("No events recorded")
        layout.addWidget(self.event_log_text)

        layout.addStretch()

    def _sim_btn_style(self, color: str) -> str:
        return f"""
            QPushButton {{
                background-color: {Theme.BG_LIGHT};
                color: {color};
                border: 1px solid {color}50;
                border-radius: 4px;
                padding: 6px 16px;
                font-weight: 600;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {color}20;
                border-color: {color};
            }}
        """

    def _connect_signals(self):
        self.sim_oc_btn.clicked.connect(self._simulate_overcurrent)
        self.sim_sc_btn.clicked.connect(self._simulate_short_circuit)
        self.sim_thermal_btn.clicked.connect(self._simulate_thermal)
        self.reset_faults_btn.clicked.connect(self._reset_faults)
        self._mock_device.fault_triggered.connect(self._on_fault)

    def _simulate_overcurrent(self):
        self._mock_device.simulate_overcurrent()

    def _simulate_short_circuit(self):
        self._mock_device.simulate_short_circuit()

    def _simulate_thermal(self):
        self._mock_device.simulate_thermal()

    def _reset_faults(self):
        from app.communication.protocol import Command, CommandType
        self._mock_device.process_command(Command(CommandType.RESET_FAULT))
        self._log_event("All faults cleared [SIMULATED]")
        self._update_status()

    def _on_fault(self, message: str):
        self._log_event(message)

    def _log_event(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        entry = f"[{timestamp}] {message}"
        self._event_log.append(entry)
        self.event_log_text.append(entry)

    def _update_status(self):
        status = self._mock_device.protection_status
        self.overcurrent_ind.set_status(not status["overcurrent"],
                                        "FAULT" if status["overcurrent"] else "NORMAL")
        self.short_circuit_ind.set_status(not status["short_circuit"],
                                          "FAULT" if status["short_circuit"] else "NORMAL")
        self.thermal_ind.set_status(not status["thermal"],
                                    "WARNING" if status["thermal"] else "NORMAL")
        self.controller_ind.set_status(status["fault_state"] == "NORMAL", "NORMAL")
