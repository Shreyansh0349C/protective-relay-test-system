# PHASE 2 FINAL TECHNICAL REPORT — RELAYLAB X
**Date:** 2026-11-05  
**Document ID:** RELAYLAB-X-PH2-TR-01  
**Status:** APPROVED — Phase 2 Engineering, Architecture, Firmware, and Software Design Complete.

---

## 1. PROJECT OVERVIEW & OBJECTIVES
RELAYLAB X is a professional research prototype protective relay test system designed to test and calibrate modern digital and electromechanical protective relays. Phase 2 extends the Phase 1 software prototype into a complete hardware and firmware engineering specification featuring:
- **1x Single-Phase Voltage Source:** $0–400\text{ V}$ AC RMS, fixed 50 Hz.
- **1x Single-Phase Current Source:** $0–40\text{ A}$ AC RMS, fixed 50 Hz.
- **Hardware-Dominant Protection:** Independent analog comparators and fault latches guaranteeing sub-microsecond response independent of MCU or PC software state.

---

## 2. SYSTEM ARCHITECTURE & SUBSYSTEMS
- **MCU & Control:** STM32H753ZIT6 (Cortex-M7, 480 MHz) handling SPWM generation, ADC sampling, and USB CDC communication.
- **Voltage Power Stage:** Full H-Bridge IGBT Inverter (FGA25N120ANTD) on a $\pm 300\text{ V}$ DC bus with $1.5\text{ mH}$ / $4.7\ \mu\text{F}$ LC filter.
- **Current Power Stage:** Full H-Bridge MOSFET Regulated Current Source (IRFP4468PBF) on a $\pm 40\text{ V}$ DC bus with Isabellenhütte BVR shunt.
- **Measurement & Protection:** AMC1311 isolated voltage conditioning, AD8429 instrumentation amplifier current conditioning, AD7606C-18 simultaneous ADC, and LM393/74HC14 hardware protection fault latching.
- **PC Application:** PySide6 / PyQtGraph desktop application with real-time waveform streaming, RMS calculations, and simulation mode.

---

## 3. VALIDATION SUMMARY
- **Software & Simulation Validation:** **COMPLETE** (Passed all protocol framing, CRC, RMS calculation, and GUI integration tests).
- **Physical Hardware Validation:** **PENDING** (Requires prototype manufacturing and completion of the Hardware Safety Checklist).

---

**Conclusion:** Phase 2 engineering design, architecture, firmware specifications, and software integration are fully complete and ready for release packaging.
