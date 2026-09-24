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

def rect(shape, x0, y0, x1, y1, fill=None, stroke=None, width=1):
    shape.draw_rect(fitz.Rect(x0, y0, x1, y1))
    shape.finish(fill=fill, color=stroke, width=width)

def circle(shape, cx, cy, r, fill=None, stroke=None, width=1):
    shape.draw_circle((cx, cy), r)
    shape.finish(fill=fill, color=stroke, width=width)

def txt(page, x, y, text, size=24, color=CREAM, bold=False):
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

def draw_h_bar(page, x, y, label, value_num, val_str, max_val, max_w, bar_color, label_color):
    txt(page, x, y, label, size=24, color=label_color, bold=True)
    bw = max(5, int((value_num / max_val) * max_w))
    shape = page.new_shape()
    rect(shape, x + 150, y - 24, x + 150 + bw, y + 4, fill=bar_color)
    shape.commit()
    txt(page, x + 160 + bw, y, val_str, size=20, color=label_color, bold=True)

# --- Build PDF ---
doc = fitz.open()
TOTAL = 8

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

txt(page, MARGIN, 640, "Turnover Breakdown (TZS)", size=22, color=NAVY, bold=True)
draw_h_bar(page, MARGIN, 700, "Bonds", 33.59, "33.59 Billion", 33.59, 500, GOLD, NAVY)
draw_h_bar(page, MARGIN, 760, "Equity", 5.07, "5.07 Billion", 33.59, 500, NAVY, NAVY)
txt(page, MARGIN, 830, "Bond turnover skyrocketed 485% in a single session.", size=20, color=TAUPE)

# PAGE 3: ORDER BOOK VODA
page, is_dark = page_template(doc, NAVY, 2, TOTAL)
section_label(page, "MARKET DEPTH", y=110, is_dark=True)
txt(page, MARGIN, 240, "VODA: ZERO", size=88, color=CREAM, bold=True)
txt(page, MARGIN, 328, "SELLERS AT", size=88, color=CREAM, bold=True)
txt(page, MARGIN, 416, "THE TOP.", size=88, color=GOLD, bold=True)

txt(page, MARGIN, 500, "VODA surged 4.8% to 1,320, hitting the exact 5% ceiling", size=24, color=CREAM)
txt(page, MARGIN, 540, "after absorbing a 1-million-share block on Monday.", size=24, color=CREAM)

txt(page, MARGIN, 640, "Order Book Dynamics:", size=24, color=TAUPE, bold=True)
draw_h_bar(page, MARGIN, 700, "Offers", 24814, "24,814 shares", 25000, 500, GOLD, CREAM)
draw_h_bar(page, MARGIN, 760, "Bids", 23119, "23,119 shares", 25000, 500, CREAM, CREAM)
txt(page, MARGIN, 830, "The book is balanced, but the price physically could not go higher today.", size=20, color=TAUPE)

# PAGE 4: ORDER BOOK CRDB
page, is_dark = page_template(doc, NAVY, 3, TOTAL)
section_label(page, "MARKET DEPTH", y=110, is_dark=True)
txt(page, MARGIN, 240, "CRDB: THE", size=88, color=CREAM, bold=True)
txt(page, MARGIN, 328, "STEALTH", size=88, color=CREAM, bold=True)
txt(page, MARGIN, 416, "DEMAND.", size=88, color=GOLD, bold=True)

txt(page, MARGIN, 500, "CRDB absorbed a massive 868,000-share block from foreign", size=24, color=CREAM)
txt(page, MARGIN, 540, "exits. On the surface, the price closed perfectly FLAT at 2,810.", size=24, color=CREAM)

txt(page, MARGIN, 640, "The Hidden Order Book (3.9x Ratio):", size=24, color=TAUPE, bold=True)
draw_h_bar(page, MARGIN, 700, "Bids", 192156, "192,156 shares", 192156, 500, CREAM, CREAM)
draw_h_bar(page, MARGIN, 760, "Offers", 49819, "49,819 shares", 192156, 500, GOLD, CREAM)
txt(page, MARGIN, 830, "Buyers are lined up. Local institutions are eagerly digesting the supply.", size=20, color=TAUPE)

# PAGE 5: FLOWS
page, is_dark = page_template(doc, CREAM, 4, TOTAL)
section_label(page, "CAPITAL FLOWS", y=110, is_dark=False)
txt(page, MARGIN, 240, "LOCAL", size=88, color=NAVY, bold=True)
txt(page, MARGIN, 328, "INSTITUTIONS", size=88, color=NAVY, bold=True)
txt(page, MARGIN, 416, "TAKE CONTROL.", size=88, color=GOLD, bold=True)

# Selling Donut
draw_donut(
    page, cx=MARGIN+180, cy=660, r_outer=130, r_inner=60, 
    segments=[42.42, 57.58], colors=[NAVY, GOLD], 
    center_text="Selling", center_text_color=NAVY, 
    legend_x=MARGIN+30, legend_y=830, legend_labels=["Local 42%", "Foreign 58%"], legend_color=NAVY, hole_color=CREAM
)
# Buying Donut
draw_donut(
    page, cx=MARGIN+650, cy=660, r_outer=130, r_inner=60, 
    segments=[99.88, 0.12], colors=[NAVY, GOLD], 
    center_text="Buying", center_text_color=NAVY, 
    legend_x=MARGIN+500, legend_y=830, legend_labels=["Local 99.88%", "Foreign 0.12%"], legend_color=NAVY, hole_color=CREAM
)
txt(page, MARGIN, 500, "Foreign exits accounted for 57.58% (TZS 2.92B) of all supply.", size=24, color=TAUPE, bold=True)


