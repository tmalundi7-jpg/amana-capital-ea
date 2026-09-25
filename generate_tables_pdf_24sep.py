import fitz
import os

desktop_path = r"C:\Users\tmalu\Desktop"
company_pdf_path = os.path.join(desktop_path, "Amana_DSE_Daily_Wrap_24Sep_COMPANY.pdf")
personal_pdf_path = os.path.join(desktop_path, "Amana_DSE_Daily_Wrap_24Sep_PERSONAL.pdf")

# Amana Brand Colors
NAVY = (11/255, 29/255, 58/255)
GOLD = (212/255, 162/255, 51/255)
CREAM = (251/255, 247/255, 240/255)
TEAL = (31/255, 78/255, 91/255)
WHITE = (1, 1, 1)
GAIN = (34/255, 197/255, 94/255)
LOSS = (239/255, 68/255, 68/255)
MIST = (156/255, 163/255, 175/255)

def draw_header(page, width, title, date_text):
    page.draw_rect(fitz.Rect(0, 0, width, 120), color=NAVY, fill=NAVY)
    p1, p2, p3 = fitz.Point(50, 80), fitz.Point(70, 30), fitz.Point(90, 80)
    page.draw_quad(fitz.Quad(p1, p2, p3, p1), color=GOLD, fill=GOLD)
    page.draw_rect(fitz.Rect(60, 65, 80, 75), color=NAVY, fill=NAVY)
    page.insert_text((110, 60), "AMANA CAPITAL EAST AFRICA", fontname="hebo", fontsize=16, color=GOLD)
    page.insert_text((110, 80), "MARKET INTELLIGENCE", fontname="helv", fontsize=12, color=WHITE)
    page.insert_text((width - 350, 60), title, fontname="hebo", fontsize=16, color=WHITE)
    page.insert_text((width - 350, 80), date_text, fontname="helv", fontsize=12, color=GOLD)

def draw_footer(page, width, height, page_num, total_pages):
    page.draw_rect(fitz.Rect(0, height - 60, width, height), color=NAVY, fill=NAVY)
    page.insert_text((50, height - 25), "www.amana-capital-ea.co.tz | Not investment advice | Capital is at risk", fontname="helv", fontsize=10, color=WHITE)
    if total_pages > 1:
        page.insert_text((width - 80, height - 25), f"{page_num}/{total_pages}", fontname="hebo", fontsize=12, color=GOLD)

def draw_table_row(page, x, y, cols, widths, colors=None, font="helv", size=20, bg_color=None):
    if bg_color:
        page.draw_rect(fitz.Rect(x-10, y-25, x+sum(widths)+10, y+10), color=bg_color, fill=bg_color)
    
    curr_x = x
    for i, text in enumerate(cols):
        c = colors[i] if colors and i < len(colors) else NAVY
        page.insert_text((curr_x, y), str(text), fontname=font, fontsize=size, color=c)
        curr_x += widths[i]

# ==========================================
# 1. Company PDF (6 Pages, 1080x1080 pts)
# ==========================================
doc_comp = fitz.open()
W, H = 1080, 1080

# Page 1: Hero
p1 = doc_comp.new_page(width=W, height=H)
p1.draw_rect(fitz.Rect(0, 0, W, H), color=NAVY, fill=NAVY)
draw_header(p1, W, "DSE DAILY WRAP", "24 SEP 2026")
p1.draw_rect(fitz.Rect(100, 250, W-100, H-250), color=CREAM, fill=CREAM)
p1.draw_rect(fitz.Rect(100, 250, W-100, 260), color=GOLD, fill=GOLD)
p1.insert_text((150, 350), "THE ORDER BOOK SIEGE", fontname="hebo", fontsize=30, color=NAVY)
p1.insert_text((150, 500), "19.2x", fontname="hebo", fontsize=120, color=TEAL)
p1.insert_text((150, 580), "Bid-to-Offer Ratio on CRDB Bank.", fontname="hebo", fontsize=35, color=GOLD)
p1.insert_text((150, 650), "450,310 bids trapped just 23,398 offers.", fontname="helv", fontsize=28, color=NAVY)
p1.insert_text((150, 700), "Institutions paused execution across both", fontname="helv", fontsize=28, color=NAVY)
p1.insert_text((150, 750), "asset classes, but local capital tightened", fontname="helv", fontsize=28, color=NAVY)
p1.insert_text((150, 800), "its grip on the supply it already holds.", fontname="helv", fontsize=28, color=NAVY)
draw_footer(p1, W, H, 1, 6)

