import fitz
import os

COMPANY_PDF_PATH = r"C:\Users\tmalu\Desktop\Amana_DSE_Daily_Wrap_23Sep_COMPANY.pdf"
PERSONAL_PDF_PATH = r"C:\Users\tmalu\Desktop\Amana_DSE_Daily_Wrap_23Sep_PERSONAL.pdf"

# Colours
NAVY = (11/255, 29/255, 58/255)
GOLD = (200/255, 150/255, 46/255)
CREAM = (251/255, 247/255, 240/255)
GREEN = (34/255, 197/255, 94/255)
RED = (239/255, 68/255, 68/255)
MUTED = (251/255, 247/255, 240/255) # we will use opacity 0.55

def draw_logo(page, x, y, scale=1.0):
    # Abstract A mark
    # Diagonal stroke
    p1 = fitz.Point(x, y + 40*scale)
    p2 = fitz.Point(x + 20*scale, y)
    p3 = fitz.Point(x + 30*scale, y)
    p4 = fitz.Point(x + 10*scale, y + 40*scale)
    page.draw_quad(fitz.Quad(p1, p2, p3, p4), color=GOLD, fill=GOLD)
    # Vertical stroke
    page.draw_rect(fitz.Rect(x + 25*scale, y, x + 35*scale, y + 40*scale), color=GOLD, fill=GOLD)
    # Crossbar
    page.draw_rect(fitz.Rect(x + 10*scale, y + 20*scale, x + 30*scale, y + 28*scale), color=GOLD, fill=GOLD)

def add_footer(page, width, height):
    page.insert_text(fitz.Point(50, height - 30), "Follow https://www.amana-capital-ea.co.tz/ for unfiltered market psychology.", fontname="helv", fontsize=16, color=GOLD)
    draw_logo(page, width - 80, height - 60, scale=0.8)

# --- COMPANY PDF ---
doc_comp = fitz.open()

# Page 1
p1 = doc_comp.new_page(width=1080, height=1080)
p1.draw_rect(fitz.Rect(0, 0, 1080, 1080), color=NAVY, fill=NAVY)
p1.draw_rect(fitz.Rect(50, 50, 1030, 60), color=GOLD, fill=GOLD)
p1.insert_text(fitz.Point(50, 150), "AMANA CAPITAL EA", fontname="hebo", fontsize=60, color=GOLD)
p1.insert_text(fitz.Point(50, 220), "DSE DAILY WRAP", fontname="hebo", fontsize=48, color=CREAM)
p1.insert_text(fitz.Point(50, 280), "Wednesday, 23 September 2026", fontname="helv", fontsize=32, color=CREAM, fill_opacity=0.55)
p1.insert_textbox(fitz.Rect(50, 400, 1030, 800), "CRDB: 4.34x Bid Ratio.\nThe Market Is Accumulating.", fontname="hebo", fontsize=70, color=CREAM)
add_footer(p1, 1080, 1080)
draw_logo(p1, 50, 1080 - 150, scale=2)

# Page 2
p2 = doc_comp.new_page(width=1080, height=1080)
p2.draw_rect(fitz.Rect(0, 0, 1080, 1080), color=NAVY, fill=NAVY)
p2.insert_text(fitz.Point(50, 120), "MARKET SNAPSHOT", fontname="hebo", fontsize=50, color=GOLD)
p2.insert_text(fitz.Point(50, 180), "Consolidation. But not retreat.", fontname="helv", fontsize=30, color=CREAM, fill_opacity=0.55)
# Dark card
p2.draw_rect(fitz.Rect(50, 250, 1030, 650), color=(0.1, 0.15, 0.25), fill=(0.1, 0.15, 0.25))

p2.insert_text(fitz.Point(100, 350), "DSEI", fontname="hebo", fontsize=30, color=CREAM)
p2.insert_text(fitz.Point(100, 420), "4,638.18", fontname="hebo", fontsize=50, color=CREAM)
p2.insert_text(fitz.Point(100, 480), "-21.05 (-0.5%)", fontname="helv", fontsize=30, color=RED)

p2.insert_text(fitz.Point(550, 350), "TSI", fontname="hebo", fontsize=30, color=CREAM)
p2.insert_text(fitz.Point(550, 420), "10,309.18", fontname="hebo", fontsize=50, color=CREAM)
p2.insert_text(fitz.Point(550, 480), "-50.74", fontname="helv", fontsize=30, color=RED)

