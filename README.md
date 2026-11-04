# 🎬 Backlight - Multi-Monitor Recording Backlight

A sleek, intuitive full-screen backlight application for multi-monitor setups. Perfect for webcam recordings, streaming, or creating custom ambient lighting on all your displays simultaneously.

## Features

✨ **Multi-Monitor Support** - Works across all connected displays simultaneously
🎨 **Full HSV Color Control** - Adjust Hue, Saturation, and Brightness independently
📊 **Real-Time Adjustments** - Instant feedback on all screens
🎯 **Quick Presets** - One-click color presets (Warm, Cool, Red, Green)
🔘 **Easy Toggle** - Quick on/off button for recording starts
💾 **Minimal Footprint** - Lightweight control panel stays on top
🖥️ **Full-Screen Mode** - Fills entire displays without taskbar interference

## Installation

### Prerequisites
- Python 3.7+
- PyQt5

### Quick Start

```bash
cd /home/hans/Projects/backlight
./run.sh
```

The script will automatically create a virtual environment and install dependencies.

### Add to the application menu

```bash
./install.sh
```

This creates a `Backlight` entry in your start/application menu.

### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 backlight.py
```

## Usage

### Controls

**Hue Slider** 🎨
- Range: 0-360°
- Controls the base color (red → yellow → green → cyan → blue → magenta → red)

**Saturation Slider** 🌈
- Range: 0-100%
- 100% = full vibrant color
- 0% = grayscale/white

**Brightness Slider** ☀️
- Range: 0-100%
- Controls intensity from off to maximum brightness

**Preset Buttons**
- **Warm**: Golden/orange tone (30° hue, full sat, 78% bright) - good for evening streams
- **Cool**: Blue tone (200° hue, full sat, 78% bright) - energetic, professional
- **Red**: Pure red for attention/alerts
- **Green**: Pure green for calmness

**Toggle Button**
- ◉ ON / ◎ OFF - Quickly turn the backlight on/off without adjusting settings
- ON state: Backlight shows current color
- OFF state: All screens go black

**Exit Button**
- ✕ Closes the application and turns off backlight

### Typical Workflow for Recording

1. Launch the application: `./run.sh`
2. The control panel appears in the center of your primary screen
3. Full-screen colored backgrounds fill all your other monitors
4. Adjust color/brightness to your preference
5. Click **ON** when you're ready to record
6. Record your content with perfect backlighting
7. Click **OFF** when done
8. Hit **Exit** to quit

## Tips & Tricks

### For Webcam Recordings
- Use **Warm** preset for a professional, natural look
- Reduce brightness to 40-60% for subtle backlighting that doesn't wash out
- Position your camera to capture the backlit background

### For Streaming
- Use **Cool** preset for high-energy streams
- Keep saturation at 100% for vibrant on-camera appearance
- Adjust brightness based on your room's ambient lighting

### For Product/Content Photography
- Experiment with **Red** or custom hues as accent lighting
- Use lower saturation (30-70%) for more subtle, professional lighting

### Keyboard Shortcuts
- Press **ESC** to close the application immediately

## Requirements

- **PyQt5** 5.15.9 or higher
- **Python** 3.7 or higher
- X11 or Wayland display server (Linux)

## Troubleshooting

### Backlight not appearing on all monitors
- Ensure all monitors are detected by your display manager
- Run `python3 backlight.py` directly to see debug output about detected screens
- Check monitor connection and display settings

### Control panel hard to interact with
- The control panel has "Always on Top" enabled
- Click anywhere in the window to focus it
- Use keyboard navigation if needed

### Colors look different on different monitors
- This is normal due to monitor calibration differences
- Try adjusting saturation/brightness on individual monitors if possible
- Consider monitor-specific color profiles

### Application crashes on startup
- Install PyQt5: `pip install PyQt5==5.15.9`
- Check Python version: `python3 --version` (should be 3.7+)
- Run with debug: `python3 backlight.py` to see error messages

## Performance

- Minimal CPU usage (pure color rendering)
- GPU-accelerated rendering when available
- Negligible memory footprint (~50MB)

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).

## Future Enhancements

- [ ] Settings persistence (remember last color/brightness)
- [ ] Animation modes (fade, pulse, strobe)
- [ ] Per-monitor independent control
- [ ] Hotkey support for quick adjustments
- [ ] Custom color preset saving
- [ ] Screen recording integration

---

Enjoy your perfectly backlit recordings! 🎬✨
