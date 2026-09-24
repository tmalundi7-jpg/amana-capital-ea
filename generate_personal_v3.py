import fitz
import math

NAVY     = (11/255,  29/255,  58/255)
CREAM    = (251/255, 247/255, 240/255)
GOLD     = (200/255, 150/255, 46/255)
RED      = (220/255, 38/255,  38/255)
GREEN    = (22/255,  163/255, 74/255)
TAUPE    = (154/255, 148/255, 144/255)
BEIGE    = (213/255, 207/255, 199/255)

W, H = 1080, 1080
MARGIN = 100

def rect(shape, x0, y0, x1, y1, fill=None, stroke=None, width=1):
    shape.draw_rect(fitz.Rect(x0, y0, x1, y1))
    shape.finish(fill=fill, color=stroke, width=width)

def circle(shape, cx, cy, r, fill=None, stroke=None, width=1):
    shape.draw_circle((cx, cy), r)
    shape.finish(fill=fill, color=stroke, width=width)

def txt(page, x, y, text, size=24, color=CREAM, bold=False):
    fn = "hebo" if bold else "helv"
    page.insert_text((x, y), text, fontname=fn, fontsize=size, color=color)

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

def draw_h_bar(page, x, y, label, value_num, val_str, max_val, max_w, bar_color, label_color):
    txt(page, x, y, label, size=24, color=label_color, bold=True)
    bw = max(5, int((value_num / max_val) * max_w))
    shape = page.new_shape()
    rect(shape, x + 150, y - 24, x + 150 + bw, y + 4, fill=bar_color)
    shape.commit()
    txt(page, x + 160 + bw, y, val_str, size=20, color=label_color, bold=True)

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


doc = fitz.open()
TOTAL = 6

# PAGE 1: COVER
page, is_dark = page_template(doc, NAVY, 0, TOTAL)
section_label(page, "MARKET PSYCHOLOGY", y=110, is_dark=True)
txt(page, MARGIN, 280, "WHEN A", size=112, color=CREAM, bold=True)
txt(page, MARGIN, 392, "STOCK", size=112, color=CREAM, bold=True)
txt(page, MARGIN, 504, "HITS THE", size=112, color=CREAM, bold=True)
txt(page, MARGIN, 616, "CEILING.", size=112, color=GOLD, bold=True)
txt(page, MARGIN, 730, "What happens when price is physically capped,", size=24, color=TAUPE)
txt(page, MARGIN, 770, "but demand refuses to stop?", size=24, color=TAUPE)

# PAGE 2: VODA
page, is_dark = page_template(doc, CREAM, 1, TOTAL)
section_label(page, "THE VISIBLE MOVER", y=110, is_dark=False)
txt(page, MARGIN, 240, "VODA", size=88, color=NAVY, bold=True)
txt(page, MARGIN, 328, "HITS", size=88, color=NAVY, bold=True)
txt(page, MARGIN, 416, "LIMIT-UP.", size=88, color=GOLD, bold=True)

txt(page, MARGIN, 500, "VODA surged 4.8% to 1,320, hitting the exact 5% daily", size=24, color=NAVY)
txt(page, MARGIN, 540, "limit. The price physically could not go higher.", size=24, color=NAVY)

draw_h_bar(page, MARGIN, 660, "Offers", 24814, "24,814 (Sellers)", 25000, 500, GOLD, NAVY)
draw_h_bar(page, MARGIN, 730, "Bids", 23119, "23,119 (Buyers)", 25000, 500, NAVY, NAVY)
txt(page, MARGIN, 830, "The book balanced out, but the momentum was unstoppable.", size=20, color=TAUPE)

# PAGE 3: CRDB
page, is_dark = page_template(doc, NAVY, 2, TOTAL)
section_label(page, "THE HIDDEN MOVER", y=110, is_dark=True)
txt(page, MARGIN, 240, "CRDB:", size=88, color=CREAM, bold=True)
txt(page, MARGIN, 328, "STEALTH", size=88, color=CREAM, bold=True)
txt(page, MARGIN, 416, "DEMAND.", size=88, color=GOLD, bold=True)