p2.insert_text(fitz.Point(100, 560), "Equity Turnover", fontname="hebo", fontsize=30, color=CREAM)
p2.insert_text(fitz.Point(100, 610), "TZS 4.13 billion", fontname="hebo", fontsize=40, color=CREAM)

p2.insert_text(fitz.Point(550, 560), "Bond Turnover", fontname="hebo", fontsize=30, color=CREAM)
p2.insert_text(fitz.Point(550, 610), "TZS 39.48 billion", fontname="hebo", fontsize=40, color=CREAM)
p2.insert_text(fitz.Point(920, 610), "(+17.5%)", fontname="helv", fontsize=30, color=GREEN)

add_footer(p2, 1080, 1080)

# Page 3
p3 = doc_comp.new_page(width=1080, height=1080)
p3.draw_rect(fitz.Rect(0, 0, 1080, 1080), color=NAVY, fill=NAVY)
p3.insert_text(fitz.Point(50, 120), "What the Price Won't Tell You", fontname="hebo", fontsize=50, color=GOLD)

y_start = 250
row_height = 120
headers = ["Counter", "Bids", "Offers", "Ratio", "Signal"]
x_coords = [50, 250, 450, 650, 800]
for i, h in enumerate(headers):
    p3.insert_text(fitz.Point(x_coords[i], y_start), h, fontname="hebo", fontsize=30, color=CREAM)

data = [
    ("CRDB", "445,689", "102,725", "4.34x", "BID-HEAVY", GREEN, 0.8),
    ("VODA", "16,170", "7,602", "2.13x", "BID-HEAVY", GOLD, 0.4),
    ("NMB", "28,127", "63,762", "0.44x", "OFFER-HEAVY", RED, 0.1),
    ("DCB", "-", "-", "0.045x", "EXTREME SELLING", RED, 0.02)
]

y = y_start + 80
for d in data:
    p3.insert_text(fitz.Point(x_coords[0], y), d[0], fontname="helv", fontsize=28, color=CREAM)
    p3.insert_text(fitz.Point(x_coords[1], y), d[1], fontname="helv", fontsize=28, color=CREAM)
    p3.insert_text(fitz.Point(x_coords[2], y), d[2], fontname="helv", fontsize=28, color=CREAM)
    p3.insert_text(fitz.Point(x_coords[3], y), d[3], fontname="helv", fontsize=28, color=CREAM)
    p3.insert_text(fitz.Point(x_coords[4], y), d[4], fontname="hebo", fontsize=28, color=d[5])
    
    # Bar chart
    bar_width = 800 * d[6]
    p3.draw_rect(fitz.Rect(50, y + 20, 50 + bar_width, y + 40), color=d[5], fill=d[5])
    y += row_height

add_footer(p3, 1080, 1080)

# Page 4
p4 = doc_comp.new_page(width=1080, height=1080)
p4.draw_rect(fitz.Rect(0, 0, 1080, 1080), color=NAVY, fill=NAVY)
p4.insert_text(fitz.Point(50, 120), "CRDB: The Most Bid-Heavy Book This Week", fontname="hebo", fontsize=40, color=GOLD)

p4.insert_text(fitz.Point(50, 300), "445,689", fontname="hebo", fontsize=90, color=GOLD)
p4.insert_text(fitz.Point(50, 360), "BIDS", fontname="hebo", fontsize=30, color=CREAM, fill_opacity=0.55)

p4.insert_text(fitz.Point(50, 480), "102,725", fontname="hebo", fontsize=60, color=CREAM, fill_opacity=0.55)
p4.insert_text(fitz.Point(50, 530), "OFFERS", fontname="hebo", fontsize=30, color=CREAM, fill_opacity=0.55)

p4.insert_text(fitz.Point(50, 700), "4.34 : 1", fontname="hebo", fontsize=100, color=GREEN)
p4.insert_text(fitz.Point(50, 760), "RATIO", fontname="hebo", fontsize=30, color=CREAM, fill_opacity=0.55)

p4.insert_text(fitz.Point(600, 300), "Closed at 2,820 (+0.4%)", fontname="hebo", fontsize=35, color=CREAM)

# Donut approximation (circle)
center = fitz.Point(750, 600)
p4.draw_sector(center, fitz.Point(750, 400), 291.6, color=GREEN, fill=GREEN) # 81%
p4.draw_sector(center, fitz.Point(750, 400), -68.4, color=RED, fill=RED) # 19%
p4.draw_circle(center, 120, color=NAVY, fill=NAVY)
p4.insert_text(fitz.Point(710, 610), "81%", fontname="hebo", fontsize=40, color=CREAM)

