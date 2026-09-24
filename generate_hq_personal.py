"""
High-Resolution LinkedIn-Optimised PDF Generator
Personal Infographic — 3x Scale (3240 x 4050 px, single page portrait)
LinkedIn rasterises pages; starting at 3x means post-compression output
stays crisp on every device screen.
"""

import fitz
import math

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY   = (11/255,  29/255,  58/255)
CREAM  = (251/255, 247/255, 240/255)
GOLD   = (200/255, 150/255, 46/255)
RED    = (220/255,  38/255,  38/255)
GREEN  = (22/255,  163/255,  74/255)
TAUPE  = (154/255, 148/255, 144/255)
BEIGE  = (213/255, 207/255, 199/255)

S  = 3                      # 3× scale factor
W  = 1080 * S               # 3240
H  = 1350 * S               # 4050  (portrait — more room for all content)
MG = 60  * S                # margin


# ── Primitives ────────────────────────────────────────────────────────────────
def rct(shape, x0, y0, x1, y1, fill=None, stroke=None, width=1):
    shape.draw_rect(fitz.Rect(x0, y0, x1, y1))
    shape.finish(fill=fill, color=stroke, width=width)

def cir(shape, cx, cy, r, fill=None, stroke=None, width=1):
    shape.draw_circle((cx, cy), r)
    shape.finish(fill=fill, color=stroke, width=width)

def txt(page, x, y, text, size=24, color=CREAM, bold=False):
    fn = "hebo" if bold else "helv"
    page.insert_text((x, y), text, fontname=fn, fontsize=size * S, color=color)

def txt_len(text, size=24, bold=False):
    fn = "hebo" if bold else "helv"
    return fitz.get_text_length(text, fontname=fn, fontsize=size * S)

def divider(page, y, color=GOLD, width=1):
    sh = page.new_shape()
    sh.draw_line((MG, y), (W - MG, y))
    sh.finish(color=color, width=width * S)
    sh.commit()

def section_box(page, x, y, w, h, bg, label, label_color):
    sh = page.new_shape()
    rct(sh, x, y, x + w, y + h, fill=bg)
    sh.commit()
    # left accent bar
    sh = page.new_shape()
    rct(sh, x, y, x + 6 * S, y + h, fill=GOLD)
    sh.commit()
    txt(page, x + 16 * S, y + 36 * S, label, size=22, color=label_color, bold=True)


def draw_hbar(page, x, y, label, val, val_str, max_val, max_w,
              bar_color, label_color, lbl_size=18, val_size=16):
    txt(page, x, y, label, size=lbl_size, color=label_color, bold=True)
    lw = txt_len(label, size=lbl_size, bold=True) + 12 * S
    bw = max(6 * S, int((val / max_val) * max_w * S))
    sh = page.new_shape()
    rct(sh, x + lw, y - 18 * S, x + lw + bw, y + 3 * S, fill=bar_color)
    sh.commit()
    txt(page, x + lw + bw + 10 * S, y, val_str, size=val_size, color=label_color, bold=True)


def draw_donut(page, cx, cy, r_out, r_in, segments, colors,
               center_text=None, ct_color=CREAM, hole_color=NAVY,
               legend_x=None, legend_y=None, legend_labels=None, leg_color=CREAM):
    total = sum(segments)
    angle = -math.pi / 2
    for seg, col in zip(segments, colors):
        da = (seg / total) * 2 * math.pi
        if seg / total < 0.001:
            angle += da
            continue
        steps = max(int(da * 30), 4)
        pts = [(cx, cy)]
        for s in range(steps + 1):
            a = angle + s * da / steps
            pts.append((cx + r_out * math.cos(a), cy + r_out * math.sin(a)))
        pts.append((cx, cy))
        sh = page.new_shape()
        sh.draw_polyline(pts)
        sh.finish(fill=col, color=col, width=0.5)
        sh.commit()
        angle += da
    sh = page.new_shape()
    cir(sh, cx, cy, r_in, fill=hole_color)
    sh.commit()
    if center_text:
        tw = txt_len(center_text, size=16, bold=True)
        page.insert_text((cx - tw / 2, cy + 6 * S),
                         center_text, fontname="hebo", fontsize=16 * S, color=ct_color)
    if legend_labels and legend_x is not None:
        for i, (lbl, col) in enumerate(zip(legend_labels, colors)):
            ly2 = legend_y + i * 26 * S
            sh = page.new_shape()
            rct(sh, legend_x, ly2, legend_x + 12 * S, ly2 + 12 * S, fill=col)
            sh.commit()
            page.insert_text((legend_x + 18 * S, ly2 + 11 * S),
                             lbl, fontname="helv", fontsize=14 * S, color=leg_color)


