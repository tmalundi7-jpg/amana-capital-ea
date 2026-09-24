import fitz
import math

# --- Brand Palette ---
NAVY     = (11/255,  29/255,  58/255)
CREAM    = (251/255, 247/255, 240/255)
GOLD     = (200/255, 150/255, 46/255)
RED      = (220/255, 38/255,  38/255)
GREEN    = (22/255,  163/255, 74/255)
TAUPE    = (154/255, 148/255, 144/255)
BEIGE    = (213/255, 207/255, 199/255)

W, H = 1080, 1080
MARGIN = 100
TEXT_W  = W - MARGIN * 2

# --- Helpers ---
def rect(shape, x0, y0, x1, y1, fill=None, stroke=None, width=1):
    shape.draw_rect(fitz.Rect(x0, y0, x1, y1))
    shape.finish(fill=fill, color=stroke, width=width)

def circle(shape, cx, cy, r, fill=None, stroke=None, width=1):
    shape.draw_circle((cx, cy), r)
    shape.finish(fill=fill, color=stroke, width=width)

def txt(page, x, y, text, size=24, color=CREAM, bold=False, font="helv"):
    fn = "hebo" if bold else "helv"
    page.insert_text((x, y), text, fontname=fn, fontsize=size, color=color)

def txt_right(page, x, y, text, size=24, color=CREAM, bold=False):
    fn = "hebo" if bold else "helv"
    tw = fitz.get_text_length(text, fontname=fn, fontsize=size)
    page.insert_text((x - tw, y), text, fontname=fn, fontsize=size, color=color)

def page_template(doc, bg, current_page, total_pages):
    page = doc.new_page(width=W, height=H)
    is_dark = (bg == NAVY)
    shape = page.new_shape()
    rect(shape, 0, 0, W, H, fill=bg)
    rect(shape, 0, 0, W, 6, fill=GOLD)
    shape.commit()
    
    shape = page.new_shape()
    dot_r = 5
    gap = 22
    total_w = total_pages * gap
    start_x = W - MARGIN - total_w + 11
    dot_y = 75
    for i in range(total_pages):
        cx = start_x + i * gap
        col = GOLD if i == current_page else (BEIGE if is_dark else (0.75, 0.72, 0.68))
        circle(shape, cx, dot_y, dot_r, fill=col)
    shape.commit()
    
    shape = page.new_shape()
    rule_y = 956
    shape.draw_line((MARGIN, rule_y), (W - MARGIN, rule_y))
    shape.finish(color=GOLD, width=1)
    shape.commit()
    
    lx, ly = MARGIN + 10, 984.8
    shape = page.new_shape()
    q = fitz.Quad((130.8, 984.8), (140.4, 984.8), (110.0, 1055.2), (119.6, 1055.2))
    shape.draw_quad(q)
    shape.finish(fill=GOLD, color=GOLD)
    shape.draw_rect(fitz.Rect(143.6, 984.8, 156.4, 1055.2))
    shape.finish(fill=GOLD, color=GOLD)
    shape.draw_rect(fitz.Rect(110.0, 1015.2, 143.6, 1021.6))
    shape.finish(fill=GOLD, color=GOLD)
    shape.commit()
    
    txt(page, 162.8, 1016.0, "AMANA CAPITAL", size=19, color=CREAM if is_dark else NAVY, bold=True)
    txt(page, 162.8, 1036.0, "East Africa Limited", size=15, color=GOLD)
    
    return page, is_dark

def section_label(page, label, y=110, is_dark=True):
    shape = page.new_shape()
    rect(shape, MARGIN, y, MARGIN+10, y+38, fill=GOLD)
    shape.commit()
    txt(page, MARGIN+16, y+30, label, size=34, color=GOLD, bold=True)

def draw_donut(page, cx, cy, r_outer, r_inner, segments, colors, center_text=None, center_text_color=CREAM, legend_x=None, legend_y=None, legend_labels=None, legend_color=CREAM, hole_color=NAVY):
    total = sum(segments)
    start_angle = -math.pi / 2
    for seg, col in zip(segments, colors):
        angle = (seg / total) * 2 * math.pi
        if seg / total < 0.001:
            start_angle += angle
            continue
        end_angle = start_angle + angle
        steps = max(int(angle * 25), 3)
        pts = [(cx, cy)]
        for s in range(steps + 1):
            a = start_angle + s * angle / steps
            pts.append((cx + r_outer * math.cos(a), cy + r_outer * math.sin(a)))
        pts.append((cx, cy))
        shape = page.new_shape()
        shape.draw_polyline(pts)
        shape.finish(fill=col, color=col, width=0.5)
        shape.commit()
        start_angle = end_angle
    shape = page.new_shape()
    circle(shape, cx, cy, r_inner, fill=hole_color)
    shape.commit()
    if center_text:
        tw = fitz.get_text_length(center_text, fontname="hebo", fontsize=18)
        page.insert_text((cx - tw/2, cy + 7), center_text, fontname="hebo", fontsize=18, color=center_text_color)
    if legend_labels and legend_x is not None:
        for i, (lbl, col) in enumerate(zip(legend_labels, colors)):
            lx = legend_x + i * 180
            shape = page.new_shape()
            rect(shape, lx, legend_y, lx + 14, legend_y + 14, fill=col)
            shape.commit()
            page.insert_text((lx + 20, legend_y + 12), lbl, fontname="helv", fontsize=16, color=legend_color)

