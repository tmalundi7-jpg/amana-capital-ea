from PIL import Image, ImageDraw, ImageFont

# LinkedIn Cover Image standard size is 1128 x 191 px
img = Image.new('RGB', (1128, 191), color=(11, 29, 58))
d = ImageDraw.Draw(img)

try:
    font_large = ImageFont.truetype(r"C:\Windows\Fonts\georgia.ttf", 36)
    font_small = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 16)
except:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Text
title = "INSTITUTIONAL-GRADE MARKET INTELLIGENCE"
subtitle = "Tanzania Investment Advisory  |  Equities & Fixed Income  |  Strategic Research"

bbox_title = d.textbbox((0, 0), title, font=font_large)
w_title = bbox_title[2] - bbox_title[0]

bbox_subtitle = d.textbbox((0, 0), subtitle, font=font_small)
w_subtitle = bbox_subtitle[2] - bbox_subtitle[0]

# Draw text centered vertically and horizontally
d.text(((1128-w_title)/2, 60), title, fill=(229, 177, 59), font=font_large)
d.text(((1128-w_subtitle)/2, 120), subtitle, fill=(251, 247, 240), font=font_small)

# Add a subtle gold line at the bottom
d.line([(0, 188), (1128, 188)], fill=(229, 177, 59), width=3)

# Save
img.save('linkedin-cover.png')
print("linkedin-cover.png created!")
