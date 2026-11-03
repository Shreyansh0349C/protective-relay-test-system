"""
RELAYLAB X — Application Settings Page

Manages user preferences, display options, and system configuration.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QCheckBox, QComboBox, QFrame, QGridLayout, QMessageBox
)
from app.ui.theme import Theme
from app.core.settings import SettingsManager


class ApplicationSettingsPage(QWidget):
    """Application settings and preferences page."""

    def __init__(self, settings_manager: SettingsManager, parent=None):
        super().__init__(parent)
        self._settings = settings_manager
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(20)

        # Title
        title = QLabel("APPLICATION SETTINGS")
        title.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; font-size: 20px; font-weight: 700; letter-spacing: 2px;")
        layout.addWidget(title)

        subtitle = QLabel("Configure display, simulation, and software preferences")
        subtitle.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(subtitle)

        # Settings card
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_MEDIUM};
                border: 1px solid {Theme.BORDER_DARK};
                border-radius: 8px;
            }}
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 16, 20, 20)
        card_layout.setSpacing(16)

        sec_title = QLabel("GENERAL PREFERENCES")
        sec_title.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        card_layout.addWidget(sec_title)

        grid = QGridLayout()
        grid.setSpacing(16)

        # Theme
        grid.addWidget(QLabel("Interface Theme"), 0, 0)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark Navy (Professional)", "Charcoal Dark"])
        grid.addWidget(self.theme_combo, 0, 1)

        # Fullscreen
        grid.addWidget(QLabel("Startup Display"), 1, 0)
        self.fullscreen_cb = QCheckBox("Start in Fullscreen Mode")
        self.fullscreen_cb.setChecked(True)
        grid.addWidget(self.fullscreen_cb, 1, 1)

        # Simulation mode
        grid.addWidget(QLabel("Execution Mode"), 2, 0)
        self.sim_mode_cb = QCheckBox("Force Simulation Mode (Phase 1 safety)")
        self.sim_mode_cb.setChecked(True)
        self.sim_mode_cb.setEnabled(False)
        grid.addWidget(self.sim_mode_cb, 2, 1)

        card_layout.addLayout(grid)
        layout.addWidget(card)

        # Buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.VOLTAGE_BLUE_GLOW};
                color: {Theme.TEXT_PRIMARY};
                border: 1px solid {Theme.VOLTAGE_BLUE};
                border-radius: 4px;
                padding: 8px 24px;
                font-weight: 700;
            }}
            QPushButton:hover {{
                background-color: {Theme.VOLTAGE_BLUE_DIM};
            }}
        """)
        self.save_btn.clicked.connect(self._save_settings)
        btn_layout.addWidget(self.save_btn)

        self.reset_btn = QPushButton("Reset to Defaults")
        self.reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.BG_LIGHT};
                color: {Theme.TEXT_SECONDARY};
                border: 1px solid {Theme.BORDER_LIGHT};
                border-radius: 4px;
                padding: 8px 24px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {Theme.BG_LIGHTER};
            }}
        """)
        self.reset_btn.clicked.connect(self._reset_settings)
        btn_layout.addWidget(self.reset_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        layout.addStretch()

    def _save_settings(self):
        self._settings.save()
        QMessageBox.information(self, "Settings Saved", "Application settings saved successfully.")

    def _reset_settings(self):
        self._settings.reset_to_defaults()
        QMessageBox.information(self, "Settings Reset", "Application settings reset to defaults.")
