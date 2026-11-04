# COMPONENT ALLOCATION TABLE — RELAYLAB X Phase 2

**Date:** 2024-11-04  
**Status:** PROPOSED — All components require datasheet verification before design commitment

---

## Allocation Categories

| Category | Meaning |
|---|---|
| **Required Phase 2** | Needed for single-phase voltage + current prototype |
| **Reserved Later** | Allocated for final product (4V+4I), not implemented now |
| **Optional** | May improve performance but not required for Phase 2 scope |
| **Requires Confirmation** | Part number, specification, or suitability needs verification |
| **Rejected/Replaced** | Original selection unsuitable; replacement identified |

---

## 1. MAIN CONTROLLER

| Component | Part Number | Package | Phase 2 | Qty | Verification |
|---|---|---|---|---|---|
| MCU | STM32H753ZIT6 | LQFP-144 | **Required** | 1 | UNVERIFIED — Pin mapping, peripheral allocation, and supply requirements must be verified against ST datasheet DS12110 |

**Notes:**
- STM32H753 provides: ARM Cortex-M7 @ 480 MHz, FPU, 2 MB Flash, 1 MB RAM
- Built-in ADC, DAC, SPI, USB OTG FS/HS, DMA — all needed for Phase 2
- LQFP-144 package has specific power pin requirements (multiple VDD, VDDA, VCAP pairs)

---

## 2. FPGA AND CONFIGURATION

| Component | Part Number | Package | Phase 2 | Qty | Verification |
|---|---|---|---|---|---|
| FPGA | GW2AR-LV18EQ144I | QFP-144 | **Requires Confirmation** | 1 | UNVERIFIED — Open decision AF-015: Is FPGA essential for Phase 2 50 Hz DDS, or can STM32 timer+DMA suffice? |
| Config Flash | W25Q128JVEIQ | SOP-8 | **Requires Confirmation** | 1 | UNVERIFIED — Only needed if FPGA is used |
| Oscillator | SIT8008BI (50 MHz) | SOT23-5 | **Requires Confirmation** | 1 | UNVERIFIED — Only needed if FPGA is used |

**Engineering Decision Required (AF-015):**
For fixed 50 Hz Phase 2 operation, the STM32H753's built-in DAC with timer-triggered DMA can generate sine waves with excellent quality. The FPGA adds complexity but enables:
- Higher update rates for lower THD
- Independent waveform generation without loading the MCU
- Clean path to variable-frequency operation in later phases

**PROPOSED decision:** Include FPGA in Phase 2 design to maintain architecture consistency with final product, even though STM32 alone could handle 50 Hz. This avoids a complete redesign for Phase 3.

---

## 3. DAC

| Component | Part Number | Package | Phase 2 | Qty | Verification |
|---|---|---|---|---|---|
| DAC | DAC8568SCPW | TSSOP-16 | **Required** | 1 | UNVERIFIED — Must verify: SPI timing, output range with ADR4525 reference, output drive capability |
| Voltage Reference | ADR4525BRZ | SOIC-8 | **Required** | 1 | UNVERIFIED — 2.500 V reference; must verify DAC output range = 0 to 2×Vref = 0–5V |

**Notes:**
- DAC8568: 8 channels × 16-bit. Phase 2 uses 2 channels (1× voltage, 1× current control). Remaining 6 reserved for later phases.
- With Vref = 2.500 V and internal 2× gain: output range = 0 to 5.000 V
- 16-bit → LSB = 5.000 V / 65536 = 76.3 µV resolution
- SPI interface up to 50 MHz clock

---

## 4. ADC

| Component | Part Number | Package | Phase 2 | Qty | Verification |
|---|---|---|---|---|---|
| ADC | AD7606C-18BSTZ | LQFP-64 | **Required** | 1 | UNVERIFIED — Must verify: input range configuration, interface timing, reference requirements |
| ADC Reference | ADR4525BRZ | SOIC-8 | **Required** | 1 | UNVERIFIED — May share with DAC reference or require separate instance; crosstalk analysis needed |

