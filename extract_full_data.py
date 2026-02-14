import fitz
import json
import base64
import os

def extract_content(pdf_path):
    doc = fitz.open(pdf_path)
    pages_data = []

    for i in range(len(doc)):
        page = doc.load_page(i)

        # Get text with formatting
        blocks = page.get_text("dict")["blocks"]

        # Get images
        image_list = page.get_images(full=True)
        images = []
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            encoded = base64.b64encode(image_bytes).decode('utf-8')
            images.append({
                "index": img_index,
                "ext": image_ext,
                "data": f"data:image/{image_ext};base64,{encoded}"
            })

        pages_data.append({
            "page_num": i + 1,
            "blocks": blocks,
            "images": images
        })

    return pages_data

if __name__ == "__main__":
    pdf_path = "Basic-English-Grammar Book.pdf"
    data = extract_content(pdf_path)
    with open("book_data.json", "w") as f:
        json.dump(data, f)
    print(f"Extracted {len(data)} pages to book_data.json")
