# PHASE 2 SYSTEM ARCHITECTURE — RELAYLAB X
## Single-Phase Voltage + Current Relay Test Prototype

**Date:** 2024-11-04  
**Version:** 0.1 (PROPOSED)  
**Status:** All architecture decisions require verification against component datasheets

---

## 1. SYSTEM OVERVIEW

The Phase 2 system generates one controlled 50 Hz AC voltage (0–400 V RMS) and one controlled 50 Hz AC current (0–40 A RMS) for testing protective relays. A PC application controls the system via USB, and the system provides real-time feedback measurements.

### 1.1 System Block Diagram (Text Representation)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                          PC (RELAYLAB X Software)                        │
│  ┌─────────┐  ┌──────────┐  ┌───────────┐  ┌───────────┐               │
│  │ Control  │  │ Waveform │  │ Measure-  │  │ Protection│               │
│  │ Panel    │  │ Display  │  │ ments     │  │ Status    │               │
│  └────┬─────┘  └────┬─────┘  └─────┬─────┘  └─────┬─────┘               │
│       └──────────────┴──────────────┴──────────────┘                     │
│                              │ USB CDC                                   │
└──────────────────────────────┼───────────────────────────────────────────┘
                               │
┌──────────────────────────────┼───────────────────────────────────────────┐
│                    STM32H753ZIT6 CONTROLLER                              │
│                              │                                           │
│  ┌────────┐  ┌──────────┐  ┌┴──────────┐  ┌───────────┐  ┌──────────┐  │
│  │ USB    │  │ SPI      │  │ GPIO/     │  │ ADC       │  │ Fault    │  │
│  │ OTG FS │  │ Master   │  │ Control   │  │ Interface │  │ Monitor  │  │
│  └────────┘  └────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬────┘  │
│                   │              │              │              │         │
└───────────────────┼──────────────┼──────────────┼──────────────┼─────────┘
                    │              │              │              │
        ┌───────────┘              │              │              │
        │                         │              │              │
┌───────┴──────────┐              │              │              │
│   GOWIN FPGA     │              │              │              │
│  ┌────────────┐  │              │              │              │
│  │ DDS Core   │  │              │              │              │
│  │ (50 Hz     │  │              │              │              │
│  │  sine LUT) │  │              │              │              │
│  └─────┬──────┘  │              │              │              │
│        │ SPI     │              │              │              │
└────────┼─────────┘              │              │              │
         │                        │              │              │
┌────────┴─────────┐              │              │              │
│    DAC8568       │              │              │              │
│  ┌───────────┐   │              │              │              │
│  │ CH_A: V   │───┼──────────────┼──────────────┼──────────────┤
│  │ CH_B: I   │───┼──────────────┤              │              │
│  └───────────┘   │              │              │              │
└──────────────────┘              │              │              │
         │                        │              │              │
    ┌────┴────┐              ┌────┴────┐         │              │
    │ VOLTAGE │              │ CURRENT │         │              │
    │ SIGNAL  │              │ SIGNAL  │         │              │
    │ CHAIN   │              │ CHAIN   │         │              │
    │         │              │         │         │              │
    │ ┌─────┐ │              │ ┌─────┐ │         │              │
    │ │Amp  │ │              │ │Amp  │ │         │              │
    │ │Stage│ │              │ │Stage│ │         │              │
    │ └──┬──┘ │              │ └──┬──┘ │         │              │
    │    │    │              │    │    │         │              │
    │ ┌──┴──┐ │              │ ┌──┴──┐ │         │              │
    │ │IGBT │ │              │ │MOSFET│ │         │              │
    │ │H-Brg│ │              │ │H-Brg│ │         │              │
    │ └──┬──┘ │              │ └──┬──┘ │         │              │
    │    │    │              │    │    │         │              │
    │ ┌──┴──┐ │              │ ┌──┴──┐ │         │              │
    │ │ LC  │ │              │ │ LC  │ │         │              │
    │ │Filter│ │              │ │Filter│ │         │              │
    │ └──┬──┘ │              │ └──┬──┘ │         │              │
    └────┼────┘              └────┼────┘         │              │
         │                        │              │              │
    ┌────┴───────────────────────┴────┐          │              │
    │    OUTPUT TERMINALS             │          │              │
    │  ┌────────┐     ┌────────┐      │          │              │
    │  │ V OUT  │     │ I OUT  │      │          │              │
    │  │0-400V  │     │ 0-40A  │      │          │              │
    │  └───┬────┘     └───┬────┘      │          │              │
    │      │              │           │          │              │
    │  ┌───┴────┐     ┌───┴────┐      │          │              │
    │  │V Sense │     │I Sense │      │          │              │
    │  │Divider │     │ Shunt  │      │          │              │
    │  └───┬────┘     └───┬────┘      │          │              │
    └──────┼──────────────┼───────────┘          │              │
           │              │                      │              │
    ┌──────┴──────────────┴──────────────────────┴──────┐       │
    │           MEASUREMENT / FEEDBACK                   │       │
    │  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │       │
    │  │ AMC1311  │  │ AD8429   │  │   AD7606C-18     │ │       │
    │  │ Isolated │  │ Instr.   │  │   18-bit ADC     │─┼───────┘
    │  │ V Amp    │  │ Shunt    │  │                  │ │
    │  └──────────┘  │ Amp      │  └──────────────────┘ │
    │                └──────────┘                        │
    └────────────────────────────────────────────────────┘
                                                         │
    ┌────────────────────────────────────────────────────┘
    │
    ┌─────────────────────────────────────────────────────┐
    │           PROTECTION SUBSYSTEM                       │
    │  ┌──────┐  ┌──────┐  ┌──────┐  ┌───────┐           │
    │  │ OC   │  │ SC   │  │ OV   │  │ E-STOP│           │
    │  │Detect│  │Detect│  │Detect│  │ XB2-  │           │
    │  │LM393 │  │LM393 │  │LM393 │  │ BS542 │           │
    │  └──┬───┘  └──┬───┘  └──┬───┘  └───┬───┘           │
    │     └────────┬┴────────┬┘           │               │
    │           ┌──┴─────────┴────────────┤               │
    │           │ 74HC14 Fault Latch     │               │
    │           │ (Hardware-dominant)      │               │
    │           └──┬──────────────────────┘               │
    │              │ Gate-driver DISABLE                   │
    │              │ → MCU fault GPIO                      │
    └──────────────┴──────────────────────────────────────┘
