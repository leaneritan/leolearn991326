import fitz
import json

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    pages_data = []

    for i in range(len(doc)):
        page = doc.load_page(i)
        text = page.get_text("dict")
        pages_data.append({
            "page_num": i + 1,
            "blocks": text["blocks"]
        })

    return pages_data

if __name__ == "__main__":
    pdf_path = "Basic-English-Grammar Book.pdf"
    data = extract_text(pdf_path)
    with open("book_text.json", "w") as f:
        json.dump(data, f)
    print(f"Extracted {len(data)} pages of text to book_text.json")
