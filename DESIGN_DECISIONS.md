# DESIGN DECISIONS — RELAYLAB X

This document records key engineering decisions, their rationale, and alternatives considered.

---

## DD-001: Desktop Application Framework
**Decision:** PySide6 + PyQtGraph + NumPy  
**Date:** 2024-11-04  
**Status:** Implemented (Phase 1)  
**Rationale:**
- PySide6 provides professional Qt-based GUI with native look
- PyQtGraph delivers high-performance real-time waveform rendering (critical for oscilloscope)
- NumPy enables efficient signal processing and RMS calculations
- Python allows rapid prototyping while maintaining scientific computing capability

**Alternatives Considered:**
- Electron + D3.js — rejected (too heavyweight, poor real-time performance)
- Tkinter + Matplotlib — rejected (poor aesthetics, slow rendering)
- C++ Qt — rejected for Phase 1 (too slow to prototype; may revisit for final product)

---

## DD-002: Simulation Mode Architecture
**Decision:** Separate simulation engine from communication layer; all simulated data explicitly labelled  
**Date:** 2024-11-04  
**Status:** Implemented (Phase 1)  
**Rationale:**
- Safety: Users can never mistake simulated data for real hardware measurements
- Testability: GUI and measurement engine can be validated without hardware
- Architecture: Clean separation allows swapping mock device for real serial communication

---

## DD-003: Communication Protocol — Placeholder
**Decision:** Abstract protocol interface with placeholder implementation  
**Date:** 2024-11-04  
**Status:** Placeholder (requires Phase 2 hardware definition)  
**Rationale:**
- Real protocol depends on STM32 firmware design and FPGA register map
- Placeholder allows full GUI testing without hardware
- Interface-based design (ProtocolHandler ABC) enables clean implementation swap

**Open Question:** Final packet format, checksum algorithm, and flow control TBD in Phase 2.

---

## DD-004: Measurement Methodology
**Decision:** True RMS from samples: `Vrms = sqrt(mean(v²))`; frequency from interpolated zero crossings  
**Date:** 2024-11-04  
**Status:** Implemented and tested  
**Rationale:**
- True RMS is correct for arbitrary waveforms (not just sinusoidal)
- Zero-crossing with linear interpolation gives sub-sample frequency accuracy
- Phase difference calculated from first positive-going zero crossings of V and I

---

## DD-005: Thread Architecture for Simulation
**Decision:** QThread + QMutex for background waveform generation at 30 fps  
**Date:** 2024-11-04  
**Status:** Implemented  
**Rationale:**
- Background thread prevents GUI blocking during continuous waveform generation
- 30 fps update rate provides smooth visual display without excessive CPU usage
- QMutex protects shared config state between GUI and worker threads

---

*Phase 2 design decisions will be added as hardware engineering progresses.*
