# STAGE 7 — USB CDC COMMUNICATION PROTOCOL
## RELAYLAB X Phase 2

**Date:** 2026-11-05  
**Protocol Version:** 1.0  
**Status:** DEFINED & SPECIFIED

---

## 1. PACKET STRUCTURE

Communication between the PC host application and the STM32H753 firmware occurs over USB CDC (Virtual COM Port) using framed binary packets with CRC-16 validation.

| Field | Size (Bytes) | Type | Description |
|---|---|---|---|
| **Header** | 2 | uint16_t | Magic marker (`0xAA55`) |
| **Version** | 1 | uint8_t | Protocol version (`0x01`) |
| **Msg Type** | 1 | uint8_t | Command or Response ID |
| **Seq Num** | 2 | uint16_t | Transaction sequence number |
| **Payload Len** | 2 | uint16_t | Length of payload (0 to 256 bytes) |
| **Payload** | *N* | uint8_t[] | Command data or response fields |
| **CRC-16** | 2 | uint16_t | CRC-16-CCITT checksum over header + payload |

---

## 2. COMMAND SET & SPECIFICATIONS

| Command Name | ID | Direction | Description | Valid Range / Units | Error Behavior |
|---|---|---|---|---|---|
| **PING** | `0x01` | PC → MCU | Connection health check | Payload: empty | Returns ACK |
| **GET_STATUS** | `0x02` | PC → MCU | Request system status and fault flags | Payload: empty | Returns status struct |
| **SET_VOLTAGE_REF**| `0x10` | PC → MCU | Set target AC RMS voltage | `0` to `400.0` V RMS (float32) | Rejects out-of-range |
| **SET_CURRENT_REF**| `0x11` | PC → MCU | Set target AC RMS current | `0` to `40.0` A RMS (float32) | Rejects out-of-range |
| **SET_FREQUENCY** | `0x12` | PC → MCU | Set output frequency | Fixed `50.0` Hz (Phase 2) | Rejects non-50Hz |
| **SET_OUTPUT_ENABLE**| `0x20` | PC → MCU | Enable power outputs | Payload: `0x01` (enable) | Blocked if fault active |
| **SET_OUTPUT_DISABLE**| `0x21` | PC → MCU | Disable power outputs | Payload: `0x00` (disable) | Always accepted |
| **GET_MEASUREMENTS**| `0x30` | PC → MCU | Request latest RMS/instantaneous samples | Payload: empty | Returns measurement block |
| **GET_FAULT_STATUS**| `0x40` | PC → MCU | Request detailed fault register | Payload: empty | Returns fault bitmask |
| **CLEAR_FAULT** | `0x41` | PC → MCU | Request fault clear (requires physical reset)| Payload: empty | Rejected if hardware latch active |

---

## 3. SAFETY & ERROR HANDLING
- **Malformed Packets:** Discarded immediately; error counter incremented.
- **CRC Mismatch:** Packet dropped; NACK returned with error code `0xEE`.
- **Fault Bypass Prevention:** Commands attempting to enable outputs while hardware `FAULT_LATCH#` is active are unconditionally rejected by firmware.