# ════════════════════════════════════════════════════════════════════════════════
# BUILD SINGLE-PAGE INFOGRAPHIC
# ════════════════════════════════════════════════════════════════════════════════
doc  = fitz.open()
page = doc.new_page(width=W, height=H)

# Background
sh = page.new_shape()
rct(sh, 0, 0, W, H, fill=NAVY)
rct(sh, 0, 0, W, 6 * S, fill=GOLD)
sh.commit()

# ── MASTHEAD ──────────────────────────────────────────────────────────────────
txt(page, MG, 90  * S, "MARKET PSYCHOLOGY · 22 SEPTEMBER 2026", size=18, color=GOLD, bold=True)
txt(page, MG, 185 * S, "WHEN A STOCK", size=76, color=CREAM, bold=True)
txt(page, MG, 275 * S, "HITS THE CEILING.", size=76, color=GOLD,  bold=True)
txt(page, MG, 330 * S,
    "What happens when price is physically capped but demand refuses to stop?",
    size=18, color=TAUPE)

divider(page, 360 * S)

# ── QUADRANT LAYOUT ───────────────────────────────────────────────────────────
# Canvas below divider: y=370 → y=1200 (830 units)
# Split horizontally at x = MG + (W-2*MG)/2

MID  = W // 2 - 10 * S
BPAD = 30 * S      # inner padding
BW   = MID - MG   # box width each side

# ── Q1 · VODA (top-left, navy bg) ─────────────────────────────────────────────
Q1X, Q1Y, Q1H = MG, 375 * S, 380 * S
section_box(page, Q1X, Q1Y, BW, Q1H, bg=(0.07,0.13,0.25), label="VODA · LIMIT-UP", label_color=GOLD)
txt(page, Q1X + 20 * S, Q1Y + 70 * S,  "Closed at 1,320 · +4.8%",               size=26, color=CREAM, bold=True)
txt(page, Q1X + 20 * S, Q1Y + 120 * S, "Price hit the 5% daily ceiling.",        size=18, color=CREAM)
txt(page, Q1X + 20 * S, Q1Y + 165 * S, "The price physically could not go higher.",size=18, color=TAUPE)
draw_hbar(page, Q1X + 20 * S, Q1Y + 240 * S,
          "Offers", 24814, "24,814", 25000, 220, GOLD,  CREAM, lbl_size=18, val_size=16)
draw_hbar(page, Q1X + 20 * S, Q1Y + 305 * S,
          "Bids  ", 23119, "23,119", 25000, 220, CREAM, CREAM, lbl_size=18, val_size=16)

# ── Q2 · CRDB (top-right, slightly lighter navy) ───────────────────────────────
Q2X, Q2Y, Q2H = MID + 20 * S, 375 * S, 380 * S
section_box(page, Q2X, Q2Y, BW, Q2H, bg=(0.08,0.16,0.30), label="CRDB · STEALTH DEMAND", label_color=GOLD)
txt(page, Q2X + 20 * S, Q2Y + 70 * S,  "Closed FLAT · 2,810",                   size=26, color=CREAM, bold=True)
txt(page, Q2X + 20 * S, Q2Y + 120 * S, "Amateur: boring day.",                  size=18, color=CREAM)
txt(page, Q2X + 20 * S, Q2Y + 165 * S, "Professional: 3.9x buyer ratio.",       size=18, color=GOLD, bold=True)
draw_hbar(page, Q2X + 20 * S, Q2Y + 240 * S,
          "Bids  ", 192156, "192,156", 192156, 220, CREAM, CREAM, lbl_size=18, val_size=16)
draw_hbar(page, Q2X + 20 * S, Q2Y + 305 * S,
          "Offers", 49819,  "49,819",  192156, 220, GOLD,  CREAM, lbl_size=18, val_size=16)

# ── MIDDLE DIVIDER ─────────────────────────────────────────────────────────────
divider(page, 775 * S, color=GOLD, width=0.5)

