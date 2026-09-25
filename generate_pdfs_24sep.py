import fitz
import os

# Desktop path
desktop_path = r"C:\Users\tmalu\Desktop"
company_pdf_path = os.path.join(desktop_path, "Amana_DSE_Daily_Wrap_24Sep_COMPANY.pdf")
personal_pdf_path = os.path.join(desktop_path, "Amana_DSE_Daily_Wrap_24Sep_PERSONAL.pdf")

# Amana Brand Colors
NAVY = (11/255, 29/255, 58/255)
GOLD = (212/255, 162/255, 51/255)
CREAM = (251/255, 247/255, 240/255)
WHITE = (1, 1, 1)
GAIN = (34/255, 197/255, 94/255)
LOSS = (239/255, 68/255, 68/255)

def draw_header(page, width, title, date_text):
    # Header bg
    page.draw_rect(fitz.Rect(0, 0, width, 120), color=NAVY, fill=NAVY)
    
    # Amana logo (A)
    p1, p2, p3 = fitz.Point(50, 80), fitz.Point(70, 30), fitz.Point(90, 80)
    page.draw_quad(fitz.Quad(p1, p2, p3, p1), color=GOLD, fill=GOLD)
    page.draw_rect(fitz.Rect(60, 65, 80, 75), color=NAVY, fill=NAVY)
    
    # Text
    page.insert_text((110, 60), "AMANA CAPITAL EAST AFRICA", fontname="hebo", fontsize=16, color=GOLD)
    page.insert_text((110, 80), "MARKET INTELLIGENCE", fontname="helv", fontsize=12, color=WHITE)
    
    # Title & Date
    page.insert_text((width - 350, 60), title, fontname="hebo", fontsize=16, color=WHITE)
    page.insert_text((width - 350, 80), date_text, fontname="helv", fontsize=12, color=GOLD)

def draw_footer(page, width, height, page_num, total_pages):
    page.draw_rect(fitz.Rect(0, height - 60, width, height), color=NAVY, fill=NAVY)
    page.insert_text((50, height - 25), "www.amana-capital-ea.co.tz | Not investment advice", fontname="helv", fontsize=10, color=WHITE)
    if total_pages > 1:
        page.insert_text((width - 80, height - 25), f"Page {page_num} of {total_pages}", fontname="hebo", fontsize=10, color=GOLD)

# ==========================================
# 1. Company PDF (8 Pages, 1080x1080 pts)
# ==========================================
doc_comp = fitz.open()
W, H = 1080, 1080

pages_data = [
    {"title": "MARKET SNAPSHOT", "main_stat": "4,658.16", "sub_stat": "DSEI (+19.98 pts)", "text": "Turnover Contracts as Institutions Pause Across Equities and Bonds."},
    {"title": "EQUITY MARKET", "main_stat": "TZS 2.73 bn", "sub_stat": "Total Equity Turnover", "text": "Equity turnover dropped 34.1%. Liquidity contracted while prices edged higher."},
    {"title": "BOND MARKET", "main_stat": "TZS 20.87 bn", "sub_stat": "Total Bond Turnover", "text": "Bond trading fell 47.1%. 20-Year bonds cleared at an unusually low 8.26% yield."},
    {"title": "ORDER BOOK: CRDB", "main_stat": "19.2x", "sub_stat": "Bid-to-Offer Ratio", "text": "450,310 Bids vs 23,398 Offers. Massive domestic demand pinning the price at 2,870."},
    {"title": "ORDER BOOK: VODA", "main_stat": "1.0x", "sub_stat": "Balanced Book", "text": "42,196 Bids vs 45,000 Offers. Pre-dividend limit-up run halts as market finds equilibrium at 1,290."},
    {"title": "TOP GAINERS", "main_stat": "TCCL (+3.7%)", "sub_stat": "3,920 TZS", "text": "NICO followed with +3.3%, and CRDB added +1.8%."},
    {"title": "FOREIGN FLOW", "main_stat": "7.91%", "sub_stat": "Foreign Selling", "text": "Foreign buying dropped to 0.00%. Local institutions are completely dominating the floor."},
    {"title": "STRATEGIC OUTLOOK", "main_stat": "AWAITING CATALYSTS", "sub_stat": "Rotation or Exhaustion?", "text": "Follow Amana Capital EA Ltd for daily institutional order book analytics."}
]