**Notes:**
- AD7606C-18: 8 channels × 18-bit simultaneous sampling, up to 1 MSa/s per channel
- Configurable input ranges: ±2.5V, ±5V, ±10V, ±20V (software selectable)
- Phase 2 uses 2–4 channels: voltage feedback, current feedback (+ optional V/I output monitoring)
- Interface decision (AF-014): Serial SPI vs 18-bit parallel. **PROPOSED:** Use SPI for Phase 2 (fewer pins, simpler routing, adequate speed for 50 Hz measurement)

---

## 5. DIGITAL ISOLATION AND INTERFACES

| Component | Part Number | Package | Phase 2 | Qty | Verification |
|---|---|---|---|---|---|
| Quad Digital Isolator | ISO7741FDBQR | SSOP-16 | **Required** | 1–2 | UNVERIFIED — Verify: data rate vs SPI clock, propagation delay, channel direction |
| 6-Channel Digital Isolator | ISO7762 | — | **Requires Confirmation** | TBD | UNVERIFIED — Exact part number, package, and quantity not confirmed |
| 3-to-8 Decoder | 74HC138D | SOIC-16 | **Optional** | 1 | UNVERIFIED — For SPI chip-select expansion; may not be needed for Phase 2 (only 2–3 SPI slaves) |
| Level Shifter | SN74LVC8T245PWR | TSSOP-24 | **Requires Confirmation** | TBD | UNVERIFIED — Needed only if FPGA I/O banks operate at different voltage than STM32 |

---

## 6. VOLTAGE OUTPUT STAGE

| Component | Part Number | Package | Phase 2 | Qty | Verification |
|---|---|---|---|---|---|
| IGBT | FGA25N120ANTD | TO-3P | **Required** | 4 | UNVERIFIED — 1200V/25A NPT IGBT; verify Vce(sat), switching times, gate charge for ±300V bus application |
| Gate Driver | UCC21520DWR | SOIC-16 | **Required** | 2 | UNVERIFIED — Dual-channel isolated driver; verify UVLO, propagation delay, dead time |
| Isolated DC-DC | B0515S-2WR3 | SIP-4 | **Required** | 2 | UNVERIFIED — 5V→±15V isolated supply for gate drivers; verify isolation voltage and power rating |
| Output Inductor | Custom Sendust toroidal | — | **Required** | 1 | UNVERIFIED — 1.5 mH, must handle peak current at 50 Hz; custom component requires detailed specification |
| Output Capacitor | MKP1848 4.7 µF / 700 V | — | **Required** | TBD | UNVERIFIED — Film cap for LC output filter; quantity depends on filter design |
| DC Bus Supply | Custom ±300 V / 2 kW | — | **Required** | 1 | UNVERIFIED — External supply; interface only, internal design not in Phase 2 scope |

**Critical Note:** Voltage output stage operates at potentially lethal voltages (±300 V DC bus, up to 400 V AC output). Design must receive independent engineering review before any energization.

---

## 7. CURRENT OUTPUT STAGE

| Component | Part Number | Package | Phase 2 | Qty | Verification |
|---|---|---|---|---|---|
| MOSFET | IRFP4468PBF | TO-247 | **Required** | 8 | UNVERIFIED — 100V/195A; verify Rds(on), gate charge, SOA for ±40V bus application |
| Gate Driver | UCC21520DWR | SOIC-16 | **Required** | 2 | UNVERIFIED — Same as voltage stage; verify shared design feasibility |
| Isolated DC-DC | B0515S-2WR3 | SIP-4 | **Required** | 2 | UNVERIFIED — For gate driver supplies |
| Output Inductor | Custom Sendust | — | **Required** | 1 | UNVERIFIED — 47 µH / 60 A; custom component |
| Output Cap (Film) | MKP 47 µF / 100 V | — | **Required** | TBD | UNVERIFIED |
| Output Cap (Electrolytic) | 680 µF / 63 V low-ESR | — | **Required** | TBD | UNVERIFIED |
| DC Bus Supply | Custom ±40 V / 3 kW | — | **Required** | 1 | UNVERIFIED — External supply; interface only |

