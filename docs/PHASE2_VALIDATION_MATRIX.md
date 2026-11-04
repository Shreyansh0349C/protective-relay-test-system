# STAGE 8 — VALIDATION MATRIX & TEST PROCEDURES TV-01 TO TV-09
## RELAYLAB X Phase 2

**Date:** 2026-11-05  
**Status:** COMPLETED — Validation matrix, test procedures TV-01 to TV-09, and classification established.

---

## 1. VALIDATION MATRIX & TEST CLASSIFICATION

| Test ID | Test Title | Applicable Subsystem | Acceptance Criteria | Execution Classification | Status | Evidence / Notes |
|---|---|---|---|---|---|---|
| **TV-01** | STM32 Initialization & Clock Tree | Firmware / MCU | 480 MHz SYSCLK, 48 MHz USB clock locked | PASS — Simulation | **PASS** | Initialized via SystemInit() and RCC configuration |
| **TV-02** | SPWM Waveform Generation | Firmware / Timer | 50 Hz sinusoidal PWM output via TIM1 | PASS — Simulation | **PASS** | Verified via timer register configuration & simulation |
| **TV-03** | ADC Acquisition & AD7606C Interface | Measurement | 10 kSa/s simultaneous sampling via SPI/DMA | PASS — Software | **PASS** | Verified via software simulation driver |
| **TV-04** | RMS Calculation & Calibration | Measurement | RMS calculation accuracy within $\pm 0.5\%$ | PASS — Software | **PASS** | Verified via pytest unit tests (`test_stage7.py`) |
| **TV-05** | Hardware Protection & Fault Latching | Protection | OCP/SCP/OVP trip disables gate drivers instantly | PENDING — Hardware | **PENDING** | Requires assembled prototype hardware |
| **TV-06** | USB CDC Protocol & Packet Framing | Communication | Valid packet parsing & CRC-16 validation | PASS — Software | **PASS** | Verified via unit tests (`test_stage7.py`) |
| **TV-07** | PC Application Waveform Display | PC Software | Live 50 Hz waveform and RMS rendering | PASS — Software | **PASS** | Desktop GUI operational with simulation fallback |
| **TV-08** | DC Bus Pre-Charge & Bleeder Discharge | Power Stage | Inrush current $\le 10\text{ A}$, discharge $< 5\text{s}$ | PASS — Calculation | **PASS** | Verified via Stage 6 engineering calculations |
| **TV-09** | Thermal Dissipation & Heatsink Limits | Power Stage | IGBT/MOSFET junction temperature within limits | PASS — Calculation | **PASS** | Verified via Stage 6 thermal analysis |

---

## 2. STANDARDIZED TEST RECORDS (TV-01 TO TV-04, TV-06 TO TV-09)

All implemented tests have been verified via software unit tests (`test_stage7.py`) or engineering calculation models. TV-05 (Hardware Protection Response) remains **PENDING** pending physical prototype assembly and qualified high-voltage safety review.
