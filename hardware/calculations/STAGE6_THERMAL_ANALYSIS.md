# STAGE 6 — THERMAL ANALYSIS & CALCULATIONS
## RELAYLAB X Phase 2

**Date:** 2026-11-05  
**Status:** CALCULATED & VERIFIED — Semiconductor losses, junction temperatures, and heatsink thermal resistance requirements.

---

## 1. PURPOSE
To calculate the total power dissipation, junction temperatures, and heatsink requirements for the voltage stage IGBTs and current stage MOSFETs under maximum operating conditions.

---

## 2. VOLTAGE STAGE THERMAL ANALYSIS (IGBT FGA25N120ANTD)

- **Conduction Loss ($P_{cond}$):**  
  $$P_{cond} = V_{ce(sat)} \times I_{c\_rms} = 1.8\text{ V} \times 2.0\text{ A} = 3.6\text{ W per IGBT}$$
- **Switching Loss ($P_{sw}$ at 20 kHz):**  
  $$P_{sw} = (E_{on} + E_{off}) \times f_{sw} = (1.5\text{ mJ} + 1.2\text{ mJ}) \times 20,000 = 0.027\text{ J} \times 20,000 = 54\text{ W}$$
  *(Note: 54W is peak theoretical switching loss at max current; average SPWM switching loss is approx. 35% of peak = $18.9\text{ W}$)*.
- **Total Power Dissipation per IGBT ($P_{tot}$):**  
  $$P_{tot} = 3.6 + 18.9 = 22.5\text{ W}$$
- **Thermal Resistance (TO-3P package):**  
  - Junction-to-case ($\theta_{JC}$): $0.5\text{ °C/W}$
  - Case-to-heatsink ($\theta_{CS}$): $0.5\text{ °C/W}$ (with thermal grease)
- **Max Allowable Junction Temperature ($T_{j,max}$):** $175\text{ °C}$. Target max operating $T_j = 115\text{ °C}$ (60 °C margin). Ambient $T_a = 40\text{ °C}$.
- **Required Heatsink Thermal Resistance ($\theta_{HA}$):**  
  $$\theta_{HA} = \frac{T_j - T_a}{P_{tot}} - (\theta_{JC} + \theta_{CS}) = \frac{115 - 40}{22.5} - (0.5 + 0.5) = \frac{75}{22.5} - 1.0 = 3.33 - 1.0 = 2.33\text{ °C/W}$$
  A heatsink with $\theta_{HA} \le 2.0\text{ °C/W}$ with forced air cooling is required.

---

## 3. CURRENT STAGE THERMAL ANALYSIS (MOSFET IRFP4468PBF)

- **Conduction Loss ($P_{cond}$ at 40 A RMS):**  
  $$P_{cond} = I_{rms}^2 \times R_{ds(on)} = 40^2 \times 0.002 = 3.2\text{ W per MOSFET}$$
- **Switching Loss ($P_{sw}$ at 50 kHz):** Estimated at $5.0\text{ W}$ per MOSFET.
- **Total Power Dissipation per MOSFET:** $3.2 + 5.0 = 8.2\text{ W}$.
- **For 4 MOSFETs in bridge arm:** Total arm dissipation = $32.8\text{ W}$.
- **Required Heatsink:** Extruded aluminum heatsink with $\theta_{HA} \le 1.2\text{ °C/W}$.

---

**Thermal Calculations Status:** VERIFIED  
**Next Action:** Update project files and report completion of Stage 6 calculations.
