import fitz
import os

desktop_path = r"C:\Users\tmalu\Desktop"
pdf_path = os.path.join(desktop_path, "Amana_Capital_Logo_Full.pdf")
jpg_path = os.path.join(desktop_path, "Amana_Capital_Logo_Full.jpg")

NAVY = (11/255, 29/255, 58/255)
GOLD = (212/255, 162/255, 51/255)
WHITE = (1, 1, 1)

doc = fitz.open()
page = doc.new_page(width=1000, height=1000)

# Background
page.draw_rect(fitz.Rect(0, 0, 1000, 1000), color=NAVY, fill=NAVY)

# Gold Triangle
p1 = fitz.Point(350, 600)
p2 = fitz.Point(500, 225)
p3 = fitz.Point(650, 600)
page.draw_quad(fitz.Quad(p1, p2, p3, p1), color=GOLD, fill=GOLD)

# Navy Cutout (creates the 'A' crossbar)
cutout = fitz.Rect(425, 487.5, 575, 562.5)
page.draw_rect(cutout, color=NAVY, fill=NAVY)

# Text
text_y = 750
page.insert_text((180, text_y), "AMANA CAPITAL EAST AFRICA", fontname="hebo", fontsize=45, color=GOLD)
page.insert_text((310, text_y + 60), "MARKET INTELLIGENCE", fontname="helv", fontsize=35, color=WHITE)

doc.save(pdf_path)

# Generate JPG
pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # 2000x2000 high res
pix.save(jpg_path)

print(f"Created PDF: {pdf_path}")
print(f"Created JPG: {jpg_path}")
