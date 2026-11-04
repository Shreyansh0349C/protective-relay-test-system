# INTERFACE COMPATIBILITY MATRIX — RELAYLAB X Phase 2
## Stage 3 Deliverable

**Date:** 2024-11-04  
**Status:** PROPOSED — Electrical interface compatibility across low-voltage subsystems.

---

## 1. INTERFACE TABLE

| Signal / Bus | Source Device | Destination Device | Dir | Logic Voltage | Max Freq / Timing | Pull-Up / Pull-Down | Isolation Req. | Verification Status |
|---|---|---|---|---|---|---|---|---|
| **SPI1_SCK** | STM32H753 | FPGA / DAC8568 | Out | 3.3V CMOS | 25 MHz | None | No (Low-voltage domain) | VERIFIED (Compatible) |
| **SPI1_MISO** | FPGA / ADC | STM32H753 | In | 3.3V CMOS | 25 MHz | None | No | VERIFIED (Compatible) |
| **SPI1_MOSI** | STM32H753 | FPGA / DAC8568 | Out | 3.3V CMOS | 25 MHz | None | No | VERIFIED (Compatible) |
| **SPI1_CS_FPGA** | STM32H753 | FPGA | Out | 3.3V CMOS | GPIO (Static) | 10k pull-up | No | VERIFIED (Compatible) |
| **SPI1_CS_DAC** | STM32H753 | DAC8568 | Out | 3.3V CMOS | GPIO (Static) | 10k pull-up | No | VERIFIED (Compatible) |
| **SPI1_CS_ADC** | STM32H753 | AD7606C-18 | Out | 3.3V CMOS | GPIO (Static) | 10k pull-up | No | VERIFIED (Compatible) |
| **ADC_CONVST** | STM32H753 | AD7606C-18 | Out | 3.3V CMOS | Timer triggered | None | No | VERIFIED (Compatible) |
| **ADC_BUSY** | AD7606C-18 | STM32H753 | In | 3.3V CMOS | Interrupt | None | No | VERIFIED (Compatible) |
| **USB_DM / DP** | PC (Host) | STM32H753 | Bi | 3.3V USB FS | 12 Mbps | Per USB spec | No | VERIFIED (Compatible) |
| **ANALOG_V_FB**| AMC1311 (Iso) | ADC1_INP0 (MCU) | In | 0 – 3V (Scaled) | 100 kHz BW | None | YES (AMC1311 provides 7kV peak isolation) | VERIFIED (Compatible) |
| **ANALOG_I_FB**| AD8429 (Amp) | ADC1_INP1 (MCU) | In | 0 – 3V (Scaled) | 100 kHz BW | None | No (Shunt on power ground; isolated downstream if needed) | VERIFIED (Compatible) |
| **FAULT_OC/SC**| LM393 Comp | 74HC14 / STM32 | In | 3.3V CMOS | Latched | 10k pull-up | No (Low-voltage fault bus) | VERIFIED (Compatible) |
| **PWM_V_H/L** | STM32 / FPGA | UCC21520 (Gate) | Out | 3.3V CMOS | 50 kHz PWM | 10k pull-down | YES (ISO7741 / UCC21520 internal isolation) | VERIFIED (Compatible) |
| **OSC_CLK** | SIT8008BI | FPGA / MCU | Out | 3.3V CMOS | 50 MHz | None | No | VERIFIED (Compatible) |

---

## 2. VOLTAGE-DOMAIN COMPATIBILITY & MISMATCH ANALYSIS

1. **Digital Logic Compatibility:**
   - All low-voltage digital ICs (STM32H753, Gowin FPGA, DAC8568, AD7606C-18, ISO7741, 74HC14) operate on **3.3V CMOS levels**.
   - Input high ($V_{IH}$) min ≈ 2.0V, input low ($V_{IL}$) max ≈ 0.8V. Output high ($V_{OH}$) min ≈ 2.4V, output low ($V_{OL}$) max ≈ 0.4V.
   - **Result:** Fully compatible; no level shifters needed within the low-voltage digital domain.

2. **Analog Input Compatibility:**
   - DAC8568 output: 0 to 5.0V (buffered with internal 2× gain from 2.5V reference).
   - ADC AD7606C-18 input range: Software-selectable (configured for ±5V or 0–5V).
   - AMC1311 isolated amplifier output: 0 to 2V nominal (differential output referenced to AGND).
   - AD8429 instrumentation amplifier output: 0 to 3.0V (referenced to AGND).
   - **Result:** All analog signals fall within ADC input ranges. Anti-aliasing RC filters required on all ADC inputs.

3. **Power Domain Isolation:**
   - Power stage gate drivers (UCC21520) are galvanically isolated from the 3.3V control domain using ISO7741 digital isolators and isolated power supplies (B0515S-2WR3).
   - Voltage feedback is isolated via AMC1311 (reinforced isolation barrier rated for high voltage).
   - **Result:** Strict separation between low-voltage control domain (DGND/AGND) and high-voltage power domains (V_HV_GND / I_HV_GND).
