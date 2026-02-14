import fitz
import json
import os

def extract_all(pdf_path, output_dir="app"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    img_dir = os.path.join(output_dir, "images")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    doc = fitz.open(pdf_path)
    pages_data = []

    for i in range(len(doc)):
        page = doc.load_page(i)

        # Text extraction with dict to get spans/styles
        text_dict = page.get_text("dict")

        # Process blocks to remove non-serializable data and save images
        clean_blocks = []
        for block in text_dict["blocks"]:
            if block["type"] == 0: # text
                clean_blocks.append(json.loads(json.dumps(block, default=str)))
            elif block["type"] == 1: # image
                img_ext = block["ext"]
                img_filename = f"page_{i+1}_block_{block['number']}.{img_ext}"
                with open(os.path.join(img_dir, img_filename), "wb") as f:
                    f.write(block["image"])

                img_block = {
                    "type": 1,
                    "bbox": list(block["bbox"]),
                    "src": f"images/{img_filename}",
                    "width": block["width"],
                    "height": block["height"]
                }
                clean_blocks.append(img_block)

        pages_data.append({
            "page_num": i + 1,
            "width": page.rect.width,
            "height": page.rect.height,
            "blocks": clean_blocks
        })

    return pages_data

if __name__ == "__main__":
    pdf_path = "Basic-English-Grammar Book.pdf"
    data = extract_all(pdf_path)
    with open("app/data.json", "w") as f:
        json.dump(data, f, indent=2)
    print(f"Extracted {len(data)} pages to app/data.json and app/images/")
