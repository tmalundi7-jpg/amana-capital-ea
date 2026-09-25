import fitz
import os

pdf_path = r"C:\Users\tmalu\Desktop\Amana_DSE_Daily_Wrap_23Sep_COMPANY_DESIGNED_Final_v3.pdf"
out_dir = r"C:\Users\tmalu\Desktop"

doc = fitz.open(pdf_path)
image_list = []
for page_index in range(len(doc)):
    page = doc[page_index]
    images = page.get_images(full=True)
    if images:
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_name = f"extracted_logo_{page_index}_{img_index}.{image_ext}"
            image_path = os.path.join(out_dir, image_name)
            with open(image_path, "wb") as f:
                f.write(image_bytes)
            image_list.append(image_path)
            
print(f"Extracted images: {image_list}")
