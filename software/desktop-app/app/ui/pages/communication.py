"""
RELAYLAB X — Device Communication Page

Serial port configuration and connection management.
Uses mock connections in Phase 1 simulation mode.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFrame, QGridLayout, QTextEdit, QSizePolicy
)
from datetime import datetime
from app.ui.theme import Theme
from app.communication.serial_manager import SerialManager, ConnectionState


class DeviceCommunicationPage(QWidget):
    """Device communication and serial port management page."""

    def __init__(self, serial_manager: SerialManager, parent=None):
        super().__init__(parent)
        self._serial = serial_manager
        self._setup_ui()
        self._connect_signals()
        self._refresh_ports()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(20)

        # Title
        title = QLabel("DEVICE COMMUNICATION")
        title.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; font-size: 20px; font-weight: 700; letter-spacing: 2px;")
        layout.addWidget(title)

        subtitle = QLabel("USB serial connection to STM32H753 controller")
        subtitle.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(subtitle)

        # Connection status
        status_frame = QFrame()
        status_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_MEDIUM};
                border: 1px solid {Theme.BORDER_DARK};
                border-radius: 8px;
            }}
        """)
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(16, 12, 16, 12)

        self.status_icon = QLabel("○")
        self.status_icon.setStyleSheet(f"color: {Theme.TEXT_DIM}; font-size: 20px;")
        status_layout.addWidget(self.status_icon)

        status_text_layout = QVBoxLayout()
        self.status_label = QLabel("DISCONNECTED")
        self.status_label.setStyleSheet(f"color: {Theme.TEXT_DIM}; font-size: 14px; font-weight: 700;")
        self.status_detail = QLabel("No device connected — using simulation mode")
        self.status_detail.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 11px;")
        status_text_layout.addWidget(self.status_label)
        status_text_layout.addWidget(self.status_detail)
        status_layout.addLayout(status_text_layout)
        status_layout.addStretch()

        self.mock_badge = QLabel("MOCK MODE")
        self.mock_badge.setStyleSheet(f"""
            color: {Theme.STATUS_WARNING};
            background-color: {Theme.STATUS_WARNING}20;
            border: 1px solid {Theme.STATUS_WARNING}50;
            border-radius: 4px;
            padding: 4px 12px;
            font-size: 10px;
            font-weight: 700;
        """)
        status_layout.addWidget(self.mock_badge)

        layout.addWidget(status_frame)

        # Connection settings
        settings_frame = QFrame()
        settings_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_MEDIUM};
                border: 1px solid {Theme.BORDER_DARK};
                border-radius: 8px;
            }}
        """)
        settings_layout = QVBoxLayout(settings_frame)
        settings_layout.setContentsMargins(16, 12, 16, 16)
        settings_layout.setSpacing(12)

        settings_title = QLabel("CONNECTION SETTINGS")
        settings_title.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        settings_layout.addWidget(settings_title)

        grid = QGridLayout()
        grid.setSpacing(8)

        # Port selection
        grid.addWidget(self._dim_label("Serial Port"), 0, 0)
        port_row = QHBoxLayout()
        self.port_combo = QComboBox()
        self.port_combo.setMinimumWidth(300)
        port_row.addWidget(self.port_combo)
        self.refresh_btn = QPushButton("↻ Refresh")
        self.refresh_btn.setFixedWidth(100)
        port_row.addWidget(self.refresh_btn)
        grid.addLayout(port_row, 0, 1)

        # Baud rate
        grid.addWidget(self._dim_label("Baud Rate"), 1, 0)
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(["9600", "19200", "38400", "57600", "115200", "230400", "460800", "921600"])
        self.baud_combo.setCurrentText("115200")
        grid.addWidget(self.baud_combo, 1, 1)

        # Data bits
        grid.addWidget(self._dim_label("Data Bits"), 2, 0)
        self.databits_combo = QComboBox()
        self.databits_combo.addItems(["7", "8"])
        self.databits_combo.setCurrentText("8")
        grid.addWidget(self.databits_combo, 2, 1)

        # Parity
        grid.addWidget(self._dim_label("Parity"), 3, 0)
        self.parity_combo = QComboBox()
        self.parity_combo.addItems(["None", "Even", "Odd"])
        grid.addWidget(self.parity_combo, 3, 1)

        # Stop bits
        grid.addWidget(self._dim_label("Stop Bits"), 4, 0)
        self.stopbits_combo = QComboBox()
        self.stopbits_combo.addItems(["1", "1.5", "2"])
        grid.addWidget(self.stopbits_combo, 4, 1)

        settings_layout.addLayout(grid)

        # Connect/Disconnect buttons
        btn_row = QHBoxLayout()
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.STATUS_OK}20;
                color: {Theme.STATUS_OK};
                border: 1px solid {Theme.STATUS_OK};
                border-radius: 4px;
                padding: 8px 24px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background-color: {Theme.STATUS_OK}40;
            }}
        """)
        btn_row.addWidget(self.connect_btn)

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.setEnabled(False)
        self.disconnect_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.STATUS_ERROR}20;
                color: {Theme.STATUS_ERROR};
                border: 1px solid {Theme.STATUS_ERROR}50;
                border-radius: 4px;
                padding: 8px 24px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background-color: {Theme.STATUS_ERROR}40;
            }}
            QPushButton:disabled {{
                color: {Theme.TEXT_DIM};
                border-color: {Theme.BORDER_DARK};
                background-color: {Theme.BG_LIGHT};
            }}
        """)
        btn_row.addWidget(self.disconnect_btn)
        btn_row.addStretch()
        settings_layout.addLayout(btn_row)

        layout.addWidget(settings_frame)

        # Communication log
        log_title = QLabel("COMMUNICATION LOG")
        log_title.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 12px; font-weight: 700; letter-spacing: 1px;")
        layout.addWidget(log_title)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(180)
        self.log_text.setPlaceholderText("No communication activity")
        layout.addWidget(self.log_text)

        layout.addStretch()

    def _dim_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 12px;")
        lbl.setFixedWidth(100)
        return lbl

    def _connect_signals(self):
        self.connect_btn.clicked.connect(self._on_connect)
        self.disconnect_btn.clicked.connect(self._on_disconnect)
        self.refresh_btn.clicked.connect(self._refresh_ports)
        self._serial.connection_state_changed.connect(self._on_state_changed)
        self._serial.error_occurred.connect(self._on_error)

    def _refresh_ports(self):
        self.port_combo.clear()
        ports = self._serial.get_available_ports()
        self.port_combo.addItems(ports)
        self._log(f"Found {len(ports)} port(s)")

    def _on_connect(self):
        port = self.port_combo.currentText()
        baud = int(self.baud_combo.currentText())
        self._log(f"Connecting to {port} at {baud} baud...")
        self._serial.connect(port, baud)

    def _on_disconnect(self):
        self._serial.disconnect()
        self._log("Disconnected")

    def _on_state_changed(self, state: str):
        self.status_label.setText(state)
        if state == ConnectionState.CONNECTED:
            self.status_icon.setText("●")
            self.status_icon.setStyleSheet(f"color: {Theme.STATUS_OK}; font-size: 20px;")
            self.status_label.setStyleSheet(f"color: {Theme.STATUS_OK}; font-size: 14px; font-weight: 700;")
            self.status_detail.setText(f"Connected to {self.port_combo.currentText()}")
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
            self._log(f"Connected to {self.port_combo.currentText()}")
        elif state == ConnectionState.CONNECTING:
            self.status_icon.setText("◐")
            self.status_icon.setStyleSheet(f"color: {Theme.STATUS_WARNING}; font-size: 20px;")
            self.status_label.setStyleSheet(f"color: {Theme.STATUS_WARNING}; font-size: 14px; font-weight: 700;")
            self.status_detail.setText("Establishing connection...")
        elif state == ConnectionState.ERROR:
            self.status_icon.setText("✕")
            self.status_icon.setStyleSheet(f"color: {Theme.STATUS_ERROR}; font-size: 20px;")
            self.status_label.setStyleSheet(f"color: {Theme.STATUS_ERROR}; font-size: 14px; font-weight: 700;")
            self.status_detail.setText("Connection error")
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)
        else:  # DISCONNECTED
            self.status_icon.setText("○")
            self.status_icon.setStyleSheet(f"color: {Theme.TEXT_DIM}; font-size: 20px;")
            self.status_label.setStyleSheet(f"color: {Theme.TEXT_DIM}; font-size: 14px; font-weight: 700;")
            self.status_detail.setText("No device connected — using simulation mode")
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)

    def _on_error(self, message: str):
        self._log(f"ERROR: {message}")

    def _log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
