# Arctis Battery Tray

A lightweight system tray battery indicator for the **SteelSeries Arctis Nova 7X** on Linux.

Displays the headset battery level as a tray icon — black background, percentage in the center, and a colored arc ring showing charge level (green / yellow / red).

![icon style](https://img.shields.io/badge/style-RazerBatteryTray--inspired-brightgreen)

## Requirements

- [linux-arctis-manager](https://github.com/elegos/Linux-Arctis-Manager) — must be installed and running (`lam-cli setup --start-now`)
- Python 3.10+
- `python-pystray`
- `python-pillow`
- `python-dbus`

On Manjaro/Arch:
```bash
sudo pacman -S python-pystray python-pillow python-dbus
```

## Usage

```bash
python3 arctis-battery-tray.py
```

## Autostart

Add to `~/.config/autostart/arctis-battery-tray.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=Arctis Battery Tray
Exec=python3 /path/to/arctis-battery-tray.py
Icon=battery
X-GNOME-Autostart-enabled=true
```

## How it works

Reads battery data from the `linux-arctis-manager` DBus service (`name.giacomofurlan.ArctisManager.Next`) and renders a tray icon updated every 30 seconds.