for i, pd in enumerate(pages_data):
    page = doc_comp.new_page(width=W, height=H)
    page.draw_rect(fitz.Rect(0, 0, W, H), color=NAVY, fill=NAVY)
    
    draw_header(page, W, "DSE DAILY WRAP", "24 SEP 2026")
    
    # Card
    card_rect = fitz.Rect(100, 250, W-100, H-250)
    page.draw_rect(card_rect, color=CREAM, fill=CREAM)
    page.draw_rect(fitz.Rect(100, 250, W-100, 260), color=GOLD, fill=GOLD)
    
    # Content
    page.insert_text((150, 350), pd["title"], fontname="hebo", fontsize=30, color=NAVY)
    page.insert_text((150, 480), pd["main_stat"], fontname="hebo", fontsize=80, color=NAVY)
    page.insert_text((150, 580), pd["sub_stat"], fontname="hebo", fontsize=35, color=GOLD)
    
    # Body text wrapping
    words = pd["text"].split()
    line, y = "", 680
    for w in words:
        if fitz.get_text_length(line + w + " ", fontname="helv", fontsize=24) < (W-300):
            line += w + " "
        else:
            page.insert_text((150, y), line, fontname="helv", fontsize=24, color=NAVY)
            line = w + " "
            y += 35
    if line:
        page.insert_text((150, y), line, fontname="helv", fontsize=24, color=NAVY)
        
    draw_footer(page, W, H, i+1, 8)

# Save with 3x scale for LinkedIn HQ
try:
    doc_comp.save(company_pdf_path, garbage=4, deflate=True)
    print(f"Saved: {company_pdf_path}")
except Exception as e:
    company_pdf_path = company_pdf_path.replace(".pdf", "_v2.pdf")
    doc_comp.save(company_pdf_path, garbage=4, deflate=True)
    print(f"Saved fallback: {company_pdf_path}")

# ==========================================
# 2. Personal PDF (1 Page, 1080x1350 pts)
# ==========================================
doc_pers = fitz.open()
W_p, H_p = 1080, 1350
page_p = doc_pers.new_page(width=W_p, height=H_p)
page_p.draw_rect(fitz.Rect(0, 0, W_p, H_p), color=CREAM, fill=CREAM)

# Header
page_p.draw_rect(fitz.Rect(0, 0, W_p, 150), color=NAVY, fill=NAVY)
page_p.insert_text((80, 90), "THE 8.26% DURATION PREMIUM", fontname="hebo", fontsize=40, color=GOLD)

# Main stat
page_p.insert_text((80, 300), "8.26%", fontname="hebo", fontsize=150, color=NAVY)
page_p.insert_text((80, 380), "The sudden plunge in 20-Year Bond Yields.", fontname="hebo", fontsize=35, color=GOLD)

# Two boxes
box1 = fitz.Rect(80, 480, W_p-80, 700)
page_p.draw_rect(box1, color=NAVY, fill=NAVY)
page_p.draw_rect(fitz.Rect(80, 480, 90, 700), color=GOLD, fill=GOLD)
page_p.insert_text((120, 550), "EQUITY LIQUIDITY DROPS 34%", fontname="hebo", fontsize=30, color=WHITE)
page_p.insert_text((120, 600), "Turnover fell to TZS 2.73 bn, yet CRDB bids stacked", fontname="helv", fontsize=25, color=CREAM)
page_p.insert_text((120, 640), "to a 19.2x ratio. Institutions are holding tight.", fontname="helv", fontsize=25, color=CREAM)

box2 = fitz.Rect(80, 750, W_p-80, 970)
page_p.draw_rect(box2, color=NAVY, fill=NAVY)
page_p.draw_rect(fitz.Rect(80, 750, 90, 970), color=GOLD, fill=GOLD)
page_p.insert_text((120, 820), "BOND VOLUMES HALVED", fontname="hebo", fontsize=30, color=WHITE)
page_p.insert_text((120, 870), "Turnover fell 47% to TZS 20.87 bn, but aggressive", fontname="helv", fontsize=25, color=CREAM)
page_p.insert_text((120, 910), "pricing secured 20-year duration at 8.26%.", fontname="helv", fontsize=25, color=CREAM)

# Conclusion
page_p.insert_text((80, 1100), "When execution pauses across both markets while", fontname="hebo", fontsize=30, color=NAVY)
page_p.insert_text((80, 1150), "yields compress, what happens when capital returns?", fontname="hebo", fontsize=30, color=NAVY)

# Footer
page_p.draw_rect(fitz.Rect(0, H_p-80, W_p, H_p), color=NAVY, fill=NAVY)
page_p.insert_text((80, H_p-35), "Data: DSE Daily Wrap | 24 Sep 2026 | @Amana Capital EA Ltd", fontname="helv", fontsize=20, color=WHITE)

try:
    doc_pers.save(personal_pdf_path, garbage=4, deflate=True)
    print(f"Saved: {personal_pdf_path}")
except Exception:
    personal_pdf_path = personal_pdf_path.replace(".pdf", "_v2.pdf")
    doc_pers.save(personal_pdf_path, garbage=4, deflate=True)
    print(f"Saved fallback: {personal_pdf_path}")
