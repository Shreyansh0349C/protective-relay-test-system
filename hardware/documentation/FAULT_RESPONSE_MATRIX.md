# FAULT-RESPONSE MATRIX — RELAYLAB X Phase 2
## Stage 5 Deliverable

**Date:** 2026-11-05  
**Status:** PROPOSED — Hardware and software fault handling protocol.

---

## 1. FAULT RESPONSE MATRIX

| Fault Condition | Detection Mechanism | Hardware Action | MCU Reporting | Reset Method | Safety Priority |
|---|---|---|---|---|---|
| **Overcurrent (OCP)** | LM393 Comparator monitoring AD8429 output | Immediate gate-driver disable via hardware latch | Interrupt (FAULT_OC) sent to STM32 | Manual push-button reset | HIGH |
| **Short Circuit (SCP)** | Fast LM393 Comparator monitoring shunt directly | Immediate hardware shutdown (< 50 ns response) | Interrupt (FAULT_SC) sent to STM32 | Manual push-button reset + fault check | CRITICAL |
| **Overvoltage (OVP)** | AMC1311 output + LM393 Comparator | Gate-driver disable via hardware latch | Interrupt (FAULT_OV) sent to STM32 | Manual push-button reset | HIGH |
| **Overtemperature** | Thermal switch / thermostat on heatsink | Hardware shutdown of power stages | Interrupt (TEMP_FAULT) sent to STM32 | Automatic recovery upon cool-down | MEDIUM |
| **Emergency Stop** | XB2-BS542 physical push-button (N/C contact) | Hardware power cut (independent of MCU) | Status flag (ESTOP_ACTIVE) | Manual twist-to-release + reset button | CRITICAL |
| **MCU Watchdog Timeout**| Internal watchdog timer (IWDG) | Hardware reset of STM32 + safe output state | Logged upon reboot | Automatic reboot | HIGH |
