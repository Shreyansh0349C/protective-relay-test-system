# STAGE 7 — PC INTEGRATION & WAVEFORM MONITORING
## RELAYLAB X Phase 2

**Date:** 2026-11-05  
**Status:** IMPLEMENTED & VERIFIED (Host Simulation Mode)

---

## 1. PC APPLICATION INTEGRATION

The existing PySide6 / PyQtGraph desktop application (`software/desktop-app/`) has been reviewed and integrated with the Stage 7 USB CDC protocol and host-simulation streaming capabilities.

1. **Live Waveform Display:**
   - Real-time plotting of voltage (`0–400 V RMS`) and current (`0–40 A RMS`) waveforms at 50 Hz.
   - Synchronized PyQtGraph oscilloscope view with trigger and timebase controls.

2. **Measurement Tiles & Telemetry:**
   - Live display of RMS voltage, RMS current, frequency (50 Hz fixed), peak values, and phase angle.
   - Fault status indicators (`FAULT_OC`, `FAULT_SC`, `FAULT_OV`, `FAULT_ESTOP`) with clear visual warnings.

3. **Connection & Streaming Management:**
   - Serial connection dialog supporting COM port auto-detection and manual selection.
   - Robust handling of USB disconnection, device reset, packet framing errors, and reconnection.
   - Clear labeling distinguishing **Hardware Live Measurements** from **Host Simulation Data** when physical hardware is not connected.

---

**PC Integration Status:** COMPLETED & TESTED
