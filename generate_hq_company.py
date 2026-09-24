"""
High-Resolution LinkedIn-Optimised PDF Generator
Company Carousel — 3x Scale (3240 x 3240 px per page)
LinkedIn rasterises each page; starting at 3x means post-compression
output still looks crisp on Retina / high-DPI screens.
"""

import fitz  # PyMuPDF
import math

# ── Palette ──────────────────────────────────────────────────────────────────
NAVY   = (11/255,  29/255,  58/255)
CREAM  = (251/255, 247/255, 240/255)
GOLD   = (200/255, 150/255, 46/255)
RED    = (220/255,  38/255,  38/255)
GREEN  = (22/255,  163/255,  74/255)
TAUPE  = (154/255, 148/255, 144/255)
BEIGE  = (213/255, 207/255, 199/255)

# ── Canvas — 3× the original 1080 so LinkedIn's downscale stays sharp ────────
S      = 3          # scale factor
W, H   = 1080 * S, 1080 * S   # 3240 × 3240
MG     = 100 * S               # margin
TOTAL  = 8


# ── Primitive helpers ────────────────────────────────────────────────────────
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


# ── Page chrome: background / gold bar / dots / logo / rule ──────────────────
def page_template(doc, bg, idx, total):
    page = doc.new_page(width=W, height=H)
    dark = (bg == NAVY)
    sh = page.new_shape()
    rct(sh, 0, 0, W, H, fill=bg)
    rct(sh, 0, 0, W, 6 * S, fill=GOLD)
    sh.commit()

    # pagination dots
    sh = page.new_shape()
    dr, gap = 5 * S, 22 * S
    sx = W - MG - total * gap + 11 * S
    for i in range(total):
        cx = sx + i * gap
        col = GOLD if i == idx else (BEIGE if dark else (0.75, 0.72, 0.68))
        cir(sh, cx, 75 * S, dr, fill=col)
    sh.commit()

    # footer rule
    sh = page.new_shape()
    ry = 956 * S
    sh.draw_line((MG, ry), (W - MG, ry))
    sh.finish(color=GOLD, width=2 * S)
    sh.commit()

    # Amana logo (abstract A mark)
    _draw_logo(page, MARGIN=MG, is_dark=dark)
    return page, dark


def _draw_logo(page, MARGIN, is_dark):
    lx = MARGIN
    # vertical offset places logo between footer rule and bottom edge
    base = H - 110 * S   # ~1040*S
    sh = page.new_shape()
    # diagonal left stroke
    q = fitz.Quad(
        (lx + 20 * S, base),
        (lx + 30 * S, base),
        (lx,          base + 70 * S),
        (lx + 10 * S, base + 70 * S),
    )
    sh.draw_quad(q)
    sh.finish(fill=GOLD, color=GOLD)
    # vertical right stroke
    sh.draw_rect(fitz.Rect(lx + 33 * S, base, lx + 46 * S, base + 70 * S))
    sh.finish(fill=GOLD, color=GOLD)
    # crossbar
    sh.draw_rect(fitz.Rect(lx, base + 30 * S, lx + 33 * S, base + 36 * S))
    sh.finish(fill=GOLD, color=GOLD)
    sh.commit()

    text_color = CREAM if is_dark else NAVY
    txt(page, lx + 58 * S, base + 32 * S, "AMANA CAPITAL",   size=19, color=text_color, bold=True)
    txt(page, lx + 58 * S, base + 52 * S, "East Africa Limited", size=15, color=GOLD)


def section_label(page, label, y=110, is_dark=True):
    sh = page.new_shape()
    rct(sh, MG, y * S, MG + 10 * S, (y + 38) * S, fill=GOLD)
    sh.commit()
    txt(page, MG + 16 * S, (y + 30) * S, label, size=34, color=GOLD, bold=True)


# ── Horizontal bar chart ──────────────────────────────────────────────────────
def draw_hbar(page, x, y, label, val, val_str, max_val, max_w,
              bar_color, label_color, lbl_size=24, val_size=20):
    txt(page, x, y, label, size=lbl_size, color=label_color, bold=True)
    lw = txt_len(label, size=lbl_size, bold=True) + 20 * S
    bw = max(8 * S, int((val / max_val) * max_w * S))
    sh = page.new_shape()
    rct(sh, x + lw, y - 20 * S, x + lw + bw, y + 4 * S, fill=bar_color)
    sh.commit()
    txt(page, x + lw + bw + 12 * S, y, val_str, size=val_size, color=label_color, bold=True)


