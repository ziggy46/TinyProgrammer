# Status Report: TinyProgrammer on RPi 4

**Date:** February 2026
**Hardware:** Raspberry Pi 4 + 5-inch HDMI display
**OS:** Raspberry Pi OS (64-bit)

## Current State: WORKING

### Display: WORKING
Direct framebuffer writes to `/dev/fb0` over HDMI. Pygame runs in `dummy` video driver mode (in-memory rendering), surfaces converted to RGB565 and written directly to framebuffer.

**Performance:** ~60 fps target, ~20-30 fps effective for full-screen updates

### AI Backend: WORKING
- **Provider:** OpenRouter API
- **Model:** DeepSeek (configurable via dashboard)
- Streams tokens directly into the editor in real time

### Application Status
- **AI Code Generation:** Working
- **Self-correction Loop:** Working
- **tiny_canvas API:** Working
- **Display Output:** Working (direct framebuffer, HDMI)
- **Web Dashboard:** Working (Flask, port 5000)
- **Autostart on Boot:** Working (systemd service)
- **Color Schemes:** Working (amber, green, blue, inverted, none)

### Systemd Service
Installed at `/etc/systemd/system/tinyprogrammer.service`. Autostarts on boot, restarts on failure. Console cursor hidden via `fbcon/cursor_blink`.

Management:
```bash
sudo systemctl status tinyprogrammer
sudo systemctl stop tinyprogrammer    # stop before shutdown!
sudo systemctl restart tinyprogrammer
journalctl -u tinyprogrammer -f
```

## Branch Notes

This branch (`rpi4-hdmi`) diverges from the original `main` branch (Pi Zero 2 W + Waveshare SPI LCD). Key differences:
- HDMI output instead of SPI display
- OpenRouter/DeepSeek instead of local Ollama/llama.cpp
- Web dashboard for remote settings
- Systemd autostart
- Color adjustment layer