```

---

## 2. SIGNAL-FLOW PATHS

### 2.1 Signal Generation Path (Control → Output)

```
PC Command (USB) → STM32 (parse) → FPGA (DDS parameters) → DAC8568 (analog) →
  Signal conditioning → Power stage (IGBT/MOSFET H-bridge) → LC filter → OUTPUT
```

**Detailed chain for VOLTAGE output:**
1. PC sends voltage setpoint (V_RMS) via USB CDC
2. STM32 receives, validates, computes peak amplitude: V_peak = V_RMS × √2
3. STM32 sends DDS configuration to FPGA via SPI (frequency word, amplitude scaling)
4. FPGA DDS generates sine lookup values at fixed 50 Hz
5. FPGA sends 16-bit samples to DAC8568 via SPI at update rate ≥100 kSa/s
6. DAC8568 CH_A outputs 0–5 V analog waveform (sine, centered at 2.5 V)
7. Signal conditioning scales and level-shifts for power stage input
8. IGBT H-bridge with ±300 V DC bus amplifies to high voltage
9. LC output filter (1.5 mH + MKP caps) reduces switching harmonics
10. Output terminals deliver 0–400 V AC RMS to relay under test

**Detailed chain for CURRENT output:**
1. PC sends current setpoint (I_RMS) via USB CDC
2. STM32 computes peak: I_peak = I_RMS × √2
3. STM32 → FPGA → DAC8568 CH_B → analog sine waveform
4. Signal conditioning for MOSFET power stage input
5. MOSFET H-bridge with ±40 V DC bus drives current
6. LC output filter (47 µH + MKP/electrolytic caps)
7. Output terminals deliver 0–40 A AC RMS through relay under test

### 2.2 Measurement Path (Output → PC Display)

```
Output terminal → Sensor (divider/shunt) → Signal conditioning → ADC → STM32 →
  RMS calculation → USB → PC display
```

**Voltage feedback:**
1. Resistive voltage divider at output terminal scales 400V → ~2V range
2. AMC1311 isolated amplifier provides galvanic isolation
3. Anti-aliasing RC filter
4. AD7606C-18 channel (±5V or ±10V range)
5. STM32 reads ADC via SPI, applies calibration
6. Firmware computes true RMS: V_rms = √(mean(v²)) over N samples
7. Sends to PC via USB for display

**Current feedback:**
1. BVR 0.5 mΩ shunt resistor in series with output
2. AD8429 instrumentation amplifier (gain ~250×) amplifies 20 mV → 5 V
3. Anti-aliasing RC filter
4. AD7606C-18 channel
5. STM32 applies calibration, computes RMS
6. Sends to PC

### 2.3 Protection Path (Hardware-Dominant)

```
Sensor → Comparator (LM393) → Schmitt trigger (74HC14) → Fault latch →
  Gate-driver DISABLE (immediate shutdown) + MCU GPIO (fault reporting)
