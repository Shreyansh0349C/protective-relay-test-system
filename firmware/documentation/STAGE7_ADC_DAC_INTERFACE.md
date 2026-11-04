# STAGE 7 — ADC & DAC INTERFACE SPECIFICATION
## RELAYLAB X Phase 2

**Date:** 2026-11-05  
**Status:** DEFINED & SPECIFIED

---

## 1. ADC ACQUISITION ARCHITECTURE (AD7606C-18)

1. **Device:** AD7606C-18 (18-bit, 8-channel simultaneous sampling SAR ADC).
2. **Interface:** SPI / Parallel interface with STM32H753.
3. **Triggering:** Timer TIM6 triggers conversion start via `ADC_CONVST` (`PB10`) at 10 kSa/s.
4. **Data Ready:** `ADC_BUSY` (`PB11`) signals conversion completion; STM32 reads conversion results via DMA.
5. **Channels Used:**
   - Channel 1 (`ANALOG_V_FB`, `PA0`): Voltage feedback from AMC1311 isolated amplifier.
   - Channel 2 (`ANALOG_I_FB`, `PA1`): Current feedback from AD8429 instrumentation amplifier.
6. **Calibration & Conversion:**
   - Raw ADC code ($C_{raw}$) converted to physical voltage ($V_{meas}$) and current ($I_{meas}$) using linear calibration coefficients:
     $$V_{meas} = (C_{raw} \times K_v) + Offset_v$$
     $$I_{meas} = (C_{raw} \times K_i) + Offset_i$$
   - RMS calculation performed over $N = 200$ samples (1 full cycle at 50 Hz):
     $$RMS = \sqrt{\frac{1}{N} \sum_{n=0}^{N-1} x[n]^2}$$

---

## 2. DAC REFERENCE ARCHITECTURE (DAC8568)

1. **Device:** DAC8568SCPW (16-bit, octal-channel low-power voltage-output DAC).
2. **Interface:** SPI1 (`PA5` SCK, `PA7` MOSI, `PC5` CS).
3. **Role:** Generates reference control signals and analog setpoints for auxiliary control loops. PWM SPWM generation is handled directly by STM32 Timer TIM1.

---

**ADC/DAC Interface Status:** SPECIFIED
