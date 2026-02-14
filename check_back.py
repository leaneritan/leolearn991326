import fitz

doc = fitz.open("Basic-English-Grammar Book.pdf")
num_pages = len(doc)
for i in range(num_pages - 10, num_pages):
    page = doc.load_page(i)
    text = page.get_text()
    print(f"--- Page {i+1} ---")
    print(text)
    print("\n")
