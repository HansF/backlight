#!/bin/bash
# Install Backlight into the application menu (start menu) for the current user.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$HOME/.local/share/applications"
cat > "$HOME/.local/share/applications/backlight.desktop" <<DESKTOP
[Desktop Entry]
Version=1.0
Type=Application
Name=Backlight
Comment=Multi-monitor recording backlight
Exec=$DIR/run.sh
Icon=video-display
Categories=AudioVideo;Video;Utility;
Keywords=recording;backlight;monitor;lighting;
Terminal=false
StartupNotify=true
DESKTOP
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
echo "Installed. Find 'Backlight' in your application menu."
