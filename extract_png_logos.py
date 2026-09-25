from PIL import Image
import fitz
import os

repo_path = r"C:\Users\tmalu\.gemini\antigravity\scratch\Amana-capital-ea"
desktop_path = r"C:\Users\tmalu\Desktop"

logo_path = os.path.join(repo_path, "logo_transparent.png")
linkedin_logo = os.path.join(repo_path, "linkedin-logo.png")

# Let's save both to desktop so the user has the options.
def process_logo(input_png, out_prefix):
    if not os.path.exists(input_png):
        print(f"Not found: {input_png}")
        return
        
    img = Image.open(input_png)
    
    # Save as JPG (needs white bg)
    rgb_img = Image.new("RGB", img.size, (255, 255, 255))
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        rgb_img.paste(img, mask=img.convert('RGBA').split()[3])
    else:
        rgb_img = img.convert("RGB")
        
    jpg_path = os.path.join(desktop_path, f"{out_prefix}.jpg")
    rgb_img.save(jpg_path, "JPEG", quality=100)
    print(f"Saved: {jpg_path}")
    
    # Save as PDF
    pdf_path = os.path.join(desktop_path, f"{out_prefix}.pdf")
    # We can create a simple PDF from the image
    doc = fitz.open()
    page = doc.new_page(width=img.width, height=img.height)
    page.insert_image(page.rect, filename=input_png)
    doc.save(pdf_path)
    print(f"Saved: {pdf_path}")

process_logo(logo_path, "Amana_Logo_Extracted")
process_logo(linkedin_logo, "Amana_LinkedIn_Logo_Extracted")
