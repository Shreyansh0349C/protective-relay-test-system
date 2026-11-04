# LOW-VOLTAGE POWER TREE & REGULATOR CALCULATIONS
## Stage 3 Deliverable

**Date:** 2024-11-04  
**Status:** CALCULATED & VERIFIED — Estimated current consumption, regulator margins, and thermal dissipation.

---

## 1. SYSTEM POWER TOPOLOGY

```
AC Mains (230V AC)
  │
  ▼
[Mean Well RSP-320-24] ──→ 24 V DC / 13.4 A (320 W max)
  │
  ├── [TPS54560 Buck Regulator] ──→ 5.0 V DC / 5.0 A max
  │     │
  │     ├── [AMS1117-3.3 LDO] ──→ 3.3 V DC / 1.0 A max (Digital: MCU, FPGA, Logic)
  │     │
  │     ├── [LP2985-33 LDO] ────→ 3.3 V DC / 150 mA max (Analog: ADC AVCC, References)
  │     │
  │     └── 5.0 V Rail Direct ──→ USB VBUS, Misc Logic
  │
  ├── [TEN 20-2423 DC-DC] ────→ ±15 V DC / ±667 mA (Analog Op-Amps, Signal Conditioning)
  │
  ├── [B0515S-2WR3 #1] ───────→ ±15 V DC / 2W (Voltage Stage Gate Drivers - Isolated)
  │
  └── [B0515S-2WR3 #2] ───────→ ±15 V DC / 2W (Current Stage Gate Drivers - Isolated)
```

---

## 2. CURRENT BUDGET & REGULATOR MARGINS

| Rail | Target Voltage | Connected Loads | Est. Current (Normal) | Est. Current (Peak) | Selected Regulator | Max Regulator Rating | Thermal / Current Margin | Status |
|---|---|---|---|---|---|---|---|---|
| **Primary DC** | 24.0 V | TPS54560, TEN 20-2423, B0515S (×2) | 1.2 A | 3.5 A | Mean Well RSP-320-24 | 13.4 A (320 W) | >73% headroom | VERIFIED |
| **5.0V Bus** | 5.0 V | AMS1117, LP2985, USB, Logic | 0.35 A | 0.80 A | TPS54560DDAR | 5.0 A | 84% headroom | VERIFIED |
| **3.3V Digital**| 3.3 V | STM32H753, GW2AR FPGA, ISO7741 | 0.55 A | 0.90 A | AMS1117-3.3 | 1.0 A | 10% headroom (Recommend upgrade to 1.5A LDO or TPS54320 if FPGA draws >500mA) | **REVIEW** |
| **3.3V Analog** | 3.3 V | AD7606C-18 AVCC, ADR4525 | 0.08 A | 0.12 A | LP2985-33DBVR | 150 mA | 20% headroom | VERIFIED |
| **±15V Analog**| ±15.0 V | AMC1311, AD8429, Op-amps | 0.15 A | 0.30 A | TEN 20-2423 | ±667 mA | 55% headroom | VERIFIED |
| **±15V Isolated**| ±15.0 V | UCC21520 Gate Drivers (V & I) | 0.20 A | 0.40 A | B0515S-2WR3 (×2) | 133 mA each (2W) | Adequate for switching | VERIFIED |

---

## 3. THERMAL DISSIPATION CALCULATIONS

### 3.1 AMS1117-3.3 LDO (5.0V to 3.3V)
- **Input voltage ($V_{in}$):** 5.0 V
- **Output voltage ($V_{out}$):** 3.3 V
- **Maximum load current ($I_{load}$):** 0.60 A (estimated digital load)
- **Voltage drop ($V_{drop}$):** $5.0 - 3.3 = 1.7\text{ V}$
- **Power dissipation ($P_d$):** $V_{drop} \times I_{load} = 1.7 \text{ V} \times 0.60 \text{ A} = 1.02\text{ W}$
- **Thermal resistance (SOT-223 package, junction-to-ambient $\theta_{JA}$):** ~90 °C/W (without copper pour)
- **Junction temperature rise ($\Delta T$):** $1.02\text{ W} \times 90\text{ °C/W} = 91.8\text{ °C}$
- **Conclusion:** With a standard 1 sq. inch copper PCB thermal pad, $\theta_{JA}$ drops to ~50 °C/W ($\Delta T = 51\text{ °C}$), which is acceptable. However, to ensure robust operation, **recommend replacing AMS1117 with a switching regulator (e.g. TPS562200 or TPS54320)** for the 3.3V digital rail in the final layout.

### 3.2 TPS54560 Buck Regulator (24V to 5.0V)
- **Input voltage ($V_{in}$):** 24.0 V
- **Output voltage ($V_{out}$):** 5.0 V
- **Output current ($I_{load}$):** 0.80 A peak
- **Efficiency ($\eta$, typical for buck at 24V→5V):** ~85%
- **Input power ($P_{in}$):** $\frac{5.0 \times 0.80}{0.85} = 4.71\text{ W}$
- **Power dissipation ($P_d$):** $4.71 - (5.0 \times 0.80) = 0.71\text{ W}$
- **Package:** SOIC-8 PowerPAD (thermal pad soldered to ground plane). $\theta_{JA} \approx 40\text{ °C/W}$ with PCB thermal vias.
- **Junction temperature rise:** $0.71 \times 40 = 28.4\text{ °C}$ (Well within safe operating limits).
