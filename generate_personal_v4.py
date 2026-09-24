import fitz
import math

NAVY     = (11/255,  29/255,  58/255)
CREAM    = (251/255, 247/255, 240/255)
GOLD     = (200/255, 150/255, 46/255)
RED      = (220/255, 38/255,  38/255)
GREEN    = (22/255,  163/255, 74/255)
TAUPE    = (154/255, 148/255, 144/255)
BEIGE    = (213/255, 207/255, 199/255)

W, H = 1080, 1350
MARGIN = 60

def rect(shape, x0, y0, x1, y1, fill=None, stroke=None, width=1):
    shape.draw_rect(fitz.Rect(x0, y0, x1, y1))
    shape.finish(fill=fill, color=stroke, width=width)

def circle(shape, cx, cy, r, fill=None, stroke=None, width=1):
    shape.draw_circle((cx, cy), r)
    shape.finish(fill=fill, color=stroke, width=width)

def txt(page, x, y, text, size=24, color=CREAM, bold=False, font="helv"):
    fn = "hebo" if bold else font
    page.insert_text((x, y), text, fontname=fn, fontsize=size, color=color)

def draw_h_bar(page, x, y, label, value_num, val_str, max_val, max_w, bar_color, label_color):
    txt(page, x, y, label, size=18, color=label_color, bold=True)
    bw = max(5, int((value_num / max_val) * max_w))
    shape = page.new_shape()
    rect(shape, x + 80, y - 18, x + 80 + bw, y + 2, fill=bar_color)
    shape.commit()
    txt(page, x + 90 + bw, y, val_str, size=16, color=label_color, bold=True)

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
        tw = fitz.get_text_length(center_text, fontname="hebo", fontsize=16)
        page.insert_text((cx - tw/2, cy + 6), center_text, fontname="hebo", fontsize=16, color=center_text_color)
    if legend_labels and legend_x is not None:
        for i, (lbl, col) in enumerate(zip(legend_labels, colors)):
            ly = legend_y + i * 24
            shape = page.new_shape()
            rect(shape, legend_x, ly, legend_x + 10, ly + 10, fill=col)
            shape.commit()
            page.insert_text((legend_x + 16, ly + 10), lbl, fontname="helv", fontsize=14, color=legend_color)


doc = fitz.open()
page = doc.new_page(width=W, height=H)
shape = page.new_shape()
rect(shape, 0, 0, W, H, fill=NAVY)
rect(shape, 0, 0, W, 6, fill=GOLD)
shape.commit()

# --- HEADER ---
txt(page, MARGIN, 120, "MARKET PSYCHOLOGY:", size=24, color=GOLD, bold=True)
txt(page, MARGIN, 210, "WHEN A STOCK", size=90, color=CREAM, bold=True)
txt(page, MARGIN, 300, "HITS THE CEILING.", size=90, color=CREAM, bold=True)

# Divider
shape = page.new_shape()
shape.draw_line((MARGIN, 340), (W - MARGIN, 340))
shape.finish(color=GOLD, width=1)
shape.commit()

# --- BOX 1: VODA (Top Left) ---
bx, by = MARGIN, 380
txt(page, bx, by+30, "VODA: LIMIT-UP", size=32, color=GOLD, bold=True)
txt(page, bx, by+70, "Closed at 1,320 (+4.8%). The price", size=20, color=CREAM)
txt(page, bx, by+100, "physically could not go higher.", size=20, color=CREAM)
draw_h_bar(page, bx, by+160, "Offers", 24814, "24,814", 25000, 200, GOLD, CREAM)
draw_h_bar(page, bx, by+210, "Bids", 23119, "23,119", 25000, 200, CREAM, CREAM)

# --- BOX 2: CRDB (Top Right) ---
bx, by = W/2 + 20, 380
txt(page, bx, by+30, "CRDB: STEALTH DEMAND", size=32, color=GOLD, bold=True)
txt(page, bx, by+70, "Closed perfectly FLAT. To the amateur,", size=20, color=CREAM)
txt(page, bx, by+100, "boring. To the pro, coiled demand.", size=20, color=CREAM)
draw_h_bar(page, bx, by+160, "Offers", 49819, "49,819", 192156, 200, GOLD, CREAM)
draw_h_bar(page, bx, by+210, "Bids", 192156, "192,156 (3.9x ratio)", 192156, 200, CREAM, CREAM)

# --- BOX 3: FLOWS (Middle Left) ---
bx, by = MARGIN, 680
txt(page, bx, by+30, "LOCAL ABSORPTION", size=32, color=GOLD, bold=True)
txt(page, bx, by+70, "Foreign exits were completely", size=20, color=CREAM)
txt(page, bx, by+100, "swallowed by local institutions.", size=20, color=CREAM)

draw_donut(
    page, cx=bx+100, cy=by+210, r_outer=70, r_inner=35, 
    segments=[99.88, 0.12], colors=[CREAM, GOLD], 
    center_text="Buying", center_text_color=NAVY, 
    legend_x=bx+200, legend_y=by+180, legend_labels=["Local 99.88%", "Foreign 0.12%"], legend_color=CREAM, hole_color=NAVY
)

# --- BOX 4: BONDS (Middle Right) ---
bx, by = W/2 + 20, 680
txt(page, bx, by+30, "THE BILLIONS ROTATE", size=32, color=GOLD, bold=True)
txt(page, bx, by+70, "Locals absorbed equity exits &", size=20, color=CREAM)
txt(page, bx, by+100, "locked away TZS 33.59B in bonds.", size=20, color=CREAM)

draw_h_bar(page, bx, by+180, "Equity", 5.07, "5.07B", 33.59, 250, CREAM, CREAM)
draw_h_bar(page, bx, by+230, "Bonds", 33.59, "33.59B", 33.59, 250, GOLD, CREAM)


# --- FOOTER ---
fy = 1100
shape = page.new_shape()
shape.draw_line((MARGIN, fy), (W - MARGIN, fy))
shape.finish(color=GOLD, width=1)
shape.commit()

# Logo
lx, ly = MARGIN + 10, fy+40
shape = page.new_shape()
q = fitz.Quad((130.8-MARGIN+10, 984.8-1100+fy+40), (140.4-MARGIN+10, 984.8-1100+fy+40), (110.0-MARGIN+10, 1055.2-1100+fy+40), (119.6-MARGIN+10, 1055.2-1100+fy+40))
# Let's hardcode logo manually at bottom left
shape.draw_quad(fitz.Quad((MARGIN+20, fy+40), (MARGIN+30, fy+40), (MARGIN, fy+110), (MARGIN+10, fy+110)))
shape.finish(fill=GOLD, color=GOLD)
shape.draw_rect(fitz.Rect(MARGIN+34, fy+40, MARGIN+46, fy+110))
shape.finish(fill=GOLD, color=GOLD)
shape.draw_rect(fitz.Rect(MARGIN, fy+70, MARGIN+34, fy+76))
shape.finish(fill=GOLD, color=GOLD)
shape.commit()

txt(page, MARGIN+60, fy+70, "AMANA CAPITAL", size=22, color=CREAM, bold=True)
txt(page, MARGIN+60, fy+100, "East Africa Limited", size=18, color=GOLD)

txt(page, MARGIN, 1260, "Follow https://www.amana-capital-ea.co.tz/ for the full institutional data breakdown.", size=20, color=GOLD, bold=True)


out_path = r'C:\Users\tmalu\Desktop\Amana_DSE_Daily_Wrap_22Sep_PERSONAL_v4.pdf'
doc.save(out_path, garbage=4, deflate=True)
doc.close()
print("Saved:", out_path)
