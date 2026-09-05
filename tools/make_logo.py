"""Simple avatar for the Telegram channel/group: dark square, rising momentum curve, monogram."""
from PIL import Image, ImageDraw, ImageFont
import math, sys
size = 1024
img = Image.new("RGB", (size, size), (14, 17, 23))
d = ImageDraw.Draw(img)
# background grid
for i in range(0, size, 128):
    d.line([(i, 0), (i, size)], fill=(24, 29, 38), width=2)
    d.line([(0, i), (size, i)], fill=(24, 29, 38), width=2)
# momentum curve: smoothed accelerating line
pts = []
for x in range(120, 904, 4):
    t = (x - 120) / 784
    y = 800 - 560 * (t ** 1.8) - 40 * math.sin(t * 9)
    pts.append((x, y))
d.line(pts, fill=(41, 200, 130), width=26, joint="curve")
# BTC baseline
d.line([(120, 640), (904, 500)], fill=(245, 166, 35), width=14)
# monogram
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 150)
except OSError:
    font = ImageFont.load_default()
d.text((120, 96), "CML", fill=(235, 238, 245), font=font)
img.save(sys.argv[1] if len(sys.argv) > 1 else "branding/logo.png")
print("ok")