add_footer(p4, 1080, 1080)

# Page 5
p5 = doc_comp.new_page(width=1080, height=1080)
p5.draw_rect(fitz.Rect(0, 0, 1080, 1080), color=NAVY, fill=NAVY)
p5.insert_text(fitz.Point(50, 120), "TOP MOVERS", fontname="hebo", fontsize=50, color=GOLD)

# Left - Gainers
p5.insert_text(fitz.Point(50, 200), "GAINERS", fontname="hebo", fontsize=35, color=GREEN)
gainers = [("MUCOBA", "+3.6%", 0.8), ("PAL", "+3.3%", 0.7), ("MBP", "+2.9%", 0.6), ("TCCL", "+1.9%", 0.4), ("TOL", "+1.1%", 0.2)]
y = 280
for g in gainers:
    p5.insert_text(fitz.Point(50, y), f"{g[0]} {g[1]}", fontname="hebo", fontsize=30, color=CREAM)
    p5.draw_rect(fitz.Rect(50, y + 20, 50 + 400 * g[2], y + 40), color=GREEN, fill=GREEN)
    y += 100

# Right - Losers
p5.insert_text(fitz.Point(550, 200), "LOSERS", fontname="hebo", fontsize=35, color=RED)
losers = [("TTP", "-2.3%", 0.6), ("TCC", "-1.6%", 0.4), ("SWIS", "-1.5%", 0.35), ("MCB", "-1.3%", 0.3), ("TBL", "-1.0%", 0.2)]
y = 280
for l in losers:
    p5.insert_text(fitz.Point(550, y), f"{l[0]} {l[1]}", fontname="hebo", fontsize=30, color=CREAM)
    p5.draw_rect(fitz.Rect(550, y + 20, 550 + 400 * l[2], y + 40), color=RED, fill=RED)
    y += 100

add_footer(p5, 1080, 1080)

# Page 6
p6 = doc_comp.new_page(width=1080, height=1080)
p6.draw_rect(fitz.Rect(0, 0, 1080, 1080), color=NAVY, fill=NAVY)
p6.insert_text(fitz.Point(50, 120), "TZS 39.48 Billion in a Single Session", fontname="hebo", fontsize=50, color=GOLD)

bonds = [
    ("20-yr 12.00%", "TZS 30.14 bn", "Yield: 9.51%-10.48%"),
    ("5-yr 10.25%", "TZS 5.00 bn", "Yield: 9.99%"),
    ("25-yr 12.56%", "TZS 1.25 bn", "Yield: 10.82%-13.00%")
]
y = 250
for b in bonds:
    p6.draw_rect(fitz.Rect(50, y, 1030, y+120), color=(0.1, 0.15, 0.25), fill=(0.1, 0.15, 0.25))
    p6.insert_text(fitz.Point(80, y + 50), b[0], fontname="hebo", fontsize=35, color=GOLD)
    p6.insert_text(fitz.Point(400, y + 50), b[1], fontname="hebo", fontsize=35, color=CREAM)
    p6.insert_text(fitz.Point(750, y + 50), b[2], fontname="helv", fontsize=30, color=CREAM, fill_opacity=0.8)
    y += 150

p6.draw_rect(fitz.Rect(50, 800, 1030, 900), color=GOLD, fill=GOLD)
p6.insert_text(fitz.Point(80, 860), "Tax-free. Long duration. Institutions are settling in.", fontname="hebo", fontsize=35, color=NAVY)

add_footer(p6, 1080, 1080)

# Page 7
p7 = doc_comp.new_page(width=1080, height=1080)
p7.draw_rect(fitz.Rect(0, 0, 1080, 1080), color=NAVY, fill=NAVY)
p7.insert_text(fitz.Point(50, 120), "The Exit Is Almost Over", fontname="hebo", fontsize=50, color=GOLD)

p7.insert_text(fitz.Point(100, 300), "Tuesday", fontname="helv", fontsize=40, color=CREAM, fill_opacity=0.55)
p7.insert_text(fitz.Point(100, 380), "57.58%", fontname="hebo", fontsize=80, color=RED)

p7.insert_text(fitz.Point(650, 300), "Wednesday", fontname="helv", fontsize=40, color=CREAM, fill_opacity=0.55)
p7.insert_text(fitz.Point(650, 380), "5.34%", fontname="hebo", fontsize=80, color=GREEN)