# --- PDF Builder ---
doc = fitz.open()
TOTAL = 6

# PAGE 1: COVER
page, is_dark = page_template(doc, NAVY, 0, TOTAL)
section_label(page, "DAILY DSE WRAP", y=110, is_dark=True)
txt(page, MARGIN, 280, "VODA", size=112, color=CREAM, bold=True)
txt(page, MARGIN, 392, "HITS THE", size=112, color=CREAM, bold=True)
txt(page, MARGIN, 504, "CEILING.", size=112, color=GOLD, bold=True)
txt(page, MARGIN, 610, "When a stock hits the 5% daily limit and the order book is wiped clean.", size=24, color=TAUPE)
txt(page, MARGIN, 650, "Tuesday, 22 September 2026", size=24, color=TAUPE)

# PAGE 2: MACRO STATS
page, is_dark = page_template(doc, CREAM, 1, TOTAL)
section_label(page, "MACRO", y=110, is_dark=False)
txt(page, MARGIN, 240, "THE DSEI", size=88, color=NAVY, bold=True)
txt(page, MARGIN, 328, "POST-SPLIT", size=88, color=NAVY, bold=True)
txt(page, MARGIN, 416, "HIGH.", size=88, color=GOLD, bold=True)

txt(page, MARGIN, 500, "DSEI closed at 4,659.23 (+25 points)", size=24, color=NAVY)
txt(page, MARGIN, 540, "TSI closed at 10,359.92 (+59 points)", size=24, color=NAVY)

txt(page, MARGIN, 640, "Turnover Comparison (TZS Billion)", size=20, color=NAVY, bold=True)
txt(page, MARGIN, 690, "Equity", size=18, color=NAVY)
shape = page.new_shape()
rect(shape, MARGIN + 100, 675, MARGIN + 100 + int(5.07/33.59 * 400), 695, fill=NAVY)
shape.commit()
txt(page, MARGIN + 110 + int(5.07/33.59 * 400), 690, "5.07B", size=16, color=NAVY, bold=True)

txt(page, MARGIN, 730, "Bonds", size=18, color=NAVY)
shape = page.new_shape()
rect(shape, MARGIN + 100, 715, MARGIN + 100 + 400, 735, fill=GOLD)
shape.commit()
txt(page, MARGIN + 510, 730, "33.59B (485% jump)", size=16, color=GOLD, bold=True)


# PAGE 3: ORDER BOOK
page, is_dark = page_template(doc, NAVY, 2, TOTAL)
section_label(page, "MARKET DEPTH", y=110, is_dark=True)
txt(page, MARGIN, 240, "THE TALE OF", size=88, color=CREAM, bold=True)
txt(page, MARGIN, 328, "TWO COUNTERS.", size=88, color=GOLD, bold=True)

shape = page.new_shape()
rect(shape, MARGIN, 420, MARGIN + 400, 750, fill=CREAM)
shape.commit()
txt(page, MARGIN + 40, 480, "VODA", size=36, color=NAVY, bold=True)
txt(page, MARGIN + 40, 530, "+4.8% (1,320)", size=28, color=GREEN, bold=True)
txt(page, MARGIN + 40, 590, "Limit-Up Close", size=20, color=NAVY)
txt(page, MARGIN + 40, 640, "Bids: 23,119", size=24, color=NAVY, bold=True)
txt(page, MARGIN + 40, 680, "Offers: 24,814", size=24, color=NAVY)

shape = page.new_shape()
rect(shape, MARGIN + 440, 420, MARGIN + 840, 750, fill=CREAM)
shape.commit()
txt(page, MARGIN + 480, 480, "CRDB", size=36, color=NAVY, bold=True)
txt(page, MARGIN + 480, 530, "FLAT (2,810)", size=28, color=TAUPE, bold=True)
txt(page, MARGIN + 480, 590, "Absorbed 868k block", size=20, color=NAVY)
txt(page, MARGIN + 480, 640, "Bids: 192,156", size=24, color=NAVY, bold=True)
txt(page, MARGIN + 480, 680, "Offers: 49,819", size=24, color=NAVY)
txt(page, MARGIN + 480, 720, "Ratio: 3.9x Buyers", size=18, color=GOLD, bold=True)

