import json

with open("book_data.json", "r") as f:
    data = json.load(f)

for page in data:
    page_text = ""
    for block in page["blocks"]:
        if "lines" in block:
            for line in block["lines"]:
                for span in line["spans"]:
                    page_text += span["text"] + " "

    if "answer" in page_text.lower() or "key" in page_text.lower():
        print(f"Found on page {page['page_num']}: {page_text[:100]}...")
