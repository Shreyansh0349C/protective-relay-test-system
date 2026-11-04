# PHASE 3 PLANNING — PROTOTYPE ASSEMBLY & PHYSICAL VALIDATION
**RELAYLAB X**  
**Date:** 2026-11-05  
**Target Phase:** Phase 3 — Hardware Prototyping, Assembly & Physical Testing

---

## 1. OBJECTIVE
To transition from the completed Phase 2 design, software, and simulation baseline into physical hardware manufacturing, board assembly, and rigorous safety-validated physical testing of the protective relay test system.

---

## 2. PHASE 3 EXECUTION PLAN

### Stage 3.1: PCB Fabrication & Component Procurement
- **Actions:**
  - Export Gerber and drill files from KiCad project (`hardware/kicad/`).
  - Order 4-layer FR-4 prototype PCBs with specified copper weight and impedance control.
  - Procure BOM components (STM32H753ZIT6, Gowin FPGA, DAC8568, AD7606C-18, FGA25N120ANTD IGBTs, IRFP4468PBF MOSFETs, UCC21520 gate drivers, Isabellenhütte BVR shunts).
- **Deliverables:** Fabricated PCBs and complete component kits.

### Stage 3.2: Low-Voltage Bench Bring-Up & Power Tree Verification
- **Actions:**
  - Assemble low-voltage power supply rails (3.3V, 5V, $\pm 15\text{ V}$ isolated).
  - Verify regulator output voltages, ripple, and thermal dissipation under load.
  - Program STM32H753 via SWD header and verify clock tree (480 MHz SYSCLK) and basic GPIO toggle.
- **Deliverables:** Powered low-voltage control board and verified MCU firmware boot.

### Stage 3.3: Hardware Protection & Safety Checklist Execution
- **Actions:**
  - Execute **Hardware Validation Safety Checklist** (`docs/PHASE2_HARDWARE_VALIDATION_CHECKLIST.md`).
  - Verify electrical isolation (creepage/clearance), protective earth continuity, and E-stop operation.
  - Test LM393 comparator trip thresholds and 74HC14 fault latching behavior without energizing high-voltage buses.
- **Deliverables:** Signed safety review and verified hardware fault-latch response (TV-05).

### Stage 3.4: DC Bus Pre-Charge & Power Stage Bring-Up
- **Actions:**
  - Test $\pm 300\text{ V}$ DC bus pre-charge circuit ($68\ \Omega, 50\text{W}$) and bleeder discharge ($1\text{ k}\Omega$).
  - Gradually energize DC buses with variable isolation transformer (Variac) under current-limited conditions.
  - Verify gate driver switching waveforms (UCC21520) and dead-time insertion.
- **Deliverables:** Energized and verified DC buses and gate-drive signals.

### Stage 3.5: Closed-Loop Testing & Calibration
- **Actions:**
  - Connect AMC1311 voltage feedback and AD8429 current feedback chains.
  - Run closed-loop PI current control and SPWM voltage generation.
  - Calibrate ADC measurement scaling against reference meters.
- **Deliverables:** Fully calibrated single-phase voltage (0–400 V RMS) and current (0–40 A RMS) outputs.

### Stage 3.6: System Integration & Final Validation (TV-01 to TV-09)
- **Actions:**
  - Establish USB CDC communication between STM32H753 and the PySide6 PC application.
  - Execute full validation test procedures TV-01 through TV-09 on physical hardware.
  - Record test evidence and transition from simulation-based verification to physical validation records.
- **Deliverables:** Phase 3 Validation Report and Production-Ready Test System.
