"""
RELAYLAB X — Mock Device

Simulates hardware responses for prototype testing.
Clearly separated from real hardware communication.
"""

from PySide6.QtCore import QObject, Signal
from .protocol import Command, Response, ResponseStatus, CommandType


class MockDevice(QObject):
    """
    Simulates the STM32H753 + FPGA hardware for testing.

    All responses are marked as simulated.
    This does NOT represent the actual hardware behaviour.
    """

    response_ready = Signal(object)
    status_changed = Signal(str)
    fault_triggered = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._voltage_setpoint: float = 0.0
        self._current_setpoint: float = 0.0
        self._output_active: bool = False
        self._fault_state: str = "NORMAL"
        self._device_id: str = "MOCK-STM32H753-RELAYLAB-v0.1"

        self._overcurrent: bool = False
        self._short_circuit: bool = False
        self._thermal_warning: bool = False

    def process_command(self, command: Command) -> Response:
        """Process a command and return a simulated response."""
        handlers = {
            CommandType.SET_VOLTAGE: self._handle_set_voltage,
            CommandType.SET_CURRENT: self._handle_set_current,
            CommandType.START_OUTPUT: self._handle_start,
            CommandType.STOP_OUTPUT: self._handle_stop,
            CommandType.READ_STATUS: self._handle_read_status,
            CommandType.READ_PROTECTION: self._handle_read_protection,
            CommandType.RESET_FAULT: self._handle_reset_fault,
            CommandType.IDENTIFY: self._handle_identify,
        }

        handler = handlers.get(command.command_type)
        if handler:
            return handler(command)

        return Response(status=ResponseStatus.ERROR)

    def _handle_set_voltage(self, cmd: Command) -> Response:
        self._voltage_setpoint = cmd.parameter
        return Response(status=ResponseStatus.OK, value=cmd.parameter)

    def _handle_set_current(self, cmd: Command) -> Response:
        self._current_setpoint = cmd.parameter
        return Response(status=ResponseStatus.OK, value=cmd.parameter)

    def _handle_start(self, cmd: Command) -> Response:
        if self._fault_state != "NORMAL":
            return Response(status=ResponseStatus.FAULT)
        self._output_active = True
        self.status_changed.emit("OUTPUT ACTIVE [SIMULATED]")
        return Response(status=ResponseStatus.OK)

    def _handle_stop(self, cmd: Command) -> Response:
        self._output_active = False
        self.status_changed.emit("OUTPUT STOPPED [SIMULATED]")
        return Response(status=ResponseStatus.OK)

    def _handle_read_status(self, cmd: Command) -> Response:
        return Response(
            status=ResponseStatus.OK,
            value=1.0 if self._output_active else 0.0
        )

    def _handle_read_protection(self, cmd: Command) -> Response:
        return Response(status=ResponseStatus.OK)

    def _handle_reset_fault(self, cmd: Command) -> Response:
        self._fault_state = "NORMAL"
        self._overcurrent = False
        self._short_circuit = False
        self._thermal_warning = False
        self.status_changed.emit("FAULTS CLEARED [SIMULATED]")
        return Response(status=ResponseStatus.OK)

    def _handle_identify(self, cmd: Command) -> Response:
        return Response(
            status=ResponseStatus.OK,
            raw_data=self._device_id.encode()
        )

    # Simulation helpers for UI testing

    def simulate_overcurrent(self):
        """Trigger a simulated overcurrent fault."""
        self._overcurrent = True
        self._fault_state = "OVERCURRENT"
        self._output_active = False
        self.fault_triggered.emit("OVERCURRENT FAULT [SIMULATED]")

    def simulate_short_circuit(self):
        """Trigger a simulated short-circuit fault."""
        self._short_circuit = True
        self._fault_state = "SHORT_CIRCUIT"
        self._output_active = False
        self.fault_triggered.emit("SHORT CIRCUIT FAULT [SIMULATED]")

    def simulate_thermal(self):
        """Trigger a simulated thermal warning."""
        self._thermal_warning = True
        self._fault_state = "THERMAL"
        self.fault_triggered.emit("THERMAL WARNING [SIMULATED]")

    @property
    def protection_status(self) -> dict:
        return {
            "overcurrent": self._overcurrent,
            "short_circuit": self._short_circuit,
            "thermal": self._thermal_warning,
            "fault_state": self._fault_state,
            "output_active": self._output_active,
        }