```

Protection operates independently of firmware — hardware comparators trip the gate drivers directly.

---

## 3. VOLTAGE DOMAINS AND ISOLATION BOUNDARIES

| Domain | Voltage | Ground Ref | Isolation Required |
|---|---|---|---|
| Digital Low-Voltage | 3.3 V / 5 V | DGND | No (common ground) |
| Analog Low-Voltage | ±15 V (op-amps) | AGND | Star-grounded to DGND |
| FPGA I/O | 3.3 V / 2.5 V | DGND | No |
| Gate Driver (V-stage) | ±15 V | V_HV_GND | YES — isolated from control |
| Gate Driver (I-stage) | ±15 V | I_HV_GND | YES — isolated from control |
| Voltage DC Bus | ±300 V | V_HV_GND | YES — lethal voltage |
| Current DC Bus | ±40 V | I_HV_GND | YES |
| Voltage Output | 0–566 V peak | V_OUT_GND | YES — lethal voltage |
| Current Output | 0–56.6 A peak | I_OUT_GND | YES |
| Voltage Sensing | Scaled to ±5 V | AGND | YES (via AMC1311) |
| Current Sensing | 0–20 mV across shunt | AGND | Via instrumentation amp |

### Isolation Barriers

```
CONTROL SIDE                    │            POWER SIDE
(3.3V/5V, safe to touch)       │   (±300V / ±40V, LETHAL)
                                │
STM32 ──── ISO7741 ────────────┼──── Gate Drivers ──── Power Stage
                                │
ADC ◄────── AMC1311 ◄──────────┼──── Voltage Divider ◄── V Output
                                │
ADC ◄────── AD8429 ◄───────────┼──── Current Shunt ◄── I Output
                                │
Fault GPIO ◄── 74HC14 ◄── LM393┼◄── OC/SC Sensors
```

---

## 4. POWER DISTRIBUTION TREE

```
AC MAINS (230V)
    │
    ├── Mean Well RSP-320-24 ──→ 24 V / 13.4 A / 320 W
    │       │
    │       ├── TPS54560 (Buck) ──→ 5 V / 5 A
    │       │       │
    │       │       ├── AMS1117-3.3 (LDO) ──→ 3.3 V / 1 A (Digital: STM32, FPGA, logic)
    │       │       │
    │       │       ├── LP2985-33 (LDO) ──→ 3.3 V / 150 mA (Analog: ADC AVCC, DAC ref)
    │       │       │
    │       │       └── 5 V direct loads (USB VBUS, misc logic)
    │       │
    │       ├── TEN 20-2423 (Isolated) ──→ ±15 V / ±667 mA (Op-amps, analog signal conditioning)
    │       │
    │       ├── B0515S-2WR3 #1 (Isolated) ──→ ±15 V (Voltage stage gate driver supply)
    │       │
    │       └── B0515S-2WR3 #2 (Isolated) ──→ ±15 V (Current stage gate driver supply)
    │
    ├── EXTERNAL: Custom ±300 V DC Bus / 2 kW ──→ Voltage H-bridge
    │
    └── EXTERNAL: Custom ±40 V DC Bus / 3 kW ──→ Current H-bridge
