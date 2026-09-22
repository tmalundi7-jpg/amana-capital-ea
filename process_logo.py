from PIL import Image

def process():
    try:
        img = Image.open(r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\linkedin-logo.png").convert("RGBA")
        data = img.getdata()
        new_data = []
        for item in data:
            if abs(item[0]-11) < 20 and abs(item[1]-29) < 20 and abs(item[2]-58) < 20:
                new_data.append((255, 255, 255, 0)) # Make navy background fully transparent
            else:
                new_data.append(item) # Keep the gold/cream parts
        img.putdata(new_data)
        img.save(r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea\logo_transparent.png", "PNG")
        print("Transparent logo saved.")
    except Exception as e:
        print("Error:", e)

process()
