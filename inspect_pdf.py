import fitz

doc = fitz.open("Basic-English-Grammar Book.pdf")
print(f"Number of pages: {len(doc)}")

for i in range(min(10, len(doc))):
    page = doc.load_page(i)
    text = page.get_text()
    print(f"--- Page {i+1} ---")
    print(text)
    print("\n")
