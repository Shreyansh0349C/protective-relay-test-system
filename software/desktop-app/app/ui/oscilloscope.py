"""
RELAYLAB X — Oscilloscope Widget

High-performance waveform canvas using PyQtGraph.
Supports dual-channel display (voltage + current), measurement cursors,
trigger controls, and real-time acquisition.
"""

import numpy as np
import pyqtgraph as pg
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QPushButton, QComboBox, QDoubleSpinBox, QGroupBox,
    QGridLayout, QFrame, QSplitter, QSlider, QSizePolicy
)
from PySide6.QtGui import QFont, QColor
from app.ui.theme import Theme
from app.core.simulation import SimulationEngine
from app.core.measurements import MeasurementEngine, CursorMeasurement, MeasurementResult


class ReadoutLabel(QLabel):
    """Styled numeric readout label for instrument displays."""

    def __init__(self, value="---", unit="", color=Theme.TEXT_PRIMARY, parent=None):
        super().__init__(parent)
        self._value = value
        self._unit = unit
        self._color = color
        self._update_display()

    def set_value(self, value: str, unit: str = ""):
        self._value = value
        if unit:
            self._unit = unit
        self._update_display()

    def _update_display(self):
        self.setText(f"{self._value} {self._unit}")
        self.setStyleSheet(f"""
            color: {self._color};
            font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
            font-size: 16px;
            font-weight: 700;
            background: transparent;
            padding: 2px 4px;
        """)


