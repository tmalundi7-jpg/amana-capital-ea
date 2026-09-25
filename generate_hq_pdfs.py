import fitz
import os

desktop_path = r"C:\Users\tmalu\Desktop"

def create_hq(pdf_path):
    doc = fitz.open(pdf_path)
    hq_path = pdf_path.replace(".pdf", "_HQ.pdf")
    hq_doc = fitz.open()
    
    for page in doc:
        # Scale 3x
        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
        # Create new PDF page
        new_page = hq_doc.new_page(width=pix.width, height=pix.height)
        new_page.insert_image(new_page.rect, pixmap=pix)
        
    try:
        hq_doc.save(hq_path, garbage=4, deflate=True)
        print(f"Created HQ: {hq_path}")
    except Exception as e:
        print(f"Error saving {hq_path}: {e}")

create_hq(os.path.join(desktop_path, "Amana_DSE_Daily_Wrap_24Sep_COMPANY.pdf"))
create_hq(os.path.join(desktop_path, "Amana_DSE_Daily_Wrap_24Sep_PERSONAL.pdf"))
