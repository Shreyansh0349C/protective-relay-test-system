"""
RELAYLAB X — Event History Page

Displays application events, test logs, and fault records.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame
)
from PySide6.QtGui import QColor
from datetime import datetime
from app.ui.theme import Theme


class EventHistoryPage(QWidget):
    """Event history and audit log page."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._events = []
        self._setup_ui()
        self.log_event("SYSTEM", "RELAYLAB X initialized in simulation mode")
        self.log_event("CONFIG", "Default test parameters loaded (230V, 10A, 50Hz)")
        self.log_event("COMM", "Mock serial communication manager started")

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 24, 32, 24)
        layout.setSpacing(20)

        # Title
        title = QLabel("EVENT HISTORY")
        title.setStyleSheet(f"color: {Theme.TEXT_PRIMARY}; font-size: 20px; font-weight: 700; letter-spacing: 2px;")
        layout.addWidget(title)

        subtitle = QLabel("Chronological log of system events, test runs, and faults")
        subtitle.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 13px;")
        layout.addWidget(subtitle)

        # Toolbar
        toolbar = QHBoxLayout()
        self.clear_btn = QPushButton("Clear Log")
        self.clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Theme.BG_LIGHT};
                color: {Theme.TEXT_SECONDARY};
                border: 1px solid {Theme.BORDER_LIGHT};
                border-radius: 4px;
                padding: 6px 16px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {Theme.BG_LIGHTER};
            }}
        """)
        self.clear_btn.clicked.connect(self.clear_events)
        toolbar.addWidget(self.clear_btn)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        # Event Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Category", "Event Description"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {Theme.BG_MEDIUM};
                border: 1px solid {Theme.BORDER_DARK};
                border-radius: 8px;
                gridline-color: {Theme.BORDER_DARK};
                font-family: 'SF Mono', monospace;
                font-size: 11px;
            }}
            QHeaderView::section {{
                background-color: {Theme.BG_DARKEST};
                color: {Theme.TEXT_SECONDARY};
                padding: 8px;
                border: none;
                border-bottom: 1px solid {Theme.BORDER_DARK};
                font-weight: 700;
            }}
            QTableWidget::item {{
                padding: 6px;
                border-bottom: 1px solid {Theme.BORDER_DARK};
            }}
        """)
        layout.addWidget(self.table)

        layout.addStretch()

    def log_event(self, category: str, description: str):
        """Add an event to the history log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        self._events.append((timestamp, category, description))

        row = self.table.rowCount()
        self.table.insertRow(row)

        item_time = QTableWidgetItem(timestamp)
        item_cat = QTableWidgetItem(category)
        item_desc = QTableWidgetItem(description)

        for item in (item_time, item_cat, item_desc):
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)

        if category == "FAULT":
            item_cat.setForeground(QColor(Theme.STATUS_ERROR))
        elif category == "WARNING":
            item_cat.setForeground(QColor(Theme.STATUS_WARNING))
        else:
            item_cat.setForeground(QColor(Theme.TEXT_SECONDARY))

        self.table.setItem(row, 0, item_time)
        self.table.setItem(row, 1, item_cat)
        self.table.setItem(row, 2, item_desc)
        self.table.scrollToBottom()

    def clear_events(self):
        self._events.clear()
        self.table.setRowCount(0)
