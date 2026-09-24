import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# Colors
NAVY = colors.HexColor('#0B1D3A')
GOLD = colors.HexColor('#C8962E')
CREAM = colors.HexColor('#FBF7F0')
TEAL = colors.HexColor('#1E3A5F')
GREEN = colors.HexColor('#22C55E')
RED = colors.HexColor('#EF4444')
MIST = colors.HexColor('#8A94A6')

# 1. Company Carousel PDF (Amana_Wrap_Carousel_22Sep.pdf)
# We will create a 3-page carousel
c1 = canvas.Canvas(r'C:\Users\tmalu\Desktop\Amana_Wrap_Carousel_22Sep.pdf', pagesize=landscape(letter))
width, height = landscape(letter)

def draw_header_footer(c, page_num):
    c.setFillColor(NAVY)
    c.rect(0, 0, width, height, fill=1)
    
    # Header
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, height - 40, "AMANA CAPITAL EAST AFRICA")
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 10)
    c.drawString(width - 150, height - 40, "22 SEPTEMBER 2026")
    
    # Footer
    c.setFillColor(MIST)
    c.setFont("Helvetica", 8)
    c.drawString(40, 20, "Registration Pending CMSA | Not financial advice. Capital at risk.")
    c.drawRightString(width - 40, 20, "www.amana-capital-ea.co.tz")
    
    # Page indicator
    c.setFillColor(GOLD)
    for i in range(3):
        if i + 1 == page_num:
            c.circle(width/2 - 20 + (i*20), 30, 4, fill=1, stroke=0)
        else:
            c.setStrokeColor(GOLD)
            c.circle(width/2 - 20 + (i*20), 30, 4, fill=0, stroke=1)

# Slide 1: Title & Macro
draw_header_footer(c1, 1)
c1.setFillColor(CREAM)
c1.setFont("Helvetica-Bold", 36)
c1.drawString(40, height - 150, "DAILY DSE WRAP")
c1.setFont("Helvetica", 20)
c1.drawString(40, height - 190, "VODA Hits Limit-Up. Bonds Explode.")

c1.setStrokeColor(GOLD)
c1.setLineWidth(2)
c1.line(40, height - 230, 300, height - 230)

# Macro Stats
c1.setFont("Helvetica-Bold", 16)
c1.setFillColor(MIST)
c1.drawString(40, height - 280, "TURNOVER")
c1.drawString(250, height - 280, "DSEI")
c1.drawString(450, height - 280, "BONDS")

c1.setFont("Helvetica-Bold", 28)
c1.setFillColor(CREAM)
c1.drawString(40, height - 320, "TZS 5.07B")
c1.drawString(250, height - 320, "4,659.23")
c1.drawString(450, height - 320, "TZS 33.59B")

c1.setFillColor(GREEN)
c1.setFont("Helvetica-Bold", 14)
c1.drawString(250, height - 340, "+25 pts (New High)")
c1.showPage()

# Slide 2: VODA & CRDB
draw_header_footer(c1, 2)
c1.setFillColor(GOLD)
c1.setFont("Helvetica-Bold", 24)
c1.drawString(40, height - 100, "THE ORDER BOOK REVEALS ALL")

# VODA box
c1.setFillColor(TEAL)
c1.rect(40, height - 280, 300, 150, fill=1)
c1.setFillColor(CREAM)
c1.setFont("Helvetica-Bold", 20)
c1.drawString(60, height - 160, "VODA")
c1.setFillColor(GREEN)
c1.drawString(250, height - 160, "+4.8%")
c1.setFillColor(CREAM)
c1.setFont("Helvetica", 14)
c1.drawString(60, height - 200, "Price: 1,320 (Limit-Up)")
c1.drawString(60, height - 230, "Bids: 23,119")
c1.drawString(60, height - 250, "Offers: 24,814 (Balanced)")

# CRDB box
c1.setFillColor(TEAL)
c1.rect(380, height - 280, 300, 150, fill=1)
c1.setFillColor(CREAM)
c1.setFont("Helvetica-Bold", 20)
c1.drawString(400, height - 160, "CRDB")
c1.setFillColor(MIST)
c1.drawString(590, height - 160, "FLAT")
c1.setFillColor(CREAM)
c1.setFont("Helvetica", 14)
c1.drawString(400, height - 200, "Price: 2,810")
c1.drawString(400, height - 230, "Bids: 192,156")
c1.drawString(400, height - 250, "Offers: 49,819 (3.9x Ratio)")
c1.showPage()

# Slide 3: Movers & Flows
draw_header_footer(c1, 3)
c1.setFillColor(GOLD)
c1.setFont("Helvetica-Bold", 24)
c1.drawString(40, height - 100, "MOVERS & CAPITAL FLOWS")

c1.setFillColor(CREAM)
c1.setFont("Helvetica-Bold", 16)
c1.drawString(40, height - 150, "TOP MOVERS")
c1.setFont("Helvetica", 16)
c1.drawString(40, height - 180, "AFRIPRISE:")
c1.setFillColor(GREEN)
c1.drawString(150, height - 180, "+5.4%")
c1.setFillColor(CREAM)
c1.drawString(40, height - 210, "TCCL:")
c1.setFillColor(RED)
c1.drawString(150, height - 210, "-5.1%")

c1.setFillColor(CREAM)
c1.setFont("Helvetica-Bold", 16)
c1.drawString(380, height - 150, "CAPITAL FLOWS")
c1.setFont("Helvetica", 14)
c1.drawString(380, height - 180, "Foreign Selling: 57.58% (TZS 2.92B)")
c1.drawString(380, height - 210, "Local Buying: 99.88%")
c1.setFillColor(GOLD)
c1.drawString(380, height - 260, "Insight: Local institutions")
c1.drawString(380, height - 280, "are absorbing foreign exits")
c1.drawString(380, height - 300, "with total ease.")

c1.showPage()
c1.save()

# 2. Personal Thumbnail PDF (Amana_Personal_Thumbnail_22Sep.pdf)
# Single page punchy graphic
c2 = canvas.Canvas(r'C:\Users\tmalu\Desktop\Amana_Personal_Thumbnail_22Sep.pdf', pagesize=landscape(letter))
c2.setFillColor(NAVY)
c2.rect(0, 0, width, height, fill=1)

c2.setFillColor(GOLD)
c2.setFont("Helvetica-Bold", 14)
c2.drawString(40, height - 40, "MARKET PSYCHOLOGY")

c2.setFillColor(CREAM)
c2.setFont("Helvetica-Bold", 40)
c2.drawString(40, height - 150, "WHEN A STOCK")
c2.drawString(40, height - 195, "HITS THE CEILING.")

c2.setFont("Helvetica", 20)
c2.setFillColor(MIST)
c2.drawString(40, height - 250, "VODA surged 4.8% to hit the 5% daily limit.")
c2.drawString(40, height - 280, "CRDB hides a 3.9x buyer ratio while closing flat.")
c2.drawString(40, height - 310, "What does it actually mean?")

c2.setStrokeColor(GOLD)
c2.setLineWidth(2)
c2.line(40, 100, 200, 100)
c2.setFont("Helvetica-Bold", 14)
c2.setFillColor(GOLD)
c2.drawString(40, 70, "Read the full breakdown below")

c2.showPage()
c2.save()

print("PDFs generated successfully.")