---

## 8. MEASUREMENT AND FEEDBACK

| Component | Part Number | Package | Phase 2 | Qty | Verification |
|---|---|---|---|---|---|
| Isolated Amplifier | AMC1311BDWVR | SOIC-8 | **Required** | 1 | UNVERIFIED — For voltage feedback isolation; verify input range, bandwidth, gain |
| Current Shunt | Isabellenhütte BVR 0.5 mΩ / 15 W / 0.1% | — | **Required** | 1 | UNVERIFIED — Verify: power dissipation at 40 A (P = I²R = 40² × 0.0005 = 0.8 W ✓), voltage drop = 20 mV at 40 A |
| Instrumentation Amp | AD8429ARZ | SOIC-8 | **Required** | 1 | UNVERIFIED — For shunt signal amplification; verify gain, bandwidth, input offset |
| True RMS-to-DC | AD8436ACPZ | LFCSP-16 | **Optional** | 1 | UNVERIFIED — Decision AF-017: analog vs digital RMS. Digital preferred for Phase 2 (simpler, uses existing ADC) |

**Preliminary Shunt Calculation (CALCULATED):**
- At 40 A: V_shunt = 40 × 0.0005 = 20 mV
- At 40 A: P_shunt = 40² × 0.0005 = 0.8 W (within 15 W rating ✓)
- AD8429 gain needed: if ADC input range = ±5 V, gain = 5.0 / 0.020 = 250×
- This is within AD8429 capability (gain up to 10,000×)

---

## 9. POWER SUPPLY

| Component | Part Number | Package | Phase 2 | Qty | Verification |
|---|---|---|---|---|---|
| 24V PSU | Mean Well RSP-320-24 | Enclosed | **Required** | 1 | UNVERIFIED — 24V/13.4A/320W; verify sufficient for low-voltage electronics |
| 24V→5V Buck | TPS54560DDAR | SOIC-8 (PowerPAD) | **Required** | 1 | UNVERIFIED — 5V/5A; verify input range includes 24V, output current sufficient |
| 5V→3.3V LDO | AMS1117-3.3 | SOT-223 | **Required** | 1 | UNVERIFIED — 3.3V/1A; verify dropout voltage, thermal dissipation from 5V input |
| 3.3V Low-Noise LDO | LP2985-33DBVR | SOT-23-5 | **Required** | 1 | UNVERIFIED — Low-noise 3.3V for analog; verify PSRR and noise specs |
| Isolated DC-DC | TEN 20-2423 | DIP-24 | **Requires Confirmation** | 1 | UNVERIFIED — 24V→±15V/±667mA isolated; verify isolation voltage and application |

---

## 10. PROTECTION AND MISCELLANEOUS

| Component | Part Number | Package | Phase 2 | Qty | Verification |
|---|---|---|---|---|---|
| Comparator | LM393DR | SOIC-8 | **Required** | 2–4 | UNVERIFIED — For OC/SC detection; verify response time |
| Schmitt Trigger | 74HC14D | SOIC-14 | **Required** | 1 | UNVERIFIED — For fault signal conditioning |
| Emergency Stop | XB2-BS542 | Panel mount | **Required** | 1 | UNVERIFIED — N/C + N/O contacts for E-stop |
| MOV | 14D471K | Radial | **Required** | TBD | UNVERIFIED — 470V MOV for transient protection |
| Inrush Limiter | SCK-105 | Radial | **Required** | 1 | UNVERIFIED — NTC for inrush current limiting |

---

## SUMMARY

| Category | Count |
|---|---|
| Required Phase 2 | ~35 unique component types |
| Reserved for Later | FPGA (conditional), extra DAC/ADC channels |
| Optional | AD8436 (analog RMS), 74HC138 (CS decoder) |
| Requires Confirmation | ISO7762, SN74LVC8T245, TEN 20-2423, FPGA subsystem |
| Rejected/Replaced | None yet (all pending verification) |

**Verification Status:** All components are UNVERIFIED. Stage 3 (Datasheet Verification) must be completed before any schematic capture begins.
