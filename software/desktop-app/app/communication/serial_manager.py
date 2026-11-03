"""
RELAYLAB X — Serial Communication Manager

Abstract communication layer for STM32 USB serial integration.
Uses a mock provider for the prototype phase.
"""

from PySide6.QtCore import QObject, Signal, QTimer
from typing import Optional, List


class ConnectionState:
    """Connection state constants."""
    DISCONNECTED = "DISCONNECTED"
    CONNECTING = "CONNECTING"
    CONNECTED = "CONNECTED"
    ERROR = "ERROR"


class SerialManager(QObject):
    """
    Manages serial port connections for hardware communication.

    In Phase 1, this uses a mock connection. The interface is designed
    to be swapped out for real PySerial communication when hardware
    is available.
    """

    connection_state_changed = Signal(str)
    data_received = Signal(bytes)
    error_occurred = Signal(str)
    ports_updated = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._state = ConnectionState.DISCONNECTED
        self._port: Optional[str] = None
        self._baud_rate: int = 115200
        self._serial_conn = None
        self._mock_mode: bool = True
        self._scan_timer = QTimer(self)
        self._scan_timer.timeout.connect(self._scan_ports)
        self._scan_timer.setInterval(3000)

    @property
    def state(self) -> str:
        return self._state

    @property
    def is_connected(self) -> bool:
        return self._state == ConnectionState.CONNECTED

    @property
    def is_mock(self) -> bool:
        return self._mock_mode

    def get_available_ports(self) -> List[str]:
        """List available serial ports. Returns mock ports in simulation mode."""
        if self._mock_mode:
            return ["MOCK-STM32H753 (Simulated)", "MOCK-FPGA-Bridge (Simulated)"]

        try:
            import serial.tools.list_ports
            return [port.device for port in serial.tools.list_ports.comports()]
        except ImportError:
            return []

    def connect(self, port: str, baud_rate: int = 115200) -> bool:
        """Establish connection to the specified port."""
        self._port = port
        self._baud_rate = baud_rate
        self._set_state(ConnectionState.CONNECTING)

        if self._mock_mode:
            QTimer.singleShot(500, self._mock_connect_complete)
            return True

        try:
            import serial
            self._serial_conn = serial.Serial(
                port=port,
                baudrate=baud_rate,
                timeout=1.0
            )
            self._set_state(ConnectionState.CONNECTED)
            return True
        except Exception as e:
            self.error_occurred.emit(f"Connection failed: {str(e)}")
            self._set_state(ConnectionState.ERROR)
            return False

    def disconnect(self):
        """Disconnect from the current port."""
        if self._serial_conn:
            try:
                self._serial_conn.close()
            except Exception:
                pass
            self._serial_conn = None
        self._set_state(ConnectionState.DISCONNECTED)

    def send_data(self, data: bytes) -> bool:
        """Send raw data to the connected device."""
        if not self.is_connected:
            self.error_occurred.emit("Not connected")
            return False

        if self._mock_mode:
            self.data_received.emit(data)
            return True

        try:
            if self._serial_conn:
                self._serial_conn.write(data)
                return True
        except Exception as e:
            self.error_occurred.emit(f"Send failed: {str(e)}")
            self._set_state(ConnectionState.ERROR)
        return False

    def start_port_scanning(self):
        """Start periodic scanning for available ports."""
        self._scan_timer.start()

    def stop_port_scanning(self):
        """Stop periodic port scanning."""
        self._scan_timer.stop()

    def _set_state(self, state: str):
        self._state = state
        self.connection_state_changed.emit(state)

    def _mock_connect_complete(self):
        self._set_state(ConnectionState.CONNECTED)

    def _scan_ports(self):
        ports = self.get_available_ports()
        self.ports_updated.emit(ports)
