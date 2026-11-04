# STAGE 7 — INTERFACE-READINESS & EXIT REVIEW REPORT
## RELAYLAB X Phase 2

**Date:** 2026-11-05  
**Status:** REVIEWED & VERIFIED — Stage 6 power-stage and Stage 5 protection interface readiness confirmed for firmware integration.

---

## 1. STAGE 6 EXIT REVIEW & PROTECTION INTERFACE VERIFICATION

A comprehensive review of Stage 6 power-stage designs, Stage 5 protection schematics, and Stage 3 MCU pin mapping confirms the following interface parameters:

1. **Power-Stage Topologies Defined:**
   - **Voltage Stage:** Full H-Bridge IGBT Inverter (FGA25N120ANTD) on a $\pm 300\text{ V}$ DC bus ($600\text{ V}$ span) with $1.5\text{ mH}$ / $4.7\ \mu\text{F}$ LC filter ($f_c \approx 1.9\text{ kHz}$).
   - **Current Stage:** Full H-Bridge MOSFET Regulated Current Source (IRFP4468PBF) on a $\pm 40\text{ V}$ DC bus ($80\text{ V}$ span) with $47\ \mu\text{H}$ / $47\ \mu\text{F}$ filter.

2. **LM393/74HC14 Protection Interface Verification:**
   - **Comparator Output & Pull-Up:** LM393 comparators feature open-collector outputs tied to 3.3V via $10\text{ k}\Omega$ pull-up resistors.
   - **Logic Voltage Compatibility:** 3.3V TTL compatible, directly interfacing with STM32H753 GPIO input pins (PE2–PE5).
   - **Fault Latching:** 74HC14 Schmitt-trigger inverter feedback network latches fault conditions (Overcurrent `FAULT_OC`, Short Circuit `FAULT_SC`, Overvoltage `FAULT_OV`, Emergency Stop `FAULT_ESTOP`).
   - **Hardware Shutdown Independence:** Gate-driver shutdown (via UCC21520 enable/disable pins or PWM tristate control) is triggered directly in hardware by the latch outputs (`FAULT_LATCH#`), acting **independently** of the STM32 firmware or USB connection.
   - **MCU Interrupt Polarity:** Falling-edge triggered external interrupts (EXTI) on PE2–PE5 notify the STM32H753 of fault events.
   - **Manual Reset Requirement:** Latched faults require a physical front-panel push-button reset to clear the 74HC14 latch. Firmware cannot automatically re-enable power outputs while a hardware fault is active.

3. **Unresolved Design Decisions:**
   - None. All electrical interfaces, isolation barriers (ISO7741, B0515S), and sensing chains (AMC1311 voltage, AD8429 current) are fully coordinated.

---

**Exit Review Conclusion:** APPROVED for Stage 7 Firmware & PC Software Integration.
