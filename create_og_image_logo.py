from PIL import Image, ImageDraw, ImageFont
import os

# Create a 1200x630 image with Amana Navy background
img = Image.new('RGB', (1200, 630), color=(11, 29, 58))
d = ImageDraw.Draw(img)

try:
    font_large = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 60)
    font_medium = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 35)
    font_small = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 25)
except:
    font_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Open the logo
try:
    logo = Image.open('favicon-192x192.png').convert("RGBA")
    # Resize if needed (let's say 150x150)
    logo = logo.resize((150, 150), Image.Resampling.LANCZOS)
    logo_w, logo_h = logo.size
    # Paste logo centered horizontally, towards the top
    logo_x = int((1200 - logo_w) / 2)
    logo_y = 120
    img.paste(logo, (logo_x, logo_y), mask=logo)
    
    text_y_offset = logo_y + logo_h + 40
except Exception as e:
    print("Could not load logo:", e)
    text_y_offset = 200

# Text
title = "Amana Capital East Africa Limited"
subtitle = "Institutional DSE Analysis & Tanzania Investment Advisory"
url = "www.amana-capital-ea.co.tz"

bbox_title = d.textbbox((0, 0), title, font=font_large)
w_title = bbox_title[2] - bbox_title[0]

bbox_subtitle = d.textbbox((0, 0), subtitle, font=font_medium)
w_subtitle = bbox_subtitle[2] - bbox_subtitle[0]

bbox_url = d.textbbox((0, 0), url, font=font_small)
w_url = bbox_url[2] - bbox_url[0]

# Draw title (Gold)
d.text(((1200-w_title)/2, text_y_offset), title, fill=(229, 177, 59), font=font_large)

# Draw subtitle (Cream)
d.text(((1200-w_subtitle)/2, text_y_offset + 90), subtitle, fill=(251, 247, 240), font=font_medium)

# Draw URL (Cream/Faded)
d.text(((1200-w_url)/2, text_y_offset + 180), url, fill=(200, 200, 200), font=font_small)

# Add a gold accent line
d.line([(450, text_y_offset + 75), (750, text_y_offset + 75)], fill=(229, 177, 59), width=3)

# Save
img.save('og-image.png')
print("og-image.png created with logo!")
