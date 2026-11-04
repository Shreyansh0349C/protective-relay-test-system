# STAGE 5 VALIDATION PLAN — MEASUREMENT & PROTECTION
## RELAYLAB X Phase 2

**Date:** 2026-11-05  
**Status:** PROPOSED — Test procedures, acceptance criteria, and verification methods for Stage 5 hardware.

---

## 1. OBJECTIVE
To verify the measurement-conditioning accuracy (voltage divider + AMC1311, current shunt + AD8429) and the reliability of the hardware-dominant protection circuits (LM393 comparators, fault latching, and gate-driver shutdown).

---

## 2. TEST MATRIX

| Test ID | Subsystem | Objective | Equipment Required | Procedure | Acceptance Criteria | Status |
|---|---|---|---|---|---|---|
| TV-01 | Voltage Feedback | Verify voltage divider ratio & AMC1311 isolation | Variac, Digital Multimeter (DMM), Oscilloscope | Apply 100V, 200V, 400V AC to input; measure AMC1311 differential output. | Output matches calculated transfer function within $\pm 0.5\%$. | Not started |
| TV-02 | Current Shunt | Verify shunt temperature rise at 40A | DC/AC Current Source, Thermal Camera | Run 40A RMS through BVR shunt for 10 minutes. | Shunt temperature stable below 65 °C ($P \le 0.8\text{W}$). | Not started |
| TV-03 | AD8429 Amplifier | Verify instrumentation amplifier gain | Function Generator, DMM, Scope | Inject 10 mV to 30 mV sine wave at shunt input; measure AD8429 output. | Gain equals $143.1 \pm 1\%$. | Not started |
| TV-04 | ADC Scaling | Verify AD7606C-18 readout accuracy | Calibrated Source, PC Software | Feed known voltage/current into test system; read values in software UI. | Displayed RMS matches reference within $\pm 1.0\%$. | Not started |
| TV-05 | OCP Trip Test | Verify overcurrent comparator trip | Adjustable Current Source | Slowly ramp current above 48A RMS threshold. | Gate drivers disabled within < 50 µs of threshold crossing. | Not started |
| TV-06 | SCP Trip Test | Verify short-circuit fast trip | Fast Pulse Generator / Simulated Fault | Inject transient pulse exceeding 120A equivalent. | Immediate hardware shutdown latching without MCU intervention. | Not started |
| TV-07 | OVP Trip Test | Verify overvoltage trip | Adjustable Voltage Source | Ramp voltage above 460V RMS equivalent. | Gate drivers disabled, fault latched. | Not started |
| TV-08 | E-Stop Test | Verify emergency stop hardware path | Push-button (XB2-BS542) | Press E-stop button during active output simulation. | Hardware outputs immediately cut regardless of MCU state. | Not started |
| TV-09 | Fault Reset | Verify manual fault reset | Panel Push-button | Trigger OCP fault, press Reset button. | Fault latch clears only when reset pressed and condition removed. | Not started |

---

**Validation Plan Status:** PROPOSED  
**Next Action:** Proceed to KiCad schematic implementation for Stage 5.
