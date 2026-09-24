import fitz
import math

NAVY     = (11/255,  29/255,  58/255)
CREAM    = (251/255, 247/255, 240/255)
GOLD     = (200/255, 150/255, 46/255)
TAUPE    = (154/255, 148/255, 144/255)

W, H = 1080, 1080
MARGIN = 100

doc = fitz.open()
page = doc.new_page(width=W, height=H)
shape = page.new_shape()
shape.draw_rect(fitz.Rect(0, 0, W, H))
shape.finish(fill=NAVY)
shape.draw_rect(fitz.Rect(0, 0, W, 6))
shape.finish(fill=GOLD)
shape.commit()

# Logo
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

page.insert_text((162.8, 1016.0), "AMANA CAPITAL", fontname="hebo", fontsize=19, color=CREAM)
page.insert_text((162.8, 1036.0), "East Africa Limited", fontname="helv", fontsize=15, color=GOLD)

page.insert_text((MARGIN, 280), "WHEN A", fontname="hebo", fontsize=112, color=CREAM)
page.insert_text((MARGIN, 392), "STOCK", fontname="hebo", fontsize=112, color=CREAM)
page.insert_text((MARGIN, 504), "HITS THE", fontname="hebo", fontsize=112, color=CREAM)
page.insert_text((MARGIN, 616), "CEILING.", fontname="hebo", fontsize=112, color=GOLD)

page.insert_text((MARGIN, 710), "VODA surged 4.8% to hit the 5% daily limit.", fontname="helv", fontsize=28, color=TAUPE)
page.insert_text((MARGIN, 760), "CRDB hides a 3.9x buyer ratio while closing flat.", fontname="helv", fontsize=28, color=TAUPE)
page.insert_text((MARGIN, 810), "What does it actually mean?", fontname="helv", fontsize=28, color=TAUPE)

page.insert_text((MARGIN, 890), "Read the full breakdown below \u2193", fontname="hebo", fontsize=22, color=GOLD)

out_path = r'C:\Users\tmalu\Desktop\Amana_Personal_Thumbnail_22Sep_v2.pdf'
doc.save(out_path, garbage=4, deflate=True)
doc.close()
print("Saved:", out_path)
