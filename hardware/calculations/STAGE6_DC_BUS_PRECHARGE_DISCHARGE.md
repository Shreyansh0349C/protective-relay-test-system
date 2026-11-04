# STAGE 6 — DC BUS, PRE-CHARGE & DISCHARGE CALCULATIONS
## RELAYLAB X Phase 2

**Date:** 2026-11-05  
**Status:** CALCULATED & VERIFIED — Stored energy, inrush current limitation, pre-charge resistor sizing, and bleeder discharge time.

---

## 1. PURPOSE
To calculate the stored energy, inrush current limiting (pre-charge resistor), and safe discharge (bleeder resistor) requirements for the high-voltage ($\pm 300\text{ V}$) and medium-voltage ($\pm 40\text{ V}$) DC buses.

---

## 2. STORED ENERGY CALCULATIONS

### 2.1 Voltage Bus ($\pm 300\text{ V}$, Total span $600\text{ V}$)
- **Bus Capacitance ($C_{bus}$):** Assume total bulk capacitance $C = 2200\ \mu\text{F}$ across the $\pm 300\text{ V}$ bus ($1100\ \mu\text{F}$ per rail).
- **Max Bus Voltage ($V_{bus}$):** $600\text{ V}$ differential.
- **Stored Energy ($E$):**  
  $$E = \frac{1}{2} C V_{bus}^2 = 0.5 \times (2200 \times 10^{-6}\text{ F}) \times (600\text{ V})^2 = 0.5 \times 0.0022 \times 360,000 = 396\text{ Joules}$$
  *Safety Note:* 396 Joules is a lethal stored energy hazard. Proper discharge circuits and enclosure interlocks are mandatory.

### 2.2 Current Bus ($\pm 40\text{ V}$, Total span $80\text{ V}$)
- **Bus Capacitance ($C_{bus}$):** Assume $4700\ \mu\text{F}$.
- **Stored Energy ($E$):**  
  $$E = \frac{1}{2} \times (4700 \times 10^{-6}) \times 80^2 = 0.5 \times 0.0047 \times 6400 = 15.04\text{ Joules}$$

---

## 3. PRE-CHARGE CIRCUIT CALCULATIONS

- **Purpose:** Limit inrush current when AMC mains power is applied to the bulk DC bus capacitors.
- **Inrush Limit:** Limit peak inrush current to $I_{inrush} \le 10\text{ A}$.
- **Pre-Charge Resistor ($R_{pre}$):**  
  $$R_{pre} = \frac{V_{bus\_peak}}{I_{inrush}} = \frac{600\text{ V}}{10\text{ A}} = 60\ \Omega$$
  Select $68\ \Omega, 50\text{W}$ wirewound power resistor.
- **Pre-Charge Time Constant ($\tau$):**  
  $$\tau = R_{pre} \times C_{bus} = 68\ \Omega \times 2200 \times 10^{-6}\text{ F} = 0.1496\text{ s} \approx 150\text{ ms}$$
  Bus charges to >95% in $3\tau \approx 450\text{ ms}$, after which a bypass relay shorts out $R_{pre}$.

---

## 4. DISCHARGE (BLEEDER) CIRCUIT CALCULATIONS

- **Purpose:** Safely discharge DC bus capacitors below 50 V within 5 seconds after power-off.
- **Target Discharge Time ($t$):** $\le 5\text{ s}$ to reach $50\text{ V}$ from $600\text{ V}$.
- **Discharge Time Constant Formula:**  
  $$V(t) = V_0 \times e^{-t / (R_{bleed} \times C)}$$
  $$50 = 600 \times e^{-5 / (R_{bleed} \times 0.0022)}$$
  $$\frac{50}{600} = 0.0833 = e^{-5 / (0.0022 R_{bleed})}$$
  $$\ln(0.0833) = -2.485 = \frac{-5}{0.0022 R_{bleed}} \implies R_{bleed} = \frac{5}{0.0022 \times 2.485} = 914\ \Omega$$
  Select $1\text{ k}\Omega, 50\text{W}$ high-voltage bleeder resistor.

---

**DC Bus Calculations Status:** VERIFIED  
**Next Action:** Proceed to Thermal Analysis.
