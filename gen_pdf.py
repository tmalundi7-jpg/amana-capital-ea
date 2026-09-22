from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import os

# Colors
navy = colors.HexColor('#0B1D3A')
gold = colors.HexColor('#C8962E')
teal = colors.HexColor('#0D9488')
cream = colors.HexColor('#FBF7F0')
white = colors.white
red = colors.HexColor('#FF0000')
green = colors.HexColor('#00B050')

def create_carousel(filepath):
    # Amana Capital Carousel
    c = canvas.Canvas(filepath, pagesize=(800, 800))
    
    # Page 1: Title
    c.setFillColor(navy)
    c.rect(0, 0, 800, 800, fill=1)
    
    c.setFillColor(gold)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, 720, "AMANA CAPITAL EAST AFRICA")
    
    c.setFillColor(teal)
    c.setFont("Helvetica", 18)
    c.drawString(50, 680, "DAILY DSE WRAP | 21 SEPTEMBER 2026")
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 60)
    c.drawString(50, 500, "100,177 Bids.")
    c.drawString(50, 420, "Zero Offers.")
    
    c.setFillColor(cream)
    c.setFont("Helvetica", 24)
    c.drawString(50, 320, "Supply has completely evaporated on VODA.")
    c.drawString(50, 280, "Local institutions take absolute control.")
    
    # Footer
    c.setFillColor(gold)
    c.setFont("Helvetica", 14)
    c.drawString(50, 50, "www.amana-capital-ea.co.tz")
    c.showPage()
    
    # Page 2: Market Snapshot
    c.setFillColor(navy)
    c.rect(0, 0, 800, 800, fill=1)
    
    c.setFillColor(gold)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, 720, "MARKET SNAPSHOT")
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 40)
    c.drawString(50, 600, "TZS 11.76 Billion")
    c.setFillColor(cream)
    c.setFont("Helvetica", 20)
    c.drawString(50, 560, "Total Equity Turnover (Up 173%)")
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 40)
    c.drawString(50, 440, "99.99%")
    c.setFillColor(cream)
    c.setFont("Helvetica", 20)
    c.drawString(50, 400, "Local Investor Buying Share")
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 40)
    c.drawString(50, 280, "TZS 5.74 Billion")
    c.setFillColor(cream)
    c.setFont("Helvetica", 20)
    c.drawString(50, 240, "Government Bond Turnover")
    
    c.setFillColor(gold)
    c.setFont("Helvetica", 14)
    c.drawString(50, 50, "www.amana-capital-ea.co.tz")
    c.showPage()
    
    # Page 3: Top Movers
    c.setFillColor(navy)
    c.rect(0, 0, 800, 800, fill=1)
    
    c.setFillColor(gold)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, 720, "TOP MOVERS")
    
    # Gainers Table
    c.setFillColor(green)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, 600, "GAINERS")
    
    c.setFillColor(white)
    c.setFont("Helvetica", 20)
    c.drawString(50, 550, "VODA")
    c.drawString(200, 550, "+3.3%")
    c.drawString(50, 500, "PAL")
    c.drawString(200, 500, "+3.3%")
    c.drawString(50, 450, "NMB")
    c.drawString(200, 450, "+2.9%")
    c.drawString(50, 400, "MUCOBA")
    c.drawString(200, 400, "+2.5%")
    
    # Losers Table
    c.setFillColor(red)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(450, 600, "LOSERS")
    
    c.setFillColor(white)
    c.setFont("Helvetica", 20)
    c.drawString(450, 550, "MCB")
    c.drawString(600, 550, "-3.8%")
    c.drawString(450, 500, "DSE")
    c.drawString(600, 500, "-2.7%")
    c.drawString(450, 450, "SWIS")
    c.drawString(600, 450, "-1.5%")
    c.drawString(450, 400, "TOL")
    c.drawString(600, 400, "-1.1%")
    
    # Order book highlight
    c.setFillColor(teal)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, 250, "ORDER BOOK SIGNAL:")
    c.setFillColor(cream)
    c.setFont("Helvetica", 18)
    c.drawString(50, 210, "CRDB closed flat, but buyers outnumbered sellers 2.8 to 1.")
    c.drawString(50, 170, "Demand is building beneath the surface.")
    
    c.setFillColor(gold)
    c.setFont("Helvetica", 14)
    c.drawString(50, 50, "www.amana-capital-ea.co.tz")
    c.showPage()
    
    c.save()

def create_thumbnail(filepath):
    # Personal Thumbnail
    c = canvas.Canvas(filepath, pagesize=(800, 800))
    
    c.setFillColor(navy)
    c.rect(0, 0, 800, 800, fill=1)
    
    # Aesthetic borders
    c.setStrokeColor(gold)
    c.setLineWidth(4)
    c.rect(40, 40, 720, 720)
    
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 48)
    c.drawString(80, 650, "IF YOU ONLY LOOK")
    c.drawString(80, 590, "AT THE CLOSING PRICE,")
    c.setFillColor(teal)
    c.drawString(80, 530, "YOU ARE TRADING BLIND.")
    
    c.setFillColor(gold)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(80, 380, "VODA ORDER BOOK:")
    
    c.setFillColor(green)
    c.setFont("Helvetica-Bold", 50)
    c.drawString(80, 280, "100,177 BIDS")
    
    c.setFillColor(red)
    c.setFont("Helvetica-Bold", 50)
    c.drawString(80, 200, "0 OFFERS")
    
    c.setFillColor(cream)
    c.setFont("Helvetica", 16)
    c.drawString(80, 80, "Market Intelligence | 21 Sep 2026")
    
    c.save()

desktop = r'C:\Users\tmalu\Desktop'
create_carousel(os.path.join(desktop, 'Amana_Wrap_Carousel_21Sep.pdf'))
create_thumbnail(os.path.join(desktop, 'Amana_Personal_Thumbnail_21Sep.pdf'))
print("PDFs generated!")
