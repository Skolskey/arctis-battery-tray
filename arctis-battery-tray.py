#!/usr/bin/env python3
import json
import threading
import dbus
import dbus.mainloop.glib
from gi.repository import GLib
from PIL import Image, ImageDraw, ImageFont
import pystray

DBUS_DEST = "name.giacomofurlan.ArctisManager.Next"
DBUS_PATH = "/name/giacomofurlan/ArctisManager/Next/Status"
DBUS_IFACE = "name.giacomofurlan.ArctisManager.Next.Status"

def get_battery():
    try:
        bus = dbus.SessionBus()
        obj = bus.get_object(DBUS_DEST, DBUS_PATH)
        iface = dbus.Interface(obj, DBUS_IFACE)
        data = json.loads(iface.GetStatus())
        return data["headset"]["headset_battery_charge"]["value"]
    except Exception:
        return None

def make_icon(percent):
    SIZE = 256
    BORDER = int(SIZE / 16)
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    text = str(percent) if percent is not None else "?"

    if percent is None:
        arc_color = (128, 128, 128, 255)
    elif percent > 60:
        arc_color = (80, 200, 80, 255)
    elif percent > 25:
        arc_color = (220, 180, 0, 255)
    else:
        arc_color = (220, 60, 60, 255)

    # Gray track (full ring)
    draw.pieslice([0, 0, SIZE - 1, SIZE - 1], -90, 270, fill=(60, 60, 60, 255))
    draw.ellipse([BORDER, BORDER, SIZE - 1 - BORDER, SIZE - 1 - BORDER], fill=(20, 20, 20, 200))

    # Colored arc
    if percent is not None and percent > 0:
        end_angle = -90 + (percent / 100) * 360
        draw.pieslice([0, 0, SIZE - 1, SIZE - 1], -90, end_angle, fill=arc_color)
        draw.ellipse([BORDER, BORDER, SIZE - 1 - BORDER, SIZE - 1 - BORDER], fill=(20, 20, 20, 200))

    font_size = int(0.56 * SIZE) if len(text) < 3 else int(0.42 * SIZE)
    try:
        font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    x = (SIZE - (bbox[2] - bbox[0])) / 2 - bbox[0]
    y = (SIZE - (bbox[3] - bbox[1])) / 2 - bbox[1] - int(0.047 * SIZE)
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

    return img.resize((64, 64), Image.Resampling.LANCZOS)

def make_title(percent):
    if percent is None:
        return "Arctis Nova 7X: недоступно"
    return f"Arctis Nova 7X: {percent}%"

def run_tray():
    percent = get_battery()
    icon = pystray.Icon(
        "arctis-battery",
        make_icon(percent),
        make_title(percent),
        menu=pystray.Menu(
            pystray.MenuItem("Выход", lambda icon, _: icon.stop())
        )
    )

    def update_loop():
        while True:
            p = get_battery()
            icon.icon = make_icon(p)
            icon.title = make_title(p)
            threading.Event().wait(30)

    t = threading.Thread(target=update_loop, daemon=True)
    t.start()
    icon.run()

def on_status_changed(status_json):
    pass  # update_loop handles polling; signal is a bonus trigger

if __name__ == "__main__":
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    run_tray()
