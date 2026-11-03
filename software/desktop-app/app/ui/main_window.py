"""
RELAYLAB X — Main Window

Professional instrument navigation header, stacked pages container,
and status bar.
"""

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QStackedWidget, QFrame, QStatusBar
)
from app.ui.theme import Theme
from app.ui.oscilloscope import OscilloscopeWidget
from app.ui.pages.test_config import TestConfigPage
from app.ui.pages.measurements import MeasurementsPage
from app.ui.pages.protection import ProtectionMonitoringPage
from app.ui.pages.communication import DeviceCommunicationPage
from app.ui.pages.history import EventHistoryPage
from app.ui.pages.settings_page import ApplicationSettingsPage
from app.core.simulation import SimulationEngine
from app.core.settings import SettingsManager
from app.communication.serial_manager import SerialManager
from app.communication.mock_device import MockDevice


class NavigationButton(QPushButton):
    """Styled navigation bar button."""

    def __init__(self, title: str, subtitle: str, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setMinimumHeight(56)
        self.setMinimumWidth(130)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(2)

        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; font-weight: 700; font-size: 11px; background: transparent;")
        self.title_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_lbl)

        self.sub_lbl = QLabel(subtitle)
        self.sub_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 9px; background: transparent;")
        self.sub_lbl.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sub_lbl)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.BG_MEDIUM};
                border: 1px solid {Theme.BORDER_DARK};
                border-radius: 6px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {Theme.BG_LIGHT};
                border-color: {Theme.BORDER_ACCENT};
            }}
            QPushButton:checked {{
                background-color: {Theme.VOLTAGE_BLUE_GLOW};
                border-color: {Theme.VOLTAGE_BLUE};
            }}
            QPushButton:checked QLabel {{
                color: {Theme.TEXT_PRIMARY};
            }}
        """)


class MainWindow(QMainWindow):
    """Main application window for RELAYLAB X."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("RELAYLAB X — Protective Relay Test Suite")
        self.resize(1400, 900)

        self.simulation_engine = SimulationEngine()
        self.settings_manager = SettingsManager()
        self.serial_manager = SerialManager()
        self.mock_device = MockDevice()

        self.settings_manager.load()

        self._setup_ui()
        self._connect_signals()

        self.simulation_engine.start()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        header = QFrame()
        header.setFixedHeight(72)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.NAV_BG};
                border-bottom: 1px solid {Theme.BORDER_DARK};
            }}
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(16, 8, 16, 8)
        header_layout.setSpacing(12)

        brand_layout = QVBoxLayout()
        brand_layout.setSpacing(0)
        title_lbl = QLabel("RELAYLAB X")
        title_lbl.setStyleSheet(f"""
            color: {Theme.TEXT_PRIMARY};
            font-size: 16px;
            font-weight: 900;
            letter-spacing: 2px;
            background: transparent;
        """)
        sub_lbl = QLabel("PROTECTIVE RELAY TEST SUITE")
        sub_lbl.setStyleSheet(f"""
            color: {Theme.VOLTAGE_BLUE};
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 1px;
            background: transparent;
        """)
        brand_layout.addWidget(title_lbl)
        brand_layout.addWidget(sub_lbl)
        header_layout.addLayout(brand_layout)

        header_layout.addSpacing(24)

        self.nav_buttons = []
        nav_items = [
            ("Oscilloscope", "Waveforms"),
            ("Test Config", "Outputs"),
            ("Measurements", "RMS / Power"),
            ("Protection", "Monitoring"),
            ("Device Comm", "USB Serial"),
            ("Event History", "Audit Log"),
            ("Settings", "Preferences")
        ]

        self.nav_layout = QHBoxLayout()
        self.nav_layout.setSpacing(8)

        for i, (title, subtitle) in enumerate(nav_items):
            btn = NavigationButton(title, subtitle)
            btn.clicked.connect(lambda checked, idx=i: self._switch_page(idx))
            self.nav_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        header_layout.addLayout(self.nav_layout)
        header_layout.addStretch()

        main_layout.addWidget(header)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet(f"background-color: {Theme.BG_DARK};")

        self.osc_page = OscilloscopeWidget(self.simulation_engine)
        self.test_config_page = TestConfigPage(self.simulation_engine)
        self.meas_page = MeasurementsPage()
        self.prot_page = ProtectionMonitoringPage(self.mock_device)
        self.comm_page = DeviceCommunicationPage(self.serial_manager)
        self.history_page = EventHistoryPage()
        self.settings_page = ApplicationSettingsPage(self.settings_manager)

        self.stacked_widget.addWidget(self.osc_page)       # 0
        self.stacked_widget.addWidget(self.test_config_page) # 1
        self.stacked_widget.addWidget(self.meas_page)      # 2
        self.stacked_widget.addWidget(self.prot_page)      # 3
        self.stacked_widget.addWidget(self.comm_page)      # 4
        self.stacked_widget.addWidget(self.history_page)   # 5
        self.stacked_widget.addWidget(self.settings_page)  # 6

        main_layout.addWidget(self.stacked_widget, stretch=1)

        self._switch_page(0)

    def _connect_signals(self):
        self.simulation_engine.data_ready.connect(self._on_simulation_data)
        self.test_config_page.test_started.connect(lambda: self.history_page.log_event("TEST", "Test started [SIMULATED]"))
        self.test_config_page.test_stopped.connect(lambda: self.history_page.log_event("TEST", "Test stopped"))
        self.mock_device.fault_triggered.connect(lambda msg: self.history_page.log_event("FAULT", msg))

    def _switch_page(self, index: int):
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
        self.stacked_widget.setCurrentIndex(index)

    def _on_simulation_data(self, time_data, voltage, current):
        result = self.osc_page.get_measurement_result()
        self.meas_page.update_measurements(result)

    def closeEvent(self, event):
        self.simulation_engine.cleanup()
        self.serial_manager.stop_port_scanning()
        event.accept()