txt(page, MARGIN, 500, "CRDB traded 1.27 million shares and closed perfectly FLAT.", size=24, color=CREAM)
txt(page, MARGIN, 540, "To the amateur, it looks like a boring day.", size=24, color=CREAM)
txt(page, MARGIN, 580, "To the professional, the order book screams coiled demand:", size=24, color=TAUPE)

draw_h_bar(page, MARGIN, 700, "Offers", 49819, "49,819", 192156, 500, GOLD, CREAM)
draw_h_bar(page, MARGIN, 770, "Bids", 192156, "192,156", 192156, 500, CREAM, CREAM)
txt(page, MARGIN, 850, "A 3.9-to-1 ratio. Buyers are cornering the remaining supply.", size=24, color=GOLD, bold=True)

# PAGE 4: LOCAL ABSORPTION
page, is_dark = page_template(doc, CREAM, 3, TOTAL)
section_label(page, "MARKET PSYCHOLOGY", y=110, is_dark=False)
txt(page, MARGIN, 240, "A MATURING", size=88, color=NAVY, bold=True)
txt(page, MARGIN, 328, "MARKET.", size=88, color=GOLD, bold=True)

txt(page, MARGIN, 450, "Foreign capital dumped TZS 2.92 billion onto the market.", size=24, color=NAVY)

draw_donut(
    page, cx=MARGIN+420, cy=660, r_outer=130, r_inner=60, 
    segments=[99.88, 0.12], colors=[NAVY, GOLD], 
    center_text="Buying", center_text_color=NAVY, 
    legend_x=MARGIN+220, legend_y=830, legend_labels=["Local (99.88%)", "Foreign (0.12%)"], legend_color=NAVY, hole_color=CREAM
)

txt(page, MARGIN, 880, "Local institutions swallowed 99.88% of it without blinking.", size=28, color=NAVY, bold=True)

# PAGE 5: BONDS
page, is_dark = page_template(doc, NAVY, 4, TOTAL)
section_label(page, "THE ROTATION", y=110, is_dark=True)
txt(page, MARGIN, 240, "THE BILLIONS", size=88, color=CREAM, bold=True)
txt(page, MARGIN, 328, "LOCKED", size=88, color=CREAM, bold=True)
txt(page, MARGIN, 416, "AWAY.", size=88, color=GOLD, bold=True)

txt(page, MARGIN, 500, "While locals absorbed the equity exits, they simultaneously", size=24, color=CREAM)
txt(page, MARGIN, 540, "locked away TZS 33.59 billion into government bonds.", size=24, color=CREAM)

draw_h_bar(page, MARGIN, 660, "Equity", 5.07, "5.07B", 33.59, 500, CREAM, CREAM)
draw_h_bar(page, MARGIN, 730, "Bonds", 33.59, "33.59B", 33.59, 500, GOLD, CREAM)

txt(page, MARGIN, 850, "Local capital is demonstrating unprecedented depth.", size=24, color=GOLD, bold=True)


# PAGE 6: CTA
page, is_dark = page_template(doc, CREAM, 5, TOTAL)
section_label(page, "DISCUSSION", y=110, is_dark=False)
txt(page, MARGIN, 240, "YOUR", size=88, color=NAVY, bold=True)
txt(page, MARGIN, 328, "STRATEGY?", size=88, color=GOLD, bold=True)

txt(page, MARGIN, 500, "Have you ever tried to execute a trade when", size=32, color=NAVY, bold=True)
txt(page, MARGIN, 550, "a stock hits limit-up?", size=32, color=NAVY, bold=True)
txt(page, MARGIN, 630, "How do you adjust your strategy when the", size=24, color=TAUPE)
txt(page, MARGIN, 670, "price is physically capped?", size=24, color=TAUPE)

txt(page, MARGIN, 800, "Follow https://www.amana-capital-ea.co.tz/ for the", size=20, color=GOLD, bold=True)
txt(page, MARGIN, 830, "full institutional data breakdown.", size=20, color=GOLD, bold=True)

out_path = r'C:\Users\tmalu\Desktop\Amana_DSE_Daily_Wrap_22Sep_PERSONAL_v3.pdf'
doc.save(out_path, garbage=4, deflate=True)
doc.close()
print("Saved:", out_path)
