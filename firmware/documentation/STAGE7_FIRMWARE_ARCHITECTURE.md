# STAGE 7 — FIRMWARE ARCHITECTURE
## RELAYLAB X Phase 2

**Date:** 2026-11-05  
**Target MCU:** STM32H753ZIT6 (Cortex-M7, 480 MHz)  
**Status:** DESIGNED & STRUCTURED — Modular firmware architecture specification.

---

## 1. FIRMWARE DIRECTORY STRUCTURE

The firmware project is organized into modular directories under `firmware/STM32H753/`:
```text
firmware/
├── README.md
└── STM32H753/
    ├── Core/
    │   ├── Inc/           # Main headers, system config, peripherals
    │   └── Src/           # System initialization, main loop, HAL stubs
    ├── Drivers/           # STM32H7xx HAL drivers & board support
    ├── USB/               # USB Device Library (CDC Class stack)
    ├── Control/           # SPWM generation, PI current control, waveform tables
    ├── Protection/        # Hardware fault monitoring & safe-state logic
    └── Diagnostics/       # Error logging, health monitoring, watchdog
```

---

## 2. PERIPHERAL ALLOCATION & CONFIGURATION

1. **Clock Tree (RCC):**
   - HSE: 8 MHz external crystal oscillator.
   - PLL1: Configured for 480 MHz SYSCLK, 240 MHz AHB clock, 120 MHz APB clocks.
   - USB PLL3: Configured for 48 MHz exact USB clock.

2. **Timers:**
   - **TIM1:** Advanced-control timer for H-bridge SPWM generation (Complementary outputs with dead-time insertion, 20 kHz switching frequency for voltage stage, 50 kHz for current stage).
   - **TIM6:** Basic timer configured for 10 kHz periodic trigger for ADC sampling and control loop execution.

3. **Analog Interfaces:**
   - **ADC1 / ADC2:** Synchronous sampling of AMC1311 voltage feedback (`PA0`) and AD8429 current feedback (`PA1`) via DMA.
   - **DAC8568:** 16-bit octal DAC interfaced via SPI1 for reference waveform generation or auxiliary analog control.

4. **Communication:**
   - **USB OTG HS / FS:** Configured as USB Communications Device Class (CDC) virtual COM port for bi-directional telemetry and command streaming at 115,200+ baud equivalent throughput.

5. **Fault Inputs (EXTI):**
   - **PE2 (`FAULT_OC`):** Overcurrent interrupt.
   - **PE3 (`FAULT_SC`):** Short-circuit interrupt.
   - **PE4 (`FAULT_OV`):** Overvoltage interrupt.
   - **PE5 (`FAULT_ESTOP`):** Emergency stop interrupt.

---

**Firmware Architecture Status:** DESIGNED  
**Next Action:** Implement USB CDC protocol specification and firmware module headers.