# ── Donut chart ────────────────────────────────────────────────────────────────
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
        tw = txt_len(center_text, size=18, bold=True)
        page.insert_text((cx - tw / 2, cy + 7 * S),
                         center_text, fontname="hebo", fontsize=18 * S, color=ct_color)
    if legend_labels and legend_x is not None:
        for i, (lbl, col) in enumerate(zip(legend_labels, colors)):
            ly2 = legend_y + i * 28 * S
            sh = page.new_shape()
            rct(sh, legend_x, ly2, legend_x + 14 * S, ly2 + 14 * S, fill=col)
            sh.commit()
            page.insert_text((legend_x + 20 * S, ly2 + 12 * S),
                             lbl, fontname="helv", fontsize=16 * S, color=leg_color)


# ════════════════════════════════════════════════════════════════════════════════
# BUILD PDF
# ════════════════════════════════════════════════════════════════════════════════
doc = fitz.open()

# ── PAGE 1 · COVER ─────────────────────────────────────────────────────────────
pg, dark = page_template(doc, NAVY, 0, TOTAL)
section_label(pg, "DAILY DSE WRAP", y=110)
txt(pg, MG, 280 * S, "VODA",     size=112, color=CREAM, bold=True)
txt(pg, MG, 392 * S, "HITS THE", size=112, color=CREAM, bold=True)
txt(pg, MG, 504 * S, "CEILING.", size=112, color=GOLD,  bold=True)
txt(pg, MG, 610 * S, "When a stock hits the 5% daily limit and the order book is wiped clean.", size=24, color=TAUPE)
txt(pg, MG, 650 * S, "Tuesday, 22 September 2026", size=24, color=TAUPE)

# ── PAGE 2 · MACRO ─────────────────────────────────────────────────────────────
pg, dark = page_template(doc, CREAM, 1, TOTAL)
section_label(pg, "MACRO", y=110, is_dark=False)
txt(pg, MG, 240 * S, "THE DSEI",    size=88, color=NAVY, bold=True)
txt(pg, MG, 328 * S, "POST-SPLIT",  size=88, color=NAVY, bold=True)
txt(pg, MG, 416 * S, "HIGH.",        size=88, color=GOLD, bold=True)
txt(pg, MG, 500 * S, "DSEI closed at 4,659.23  (+25 points)", size=24, color=NAVY)
txt(pg, MG, 540 * S, "TSI closed at 10,359.92  (+59 points)", size=24, color=NAVY)
txt(pg, MG, 600 * S, "Turnover Breakdown (TZS)", size=22, color=NAVY, bold=True)
draw_hbar(pg, MG, 670 * S, "Bonds  ", 33.59, "33.59 Billion", 33.59, 460, GOLD, NAVY)
draw_hbar(pg, MG, 730 * S, "Equity ", 5.07,  "5.07 Billion",  33.59, 460, NAVY, NAVY)
txt(pg, MG, 800 * S, "Bond turnover skyrocketed 485% in a single session.", size=20, color=TAUPE)

# ── PAGE 3 · VODA ORDER BOOK ───────────────────────────────────────────────────
pg, dark = page_template(doc, NAVY, 2, TOTAL)
section_label(pg, "MARKET DEPTH", y=110)
txt(pg, MG, 240 * S, "VODA: ZERO",   size=88, color=CREAM, bold=True)
txt(pg, MG, 328 * S, "SELLERS AT",   size=88, color=CREAM, bold=True)
txt(pg, MG, 416 * S, "THE TOP.",      size=88, color=GOLD,  bold=True)
txt(pg, MG, 500 * S, "VODA surged 4.8% to 1,320, hitting the exact 5% ceiling", size=24, color=CREAM)
txt(pg, MG, 540 * S, "after absorbing a 1-million-share block on Monday.", size=24, color=CREAM)
txt(pg, MG, 620 * S, "Order Book Dynamics:", size=24, color=TAUPE, bold=True)
draw_hbar(pg, MG, 690 * S, "Offers", 24814, "24,814 shares", 25000, 460, GOLD,  CREAM)
draw_hbar(pg, MG, 760 * S, "Bids  ", 23119, "23,119 shares", 25000, 460, CREAM, CREAM)
txt(pg, MG, 830 * S, "The book is balanced, but the price physically could not go higher today.", size=20, color=TAUPE)