# Page 2: Market Snapshot Table
p2 = doc_comp.new_page(width=W, height=H)
p2.draw_rect(fitz.Rect(0, 0, W, H), color=NAVY, fill=NAVY)
draw_header(p2, W, "MARKET SNAPSHOT", "24 SEP 2026")
p2.draw_rect(fitz.Rect(100, 250, W-100, H-250), color=CREAM, fill=CREAM)
p2.draw_rect(fitz.Rect(100, 250, W-100, 260), color=GOLD, fill=GOLD)
p2.insert_text((150, 350), "TURNOVER CONTRACTION", fontname="hebo", fontsize=30, color=NAVY)

headers = ["Metric", "Wed 23 Sep", "Thu 24 Sep", "Change"]
widths = [220, 220, 220, 200]
draw_table_row(p2, 150, 450, headers, widths, colors=[WHITE]*4, font="hebo", size=22, bg_color=TEAL)

data = [
    (["DSEI", "4,638.18", "4,658.16", "+19.98 pts"], [NAVY, NAVY, NAVY, GAIN]),
    (["TSI", "10,309.18", "10,362.31", "+53.13 pts"], [NAVY, NAVY, NAVY, GAIN]),
    (["Equity Turnover", "TZS 4.13 bn", "TZS 2.73 bn", "-34.1%"], [NAVY, NAVY, NAVY, LOSS]),
    (["Shares Traded", "1.91 million", "1.23 million", "-35.7%"], [NAVY, NAVY, NAVY, LOSS]),
    (["Bond Turnover", "TZS 39.48 bn", "TZS 20.87 bn", "-47.1%"], [NAVY, NAVY, NAVY, LOSS]),
    (["Foreign Selling", "5.34%", "7.91%", "+2.57 pts"], [NAVY, NAVY, NAVY, LOSS]),
    (["Foreign Buying", "0.00%", "0.00%", "0.00 pts"], [NAVY, NAVY, NAVY, MIST]),
]
y = 510
for row, cols in data:
    draw_table_row(p2, 150, y, row, widths, colors=cols, size=22)
    p2.draw_line(fitz.Point(150, y+15), fitz.Point(150+sum(widths), y+15), color=MIST, width=0.5)
    y += 50
draw_footer(p2, W, H, 2, 6)

# Page 3: Top Movers Table
p3 = doc_comp.new_page(width=W, height=H)
p3.draw_rect(fitz.Rect(0, 0, W, H), color=NAVY, fill=NAVY)
draw_header(p3, W, "TOP MOVERS", "24 SEP 2026")
p3.draw_rect(fitz.Rect(100, 250, W-100, H-250), color=CREAM, fill=CREAM)
p3.draw_rect(fitz.Rect(100, 250, W-100, 260), color=GOLD, fill=GOLD)
p3.insert_text((150, 350), "EQUITY GAINERS & LOSERS", fontname="hebo", fontsize=30, color=NAVY)

widths_movers = [200, 200, 200, 200]
draw_table_row(p3, 150, 430, ["Ticker", "Price (TZS)", "Volume", "Change"], widths_movers, colors=[WHITE]*4, font="hebo", size=22, bg_color=TEAL)

movers_data = [
    (["TCCL", "3,920", "4,166", "+3.7%"], [NAVY, NAVY, NAVY, GAIN]),
    (["NICO", "3,740", "8,960", "+3.3%"], [NAVY, NAVY, NAVY, GAIN]),
    (["CRDB", "2,870", "450,310", "+1.8%"], [NAVY, NAVY, NAVY, GAIN]),
    (["MCB", "380", "52,320", "+1.3%"], [NAVY, NAVY, NAVY, GAIN]),
    (["VODA", "1,290", "42,196", "-1.5%"], [NAVY, NAVY, NAVY, LOSS]),
    (["AFRIPRISE", "775", "63,851", "-1.9%"], [NAVY, NAVY, NAVY, LOSS]),
    (["PAL", "305", "15,308", "-3.2%"], [NAVY, NAVY, NAVY, LOSS]),
    (["MUCOBA", "405", "5,712", "-5.8%"], [NAVY, NAVY, NAVY, LOSS]),
]
y = 490
for row, cols in movers_data:
    draw_table_row(p3, 150, y, row, widths_movers, colors=cols, size=22)
    p3.draw_line(fitz.Point(150, y+15), fitz.Point(150+sum(widths_movers), y+15), color=MIST, width=0.5)
    y += 45
