from PIL import Image, ImageDraw, ImageFont
import os

# Create a 1200x630 image with Amana Navy background
img = Image.new('RGB', (1200, 630), color=(11, 29, 58))
d = ImageDraw.Draw(img)

# Try to find a nice font, otherwise use default
try:
    font_large = ImageFont.truetype("arial.ttf", 80)
    font_medium = ImageFont.truetype("arial.ttf", 40)
    font_small = ImageFont.truetype("arial.ttf", 30)
except:
    # On Windows, arial.ttf is usually at C:\Windows\Fonts\arial.ttf
    try:
        font_large = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 80)
        font_medium = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 40)
        font_small = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 30)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

# Text
title = "Amana Capital"
subtitle = "Institutional DSE Analysis & Tanzania Investment Advisory"
url = "www.amana-capital-ea.co.tz"

# Get text bounding boxes to center them
bbox_title = d.textbbox((0, 0), title, font=font_large)
w_title = bbox_title[2] - bbox_title[0]

bbox_subtitle = d.textbbox((0, 0), subtitle, font=font_medium)
w_subtitle = bbox_subtitle[2] - bbox_subtitle[0]

bbox_url = d.textbbox((0, 0), url, font=font_small)
w_url = bbox_url[2] - bbox_url[0]

# Draw title (Gold)
d.text(((1200-w_title)/2, 220), title, fill=(229, 177, 59), font=font_large)

# Draw subtitle (Cream)
d.text(((1200-w_subtitle)/2, 340), subtitle, fill=(251, 247, 240), font=font_medium)

# Draw URL (Cream/Faded)
d.text(((1200-w_url)/2, 450), url, fill=(200, 200, 200), font=font_small)

# Add a gold accent line
d.line([(400, 315), (800, 315)], fill=(229, 177, 59), width=3)

# Save
img.save('og-image.png')
print("og-image.png created!")
