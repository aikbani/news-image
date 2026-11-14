"""news-image-01: front page summing up the world's news of Friday 13 November 2026.

Procedural Python, standard library only. Draws a newspaper front page:
masthead "FRIDAY 13 NOVEMBER 2026" + "THE WORLD TODAY", six panels in a
2x3 grid, each a simple flat editorial drawing plus one short bold label.
Writes /output/entry.png (or ./entry.png when /output is absent).
Deterministic: two runs produce byte-identical output.
"""

import math
import os
import struct
import sys
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (246, 241, 230)      # newsprint cream
INK = (26, 42, 74)           # dark navy ink
RED = (179, 32, 44)          # accent red
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GREY = (120, 124, 130)
LIGHT_GREY = (233, 237, 242)
GOLD = (212, 160, 32)
DARK_NAVY = (30, 42, 68)
SKY = (223, 230, 238)
SEA = (46, 74, 102)
SAND = (236, 217, 168)
WOOD = (122, 84, 48)
STEEL = (96, 110, 126)

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows of 5 bits, "1" = ink.
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "J": ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    "3": ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    "6": ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    "&": ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    ":": ["00000", "00100", "00000", "00000", "00000", "00100", "00000"],
    ".": ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ",": ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    "-": ["00000", "00000", "00000", "01110", "00000", "00000", "00000"],
    "/": ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    "$": ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
}


def text_width(s, scale):
    return len(s) * (5 * scale + scale) - scale


def draw_text(cv, s, x, y, scale, color):
    cx = x
    for ch in s:
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    cv.rect(cx + col * scale, y + row * scale,
                            scale, scale, color)
        cx += 5 * scale + scale