# ── PAGE 4 · CRDB ORDER BOOK ───────────────────────────────────────────────────
pg, dark = page_template(doc, NAVY, 3, TOTAL)
section_label(pg, "MARKET DEPTH", y=110)
txt(pg, MG, 240 * S, "CRDB: THE",  size=88, color=CREAM, bold=True)
txt(pg, MG, 328 * S, "STEALTH",    size=88, color=CREAM, bold=True)
txt(pg, MG, 416 * S, "DEMAND.",    size=88, color=GOLD,  bold=True)
txt(pg, MG, 500 * S, "CRDB absorbed a massive 868,000-share block from foreign", size=24, color=CREAM)
txt(pg, MG, 540 * S, "exits. On the surface, the price closed perfectly FLAT at 2,810.", size=24, color=CREAM)
txt(pg, MG, 620 * S, "The Hidden Order Book (3.9x Ratio):", size=24, color=TAUPE, bold=True)
draw_hbar(pg, MG, 690 * S, "Bids  ", 192156, "192,156 shares", 192156, 460, CREAM, CREAM)
draw_hbar(pg, MG, 760 * S, "Offers", 49819,  "49,819 shares",  192156, 460, GOLD,  CREAM)
txt(pg, MG, 830 * S, "Buyers are lined up. Local institutions are eagerly digesting the supply.", size=20, color=TAUPE)

# ── PAGE 5 · FLOWS ─────────────────────────────────────────────────────────────
pg, dark = page_template(doc, CREAM, 4, TOTAL)
section_label(pg, "CAPITAL FLOWS", y=110, is_dark=False)
txt(pg, MG, 240 * S, "LOCAL",          size=88, color=NAVY, bold=True)
txt(pg, MG, 328 * S, "INSTITUTIONS",   size=88, color=NAVY, bold=True)
txt(pg, MG, 416 * S, "TAKE CONTROL.",  size=88, color=GOLD, bold=True)
txt(pg, MG, 490 * S, "Foreign exits accounted for 57.58% (TZS 2.92B) of all supply.", size=24, color=TAUPE, bold=True)
# Selling donut
draw_donut(pg, cx=MG + 180 * S, cy=660 * S, r_out=120 * S, r_in=60 * S,
           segments=[42.42, 57.58], colors=[NAVY, GOLD],
           center_text="Selling", ct_color=NAVY, hole_color=CREAM,
           legend_x=MG + 30 * S, legend_y=800 * S,
           legend_labels=["Local 42%", "Foreign 58%"], leg_color=NAVY)
# Buying donut
draw_donut(pg, cx=MG + 650 * S, cy=660 * S, r_out=120 * S, r_in=60 * S,
           segments=[99.88, 0.12], colors=[NAVY, GOLD],
           center_text="Buying", ct_color=NAVY, hole_color=CREAM,
           legend_x=MG + 500 * S, legend_y=800 * S,
           legend_labels=["Local 99.88%", "Foreign 0.12%"], leg_color=NAVY)
txt(pg, MG + 300 * S, 570 * S, "Selling", size=22, color=TAUPE, bold=True)
txt(pg, MG + 760 * S, 570 * S, "Buying",  size=22, color=TAUPE, bold=True)

# ── PAGE 6 · BOND BREAKDOWN ────────────────────────────────────────────────────
pg, dark = page_template(doc, NAVY, 5, TOTAL)
section_label(pg, "FIXED INCOME", y=110)
txt(pg, MG, 240 * S, "WHERE THE",    size=88, color=CREAM, bold=True)
txt(pg, MG, 328 * S, "BILLIONS",     size=88, color=CREAM, bold=True)
txt(pg, MG, 416 * S, "ARE GOING.",   size=88, color=GOLD,  bold=True)
txt(pg, MG, 498 * S, "Govt bond turnover skyrocketed 485% to TZS 33.59 billion.", size=24, color=CREAM)
txt(pg, MG, 576 * S, "Bond Allocation:", size=24, color=TAUPE, bold=True)
# Bond donut — pushed far right to avoid text collision
draw_donut(pg, cx=MG + 700 * S, cy=740 * S, r_out=140 * S, r_in=70 * S,
           segments=[30.00, 1.77, 0.71, 0.63], colors=[GOLD, BEIGE, CREAM, TAUPE],
           center_text="33.59B", ct_color=CREAM, hole_color=NAVY)