# PAGE 4: FLOWS
page, is_dark = page_template(doc, CREAM, 3, TOTAL)
section_label(page, "FLOWS", y=110, is_dark=False)
txt(page, MARGIN, 240, "LOCAL", size=88, color=NAVY, bold=True)
txt(page, MARGIN, 328, "INSTITUTIONS", size=88, color=NAVY, bold=True)
txt(page, MARGIN, 416, "TAKE CONTROL.", size=88, color=GOLD, bold=True)

draw_donut(
    page, cx=MARGIN+200, cy=680, r_outer=150, r_inner=80, 
    segments=[99.88, 0.12], colors=[NAVY, GOLD], 
    center_text="Buying", center_text_color=NAVY, 
    legend_x=MARGIN, legend_y=870, legend_labels=["Local (99.88%)", "Foreign (0.12%)"], legend_color=NAVY, hole_color=CREAM
)

txt(page, MARGIN + 420, 600, "Foreign exits were completely", size=28, color=NAVY, bold=True)
txt(page, MARGIN + 420, 640, "absorbed.", size=28, color=NAVY, bold=True)
txt(page, MARGIN + 420, 700, "Foreign selling surged to 57.58%", size=20, color=TAUPE)
txt(page, MARGIN + 420, 730, "of total equity turnover (TZS 2.92B).", size=20, color=TAUPE)
txt(page, MARGIN + 420, 780, "But local capital stepped in and", size=20, color=NAVY)
txt(page, MARGIN + 420, 810, "devoured 99.88% of all shares offered.", size=20, color=NAVY)


# PAGE 5: BONDS
page, is_dark = page_template(doc, NAVY, 4, TOTAL)
section_label(page, "FIXED INCOME", y=110, is_dark=True)
txt(page, MARGIN, 280, "BONDS", size=112, color=CREAM, bold=True)
txt(page, MARGIN, 392, "EXPLODE.", size=112, color=GOLD, bold=True)

txt(page, MARGIN, 500, "Government bond turnover skyrocketed 485%", size=32, color=CREAM)
txt(page, MARGIN, 550, "to TZS 33.59 billion in a single session.", size=32, color=CREAM)

txt(page, MARGIN, 640, "Most Active Instrument:", size=24, color=TAUPE)
shape = page.new_shape()
rect(shape, MARGIN, 680, MARGIN + 880, 820, fill=CREAM)
shape.commit()

txt(page, MARGIN + 40, 730, "20-Year 12.00% Bond (Mar 2026)", size=28, color=NAVY, bold=True)
txt(page, MARGIN + 40, 780, "Traded: TZS 30.00B", size=24, color=NAVY)
txt(page, MARGIN + 340, 780, "Yield: 10.71%", size=24, color=GOLD, bold=True)


# PAGE 6: EPILOGUE
page, is_dark = page_template(doc, CREAM, 5, TOTAL)
section_label(page, "EPILOGUE", y=110, is_dark=False)
txt(page, MARGIN, 240, "AMANA", size=88, color=NAVY, bold=True)
txt(page, MARGIN, 328, "CAPITAL'S", size=88, color=NAVY, bold=True)
txt(page, MARGIN, 416, "VIEW.", size=88, color=GOLD, bold=True)

txt(page, MARGIN, 520, "For the multi-year investor, Tuesday's message is clear:", size=28, color=NAVY, bold=True)
txt(page, MARGIN, 580, "This is a market that rewards patience and education.", size=24, color=NAVY)
txt(page, MARGIN, 630, "Different stocks tell different stories. VODA is seeing", size=24, color=TAUPE)
txt(page, MARGIN, 670, "aggressive pre-dividend accumulation, while CRDB pauses", size=24, color=TAUPE)
txt(page, MARGIN, 710, "heavily bid. The crowd chases sharp price moves, but the", size=24, color=TAUPE)
txt(page, MARGIN, 750, "wise investor reads the order books and respects the", size=24, color=TAUPE)
txt(page, MARGIN, 790, "exchange's price bands.", size=24, color=TAUPE)

txt(page, MARGIN, 860, "Follow https://www.amana-capital-ea.co.tz/ for unfiltered market psychology.", size=19, color=GOLD, bold=True)

# Save
out_path = r'C:\Users\tmalu\Desktop\Amana_DSE_Daily_Wrap_22Sep_COMPANY_v3.pdf'
doc.save(out_path, garbage=4, deflate=True)
doc.close()
print("Saved:", out_path)
