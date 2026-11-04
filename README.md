# Backlight

A full-screen colored backlight for multi-monitor setups. Every connected display is filled with one adjustable color, which is handy as soft light for webcam recordings and streams.

Built with PyQt5. Works on Wayland (tested on KDE Plasma) and X11. Each display gets its own fullscreen window, assigned through Qt's screen list, so placement doesn't depend on `xrandr`.

## Features

- Fills all connected displays at once
- Hue, saturation and brightness sliders, applied live
- Presets: Soft, Golden, Bright (warm tones) and Cool, Red, Green, Purple
- ON/OFF button (OFF turns all screens black without losing your settings)
- Small always-on-top control panel on the primary screen
- Keeps the screens awake while it runs (screen saver, dimming and idle sleep are inhibited; released on exit)
- Starts with a warm golden light (hue 30°, 78% saturation, 78% brightness)

## Install

Requires Python 3 and PyQt5.

```bash
git clone https://github.com/HansF/backlight.git
cd backlight
./run.sh
```

`run.sh` creates a virtual environment, installs the requirements and starts the app. It can be launched from any directory.

### Add to the application menu

```bash
./install.sh
```

This creates a `Backlight` entry in your start/application menu (`~/.local/share/applications/backlight.desktop`) that points at this folder. Run it again if you move the folder.

### Manual

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 backlight.py
```

## Controls

| Control | Effect |
|---|---|
| **Hue** (0-360°) | Base color |
| **Sat** (0-100%) | 100% is vivid, 0% is white |
| **Bright** (0-100%) | Intensity |
| **Presets** | Sets hue/saturation/brightness in one click |
| **ON / OFF** | Toggle the backlight (OFF = black screens) |
| **ESC** | Quits (works when the control panel or a backlight window has focus) |
| **EXIT** | Closes the control panel and all backlight windows |

Closing the control panel window also quits the app.

## Troubleshooting

- **Screens still go to sleep:** the app asks the desktop to stay awake over D-Bus (`org.freedesktop.ScreenSaver` and `org.freedesktop.PowerManagement.Inhibit`; `caffeinate` on macOS). It prints `✓ Screen sleep inhibited` on success or a warning if no inhibit service was found.

- **A screen stays dark:** run `python3 backlight.py` from a terminal. It prints one line per detected display; if a screen is missing there, Qt doesn't see it.
- **Control panel hidden behind a backlight window:** it requests always-on-top, but some window managers ignore that on fullscreen windows. Raise it via the taskbar.
- **Crash on startup:** check that PyQt5 is installed in the venv (`pip install -r requirements.txt`).

## Ideas

- Remember the last color between runs
- Per-monitor color and brightness
- More keyboard shortcuts (brightness, presets)
- Custom saved presets

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