```

**Current Budget Estimate (Low-Voltage 24V Rail):**

| Load | Estimated Current | Rail |
|---|---|---|
| STM32H753 | 200 mA | 3.3 V |
| Gowin FPGA | 300 mA | 3.3 V + 1.2 V core |
| DAC8568 | 10 mA | 5 V (AVDD) |
| AD7606C-18 | 50 mA | 5 V (AVDD) |
| ADR4525 references (×2) | 10 mA | 5 V |
| Digital isolators | 50 mA | 3.3 V + isolated side |
| Op-amps, comparators | 50 mA | ±15 V |
| LEDs, buzzer, misc | 100 mA | 5 V |
| USB | 100 mA | 5 V |
| **Total 5V rail** | **~500 mA** | 5 V (TPS54560 has 5A capacity ✓) |
| **Total 3.3V rail** | **~600 mA** | 3.3 V (AMS1117 has 1A capacity ✓) |

**Note:** FPGA core voltage (1.2 V or 1.0 V depending on Gowin device variant) requires a separate regulator not yet specified. This is an **OPEN ISSUE**.

---

## 5. INTERFACE TABLE

| Interface | From | To | Type | Signals | Speed | Notes |
|---|---|---|---|---|---|---|
| USB CDC | PC | STM32 USB OTG FS | USB 2.0 Full Speed | D+, D−, VBUS, GND | 12 Mbps | Command/data/waveform streaming |
| SPI-FPGA | STM32 | Gowin FPGA | SPI Master | SCK, MOSI, MISO, CS | ≤25 MHz | DDS parameters, status |
| SPI-DAC | FPGA | DAC8568 | SPI Master | SCK, MOSI, CS, LDAC | ≤50 MHz | Waveform samples, 16-bit |
| SPI-ADC | STM32 | AD7606C-18 | SPI Master | SCK, MISO, CS, CONVST, BUSY | ≤20 MHz | Measurement data, 18-bit |
| Gate-V | STM32/FPGA | UCC21520 ×2 | PWM + Enable | INH, INL, EN | — | Via ISO7741 isolator |
| Gate-I | STM32/FPGA | UCC21520 ×2 | PWM + Enable | INH, INL, EN | — | Via ISO7741 isolator |
| Fault-in | Protection HW | STM32 GPIO | Digital input | FAULT_OC, FAULT_SC, FAULT_OV, ESTOP | — | Active-low, interrupt-capable |
| SWD | Debugger | STM32 | Debug | SWDIO, SWCLK, SWO, NRST | — | Programming and debug |
| JTAG-FPGA | Programmer | Gowin FPGA | JTAG | TCK, TMS, TDI, TDO | — | FPGA programming |

---

## 6. SUBSYSTEM DEPENDENCY DIAGRAM

```
                ┌─────────────┐
                │ Power Supply │
                └──────┬──────┘
                       │ (all subsystems depend on power)
          ┌────────────┼────────────┐
          │            │            │
    ┌─────┴─────┐ ┌────┴────┐ ┌────┴─────┐
    │ STM32     │ │  FPGA   │ │Protection│
    │ Controller│ │  DDS    │ │  HW      │
    └─────┬─────┘ └────┬────┘ └────┬─────┘
          │            │           │
          │      ┌─────┴─────┐     │
          │      │  DAC8568  │     │
          │      └─────┬─────┘     │
          │            │           │
    ┌─────┴────────────┴───────────┴──────┐
    │         POWER STAGES                │
    │  ┌──────────┐  ┌──────────┐         │
    │  │ V Stage  │  │ I Stage  │         │
    │  │ (IGBT)   │  │ (MOSFET) │         │
    │  └────┬─────┘  └────┬─────┘         │
    └───────┼──────────────┼──────────────┘
            │              │
    ┌───────┴──────────────┴──────────────┐
    │    MEASUREMENT / FEEDBACK            │
    │  ┌──────────┐  ┌──────────┐         │
    │  │ V Sense  │  │ I Sense  │         │
    │  └────┬─────┘  └────┬─────┘         │
    │       └──────┬───────┘              │
    │         ┌────┴─────┐                │
    │         │AD7606C-18│                │
    │         └────┬─────┘                │
    └──────────────┼──────────────────────┘
                   │
                   └──→ STM32 → USB → PC
```

**Build/Test Order:**
1. Power supply (24V → 5V → 3.3V) — standalone test
2. STM32 controller — bring-up with SWD
3. FPGA — configuration and SPI communication
4. DAC — waveform output verification
5. ADC — input measurement verification
6. Measurement chain — signal conditioning
7. Protection — standalone fault latch test
8. Power stages — LOW VOLTAGE FIRST, then controlled ramp to full voltage
9. Integration — full loop with PC software

---

## 7. OPEN ARCHITECTURE DECISIONS

| ID | Decision | Options | Status | Impact |
|---|---|---|---|---|
| AF-015 | FPGA inclusion in Phase 2 | A: Include FPGA (architecture consistency) / B: STM32-only (simpler) | PROPOSED: Option A | Affects bill of materials, PCB complexity, firmware |
| AF-014 | AD7606C-18 interface | A: SPI (fewer pins) / B: Parallel (faster) | PROPOSED: Option A (SPI) | Affects STM32 pin allocation, data rate |
| AF-016 | Voltage stage topology | A: Full H-bridge / B: Half-bridge + transformer | PROPOSED: Option A (H-bridge) | Affects component count, transformer requirement, output voltage capability |
| AF-017 | RMS measurement method | A: Analog AD8436 / B: Digital (ADC + firmware) | PROPOSED: Option B (Digital) | Affects BOM, firmware complexity |
| NEW | FPGA core voltage regulator | Must add 1.0/1.2V regulator for FPGA core | Not specified in component list | Blocks FPGA power design |
| NEW | Switching frequency for H-bridges | Typically 20–100 kHz; higher = better THD but higher losses | Needs calculation | Affects filter design, thermal, EMC |

---

**Architecture Status:** PROPOSED  
**Next Action:** Stage 3 — Begin datasheet verification for STM32H753ZIT6 pin mapping and supply requirements.
