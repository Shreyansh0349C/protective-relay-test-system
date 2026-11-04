# STAGE 8 — HARDWARE VALIDATION SAFETY CHECKLIST
## RELAYLAB X Phase 2

**Date:** 2026-11-05  
**Status:** MANDATORY SAFETY PREREQUISITES ESTABLISHED

---

## 1. PURPOSE
The RELAYLAB X Phase 2 hardware architecture includes high-energy power stages ($\pm 300\text{ V}$ DC bus, $400\text{ V}$ AC RMS output, and $40\text{ A}$ RMS current output). Software simulation and host unit tests **do not** constitute safety validation for high-energy circuits. Prior to physical energization or hardware testing, the following safety checklist must be completed and signed off by a qualified safety reviewer.

---

## 2. HARDWARE SAFETY CHECKLIST

| Item | Requirement / Verification Item | Standard / Criteria | Status | Sign-off / Date |
|---|---|---|---|---|
| **HS-01** | Electrical Isolation & Creepage | Clearance and creepage distances meet IEC 61010-1 for $\pm 300\text{ V}$ bus. | **PENDING** | Unsigned |
| **HS-02** | Protective Earth (PE) Continuity | Enclosure and heatsink bonded to Earth ground ($< 0.1\ \Omega$). | **PENDING** | Unsigned |
| **HS-03** | Emergency Stop Functionality | XB2-BS542 push-button cuts main AC input and disables DC contactors within 20 ms. | **PENDING** | Unsigned |
| **HS-04** | DC Bus Pre-Charge Operation | $68\ \Omega$ pre-charge resistor limits inrush current to $\le 10\text{ A}$; bypass relay operates correctly. | **PENDING** | Unsigned |
| **HS-05** | DC Bus Bleeder Discharge | Stored energy (396 J) discharges below 50 V within 5 seconds of power-off via $1\text{ k}\Omega$ bleeders. | **PENDING** | Unsigned |
| **HS-06** | Hardware Gate-Driver Shutdown | UCC21520 disable pins wired directly to 74HC14 fault latch, independent of MCU. | **PENDING** | Unsigned |
| **HS-07** | Overcurrent & Short-Circuit Hardware | Shunt + AD8429 + LM393 comparators trip in $< 50\text{ ns}$ during fault conditions. | **PENDING** | Unsigned |
| **HS-08** | Thermal Protection Interlock | Heatsink thermostat opens circuit if temperature exceeds 85 °C. | **PENDING** | Unsigned |
| **HS-09** | Measurement Isolation Barrier | AMC1311 and ISO7741 isolation barriers tested to 2.5 kVrms dielectric strength. | **PENDING** | Unsigned |
| **HS-10** | Enclosure & Interlock Access | Interlock switch disables high-voltage supplies when enclosure panel is opened. | **PENDING** | Unsigned |

---

**Warning:** Energizing high-energy power stages without completing this safety checklist and obtaining qualified engineering sign-off creates severe electrical shock, arc flash, and fire hazards.
