"""
RELAYLAB X — Application Theme

Dark navy/charcoal professional instrumentation theme
with blue (voltage) and amber (current) accents.
"""


class Theme:
    """Centralised theme constants for the entire application."""

    # Primary background colours
    BG_DARKEST = "#0a0e17"       # Deepest background
    BG_DARK = "#0f1520"          # Main background
    BG_MEDIUM = "#151c2c"        # Panel background
    BG_LIGHT = "#1a2236"         # Card/elevated background
    BG_LIGHTER = "#1f2940"       # Hover/selected background

    # Borders
    BORDER_DARK = "#1e2a3e"
    BORDER_LIGHT = "#2a3a52"
    BORDER_ACCENT = "#334466"

    # Text colours
    TEXT_PRIMARY = "#e8edf5"
    TEXT_SECONDARY = "#8899b0"
    TEXT_DIM = "#556680"
    TEXT_MUTED = "#3d5070"

    # Accent colours
    VOLTAGE_BLUE = "#4d9fff"       # Channel 1 — Voltage
    VOLTAGE_BLUE_DIM = "#2a6bcc"
    VOLTAGE_BLUE_GLOW = "#1a4d99"
    CURRENT_AMBER = "#ffaa2d"      # Channel 2 — Current
    CURRENT_AMBER_DIM = "#cc8520"
    CURRENT_AMBER_GLOW = "#996318"

    # Status colours
    STATUS_OK = "#2dd47e"
    STATUS_WARNING = "#ffaa2d"
    STATUS_ERROR = "#ff4d5e"
    STATUS_INFO = "#4d9fff"

    # Oscilloscope
    GRID_LINE = "#1a2540"
    GRID_LINE_MAJOR = "#223050"
    SCOPE_BG = "#080c14"
    CURSOR_A = "#ff6b9d"
    CURSOR_B = "#7dffb3"

    # Navigation
    NAV_BG = "#0c1018"
    NAV_ACTIVE = "#1a2540"
    NAV_HOVER = "#141e30"
    NAV_INDICATOR = "#4d9fff"

    @classmethod
    def get_stylesheet(cls) -> str:
        """Return the complete application stylesheet."""
        return f"""
        /* ===== Global ===== */
        QMainWindow, QWidget {{
            background-color: {cls.BG_DARK};
            color: {cls.TEXT_PRIMARY};
            font-family: 'SF Mono', 'Menlo', 'Consolas', 'Liberation Mono', monospace;
            font-size: 12px;
        }}

        /* ===== Scroll bars ===== */
        QScrollBar:vertical {{
            background: {cls.BG_DARKEST};
            width: 8px;
            border: none;
        }}
        QScrollBar::handle:vertical {{
            background: {cls.BORDER_LIGHT};
            border-radius: 4px;
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background: {cls.BORDER_ACCENT};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        QScrollBar:horizontal {{
            background: {cls.BG_DARKEST};
            height: 8px;
            border: none;
        }}
        QScrollBar::handle:horizontal {{
            background: {cls.BORDER_LIGHT};
            border-radius: 4px;
            min-width: 20px;
        }}

        /* ===== Labels ===== */
        QLabel {{
            color: {cls.TEXT_PRIMARY};
            background: transparent;
            border: none;
        }}

        /* ===== Buttons ===== */
        QPushButton {{
            background-color: {cls.BG_LIGHT};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_LIGHT};
            border-radius: 4px;
            padding: 6px 16px;
            font-weight: 500;
            min-height: 28px;
        }}
        QPushButton:hover {{
            background-color: {cls.BG_LIGHTER};
            border-color: {cls.BORDER_ACCENT};
        }}
        QPushButton:pressed {{
            background-color: {cls.BORDER_LIGHT};
        }}
        QPushButton:disabled {{
            color: {cls.TEXT_DIM};
            border-color: {cls.BORDER_DARK};
        }}
        QPushButton[class="primary"] {{
            background-color: {cls.VOLTAGE_BLUE_GLOW};
            border-color: {cls.VOLTAGE_BLUE_DIM};
            color: {cls.TEXT_PRIMARY};
        }}
        QPushButton[class="primary"]:hover {{
            background-color: {cls.VOLTAGE_BLUE_DIM};
        }}
        QPushButton[class="danger"] {{
            background-color: #4d1a22;
            border-color: {cls.STATUS_ERROR};
            color: {cls.STATUS_ERROR};
        }}

        /* ===== Combo Box ===== */
        QComboBox {{
            background-color: {cls.BG_LIGHT};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_LIGHT};
            border-radius: 4px;
            padding: 4px 8px;
            min-height: 26px;
        }}
        QComboBox:hover {{
            border-color: {cls.BORDER_ACCENT};
        }}
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        QComboBox QAbstractItemView {{
            background-color: {cls.BG_MEDIUM};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_LIGHT};
            selection-background-color: {cls.BG_LIGHTER};
        }}

        /* ===== Spin Box ===== */
        QSpinBox, QDoubleSpinBox {{
            background-color: {cls.BG_LIGHT};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_LIGHT};
            border-radius: 4px;
            padding: 4px 8px;
            min-height: 26px;
        }}
        QSpinBox:hover, QDoubleSpinBox:hover {{
            border-color: {cls.BORDER_ACCENT};
        }}

        /* ===== Line Edit ===== */
        QLineEdit {{
            background-color: {cls.BG_LIGHT};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_LIGHT};
            border-radius: 4px;
            padding: 4px 8px;
            min-height: 26px;
        }}
        QLineEdit:focus {{
            border-color: {cls.VOLTAGE_BLUE};
        }}

        /* ===== Group Box ===== */
        QGroupBox {{
            color: {cls.TEXT_SECONDARY};
            border: 1px solid {cls.BORDER_DARK};
            border-radius: 6px;
            margin-top: 12px;
            padding-top: 16px;
            font-weight: 600;
            font-size: 11px;
            text-transform: uppercase;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 6px;
        }}

        /* ===== Slider ===== */
        QSlider::groove:horizontal {{
            background: {cls.BG_DARKEST};
            height: 4px;
            border-radius: 2px;
        }}
        QSlider::handle:horizontal {{
            background: {cls.VOLTAGE_BLUE};
            width: 14px;
            height: 14px;
            margin: -5px 0;
            border-radius: 7px;
        }}
        QSlider::handle:horizontal:hover {{
            background: {cls.VOLTAGE_BLUE_DIM};
        }}

        /* ===== Tab Widget ===== */
        QTabWidget::pane {{
            border: 1px solid {cls.BORDER_DARK};
            border-radius: 4px;
        }}
        QTabBar::tab {{
            background: {cls.BG_MEDIUM};
            color: {cls.TEXT_SECONDARY};
            border: 1px solid {cls.BORDER_DARK};
            padding: 8px 20px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }}
        QTabBar::tab:selected {{
            background: {cls.BG_LIGHT};
            color: {cls.TEXT_PRIMARY};
            border-bottom-color: {cls.BG_LIGHT};
        }}
        QTabBar::tab:hover {{
            background: {cls.BG_LIGHTER};
        }}

        /* ===== Check Box ===== */
        QCheckBox {{
            color: {cls.TEXT_PRIMARY};
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border: 1px solid {cls.BORDER_LIGHT};
            border-radius: 3px;
            background: {cls.BG_LIGHT};
        }}
        QCheckBox::indicator:checked {{
            background: {cls.VOLTAGE_BLUE};
            border-color: {cls.VOLTAGE_BLUE};
        }}

        /* ===== Tool Tip ===== */
        QToolTip {{
            background-color: {cls.BG_MEDIUM};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_LIGHT};
            padding: 4px 8px;
            border-radius: 4px;
        }}

        /* ===== Status Bar ===== */
        QStatusBar {{
            background-color: {cls.BG_DARKEST};
            color: {cls.TEXT_SECONDARY};
            border-top: 1px solid {cls.BORDER_DARK};
            font-size: 11px;
        }}

        /* ===== Splitter ===== */
        QSplitter::handle {{
            background: {cls.BORDER_DARK};
        }}
        QSplitter::handle:horizontal {{
            width: 2px;
        }}
        QSplitter::handle:vertical {{
            height: 2px;
        }}

        /* ===== Text Edit ===== */
        QTextEdit, QPlainTextEdit {{
            background-color: {cls.BG_DARKEST};
            color: {cls.TEXT_PRIMARY};
            border: 1px solid {cls.BORDER_DARK};
            border-radius: 4px;
            font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
            font-size: 11px;
        }}
        """
