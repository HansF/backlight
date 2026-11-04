#!/usr/bin/env python3
# Copyright (C) 2026 HansF
# Licensed under the GNU GPL v3 or later. See LICENSE.
"""
Backlight - Multi-display backlight control
Direct approach: create windows on each physical display
"""

import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,
    QSlider, QLabel, QPushButton, QFrame, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal, QRect
from PyQt5.QtGui import QColor, QFont
from colorsys import hsv_to_rgb


class BacklightWindow(QWidget):
    """Fullscreen backlight on one QScreen"""

    def __init__(self, screen):
        super().__init__()
        self.display_name = screen.name()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: rgb(255, 153, 50);")
        # Native window must exist before it can be assigned to a screen
        self.winId()
        self.windowHandle().setScreen(screen)
        self.setGeometry(screen.geometry())
        self.showFullScreen()
        print(f"✓ {self.display_name}: backlight active {screen.geometry().width()}x{screen.geometry().height()}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()
        else:
            super().keyPressEvent(event)

    def update_color(self, color):
        rgb = color.getRgb()[:3]
        self.setStyleSheet(f"background-color: rgb({rgb[0]}, {rgb[1]}, {rgb[2]});")


class ControlPanel(QMainWindow):
    """Control panel with integrated controls"""

    color_changed = pyqtSignal(QColor)

    def __init__(self, backlight_windows, primary_geom):
        super().__init__()
        self.backlight_windows = backlight_windows

        self.hue = 30
        self.saturation = 200
        self.value = 200
        self.backlight_on = True

        self.init_ui()

        # Position on primary monitor
        self.setGeometry(primary_geom.x() + 50, primary_geom.y() + 50, 300, 700)
        self.show()
        self.raise_()

        print("✓ Control panel ready!")
        self.update_color()

    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Backlight Control")
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #1a1a1a; color: #CCC;")

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 15, 12, 15)
        layout.setSpacing(10)

        # Title
        title = QLabel("✨ BACKLIGHT")
        title_font = QFont()
        title_font.setPointSize(13)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #FFD700;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Sep
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #444;")
        layout.addWidget(sep)

        # Color display
        self.color_label = QLabel("#FF9932")
        self.color_label.setFont(QFont("Courier", 11, QFont.Bold))
        self.color_label.setStyleSheet("color: #FFD700;")
        self.color_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.color_label)

        # WARM PRESETS
        warm_title = QLabel("🔥 WARM TONES")
        warm_title.setStyleSheet("color: #FFA500; font-weight: bold; font-size: 10px;")
        warm_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(warm_title)

        warm_layout = QHBoxLayout()
        warm_layout.setSpacing(6)

        for name, h, s, v in [("Soft", 25, 180, 120), ("Golden", 30, 200, 150), ("Bright", 35, 200, 180)]:
            btn = QPushButton(name)
            btn.setMinimumHeight(32)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda c, hue=h, sat=s, val=v: self.set_preset(hue, sat, val))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #333;
                    color: #FFA500;
                    border: 1px solid #FF8C00;
                    border-radius: 3px;
                    font-weight: bold;
                    padding: 5px;
                }
                QPushButton:hover { background-color: #FF8C00; color: white; }
            """)
            warm_layout.addWidget(btn)

        layout.addLayout(warm_layout)

        # Sep
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.HLine)
        sep2.setStyleSheet("background-color: #444;")
        layout.addWidget(sep2)

        # SLIDERS
        layout.addWidget(QLabel("🎨 HUE"))
        hue_h = QHBoxLayout()
        self.hue_slider = QSlider(Qt.Horizontal)
        self.hue_slider.setRange(0, 360)
        self.hue_slider.setValue(30)
        self.hue_slider.sliderMoved.connect(lambda v: self.on_hue_changed(v))
        self.hue_label = QLabel("30°")
        self.hue_label.setMinimumWidth(30)
        self.hue_label.setStyleSheet("color: #87CEEB;")
        hue_h.addWidget(self.hue_slider)
        hue_h.addWidget(self.hue_label)
        layout.addLayout(hue_h)

        layout.addWidget(QLabel("🌈 SAT"))
        sat_h = QHBoxLayout()
        self.sat_slider = QSlider(Qt.Horizontal)
        self.sat_slider.setRange(0, 255)
        self.sat_slider.setValue(200)
        self.sat_slider.sliderMoved.connect(lambda v: self.on_sat_changed(v))
        self.sat_label = QLabel("78%")
        self.sat_label.setMinimumWidth(30)
        self.sat_label.setStyleSheet("color: #87CEEB;")
        sat_h.addWidget(self.sat_slider)
        sat_h.addWidget(self.sat_label)
        layout.addLayout(sat_h)

        layout.addWidget(QLabel("☀️  BRIGHT"))
        val_h = QHBoxLayout()
        self.val_slider = QSlider(Qt.Horizontal)
        self.val_slider.setRange(0, 255)
        self.val_slider.setValue(200)
        self.val_slider.sliderMoved.connect(lambda v: self.on_val_changed(v))
        self.val_label = QLabel("78%")
        self.val_label.setMinimumWidth(30)
        self.val_label.setStyleSheet("color: #87CEEB;")
        val_h.addWidget(self.val_slider)
        val_h.addWidget(self.val_label)
        layout.addLayout(val_h)

        # Sep
        sep3 = QFrame()
        sep3.setFrameShape(QFrame.HLine)
        sep3.setStyleSheet("background-color: #444;")
        layout.addWidget(sep3)

        # QUICK PRESETS
        layout.addWidget(QLabel("🎯 QUICK"))
        quick_grid = QGridLayout()
        quick_grid.setSpacing(5)

        for i, (name, h, s, v) in enumerate([("Cool", 200, 255, 200), ("Red", 0, 255, 200),
                                              ("Green", 120, 255, 200), ("Purple", 270, 255, 180)]):
            btn = QPushButton(name)
            btn.setMinimumHeight(28)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda c, hue=h, sat=s, val=v: self.set_preset(hue, sat, val))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #333; color: #BBB; border: 1px solid #555;
                    border-radius: 3px; font-weight: bold; font-size: 9px; padding: 4px;
                }
                QPushButton:hover { background-color: #444; }
            """)
            quick_grid.addWidget(btn, i // 2, i % 2)

        layout.addLayout(quick_grid)

        # Sep
        sep4 = QFrame()
        sep4.setFrameShape(QFrame.HLine)
        sep4.setStyleSheet("background-color: #444;")
        layout.addWidget(sep4)

        # BUTTONS
        self.toggle_btn = QPushButton("◉ ON")
        self.toggle_btn.setMinimumHeight(38)
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_light)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #228B22; color: white;
                border: none; border-radius: 4px; font-weight: bold; font-size: 12px;
            }
            QPushButton:hover { background-color: #32CD32; }
        """)
        layout.addWidget(self.toggle_btn)

        exit_btn = QPushButton("✕ EXIT")
        exit_btn.setMinimumHeight(38)
        exit_btn.setCursor(Qt.PointingHandCursor)
        exit_btn.clicked.connect(self.close_all)
        exit_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B0000; color: white;
                border: none; border-radius: 4px; font-weight: bold; font-size: 12px;
            }
            QPushButton:hover { background-color: #DC143C; }
        """)
        layout.addWidget(exit_btn)

        layout.addStretch()

        # Slider styling
        self.setStyleSheet(self.styleSheet() + """
            QSlider::groove:horizontal {
                background-color: #333; height: 5px; margin: 3px 0; border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background-color: #00BFFF; border: 1px solid #00BFFF;
                width: 12px; margin: -3px 0; border-radius: 6px;
            }
            QSlider::handle:horizontal:hover { background-color: #1E90FF; }
        """)

    def on_hue_changed(self, v):
        self.hue = v
        self.hue_label.setText(f"{v}°")
        self.update_color()

    def on_sat_changed(self, v):
        self.saturation = v
        self.sat_label.setText(f"{int((v/255)*100)}%")
        self.update_color()

    def on_val_changed(self, v):
        self.value = v
        self.val_label.setText(f"{int((v/255)*100)}%")
        self.update_color()

    def set_preset(self, h, s, v):
        self.hue_slider.blockSignals(True)
        self.sat_slider.blockSignals(True)
        self.val_slider.blockSignals(True)

        self.hue_slider.setValue(h)
        self.sat_slider.setValue(s)
        self.val_slider.setValue(v)

        self.hue = h
        self.saturation = s
        self.value = v

        self.hue_slider.blockSignals(False)
        self.sat_slider.blockSignals(False)
        self.val_slider.blockSignals(False)

        self.update_color()

    def update_color(self):
        if not self.backlight_on:
            color = QColor(0, 0, 0)
        else:
            h, s, v = self.hue / 360, self.saturation / 255, self.value / 255
            r, g, b = hsv_to_rgb(h, s, v)
            color = QColor(int(r*255), int(g*255), int(b*255))

        self.color_label.setText(color.name().upper())
        self.color_changed.emit(color)

        for window in self.backlight_windows:
            window.update_color(color)

    def toggle_light(self):
        self.backlight_on = not self.backlight_on
        if self.backlight_on:
            self.toggle_btn.setText("◉ ON")
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #228B22; color: white;
                    border: none; border-radius: 4px; font-weight: bold; font-size: 12px;
                }
                QPushButton:hover { background-color: #32CD32; }
            """)
        else:
            self.toggle_btn.setText("◎ OFF")
            self.toggle_btn.setStyleSheet("""
                QPushButton {
                    background-color: #444; color: #aaa;
                    border: none; border-radius: 4px; font-weight: bold; font-size: 12px;
                }
                QPushButton:hover { background-color: #555; }
            """)
        self.update_color()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_all()
        else:
            super().keyPressEvent(event)

    def close_all(self):
        for window in self.backlight_windows:
            window.close()
        self.close()

    def closeEvent(self, event):
        for window in self.backlight_windows:
            window.close()
        QApplication.quit()


def main():
    app = QApplication(sys.argv)
    screens = app.screens()
    print(f"🔥 Backlight - {len(screens)} display(s)\n")

    backlight_windows = [BacklightWindow(sc) for sc in screens]
    primary = app.primaryScreen().geometry()

    control = ControlPanel(backlight_windows, primary)
    control.setWindowFlags(control.windowFlags() | Qt.WindowStaysOnTopHint)
    control.show()
    control.raise_()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
