import fitz
import os

doc = fitz.open("Basic-English-Grammar Book.pdf")
os.makedirs("images", exist_ok=True)

for i in range(len(doc)):
    page = doc.load_page(i)
    image_list = page.get_images(full=True)
    for img_index, img in enumerate(image_list):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        with open(f"images/page_{i+1}_img_{img_index}.{image_ext}", "wb") as f:
            f.write(image_bytes)

print(f"Extracted images from {len(doc)} pages.")