def draw_text_centered(cv, s, cx, y, scale, color):
    w = text_width(s, scale)
    draw_text(cv, s, cx - w // 2, y, scale, color)


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        for i in range(w * h):
            self.px[i * 3] = bg[0]
            self.px[i * 3 + 1] = bg[1]
            self.px[i * 3 + 2] = bg[2]

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i] = color[0]
            self.px[i + 1] = color[1]
            self.px[i + 2] = color[2]

    def rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i] = color[0]
                self.px[i + 1] = color[1]
                self.px[i + 2] = color[2]

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def vline(self, x, y, h, color, thick=1):
        self.rect(x, y, thick, h, color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        while True:
            self.rect(x - thick // 2, y - thick // 2, thick, thick, color)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x += sx
            if e2 <= dx:
                err += dx
                y += sy

    def disc(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            dy = yy - cy
            dx = int(math.sqrt(max(0, r * r - dy * dy)))
            self.rect(cx - dx, yy, 2 * dx + 1, 1, color)

    def ellipse(self, cx, cy, rx, ry, color):
        for yy in range(cy - ry, cy + ry + 1):
            dy = (yy - cy) / float(ry)
            dx = int(rx * math.sqrt(max(0.0, 1.0 - dy * dy)))
            self.rect(cx - dx, yy, 2 * dx + 1, 1, color)

    def poly(self, pts, color):
        # Scanline fill of a simple polygon.
        ys = [p[1] for p in pts]
        for yy in range(min(ys), max(ys) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= yy < y1) or (y1 <= yy < y0):
                    if y1 != y0:
                        t = (yy - y0) / float(y1 - y0)
                        xs.append(x0 + t * (x1 - x0))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                self.rect(int(xs[j]), yy, max(1, int(xs[j + 1]) - int(xs[j])), 1, color)

    def frame(self, x, y, w, h, color, thick=2):
        self.rect(x, y, w, thick, color)
        self.rect(x, y + h - thick, w, thick, color)
        self.rect(x, y, thick, h, color)
        self.rect(x + w - thick, y, thick, h, color)


def png_bytes(cv):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


# ---------------------------------------------------------------- panels
# Panel grid: x in {16, 516}, width 492; y in {164, 448, 732}, height 268.
PANEL_W, PANEL_H = 492, 268
PANEL_X = [16, 516]
PANEL_Y = [164, 448, 732]
BAR_COLORS = [INK, (90, 90, 96), (150, 110, 40), DARK_NAVY, (60, 90, 140), (120, 60, 60)]


def panel_base(cv, idx, bg):
    x = PANEL_X[idx % 2]
    y = PANEL_Y[idx // 2]
    cv.rect(x, y, PANEL_W, PANEL_H, bg)
    cv.rect(x, y, PANEL_W, 10, BAR_COLORS[idx])
    cv.frame(x, y, PANEL_W, PANEL_H, INK, 2)
    return x, y


def panel_label(cv, x, y, line1, line2):
    # Light caption strip so the label is legible on any panel background.
    cv.rect(x + 2, y + 196, PANEL_W - 4, PANEL_H - 198, PAPER)
    cx = x + PANEL_W // 2
    draw_text_centered(cv, line1, cx, y + 204, 4, INK)
    if line2:
        draw_text_centered(cv, line2, cx, y + 240, 4, INK)


def chair(cv, x, y, color):
    # Empty witness chair: tall back, seat, two legs.
    cv.rect(x, y, 66, 74, color)
    cv.rect(x - 8, y + 74, 82, 12, color)
    cv.rect(x + 4, y + 86, 8, 30, color)
    cv.rect(x + 54, y + 86, 8, 30, color)
    cv.rect(x + 8, y + 12, 50, 6, (200, 200, 200))


def panel_senate(cv, idx):
    x, y = panel_base(cv, idx, SKY)
    # Hearing-room wall + floor.
    cv.rect(x + 2, y + 150, PANEL_W - 4, 46, (196, 188, 172))
    # Two empty witness chairs.
    chair(cv, x + 96, y + 34, INK)
    chair(cv, x + 330, y + 34, INK)
    # Long hearing desk.
    cv.rect(x + 40, y + 150, 412, 14, WOOD)
    cv.rect(x + 40, y + 164, 412, 26, (96, 64, 36))
    # Nameplates on the desk.
    cv.rect(x + 120, y + 138, 60, 12, WHITE)
    cv.rect(x + 320, y + 138, 60, 12, WHITE)
    # Gavel resting on the desk.
    cv.rect(x + 400, y + 140, 34, 8, WOOD)
    cv.rect(x + 414, y + 140, 6, 12, WOOD)
    # Small flag on the desk.
    cv.vline(x + 66, y + 112, 38, INK, 3)
    cv.rect(x + 69, y + 112, 34, 22, RED)
    cv.rect(x + 69, y + 112, 14, 12, INK)
    panel_label(cv, x, y, "SENATE SUMMONS", "HUANG & LUTNICK")


def panel_warship(cv, idx):
    x, y = panel_base(cv, idx, (143, 163, 184))
    # Dusk sky bands.
    cv.rect(x + 2, y + 10, PANEL_W - 4, 60, (168, 182, 198))
    cv.rect(x + 2, y + 70, PANEL_W - 4, 50, (143, 163, 184))
    # Sea.
    cv.rect(x + 2, y + 120, PANEL_W - 4, 76, SEA)
    for wy in (132, 150, 170, 186):
        for wx in range(0, PANEL_W - 4, 46):
            cv.hline(x + 6 + wx, y + wy, 26, (120, 160, 196), 2)
    # Warship hull.
    cv.poly([(x + 90, y + 118), (x + 410, y + 118), (x + 380, y + 148),
             (x + 120, y + 148)], (58, 66, 76))
    cv.rect(x + 180, y + 88, 130, 30, (74, 84, 96))
    cv.rect(x + 300, y + 70, 26, 48, (74, 84, 96))
    cv.vline(x + 240, y + 52, 40, (58, 66, 76), 4)
    # Smoke rising from the deck hit.
    cv.disc(x + 330, y + 62, 16, (90, 90, 90))
    cv.disc(x + 348, y + 44, 20, (110, 110, 110))
    cv.disc(x + 330, y + 24, 14, (130, 130, 130))
    # Orange flash at the impact point.
    cv.disc(x + 330, y + 108, 12, (230, 120, 30))
    cv.disc(x + 330, y + 108, 6, (250, 200, 60))
    # Small drone in the sky.
    cv.disc(x + 430, y + 40, 4, BLACK)
    cv.hline(x + 420, y + 38, 20, BLACK, 2)
    panel_label(cv, x, y, "DRONE HITS", "RUSSIAN WARSHIP")


def panel_bahrain(cv, idx):
    x, y = panel_base(cv, idx, (242, 227, 192))
    # Sun.
    cv.disc(x + 70, y + 48, 22, (240, 190, 60))
    # Desert ground.
    cv.rect(x + 2, y + 140, PANEL_W - 4, 56, SAND)
    cv.rect(x + 2, y + 140, PANEL_W - 4, 4, (210, 180, 120))
    # Radar tower + dome.
    cv.rect(x + 216, y + 78, 28, 66, STEEL)
    cv.rect(x + 200, y + 140, 60, 6, STEEL)
    cv.disc(x + 230, y + 78, 44, WHITE)
    cv.rect(x + 186, y + 78, 88, 30, (242, 227, 192))
    cv.vline(x + 230, y + 34, 12, STEEL, 3)
    # Missile streak from the top right.
    cv.line(x + 470, y + 16, x + 300, y + 66, (250, 240, 200), 4)
    cv.line(x + 470, y + 16, x + 300, y + 66, WHITE, 2)
    cv.disc(x + 300, y + 66, 10, (250, 150, 40))
    cv.disc(x + 300, y + 66, 5, (255, 220, 90))
    # Small buildings on the coast.
    cv.rect(x + 380, y + 116, 40, 24, (190, 170, 130))
    cv.rect(x + 428, y + 124, 30, 16, (190, 170, 130))
    panel_label(cv, x, y, "IRAN CLAIMS STRIKE", "IN BAHRAIN")


def panel_hack(cv, idx):
    x, y = panel_base(cv, idx, (28, 36, 58))
    # Laptop screen.
    cv.rect(x + 110, y + 26, 272, 118, (12, 18, 34))
    cv.frame(x + 110, y + 26, 272, 118, (150, 156, 166), 3)
    # Masked face on the screen: dark hood + white mask.
    cv.ellipse(x + 246, y + 82, 52, 46, (16, 20, 30))
    cv.ellipse(x + 246, y + 86, 38, 34, (235, 235, 235))
    cv.ellipse(x + 232, y + 80, 8, 5, BLACK)
    cv.ellipse(x + 260, y + 80, 8, 5, BLACK)
    cv.rect(x + 238, y + 100, 16, 4, BLACK)
    # Laptop base.
    cv.poly([(x + 96, y + 144), (x + 396, y + 144), (x + 420, y + 164),
             (x + 72, y + 164)], (120, 126, 136))
    # Gold coins spilling out of the screen.
    for cx, cy, r in [(140, 176, 13), (176, 184, 11), (212, 176, 13),
                      (300, 182, 12), (340, 174, 13), (372, 184, 11)]:
        cv.disc(x + cx, y + cy, r, GOLD)
        cv.disc(x + cx, y + cy, r - 4, (232, 190, 70))
    panel_label(cv, x, y, "FBI: N. KOREA", "$400M HACK")


def panel_outage(cv, idx):
    x, y = panel_base(cv, idx, LIGHT_GREY)
    # Big monitor, dark screen.
    cv.rect(x + 130, y + 24, 232, 122, (34, 48, 74))
    cv.frame(x + 130, y + 24, 232, 122, (150, 156, 166), 3)
    cv.rect(x + 226, y + 146, 10, 22, (150, 156, 166))
    cv.rect(x + 180, y + 166, 102, 8, (150, 156, 166))
    # Envelope on the screen with a red X over it.
    cv.rect(x + 196, y + 62, 100, 56, WHITE)
    cv.line(x + 196, y + 62, x + 246, y + 94, (150, 156, 166), 3)
    cv.line(x + 296, y + 62, x + 246, y + 94, (150, 156, 166), 3)
    cv.line(x + 186, y + 52, x + 306, y + 128, RED, 7)
    cv.line(x + 306, y + 52, x + 186, y + 128, RED, 7)
    # Cloud with a lightning bolt.
    cv.disc(x + 410, y + 52, 22, WHITE)
    cv.disc(x + 436, y + 60, 26, WHITE)
    cv.rect(x + 392, y + 52, 66, 22, WHITE)
    cv.poly([(x + 424, y + 66), (x + 410, y + 96), (x + 424, y + 96),
             (x + 414, y + 118), (x + 440, y + 84), (x + 428, y + 84)],
            (240, 190, 60))
    # Dead signal bars.
    for i, bh in enumerate((14, 22, 30)):
        cv.rect(x + 60 + i * 18, y + 156 - bh, 12, bh, (120, 126, 136))
    cv.line(x + 58, y + 118, x + 116, y + 160, RED, 5)
    cv.line(x + 116, y + 118, x + 58, y + 160, RED, 5)
    panel_label(cv, x, y, "MICROSOFT OUTAGE", "DAY 2")


def panel_deportations(cv, idx):
    x, y = panel_base(cv, idx, (236, 231, 219))
    # Pale sky + small globe.
    cv.disc(x + 76, y + 66, 34, (110, 160, 210))
    cv.ellipse(x + 66, y + 60, 12, 8, (90, 170, 110))
    cv.ellipse(x + 86, y + 76, 10, 7, (90, 170, 110))
    # Dotted flight path.
    for i in range(14):
        t = i / 13.0
        px = int(x + 120 + t * 300)
        py = int(y + 96 - 26 * math.sin(t * math.pi) + 10 * t)
        cv.disc(px, py, 3, INK)
    # Airplane silhouette flying right.
    px, py = x + 400, y + 62
    cv.ellipse(px, py, 46, 10, INK)
    cv.poly([(px - 8, py - 6), (px + 6, py - 6), (px + 26, py - 30),
             (px + 34, py - 30), (px + 16, py - 4)], INK)
    cv.poly([(px - 4, py + 4), (px + 8, py + 4), (px + 18, py + 22),
             (px + 26, py + 22), (px + 12, py + 6)], INK)
    cv.poly([(px + 40, py - 4), (px + 56, py - 12), (px + 56, py + 2),
             (px + 42, py + 6)], INK)
    # Runway strip at the bottom.
    cv.rect(x + 2, y + 158, PANEL_W - 4, 8, (150, 146, 134))
    for rx in range(20, PANEL_W - 20, 44):
        cv.hline(x + rx, y + 161, 22, WHITE, 2)
    panel_label(cv, x, y, "US: RECORD 483,200", "DEPORTATIONS")


# ---------------------------------------------------------------- page
def draw_page():
    cv = Canvas(W, H, PAPER)
    # Masthead.
    cv.hline(16, 20, 992, INK, 3)
    draw_text_centered(cv, "FRIDAY 13 NOVEMBER 2026", W // 2, 34, 5, INK)
    draw_text_centered(cv, "THE WORLD TODAY", W // 2, 92, 5, RED)
    cv.hline(16, 142, 992, RED, 4)
    cv.hline(16, 150, 992, INK, 2)
    # Six panels.
    panel_senate(cv, 0)
    panel_warship(cv, 1)
    panel_bahrain(cv, 2)
    panel_hack(cv, 3)
    panel_outage(cv, 4)
    panel_deportations(cv, 5)
    # Footer.
    cv.hline(16, 1004, 992, INK, 2)
    draw_text_centered(cv, "ALL STORIES FIRST REPORTED 13 NOVEMBER 2026",
                       W // 2, 1008, 2, GREY)
    return cv


def main():
    cv = draw_page()
    data = png_bytes(cv)
    outdir = "/output" if os.path.isdir("/output") else "."
    path = os.path.join(outdir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    sys.stdout.write("wrote %s %d bytes\n" % (path, len(data)))


if __name__ == "__main__":
    main()
