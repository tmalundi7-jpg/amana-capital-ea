from PIL import Image

try:
    # Create a 300x300 image with Amana Navy background
    img = Image.new('RGB', (300, 300), color=(11, 29, 58))
    
    # Open the logo
    logo = Image.open('favicon-192x192.png').convert("RGBA")
    
    # Resize slightly to fit well within the 300x300 square
    logo = logo.resize((180, 180), Image.Resampling.LANCZOS)
    logo_w, logo_h = logo.size
    
    # Center it
    logo_x = int((300 - logo_w) / 2)
    logo_y = int((300 - logo_h) / 2)
    
    img.paste(logo, (logo_x, logo_y), mask=logo)
    
    # Save the logo for LinkedIn
    img.save('linkedin-logo.png')
    print("linkedin-logo.png created!")
except Exception as e:
    print("Error:", e)