draw_footer(p3, W, H, 3, 6)

# Page 4: Block Trade
p4 = doc_comp.new_page(width=W, height=H)
p4.draw_rect(fitz.Rect(0, 0, W, H), color=NAVY, fill=NAVY)
draw_header(p4, W, "PRE-ARRANGED BOARD", "24 SEP 2026")
p4.draw_rect(fitz.Rect(100, 250, W-100, H-250), color=CREAM, fill=CREAM)
p4.draw_rect(fitz.Rect(100, 250, W-100, 260), color=GOLD, fill=GOLD)
p4.insert_text((150, 350), "BLOCK TRADES", fontname="hebo", fontsize=30, color=NAVY)
p4.insert_text((150, 480), "NMB", fontname="hebo", fontsize=80, color=NAVY)
p4.insert_text((150, 560), "140,968 Shares", fontname="hebo", fontsize=40, color=GOLD)
p4.insert_text((150, 650), "NMB absorbed a block trade and closed at 2,130", fontname="helv", fontsize=28, color=NAVY)
p4.insert_text((150, 700), "with a highly offer-heavy book (507k vs 195k).", fontname="helv", fontsize=28, color=NAVY)
p4.insert_text((150, 750), "Caution is warranted until the TZS 61.015", fontname="helv", fontsize=28, color=NAVY)
p4.insert_text((150, 800), "ex-dividend date is finalized.", fontname="helv", fontsize=28, color=NAVY)
draw_footer(p4, W, H, 4, 6)

# Page 5: Bond Market 
p5 = doc_comp.new_page(width=W, height=H)
p5.draw_rect(fitz.Rect(0, 0, W, H), color=NAVY, fill=NAVY)
draw_header(p5, W, "FIXED INCOME", "24 SEP 2026")
p5.draw_rect(fitz.Rect(100, 250, W-100, H-250), color=CREAM, fill=CREAM)
p5.draw_rect(fitz.Rect(100, 250, W-100, 260), color=GOLD, fill=GOLD)
p5.insert_text((150, 350), "20-YEAR DURATION PREMIUM", fontname="hebo", fontsize=30, color=NAVY)
p5.insert_text((150, 480), "8.26%", fontname="hebo", fontsize=100, color=TEAL)
p5.insert_text((150, 560), "A shocking compression in yield.", fontname="hebo", fontsize=35, color=GOLD)
p5.insert_text((150, 650), "Bond turnover fell nearly in half to TZS 20.87 bn.", fontname="helv", fontsize=28, color=NAVY)
p5.insert_text((150, 700), "Yet a surgical strike of TZS 18 billion secured", fontname="helv", fontsize=28, color=NAVY)
p5.insert_text((150, 750), "20-year paper at yields as low as 8.26%.", fontname="helv", fontsize=28, color=NAVY)
p5.insert_text((150, 800), "Institutions are locking the exits.", fontname="helv", fontsize=28, color=NAVY)
draw_footer(p5, W, H, 5, 6)

# Page 6: Outro
p6 = doc_comp.new_page(width=W, height=H)
p6.draw_rect(fitz.Rect(0, 0, W, H), color=NAVY, fill=NAVY)
draw_header(p6, W, "STRATEGIC OUTLOOK", "24 SEP 2026")
p6.draw_rect(fitz.Rect(100, 250, W-100, H-250), color=CREAM, fill=CREAM)
p6.draw_rect(fitz.Rect(100, 250, W-100, 260), color=GOLD, fill=GOLD)
p6.insert_text((150, 350), "THE PAUSE BEFORE...", fontname="hebo", fontsize=30, color=NAVY)
p6.insert_text((150, 500), "Does this silence precede a massive", fontname="hebo", fontsize=40, color=NAVY)
p6.insert_text((150, 560), "capital rotation, or are institutions", fontname="hebo", fontsize=40, color=NAVY)
p6.insert_text((150, 620), "simply starving the market of supply?", fontname="hebo", fontsize=40, color=NAVY)
p6.insert_text((150, 750), "Follow Amana Capital EA Ltd for", fontname="helv", fontsize=26, color=TEAL)
p6.insert_text((150, 800), "daily institutional order book analytics.", fontname="helv", fontsize=26, color=TEAL)
draw_footer(p6, W, H, 6, 6)

