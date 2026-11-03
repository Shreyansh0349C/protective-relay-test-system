# RELAYLAB X — Protective Relay Test Suite (Phase 1 Prototype)

Professional laboratory instrumentation software for protective relay testing, powered by Python, PySide6, PyQtGraph, and NumPy.

## System Overview & Hardware Context (Phase 1)
- **Controller:** STM32H753
- **DDS/DAC/ADC:** Gowin FPGA, DAC8568 (16-bit), AD7606C-18 (18-bit)
- **Channels:** 1x Voltage (0–400 V AC), 1x Current (0–40 A AC)
- **Frequency:** 50 Hz (fixed for Phase 1)
- **Mode:** **SIMULATION MODE** (Fully functional software prototype; does not energise physical hardware).

---

## Installation Instructions (macOS & Windows)

### 1. Prerequisites
Ensure Python 3.11 or later is installed:
```bash
python3 --version
```

### 2. Navigate to the Desktop App Directory
```bash
cd software/desktop-app
```

### 3. Create a Virtual Environment & Activate It
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  venv\Scripts\Activate.ps1
  ```

### 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Running the Application

With the virtual environment activated:
```bash
python main.py
```

---

## Running Automated Tests

To run the pytest suite for signal generation, simulation accuracy, and RMS calculations:
```bash
pytest tests/ -v
```

---

## Cross-Platform Packaging (PyInstaller & GitHub Actions)

RELAYLAB X includes automated cross-platform packaging via GitHub Actions and PyInstaller.

### Automated GitHub Actions Builds
Whenever code is pushed to `main` or a release tag (`v*`), GitHub Actions automatically:
1. Runs on `macos-latest` and `windows-latest`.
2. Executes the full test suite (`pytest`).
3. Builds standalone bundles using PyInstaller and `relaylab.spec`:
   - **macOS:** `RELAYLAB X.app` packaged into `RELAYLAB-X-macOS.zip`
   - **Windows:** `RELAYLAB-X.exe` folder packaged into `RELAYLAB-X-Windows.zip`
4. Uploads both zips as downloadable GitHub Actions artifacts.

### Local Packaging with PyInstaller
To build locally on your machine:
```bash
cd software/desktop-app
pip install pyinstaller
pyinstaller relaylab.spec
```
- Built deliverables will be found in `software/desktop-app/dist/`.