class ChannelControl(QFrame):
    """Control panel for a single oscilloscope channel."""

    settings_changed = Signal()

    def __init__(self, channel_name: str, color: str, parent=None):
        super().__init__(parent)
        self._channel_name = channel_name
        self._color = color
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_MEDIUM};
                border: 1px solid {Theme.BORDER_DARK};
                border-radius: 6px;
                border-left: 3px solid {self._color};
            }}
        """)

        header = QHBoxLayout()
        self.enable_cb = QCheckBox(self._channel_name)
        self.enable_cb.setChecked(True)
        self.enable_cb.setStyleSheet(f"""
            QCheckBox {{
                color: {self._color};
                font-weight: 700;
                font-size: 12px;
            }}
            QCheckBox::indicator:checked {{
                background: {self._color};
                border-color: {self._color};
            }}
        """)
        self.enable_cb.toggled.connect(self.settings_changed.emit)
        header.addWidget(self.enable_cb)
        header.addStretch()

        self.rms_label = ReadoutLabel("---", "V" if "Voltage" in self._channel_name else "A", self._color)
        header.addWidget(self.rms_label)
        layout.addLayout(header)

        scale_layout = QHBoxLayout()
        scale_lbl = QLabel("Scale")
        scale_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px;")
        scale_layout.addWidget(scale_lbl)

        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.1, 500.0)
        self.scale_spin.setValue(100.0 if "Voltage" in self._channel_name else 5.0)
        self.scale_spin.setSuffix(" /div")
        self.scale_spin.setDecimals(1)
        self.scale_spin.setSingleStep(10.0 if "Voltage" in self._channel_name else 1.0)
        self.scale_spin.valueChanged.connect(self.settings_changed.emit)
        scale_layout.addWidget(self.scale_spin)
        layout.addLayout(scale_layout)

        offset_layout = QHBoxLayout()
        offset_lbl = QLabel("Offset")
        offset_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px;")
        offset_layout.addWidget(offset_lbl)

        self.offset_spin = QDoubleSpinBox()
        self.offset_spin.setRange(-500.0, 500.0)
        self.offset_spin.setValue(0.0)
        self.offset_spin.setSuffix(" V" if "Voltage" in self._channel_name else " A")
        self.offset_spin.setDecimals(1)
        self.offset_spin.setSingleStep(10.0 if "Voltage" in self._channel_name else 1.0)
        self.offset_spin.valueChanged.connect(self.settings_changed.emit)
        offset_layout.addWidget(self.offset_spin)
        layout.addLayout(offset_layout)

    @property
    def is_enabled(self) -> bool:
        return self.enable_cb.isChecked()

    @property
    def scale(self) -> float:
        return self.scale_spin.value()

    @property
    def offset(self) -> float:
        return self.offset_spin.value()


class OscilloscopeWidget(QWidget):
    """
    Main oscilloscope widget with waveform display, channel controls,
    trigger settings, and measurement cursors.
    """

    def __init__(self, simulation_engine: SimulationEngine, parent=None):
        super().__init__(parent)
        self._sim_engine = simulation_engine
        self._measurement_engine = MeasurementEngine()
        self._cursor_measurement = CursorMeasurement()

        self._display_samples = 2000
        self._time_data = np.array([])
        self._voltage_data = np.array([])
        self._current_data = np.array([])

        self._running = False
        self._paused = False
        self._single_shot = False
        self._single_captured = False
        self._acquisition_mode = "normal"
        self._avg_buffer_v = []
        self._avg_buffer_i = []
        self._avg_count = 0
        self._peak_max_v = None
        self._peak_min_v = None
        self._peak_max_i = None
        self._peak_min_i = None

        self._trigger_source = "CH1"
        self._trigger_edge = "rising"
        self._trigger_level = 0.0
        self._trigger_mode = "auto"
        self._triggered = False

        self._setup_ui()
        self._connect_signals()

        self._measure_timer = QTimer(self)
        self._measure_timer.timeout.connect(self._update_measurements)
        self._measure_timer.setInterval(200)
        self._measure_timer.start()

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        controls_widget = QWidget()
        controls_widget.setFixedWidth(260)
        controls_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {Theme.BG_DARKEST};
                border-right: 1px solid {Theme.BORDER_DARK};
            }}
        """)
        controls_layout = QVBoxLayout(controls_widget)
        controls_layout.setContentsMargins(8, 8, 8, 8)
        controls_layout.setSpacing(8)

        acq_frame = QFrame()
        acq_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_MEDIUM};
                border: 1px solid {Theme.BORDER_DARK};
                border-radius: 6px;
            }}
        """)
        acq_layout = QVBoxLayout(acq_frame)
        acq_layout.setContentsMargins(8, 6, 8, 6)
        acq_layout.setSpacing(4)

        acq_title = QLabel("ACQUISITION")
        acq_title.setStyleSheet(f"""
            color: {Theme.TEXT_SECONDARY};
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 1px;
        """)
        acq_layout.addWidget(acq_title)

        btn_row1 = QHBoxLayout()
        self.run_btn = QPushButton("▶ Run")
        self.run_btn.setStyleSheet(self._acq_btn_style(Theme.STATUS_OK))
        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.setStyleSheet(self._acq_btn_style(Theme.STATUS_WARNING))
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setStyleSheet(self._acq_btn_style(Theme.STATUS_ERROR))
        btn_row1.addWidget(self.run_btn)
        btn_row1.addWidget(self.pause_btn)
        btn_row1.addWidget(self.stop_btn)
        acq_layout.addLayout(btn_row1)

        btn_row2 = QHBoxLayout()
        self.single_btn = QPushButton("Single")
        self.single_btn.setStyleSheet(self._acq_btn_style(Theme.STATUS_INFO))
        btn_row2.addWidget(self.single_btn)

        mode_lbl = QLabel("Mode")
        mode_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px;")
        btn_row2.addWidget(mode_lbl)
        self.acq_mode_combo = QComboBox()
        self.acq_mode_combo.addItems(["Normal", "Average", "Peak Detect"])
        btn_row2.addWidget(self.acq_mode_combo)
        acq_layout.addLayout(btn_row2)

        controls_layout.addWidget(acq_frame)

        self.ch1_ctrl = ChannelControl("CH1 — Voltage", Theme.VOLTAGE_BLUE)
        self.ch2_ctrl = ChannelControl("CH2 — Current", Theme.CURRENT_AMBER)
        controls_layout.addWidget(self.ch1_ctrl)
        controls_layout.addWidget(self.ch2_ctrl)

        h_frame = QFrame()
        h_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_MEDIUM};
                border: 1px solid {Theme.BORDER_DARK};
                border-radius: 6px;
            }}
        """)
        h_layout = QVBoxLayout(h_frame)
        h_layout.setContentsMargins(8, 6, 8, 6)
        h_layout.setSpacing(4)

        h_title = QLabel("HORIZONTAL")
        h_title.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        h_layout.addWidget(h_title)

        tb_row = QHBoxLayout()
        tb_lbl = QLabel("Time/div")
        tb_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px;")
        tb_row.addWidget(tb_lbl)
        self.timebase_spin = QDoubleSpinBox()
        self.timebase_spin.setRange(0.1, 100.0)
        self.timebase_spin.setValue(5.0)
        self.timebase_spin.setSuffix(" ms")
        self.timebase_spin.setDecimals(1)
        self.timebase_spin.setSingleStep(1.0)
        tb_row.addWidget(self.timebase_spin)
        h_layout.addLayout(tb_row)

        zoom_row = QHBoxLayout()
        self.zoom_in_btn = QPushButton("🔍+")
        self.zoom_out_btn = QPushButton("🔍−")
        self.zoom_in_btn.setFixedWidth(50)
        self.zoom_out_btn.setFixedWidth(50)
        zoom_row.addWidget(self.zoom_in_btn)
        zoom_row.addWidget(self.zoom_out_btn)
        zoom_row.addStretch()
        h_layout.addLayout(zoom_row)

        controls_layout.addWidget(h_frame)

        trig_frame = QFrame()
        trig_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_MEDIUM};
                border: 1px solid {Theme.BORDER_DARK};
                border-radius: 6px;
            }}
        """)
        trig_layout = QVBoxLayout(trig_frame)
        trig_layout.setContentsMargins(8, 6, 8, 6)
        trig_layout.setSpacing(4)

        trig_title = QLabel("TRIGGER")
        trig_title.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        trig_layout.addWidget(trig_title)

        src_row = QHBoxLayout()
        src_lbl = QLabel("Source")
        src_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px;")
        src_row.addWidget(src_lbl)
        self.trigger_source_combo = QComboBox()
        self.trigger_source_combo.addItems(["CH1", "CH2"])
        src_row.addWidget(self.trigger_source_combo)
        trig_layout.addLayout(src_row)

        edge_row = QHBoxLayout()
        edge_lbl = QLabel("Edge")
        edge_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px;")
        edge_row.addWidget(edge_lbl)
        self.trigger_edge_combo = QComboBox()
        self.trigger_edge_combo.addItems(["Rising ↑", "Falling ↓"])
        edge_row.addWidget(self.trigger_edge_combo)
        trig_layout.addLayout(edge_row)

        lvl_row = QHBoxLayout()
        lvl_lbl = QLabel("Level")
        lvl_lbl.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px;")
        lvl_row.addWidget(lvl_lbl)
        self.trigger_level_spin = QDoubleSpinBox()
        self.trigger_level_spin.setRange(-500.0, 500.0)
        self.trigger_level_spin.setValue(0.0)
        self.trigger_level_spin.setDecimals(1)
        lvl_row.addWidget(self.trigger_level_spin)
        trig_layout.addLayout(lvl_row)

        mode_row = QHBoxLayout()
        mode_lbl2 = QLabel("Mode")
        mode_lbl2.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px;")
        mode_row.addWidget(mode_lbl2)
        self.trigger_mode_combo = QComboBox()
        self.trigger_mode_combo.addItems(["Auto", "Normal", "Single"])
        mode_row.addWidget(self.trigger_mode_combo)
        trig_layout.addLayout(mode_row)

        controls_layout.addWidget(trig_frame)

        cursor_frame = QFrame()
        cursor_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_MEDIUM};
                border: 1px solid {Theme.BORDER_DARK};
                border-radius: 6px;
            }}
        """)
        cursor_layout = QVBoxLayout(cursor_frame)
        cursor_layout.setContentsMargins(8, 6, 8, 6)
        cursor_layout.setSpacing(4)

        cursor_title = QLabel("CURSORS")
        cursor_title.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px; font-weight: 700; letter-spacing: 1px;")
        cursor_layout.addWidget(cursor_title)

        self.cursor_a_cb = QCheckBox("Cursor A")
        self.cursor_a_cb.setStyleSheet(f"QCheckBox {{ color: {Theme.CURSOR_A}; }}"
                                       f"QCheckBox::indicator:checked {{ background: {Theme.CURSOR_A}; border-color: {Theme.CURSOR_A}; }}")
        cursor_layout.addWidget(self.cursor_a_cb)

        self.cursor_b_cb = QCheckBox("Cursor B")
        self.cursor_b_cb.setStyleSheet(f"QCheckBox {{ color: {Theme.CURSOR_B}; }}"
                                       f"QCheckBox::indicator:checked {{ background: {Theme.CURSOR_B}; border-color: {Theme.CURSOR_B}; }}")
        cursor_layout.addWidget(self.cursor_b_cb)

        self.cursor_info = QLabel("Δt: ---    1/Δt: ---")
        self.cursor_info.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px; font-family: 'SF Mono', monospace;")
        cursor_layout.addWidget(self.cursor_info)

        controls_layout.addWidget(cursor_frame)
        controls_layout.addStretch()

        main_layout.addWidget(controls_widget)

        centre_widget = QWidget()
        centre_layout = QVBoxLayout(centre_widget)
        centre_layout.setContentsMargins(0, 0, 0, 0)
        centre_layout.setSpacing(0)

        self._meas_bar = self._create_measurement_bar()
        centre_layout.addWidget(self._meas_bar)

        self._setup_plot()
        centre_layout.addWidget(self._plot_widget, stretch=1)

        self._status_bar = self._create_status_bar()
        centre_layout.addWidget(self._status_bar)

        main_layout.addWidget(centre_widget, stretch=1)

    def _acq_btn_style(self, color: str) -> str:
        return f"""
            QPushButton {{
                background-color: {Theme.BG_LIGHT};
                color: {color};
                border: 1px solid {color}40;
                border-radius: 4px;
                padding: 4px 8px;
                font-weight: 700;
                font-size: 11px;
                min-height: 26px;
            }}
            QPushButton:hover {{
                background-color: {color}20;
                border-color: {color};
            }}
            QPushButton:pressed {{
                background-color: {color}40;
            }}
        """

    def _create_measurement_bar(self) -> QFrame:
        bar = QFrame()
        bar.setFixedHeight(52)
        bar.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_DARKEST};
                border-bottom: 1px solid {Theme.BORDER_DARK};
            }}
        """)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 4, 16, 4)
        layout.setSpacing(24)

        v_group = QVBoxLayout()
        v_label = QLabel("V RMS")
        v_label.setStyleSheet(f"color: {Theme.VOLTAGE_BLUE}; font-size: 9px; font-weight: 700; letter-spacing: 1px;")
        self.vrms_readout = ReadoutLabel("---", "V", Theme.VOLTAGE_BLUE)
        v_group.addWidget(v_label)
        v_group.addWidget(self.vrms_readout)
        layout.addLayout(v_group)

        i_group = QVBoxLayout()
        i_label = QLabel("I RMS")
        i_label.setStyleSheet(f"color: {Theme.CURRENT_AMBER}; font-size: 9px; font-weight: 700; letter-spacing: 1px;")
        self.irms_readout = ReadoutLabel("---", "A", Theme.CURRENT_AMBER)
        i_group.addWidget(i_label)
        i_group.addWidget(self.irms_readout)
        layout.addLayout(i_group)

        f_group = QVBoxLayout()
        f_label = QLabel("FREQ")
        f_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 9px; font-weight: 700; letter-spacing: 1px;")
        self.freq_readout = ReadoutLabel("---", "Hz", Theme.TEXT_PRIMARY)
        f_group.addWidget(f_label)
        f_group.addWidget(self.freq_readout)
        layout.addLayout(f_group)

        p_group = QVBoxLayout()
        p_label = QLabel("PHASE")
        p_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 9px; font-weight: 700; letter-spacing: 1px;")
        self.phase_readout = ReadoutLabel("---", "°", Theme.TEXT_PRIMARY)
        p_group.addWidget(p_label)
        p_group.addWidget(self.phase_readout)
        layout.addLayout(p_group)

        vp_group = QVBoxLayout()
        vp_label = QLabel("V PEAK")
        vp_label.setStyleSheet(f"color: {Theme.VOLTAGE_BLUE_DIM}; font-size: 9px; font-weight: 700; letter-spacing: 1px;")
        self.vpeak_readout = ReadoutLabel("---", "V", Theme.VOLTAGE_BLUE_DIM)
        vp_group.addWidget(vp_label)
        vp_group.addWidget(self.vpeak_readout)
        layout.addLayout(vp_group)

        ip_group = QVBoxLayout()
        ip_label = QLabel("I PEAK")
        ip_label.setStyleSheet(f"color: {Theme.CURRENT_AMBER_DIM}; font-size: 9px; font-weight: 700; letter-spacing: 1px;")
        self.ipeak_readout = ReadoutLabel("---", "A", Theme.CURRENT_AMBER_DIM)
        ip_group.addWidget(ip_label)
        ip_group.addWidget(self.ipeak_readout)
        layout.addLayout(ip_group)

        layout.addStretch()
        return bar

    def _create_status_bar(self) -> QFrame:
        bar = QFrame()
        bar.setFixedHeight(28)
        bar.setStyleSheet(f"""
            QFrame {{
                background-color: {Theme.BG_DARKEST};
                border-top: 1px solid {Theme.BORDER_DARK};
            }}
        """)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(16)

        self.status_label = QLabel("STOPPED")
        self.status_label.setStyleSheet(f"color: {Theme.TEXT_DIM}; font-size: 10px; font-weight: 600;")
        layout.addWidget(self.status_label)

        self.sim_label = QLabel("⚡ SIMULATION MODE")
        self.sim_label.setStyleSheet(f"color: {Theme.STATUS_WARNING}; font-size: 10px; font-weight: 600;")
        layout.addWidget(self.sim_label)

        layout.addStretch()

        self.trigger_status_label = QLabel("Trigger: Auto")
        self.trigger_status_label.setStyleSheet(f"color: {Theme.TEXT_DIM}; font-size: 10px;")
        layout.addWidget(self.trigger_status_label)

        self.timebase_label = QLabel("5.0 ms/div")
        self.timebase_label.setStyleSheet(f"color: {Theme.TEXT_SECONDARY}; font-size: 10px;")
        layout.addWidget(self.timebase_label)

        return bar

    def _setup_plot(self):
        pg.setConfigOptions(
            antialias=True,
            useOpenGL=False,
            background=QColor(Theme.SCOPE_BG),
            foreground=QColor(Theme.TEXT_DIM)
        )

        self._plot_widget = pg.PlotWidget()
        self._plot_widget.setBackground(QColor(Theme.SCOPE_BG))
        self._plot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self._plot = self._plot_widget.getPlotItem()
        self._plot.setLabel("bottom", "Time", units="s")
        self._plot.setLabel("left", "")
        self._plot.showGrid(x=True, y=True, alpha=0.15)
        self._plot.setXRange(0, 0.040, padding=0.02)
        self._plot.setYRange(-400, 400, padding=0.05)

        for axis_name in ("bottom", "left"):
            axis = self._plot.getAxis(axis_name)
            axis.setPen(pg.mkPen(color=Theme.BORDER_LIGHT, width=1))
            axis.setTextPen(pg.mkPen(color=Theme.TEXT_DIM))
            axis.setStyle(tickFont=QFont("SF Mono", 9))

        self._voltage_curve = self._plot.plot(
            pen=pg.mkPen(color=Theme.VOLTAGE_BLUE, width=2),
            name="CH1 Voltage"
        )
        self._current_curve = self._plot.plot(
            pen=pg.mkPen(color=Theme.CURRENT_AMBER, width=2),
            name="CH2 Current"
        )

        self._trigger_line = pg.InfiniteLine(
            pos=0,
            angle=0,
            pen=pg.mkPen(color="#ff4d5e", width=1, style=Qt.DashLine),
            movable=True,
            label="Trig",
            labelOpts={"color": Theme.STATUS_ERROR, "position": 0.98}
        )
        self._trigger_line.sigPositionChanged.connect(self._on_trigger_line_moved)
        self._plot.addItem(self._trigger_line)

        self._cursor_a_line = pg.InfiniteLine(
            pos=0.010,
            angle=90,
            pen=pg.mkPen(color=Theme.CURSOR_A, width=1, style=Qt.DashLine),
            movable=True,
            label="A",
            labelOpts={"color": Theme.CURSOR_A, "position": 0.95}
        )
        self._cursor_b_line = pg.InfiniteLine(
            pos=0.030,
            angle=90,
            pen=pg.mkPen(color=Theme.CURSOR_B, width=1, style=Qt.DashLine),
            movable=True,
            label="B",
            labelOpts={"color": Theme.CURSOR_B, "position": 0.95}
        )
        self._cursor_a_line.sigPositionChanged.connect(self._on_cursor_moved)
        self._cursor_b_line.sigPositionChanged.connect(self._on_cursor_moved)
        self._cursor_a_line.setVisible(False)
        self._cursor_b_line.setVisible(False)

        self._plot.addItem(self._cursor_a_line)
        self._plot.addItem(self._cursor_b_line)

    def _connect_signals(self):
        self.run_btn.clicked.connect(self._on_run)
        self.pause_btn.clicked.connect(self._on_pause)
        self.stop_btn.clicked.connect(self._on_stop)
        self.single_btn.clicked.connect(self._on_single)
        self.acq_mode_combo.currentTextChanged.connect(self._on_acq_mode_changed)

        self.timebase_spin.valueChanged.connect(self._on_timebase_changed)
        self.zoom_in_btn.clicked.connect(self._on_zoom_in)
        self.zoom_out_btn.clicked.connect(self._on_zoom_out)

        self.trigger_source_combo.currentTextChanged.connect(self._on_trigger_source_changed)
        self.trigger_edge_combo.currentTextChanged.connect(self._on_trigger_edge_changed)
        self.trigger_level_spin.valueChanged.connect(self._on_trigger_level_changed)
        self.trigger_mode_combo.currentTextChanged.connect(self._on_trigger_mode_changed)

        self.cursor_a_cb.toggled.connect(self._on_cursor_a_toggled)
        self.cursor_b_cb.toggled.connect(self._on_cursor_b_toggled)

        self.ch1_ctrl.settings_changed.connect(self._on_channel_settings_changed)
        self.ch2_ctrl.settings_changed.connect(self._on_channel_settings_changed)

        self._sim_engine.data_ready.connect(self._on_data_received)
        self._sim_engine.status_changed.connect(self._on_status_changed)

    def _on_data_received(self, time_data: np.ndarray, voltage: np.ndarray, current: np.ndarray):
        if self._paused:
            return
        if self._single_shot and self._single_captured:
            return

        if self._trigger_mode != "auto":
            if not self._check_trigger(voltage if self._trigger_source == "CH1" else current):
                if self._trigger_mode == "normal":
                    return
                if self._trigger_mode == "single":
                    return

        self._time_data = np.concatenate([self._time_data, time_data])
        self._voltage_data = np.concatenate([self._voltage_data, voltage])
        self._current_data = np.concatenate([self._current_data, current])

        max_samples = self._display_samples * 4
        if len(self._time_data) > max_samples:
            self._time_data = self._time_data[-max_samples:]
            self._voltage_data = self._voltage_data[-max_samples:]
            self._current_data = self._current_data[-max_samples:]

        display_v, display_i = self._process_acquisition_mode(
            self._voltage_data, self._current_data
        )

        self._measurement_engine.update_data(time_data, voltage, current)
        self._update_plot(display_v, display_i)

        if self._single_shot:
            self._single_captured = True
            self._sim_engine.stop()
            self.status_label.setText("SINGLE CAPTURED")
            self.status_label.setStyleSheet(f"color: {Theme.STATUS_INFO}; font-size: 10px; font-weight: 600;")

    def _check_trigger(self, signal: np.ndarray) -> bool:
        if len(signal) < 2:
            return False
        level = self._trigger_level
        for i in range(1, len(signal)):
            if self._trigger_edge == "rising":
                if signal[i - 1] <= level < signal[i]:
                    return True
            else:
                if signal[i - 1] >= level > signal[i]:
                    return True
        return False

    def _process_acquisition_mode(self, voltage: np.ndarray, current: np.ndarray):
        if self._acquisition_mode == "average":
            self._avg_buffer_v.append(voltage.copy())
            self._avg_buffer_i.append(current.copy())
            self._avg_count += 1
            if len(self._avg_buffer_v) > 8:
                self._avg_buffer_v.pop(0)
                self._avg_buffer_i.pop(0)
            min_len = min(len(b) for b in self._avg_buffer_v)
            if min_len > 0:
                avg_v = np.mean([b[:min_len] for b in self._avg_buffer_v], axis=0)
                avg_i = np.mean([b[:min_len] for b in self._avg_buffer_i], axis=0)
                return avg_v, avg_i
            return voltage, current

        elif self._acquisition_mode == "peak_detect":
            if self._peak_max_v is None or len(self._peak_max_v) != len(voltage):
                self._peak_max_v = voltage.copy()
                self._peak_min_v = voltage.copy()
                self._peak_max_i = current.copy()
                self._peak_min_i = current.copy()
            else:
                self._peak_max_v = np.maximum(self._peak_max_v, voltage)
                self._peak_min_v = np.minimum(self._peak_min_v, voltage)
                self._peak_max_i = np.maximum(self._peak_max_i, current)
                self._peak_min_i = np.minimum(self._peak_min_i, current)
            return self._peak_max_v, self._peak_max_i

        return voltage, current

    def _update_plot(self, voltage: np.ndarray, current: np.ndarray):
        if len(self._time_data) == 0:
            return

        t = self._time_data
        v_offset = self.ch1_ctrl.offset
        i_offset = self.ch2_ctrl.offset

        if self.ch1_ctrl.is_enabled and len(voltage) == len(t):
            self._voltage_curve.setData(t, voltage + v_offset)
            self._voltage_curve.setVisible(True)
        else:
            self._voltage_curve.setVisible(False)

        if self.ch2_ctrl.is_enabled and len(current) == len(t):
            v_scale = self.ch1_ctrl.scale if self.ch1_ctrl.scale > 0 else 100.0
            i_scale = self.ch2_ctrl.scale if self.ch2_ctrl.scale > 0 else 5.0
            scale_factor = v_scale / i_scale
            self._current_curve.setData(t, current * scale_factor + i_offset)
            self._current_curve.setVisible(True)
        else:
            self._current_curve.setVisible(False)

        timebase_ms = self.timebase_spin.value()
        total_time = timebase_ms * 10 / 1000.0
        if len(t) > 1:
            t_end = t[-1]
            t_start = max(t[0], t_end - total_time)
            self._plot.setXRange(t_start, t_end, padding=0)

    def _update_measurements(self):
        if not self._running and not self._single_captured:
            return

        result = self._measurement_engine.compute()
        if not result.is_valid:
            return

        self.vrms_readout.set_value(f"{result.voltage_rms:.1f}", "V")
        self.irms_readout.set_value(f"{result.current_rms:.2f}", "A")
        self.freq_readout.set_value(f"{result.frequency:.1f}", "Hz")
        self.phase_readout.set_value(f"{result.phase_difference:.1f}", "°")
        self.vpeak_readout.set_value(f"{result.voltage_peak:.1f}", "V")
        self.ipeak_readout.set_value(f"{result.current_peak:.2f}", "A")

        self.ch1_ctrl.rms_label.set_value(f"{result.voltage_rms:.1f}", "Vrms")
        self.ch2_ctrl.rms_label.set_value(f"{result.current_rms:.2f}", "Arms")
        self._update_cursor_info()

    def _update_cursor_info(self):
        if not self.cursor_a_cb.isChecked() and not self.cursor_b_cb.isChecked():
            self.cursor_info.setText("Δt: ---    1/Δt: ---")
            return

        a_pos = self._cursor_a_line.value()
        b_pos = self._cursor_b_line.value()
        self._cursor_measurement.cursor_a_time = a_pos
        self._cursor_measurement.cursor_b_time = b_pos

        dt = self._cursor_measurement.delta_time
        freq = self._cursor_measurement.frequency

        dt_str = f"{dt * 1000:.2f} ms" if dt > 0 else "---"
        freq_str = f"{freq:.1f} Hz" if freq else "---"

        info_parts = [f"A: {a_pos * 1000:.2f} ms"]
        if self.cursor_b_cb.isChecked():
            info_parts.append(f"B: {b_pos * 1000:.2f} ms")
            info_parts.append(f"Δt: {dt_str}")
            info_parts.append(f"1/Δt: {freq_str}")

        self.cursor_info.setText("  ".join(info_parts))

    def _on_run(self):
        self._running = True
        self._paused = False
        self._single_shot = False
        self._single_captured = False
        self._reset_acq_buffers()
        self._sim_engine.start()
        self.status_label.setText("▶ RUNNING")
        self.status_label.setStyleSheet(f"color: {Theme.STATUS_OK}; font-size: 10px; font-weight: 600;")

    def _on_pause(self):
        if self._running:
            self._paused = not self._paused
            if self._paused:
                self.status_label.setText("⏸ PAUSED")
                self.status_label.setStyleSheet(f"color: {Theme.STATUS_WARNING}; font-size: 10px; font-weight: 600;")
            else:
                self.status_label.setText("▶ RUNNING")
                self.status_label.setStyleSheet(f"color: {Theme.STATUS_OK}; font-size: 10px; font-weight: 600;")

    def _on_stop(self):
        self._running = False
        self._paused = False
        self._single_shot = False
        self._sim_engine.stop()
        self.status_label.setText("⏹ STOPPED")
        self.status_label.setStyleSheet(f"color: {Theme.TEXT_DIM}; font-size: 10px; font-weight: 600;")

    def _on_single(self):
        self._running = True
        self._paused = False
        self._single_shot = True
        self._single_captured = False
        self._reset_acq_buffers()
        self._clear_waveform_data()
        self._sim_engine.start()
        self.status_label.setText("⏳ WAITING FOR TRIGGER")
        self.status_label.setStyleSheet(f"color: {Theme.STATUS_INFO}; font-size: 10px; font-weight: 600;")

    def _on_acq_mode_changed(self, text: str):
        mode_map = {"Normal": "normal", "Average": "average", "Peak Detect": "peak_detect"}
        self._acquisition_mode = mode_map.get(text, "normal")
        self._reset_acq_buffers()

    def _reset_acq_buffers(self):
        self._avg_buffer_v = []
        self._avg_buffer_i = []
        self._avg_count = 0
        self._peak_max_v = None
        self._peak_min_v = None
        self._peak_max_i = None
        self._peak_min_i = None

    def _clear_waveform_data(self):
        self._time_data = np.array([])
        self._voltage_data = np.array([])
        self._current_data = np.array([])
        self._measurement_engine.reset()

    def _on_timebase_changed(self, value):
        self.timebase_label.setText(f"{value:.1f} ms/div")

    def _on_zoom_in(self):
        current = self.timebase_spin.value()
        self.timebase_spin.setValue(max(0.1, current / 2))

    def _on_zoom_out(self):
        current = self.timebase_spin.value()
        self.timebase_spin.setValue(min(100.0, current * 2))

    def _on_trigger_source_changed(self, text):
        self._trigger_source = text
        self.trigger_status_label.setText(f"Trigger: {self._trigger_mode.title()} ({text})")

    def _on_trigger_edge_changed(self, text):
        self._trigger_edge = "rising" if "Rising" in text else "falling"

    def _on_trigger_level_changed(self, value):
        self._trigger_level = value
        self._trigger_line.setValue(value)

    def _on_trigger_line_moved(self, line):
        self._trigger_level = line.value()
        self.trigger_level_spin.blockSignals(True)
        self.trigger_level_spin.setValue(self._trigger_level)
        self.trigger_level_spin.blockSignals(False)

    def _on_trigger_mode_changed(self, text):
        mode_map = {"Auto": "auto", "Normal": "normal", "Single": "single"}
        self._trigger_mode = mode_map.get(text, "auto")
        self.trigger_status_label.setText(f"Trigger: {text} ({self._trigger_source})")

    def _on_cursor_a_toggled(self, checked):
        self._cursor_a_line.setVisible(checked)
        self._cursor_measurement.cursor_a_enabled = checked

    def _on_cursor_b_toggled(self, checked):
        self._cursor_b_line.setVisible(checked)
        self._cursor_measurement.cursor_b_enabled = checked

    def _on_cursor_moved(self):
        self._update_cursor_info()

    def _on_channel_settings_changed(self):
        self._sim_engine.config.voltage_enabled = self.ch1_ctrl.is_enabled
        self._sim_engine.config.current_enabled = self.ch2_ctrl.is_enabled

    def _on_status_changed(self, status: str):
        self.status_label.setText(status)

    def get_measurement_result(self) -> MeasurementResult:
        return self._measurement_engine.compute()
