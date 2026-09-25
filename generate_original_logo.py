import fitz
import os

desktop_path = r"C:\Users\tmalu\Desktop"
pdf_path = os.path.join(desktop_path, "Amana_Capital_Logo.pdf")
jpg_path = os.path.join(desktop_path, "Amana_Capital_Logo.jpg")
pdf_full_path = os.path.join(desktop_path, "Amana_Capital_Logo_Full.pdf")
jpg_full_path = os.path.join(desktop_path, "Amana_Capital_Logo_Full.jpg")

NAVY = (11/255, 29/255, 58/255)
GOLD = (212/255, 162/255, 51/255)
WHITE = (1, 1, 1)

def draw_logo(page, x, y, scale=1.0):
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

# --- 1. Minimalist Icon ---
doc1 = fitz.open()
page1 = doc1.new_page(width=1000, height=1000)
page1.draw_rect(fitz.Rect(0, 0, 1000, 1000), color=NAVY, fill=NAVY)

# Center the logo (scale = 15 => width = 525, height = 600)
# x = (1000-525)/2 = 237.5, y = (1000-600)/2 = 200
draw_logo(page1, 237.5, 200, scale=15)

doc1.save(pdf_path)
pix1 = page1.get_pixmap(matrix=fitz.Matrix(2, 2))
pix1.save(jpg_path)

# --- 2. Full Brand Logo (Icon + Text) ---
doc2 = fitz.open()
page2 = doc2.new_page(width=1000, height=1000)
page2.draw_rect(fitz.Rect(0, 0, 1000, 1000), color=NAVY, fill=NAVY)

# Shift logo up to make room for text
draw_logo(page2, 325, 250, scale=10) # width=350, height=400, x=(1000-350)/2=325

# Text
text_y = 750
page2.insert_text((180, text_y), "AMANA CAPITAL EAST AFRICA", fontname="hebo", fontsize=45, color=GOLD)
page2.insert_text((310, text_y + 60), "MARKET INTELLIGENCE", fontname="helv", fontsize=35, color=WHITE)

doc2.save(pdf_full_path)
pix2 = page2.get_pixmap(matrix=fitz.Matrix(2, 2))
pix2.save(jpg_full_path)

print("Generated original Amana logos matching 23Sep PDFs.")