# arrow
p7.draw_line(fitz.Point(400, 350), fitz.Point(600, 350), color=CREAM, width=5)
p7.draw_line(fitz.Point(570, 320), fitz.Point(600, 350), color=CREAM, width=5)
p7.draw_line(fitz.Point(570, 380), fitz.Point(600, 350), color=CREAM, width=5)

p7.insert_textbox(fitz.Rect(100, 500, 980, 700), "Local capital absorbed 100% of shares offered without demanding a discount.", fontname="hebo", fontsize=40, color=CREAM)

p7.draw_rect(fitz.Rect(100, 750, 100 + 575, 800), color=RED, fill=RED)
p7.draw_rect(fitz.Rect(100, 820, 100 + 53, 870), color=GREEN, fill=GREEN)

add_footer(p7, 1080, 1080)

# Page 8
p8 = doc_comp.new_page(width=1080, height=1080)
p8.draw_rect(fitz.Rect(0, 0, 1080, 1080), color=NAVY, fill=NAVY)
p8.insert_text(fitz.Point(50, 120), "When 4.34 Buyers Compete for Every 1 Seller...", fontname="hebo", fontsize=42, color=GOLD)

p8.insert_textbox(fitz.Rect(50, 250, 1030, 600), "The closing price is a lagging indicator. When supply runs dry — and 445,689 buyers are still waiting — the equilibrium must reset. The question is when, not if.", fontname="helv", fontsize=40, color=CREAM)

p8.insert_textbox(fitz.Rect(50, 650, 1030, 800), "Follow Amana Capital EA Ltd on LinkedIn for the full institutional breakdown every session.", fontname="hebo", fontsize=35, color=GOLD)

draw_logo(p8, 450, 850, scale=4)

p8.insert_text(fitz.Point(50, 1050), "amana-capital-ea.co.tz | For informational and educational purposes only. Capital is at risk.", fontname="helv", fontsize=20, color=CREAM, fill_opacity=0.55)

doc_comp.save(COMPANY_PDF_PATH)
doc_comp.close()

# --- PERSONAL PDF ---
doc_pers = fitz.open()
pp = doc_pers.new_page(width=1080, height=1350)
pp.draw_rect(fitz.Rect(0, 0, 1080, 1350), color=NAVY, fill=NAVY)

pp.insert_text(fitz.Point(50, 80), "DSE DAILY WRAP · 23 SEPTEMBER 2026", fontname="hebo", fontsize=35, color=GOLD)

# Inner card
pp.draw_rect(fitz.Rect(50, 150, 1030, 1250), color=CREAM, fill=CREAM)

# Top-left
pp.insert_text(fitz.Point(100, 300), "4.34x", fontname="hebo", fontsize=100, color=GOLD)
pp.insert_text(fitz.Point(100, 350), "CRDB Bid/Offer Ratio", fontname="hebo", fontsize=30, color=NAVY)

# Top-right
pp.insert_text(fitz.Point(600, 300), "TZS 39.48B", fontname="hebo", fontsize=70, color=NAVY)
pp.insert_text(fitz.Point(600, 350), "Bond Market (1 Session)", fontname="hebo", fontsize=30, color=NAVY)

# Bottom-left
pp.insert_text(fitz.Point(100, 800), "DSEI 4,638.18", fontname="hebo", fontsize=50, color=NAVY)
pp.insert_text(fitz.Point(100, 850), "(-21.05)", fontname="hebo", fontsize=40, color=RED)

pp.insert_text(fitz.Point(100, 950), "TSI 10,309.18", fontname="hebo", fontsize=50, color=NAVY)

# Bottom-right
pp.insert_text(fitz.Point(600, 800), "Top Movers", fontname="hebo", fontsize=50, color=NAVY)
pp.insert_text(fitz.Point(600, 880), "MUCOBA +3.6%", fontname="hebo", fontsize=40, color=GREEN)
pp.insert_text(fitz.Point(600, 950), "TTP -2.3%", fontname="hebo", fontsize=40, color=RED)

pp.insert_text(fitz.Point(50, 1320), "amana-capital-ea.co.tz | For informational purposes only.", fontname="helv", fontsize=20, color=CREAM, fill_opacity=0.55)
draw_logo(pp, 950, 1280, scale=1.5)

doc_pers.save(PERSONAL_PDF_PATH)
doc_pers.close()

print(f"Created: {COMPANY_PDF_PATH}")
print(f"Created: {PERSONAL_PDF_PATH}")
import os
print("Size Company:", os.path.getsize(COMPANY_PDF_PATH), "bytes")
print("Size Personal:", os.path.getsize(PERSONAL_PDF_PATH), "bytes")