txt(pg, MG, 640 * S, "20-Yr Mar 2026: TZS 30.00B  (89%)", size=20, color=GOLD,  bold=True)
txt(pg, MG, 690 * S, "20-Yr Jul 2026: TZS 1.77B   (5%)",  size=20, color=BEIGE)
txt(pg, MG, 740 * S, "15-Yr Feb 2024: TZS 0.71B   (2%)",  size=20, color=CREAM)
txt(pg, MG, 790 * S, "5-Yr  Apr 2026: TZS 0.63B   (2%)",  size=20, color=TAUPE)
txt(pg, MG, 850 * S, "Yield locked in on the 20-Year: 10.71% tax-free.", size=24, color=CREAM, bold=True)

# ── PAGE 7 · MARKET MOVERS ─────────────────────────────────────────────────────
pg, dark = page_template(doc, CREAM, 6, TOTAL)
section_label(pg, "MARKET MOVERS", y=110, is_dark=False)
txt(pg, MG, 240 * S, "THE DAY'S", size=88, color=NAVY, bold=True)
txt(pg, MG, 328 * S, "BIGGEST",   size=88, color=NAVY, bold=True)
txt(pg, MG, 416 * S, "SWINGS.",   size=88, color=GOLD, bold=True)
txt(pg, MG, 530 * S, "Top Gainers", size=28, color=GREEN, bold=True)
draw_hbar(pg, MG, 600 * S, "AFRIPRISE", 5.4, "+5.4%", 5.4, 350, GREEN, NAVY)
draw_hbar(pg, MG, 665 * S, "VODA      ", 4.8, "+4.8%", 5.4, 350, GREEN, NAVY)
txt(pg, MG, 730 * S, "Top Losers",  size=28, color=RED, bold=True)
draw_hbar(pg, MG, 800 * S, "TCCL", 5.1, "-5.1%", 5.4, 350, RED, NAVY)
txt(pg, MG, 875 * S, "TCCL gave back gains after rising sharply in recent sessions.", size=20, color=TAUPE)

# ── PAGE 8 · EPILOGUE ──────────────────────────────────────────────────────────
pg, dark = page_template(doc, NAVY, 7, TOTAL)
section_label(pg, "EPILOGUE", y=110)
txt(pg, MG, 240 * S, "AMANA",     size=88, color=CREAM, bold=True)
txt(pg, MG, 328 * S, "CAPITAL'S", size=88, color=CREAM, bold=True)
txt(pg, MG, 416 * S, "VIEW.",     size=88, color=GOLD,  bold=True)
txt(pg, MG, 510 * S, "For the multi-year investor, Tuesday's message is clear:", size=28, color=GOLD,  bold=True)
txt(pg, MG, 570 * S, "This is a market that rewards patience and education.", size=24, color=CREAM)
txt(pg, MG, 620 * S, "Different stocks tell different stories. VODA is seeing",  size=24, color=TAUPE)
txt(pg, MG, 665 * S, "aggressive pre-dividend accumulation, while CRDB pauses", size=24, color=TAUPE)
txt(pg, MG, 710 * S, "heavily bid. The crowd chases sharp price moves, but the", size=24, color=TAUPE)
txt(pg, MG, 755 * S, "wise investor reads the order books and respects the",    size=24, color=TAUPE)
txt(pg, MG, 800 * S, "exchange's price bands.",                                  size=24, color=TAUPE)
txt(pg, MG, 870 * S, "Follow https://www.amana-capital-ea.co.tz/ for unfiltered market psychology.", size=20, color=GOLD, bold=True)

# ── SAVE — maximum quality PDF settings ────────────────────────────────────────
out = r"C:\Users\tmalu\Desktop\Amana_DSE_Daily_Wrap_22Sep_COMPANY_HQ.pdf"
doc.save(out,
         garbage=4,        # full cross-reference rebuild
         deflate=True,     # compress streams
         clean=True,       # sanitise content streams
         linear=False)     # not needed for LinkedIn documents
doc.close()
print("Saved:", out)
