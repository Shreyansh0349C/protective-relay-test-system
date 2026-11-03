"""
RELAYLAB X — Protective Relay Test Suite
Phase 1 Desktop Software Prototype

Technology Stack:
- Python 3.11+
- PySide6
- PyQtGraph
- NumPy
- PySerial

Usage:
    python main.py
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.ui.theme import Theme


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(Theme.get_stylesheet())

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