# ── Q3 · FLOWS (bottom-left, donut) ───────────────────────────────────────────
Q3X, Q3Y, Q3H = MG, 790 * S, 380 * S
section_box(page, Q3X, Q3Y, BW, Q3H, bg=(0.07,0.13,0.25), label="LOCAL ABSORPTION", label_color=GOLD)
txt(page, Q3X + 20 * S, Q3Y + 70 * S,  "Foreign sold TZS 2.92B.", size=18, color=CREAM)
txt(page, Q3X + 20 * S, Q3Y + 105 * S, "Local devoured 99.88% of it.", size=18, color=GOLD, bold=True)
draw_donut(page,
           cx=Q3X + BW // 2, cy=Q3Y + 260 * S,
           r_out=80 * S, r_in=40 * S,
           segments=[99.88, 0.12], colors=[CREAM, GOLD],
           center_text="Buying", ct_color=NAVY, hole_color=(0.07,0.13,0.25),
           legend_x=Q3X + 20 * S, legend_y=Q3Y + 330 * S,
           legend_labels=["Local 99.88%", "Foreign 0.12%"], leg_color=CREAM)

# ── Q4 · BONDS (bottom-right, bars) ────────────────────────────────────────────
Q4X, Q4Y, Q4H = MID + 20 * S, 790 * S, 380 * S
section_box(page, Q4X, Q4Y, BW, Q4H, bg=(0.08,0.16,0.30), label="THE ROTATION", label_color=GOLD)
txt(page, Q4X + 20 * S, Q4Y + 70 * S,  "While absorbing equity, locals also", size=18, color=CREAM)
txt(page, Q4X + 20 * S, Q4Y + 105 * S, "locked away TZS 33.59B in bonds.", size=18, color=CREAM)
txt(page, Q4X + 20 * S, Q4Y + 155 * S, "Turnover:", size=18, color=TAUPE)
draw_hbar(page, Q4X + 20 * S, Q4Y + 220 * S,
          "Equity", 5.07,  "5.07B",   33.59, 220, CREAM, CREAM, lbl_size=18, val_size=16)
draw_hbar(page, Q4X + 20 * S, Q4Y + 285 * S,
          "Bonds ", 33.59, "33.59B",  33.59, 220, GOLD,  CREAM, lbl_size=18, val_size=16)
txt(page, Q4X + 20 * S, Q4Y + 345 * S, "+485% jump vs prior session.", size=18, color=GOLD, bold=True)

# ── FOOTER RULE & CTA ─────────────────────────────────────────────────────────
divider(page, 1185 * S)

txt(page, MG, 1225 * S,
    "Have you ever tried to buy into a market where the sellers have simply disappeared?",
    size=18, color=CREAM, bold=True)
txt(page, MG, 1270 * S,
    "Follow https://www.amana-capital-ea.co.tz/ for the full institutional data breakdown.",
    size=18, color=GOLD)

# ── AMANA LOGO (bottom-left) ──────────────────────────────────────────────────
LX, LY = MG, 1296 * S
sh = page.new_shape()
sh.draw_quad(fitz.Quad(
    (LX + 20 * S, LY),     (LX + 30 * S, LY),
    (LX,          LY + 50 * S), (LX + 10 * S, LY + 50 * S),
))
sh.finish(fill=GOLD, color=GOLD)
sh.draw_rect(fitz.Rect(LX + 34 * S, LY, LX + 46 * S, LY + 50 * S))
sh.finish(fill=GOLD, color=GOLD)
sh.draw_rect(fitz.Rect(LX, LY + 21 * S, LX + 34 * S, LY + 27 * S))
sh.finish(fill=GOLD, color=GOLD)
sh.commit()

txt(page, LX + 60 * S, LY + 22 * S, "AMANA CAPITAL",       size=19, color=CREAM, bold=True)
txt(page, LX + 60 * S, LY + 42 * S, "East Africa Limited", size=15, color=GOLD)

# ── SAVE ──────────────────────────────────────────────────────────────────────
out = r"C:\Users\tmalu\Desktop\Amana_DSE_Daily_Wrap_22Sep_PERSONAL_HQ.pdf"
doc.save(out, garbage=4, deflate=True, clean=True, linear=False)
doc.close()
print("Saved:", out)
