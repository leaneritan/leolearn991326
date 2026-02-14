import fitz
import json

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    pages_data = []

    for i in range(len(doc)):
        page = doc.load_page(i)
        blocks = page.get_text("blocks")
        # blocks is a list of tuples: (x0, y0, x1, y1, "text", block_no, block_type)
        page_blocks = []
        for b in blocks:
            page_blocks.append({
                "bbox": b[:4],
                "text": b[4],
                "type": b[6]
            })
        pages_data.append({
            "page_num": i + 1,
            "blocks": page_blocks
        })

    return pages_data

if __name__ == "__main__":
    pdf_path = "Basic-English-Grammar Book.pdf"
    data = extract_text(pdf_path)
    with open("book_text.json", "w") as f:
        json.dump(data, f)
    print(f"Extracted {len(data)} pages of text to book_text.json")
