# POWER-STAGE ARCHITECTURE & FAULT COORDINATION — STAGE 6
## RELAYLAB X Phase 2

**Date:** 2026-11-05  
**Status:** PROPOSED — Complete power stage architecture and fault coordination with Stage 5 protection.

---

## 1. POWER STAGE ARCHITECTURE SUMMARY

1. **Voltage Source (0–400 V AC RMS):**
   - **Topology:** Full H-Bridge IGBT Inverter (FGA25N120ANTD).
   - **DC Bus:** $\pm 300\text{ V}$ DC bus ($600\text{ V}$ span).
   - **Gate Driver:** UCC21520 isolated dual-channel driver powered by B0515S-2WR3 isolated supplies.
   - **Output Filter:** $1.5\text{ mH}$ Sendust inductor + $4.7\ \mu\text{F}$ / 700V MKP film capacitor LC filter ($f_c \approx 1.9\text{ kHz}$).

2. **Current Source (0–40 A AC RMS):**
   - **Topology:** Full H-Bridge Regulated MOSFET Current Source (IRFP4468PBF).
   - **DC Bus:** $\pm 40\text{ V}$ DC bus ($80\text{ V}$ span).
   - **Gate Driver:** UCC21520 isolated dual-channel driver.
   - **Output Filter:** $47\ \mu\text{H}$ / 60A Sendust inductor + $47\ \mu\text{F}$ film / $680\ \mu\text{F}$ electrolytic capacitors.

---

## 2. FAULT COORDINATION WITH STAGE 5 PROTECTION

| Fault Condition | Detection Subsystem | Hardware Action | Gate-Driver Response | Latching? | Manual Reset Required? | MCU Reporting |
|---|---|---|---|---|---|---|
| **Overcurrent (OCP)** | Shunt + AD8429 + LM393 Comparator | Disable Gate Drivers | Immediate output disable via INA/INB low | Yes (74HC14 Latch) | Yes (Push-button) | Interrupt (FAULT_OC) |
| **Short Circuit (SCP)** | Fast Shunt Comparator | Fast Hardware Shutdown | Immediate shutdown (< 50 ns) | Yes (74HC14 Latch) | Yes (Push-button) | Interrupt (FAULT_SC) |
| **Overvoltage (OVP)** | Voltage Divider + AMC1311 + LM393 | Disable Gate Drivers | Immediate output disable | Yes (74HC14 Latch) | Yes (Push-button) | Interrupt (FAULT_OV) |
| **Bus Undervoltage** | Bus Voltage Comparator | Safe State Transition | Disable outputs | No | Automatic | Warning Flag |
| **Overtemperature** | Heatsink Thermostat | Thermal Trip | Disable gate drivers | Yes | Manual / Auto cool | Interrupt (TEMP_TRIP) |
| **Emergency Stop** | XB2-BS542 Push-button | Hardware Bus Contactor Open | Immediate power cut | Yes | Twist-to-release + Reset | Status Flag |

---

**Fault Coordination Status:** VERIFIED  
**Next Action:** Update project management files (`PROJECT_STATUS.md`, `OPEN_ISSUES.md`, `CHANGELOG.md`).