# PAGE 6: BOND BREAKDOWN
page, is_dark = page_template(doc, NAVY, 5, TOTAL)
section_label(page, "FIXED INCOME", y=110, is_dark=True)
txt(page, MARGIN, 240, "WHERE THE", size=88, color=CREAM, bold=True)
txt(page, MARGIN, 328, "BILLIONS", size=88, color=CREAM, bold=True)
txt(page, MARGIN, 416, "ARE GOING.", size=88, color=GOLD, bold=True)

txt(page, MARGIN, 500, "Government bond turnover skyrocketed 485% to TZS 33.59 billion.", size=24, color=CREAM)
txt(page, MARGIN, 580, "Bond Allocation Breakdown:", size=24, color=TAUPE, bold=True)

draw_donut(
    page, cx=MARGIN+580, cy=740, r_outer=140, r_inner=70, 
    segments=[30.00, 1.77, 0.71, 0.63], colors=[GOLD, BEIGE, CREAM, TAUPE], 
    center_text="33.59B", center_text_color=CREAM, 
    hole_color=NAVY
)
# Manual legend
txt(page, MARGIN, 660, "20-Year (Mar 2026): TZS 30.00B (89%)", size=20, color=GOLD, bold=True)
txt(page, MARGIN, 700, "20-Year (Jul 2026): TZS 1.77B (5%)", size=20, color=BEIGE)
txt(page, MARGIN, 740, "15-Year (Feb 2024): TZS 0.71B (2%)", size=20, color=CREAM)
txt(page, MARGIN, 780, "5-Year (Apr 2026): TZS 0.63B (2%)", size=20, color=TAUPE)
txt(page, MARGIN, 840, "Yield locked in on the 20-Year: 10.71% tax-free.", size=24, color=CREAM, bold=True)

# PAGE 7: TOP MOVERS
page, is_dark = page_template(doc, CREAM, 6, TOTAL)
section_label(page, "MARKET MOVERS", y=110, is_dark=False)
txt(page, MARGIN, 240, "THE DAY'S", size=88, color=NAVY, bold=True)
txt(page, MARGIN, 328, "BIGGEST", size=88, color=NAVY, bold=True)
txt(page, MARGIN, 416, "SWINGS.", size=88, color=GOLD, bold=True)

txt(page, MARGIN, 540, "Top Gainers", size=28, color=GREEN, bold=True)
draw_h_bar(page, MARGIN, 600, "AFRIPRISE", 5.4, "+5.4%", 5.4, 400, GREEN, NAVY)
draw_h_bar(page, MARGIN, 660, "VODA", 4.8, "+4.8%", 5.4, 400, GREEN, NAVY)

txt(page, MARGIN, 740, "Top Losers", size=28, color=RED, bold=True)
draw_h_bar(page, MARGIN, 800, "TCCL", 5.1, "-5.1%", 5.4, 400, RED, NAVY)
txt(page, MARGIN, 880, "TCCL gave back gains after rising sharply in recent sessions.", size=20, color=TAUPE)

# PAGE 8: EPILOGUE
page, is_dark = page_template(doc, NAVY, 7, TOTAL)
section_label(page, "EPILOGUE", y=110, is_dark=True)
txt(page, MARGIN, 240, "AMANA", size=88, color=CREAM, bold=True)
txt(page, MARGIN, 328, "CAPITAL'S", size=88, color=CREAM, bold=True)
txt(page, MARGIN, 416, "VIEW.", size=88, color=GOLD, bold=True)

txt(page, MARGIN, 520, "For the multi-year investor, Tuesday's message is clear:", size=28, color=GOLD, bold=True)
txt(page, MARGIN, 580, "This is a market that rewards patience and education.", size=24, color=CREAM)
txt(page, MARGIN, 630, "Different stocks tell different stories. VODA is seeing", size=24, color=TAUPE)
txt(page, MARGIN, 670, "aggressive pre-dividend accumulation, while CRDB pauses", size=24, color=TAUPE)
txt(page, MARGIN, 710, "heavily bid. The crowd chases sharp price moves, but the", size=24, color=TAUPE)
txt(page, MARGIN, 750, "wise investor reads the order books and respects the", size=24, color=TAUPE)
txt(page, MARGIN, 790, "exchange's price bands.", size=24, color=TAUPE)

txt(page, MARGIN, 860, "Follow https://www.amana-capital-ea.co.tz/ for unfiltered market psychology.", size=20, color=GOLD, bold=True)

# Save
out_path = r'C:\Users\tmalu\Desktop\Amana_DSE_Daily_Wrap_22Sep_COMPANY_v4.pdf'
doc.save(out_path, garbage=4, deflate=True)
doc.close()
print("Saved:", out_path)