doc_comp.save(company_pdf_path, garbage=4, deflate=True)


# ==========================================
# 2. Personal PDF (1 Page, 1080x1350 pts)
# ==========================================
doc_pers = fitz.open()
W_p, H_p = 1080, 1350
page_p = doc_pers.new_page(width=W_p, height=H_p)
page_p.draw_rect(fitz.Rect(0, 0, W_p, H_p), color=CREAM, fill=CREAM)

page_p.draw_rect(fitz.Rect(0, 0, W_p, 150), color=NAVY, fill=NAVY)
page_p.insert_text((80, 90), "THE 8.26% DURATION PREMIUM", fontname="hebo", fontsize=40, color=GOLD)

page_p.insert_text((80, 250), "8.26%", fontname="hebo", fontsize=120, color=NAVY)
page_p.insert_text((80, 320), "The sudden plunge in 20-Year Bond Yields.", fontname="hebo", fontsize=30, color=TEAL)

# Data Tables on Personal
box_rect = fitz.Rect(80, 380, W_p-80, 1050)
page_p.draw_rect(box_rect, color=WHITE, fill=WHITE)
page_p.draw_rect(box_rect, color=MIST, width=2)
page_p.draw_rect(fitz.Rect(80, 380, W_p-80, 440), color=NAVY, fill=NAVY)
page_p.insert_text((120, 420), "THURSDAY MARKET CONTRACTION", fontname="hebo", fontsize=24, color=WHITE)

pers_headers = ["Metric", "Volume", "Change"]
pers_widths = [280, 300, 200]
draw_table_row(page_p, 120, 500, pers_headers, pers_widths, colors=[NAVY]*3, font="hebo", size=24)
p_data = [
    (["Equity Turnover", "TZS 2.73 billion", "-34.1%"], [NAVY, NAVY, LOSS]),
    (["Bond Turnover", "TZS 20.87 billion", "-47.1%"], [NAVY, NAVY, LOSS]),
    (["CRDB Bid/Offer", "19.2x Ratio", "Hold"], [NAVY, NAVY, GAIN]),
    (["VODA Bid/Offer", "1.0x Ratio", "Balanced"], [NAVY, NAVY, MIST]),
]
y_p = 560
for row, cols in p_data:
    draw_table_row(page_p, 120, y_p, row, pers_widths, colors=cols, size=24)
    page_p.draw_line(fitz.Point(120, y_p+15), fitz.Point(120+sum(pers_widths), y_p+15), color=MIST, width=0.5)
    y_p += 55

page_p.draw_rect(fitz.Rect(80, 750, W_p-80, 810), color=TEAL, fill=TEAL)
page_p.insert_text((120, 790), "KEY PRICE MOVERS", fontname="hebo", fontsize=24, color=WHITE)
draw_table_row(page_p, 120, 860, ["Ticker", "Price", "Change"], pers_widths, colors=[NAVY]*3, font="hebo", size=24)
m_data = [
    (["TCCL", "3,920 TZS", "+3.7%"], [NAVY, NAVY, GAIN]),
    (["CRDB", "2,870 TZS", "+1.8%"], [NAVY, NAVY, GAIN]),
    (["VODA", "1,290 TZS", "-1.5%"], [NAVY, NAVY, LOSS]),
    (["MUCOBA", "405 TZS", "-5.8%"], [NAVY, NAVY, LOSS]),
]
y_m = 910
for row, cols in m_data:
    draw_table_row(page_p, 120, y_m, row, pers_widths, colors=cols, size=24)
    page_p.draw_line(fitz.Point(120, y_m+15), fitz.Point(120+sum(pers_widths), y_m+15), color=MIST, width=0.5)
    y_m += 50

# Conclusion
page_p.insert_text((80, 1150), "When execution pauses across both markets while", fontname="hebo", fontsize=30, color=NAVY)
page_p.insert_text((80, 1200), "yields compress, what happens when capital returns?", fontname="hebo", fontsize=30, color=NAVY)

# Footer
page_p.draw_rect(fitz.Rect(0, H_p-80, W_p, H_p), color=NAVY, fill=NAVY)
page_p.insert_text((80, H_p-35), "Data: DSE Daily Wrap | 24 Sep 2026 | @Amana Capital EA Ltd", fontname="helv", fontsize=20, color=WHITE)

doc_pers.save(personal_pdf_path, garbage=4, deflate=True)
print("Saved both PDF forms with colour-coded tables.")
