import fitz
import json

def extract_toc(pdf_path):
    doc = fitz.open(pdf_path)
    toc = []

    # Simple heuristic: Look for large bold text at the start of pages
    for i in range(len(doc)):
        page = doc.load_page(i)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["size"] > 20 and "Bold" in span["font"]:
                            title = span["text"].strip()
                            if title and len(title) > 3:
                                # Check if already added
                                if not any(t["title"] == title for t in toc):
                                    toc.append({"title": title, "page": i + 1})
                                break
                    else: continue
                    break
                else: continue
                break
    return toc

if __name__ == "__main__":
    pdf_path = "Basic-English-Grammar Book.pdf"
    toc = extract_toc(pdf_path)
    with open("app/toc.json", "w") as f:
        json.dump(toc, f, indent=2)
    print(f"Extracted {len(toc)} TOC items")
