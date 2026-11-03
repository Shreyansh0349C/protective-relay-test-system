"""
RELAYLAB X — Communication Protocol

Abstract protocol layer for hardware communication.
Does NOT define the final hardware protocol — provides an interface
for future implementation.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class CommandType(Enum):
    """Types of commands that can be sent to the hardware."""
    SET_VOLTAGE = "SET_VOLTAGE"
    SET_CURRENT = "SET_CURRENT"
    SET_FREQUENCY = "SET_FREQUENCY"
    START_OUTPUT = "START_OUTPUT"
    STOP_OUTPUT = "STOP_OUTPUT"
    READ_ADC = "READ_ADC"
    READ_STATUS = "READ_STATUS"
    READ_PROTECTION = "READ_PROTECTION"
    RESET_FAULT = "RESET_FAULT"
    IDENTIFY = "IDENTIFY"


class ResponseStatus(Enum):
    """Response status from hardware."""
    OK = "OK"
    ERROR = "ERROR"
    BUSY = "BUSY"
    FAULT = "FAULT"
    UNKNOWN = "UNKNOWN"


@dataclass
class Command:
    """A command packet to send to the hardware."""
    command_type: CommandType
    parameter: float = 0.0
    payload: bytes = b""

    def serialize(self) -> bytes:
        """
        Serialize command to bytes for transmission.
        NOTE: Final protocol TBD — this is a placeholder format.
        """
        header = b"\xAA\x55"
        cmd_byte = list(CommandType).index(self.command_type).to_bytes(1, "big")
        param_bytes = int(self.parameter * 1000).to_bytes(4, "big", signed=True)
        return header + cmd_byte + param_bytes + self.payload


@dataclass
class Response:
    """A response packet received from the hardware."""
    status: ResponseStatus = ResponseStatus.UNKNOWN
    command_type: Optional[CommandType] = None
    value: float = 0.0
    raw_data: bytes = b""


class ProtocolHandler(ABC):
    """
    Abstract protocol handler interface.
    Implementations handle specific protocol versions.
    """

    @abstractmethod
    def encode_command(self, command: Command) -> bytes:
        """Encode a command into raw bytes."""
        ...

    @abstractmethod
    def decode_response(self, data: bytes) -> Optional[Response]:
        """Decode raw bytes into a response."""
        ...

    @abstractmethod
    def validate_checksum(self, data: bytes) -> bool:
        """Validate the checksum of received data."""
        ...


class PlaceholderProtocol(ProtocolHandler):
    """
    Placeholder protocol implementation.
    To be replaced with actual hardware protocol when defined.
    """

    def encode_command(self, command: Command) -> bytes:
        return command.serialize()

    def decode_response(self, data: bytes) -> Optional[Response]:
        if not data:
            return None
        return Response(
            status=ResponseStatus.OK,
            raw_data=data
        )

    def validate_checksum(self, data: bytes) -> bool:
        return True
