import fitz
import json
import os
import re

def extract_book(pdf_path, output_dir="app"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    img_dir = os.path.join(output_dir, "images")
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    doc = fitz.open(pdf_path)
    pages_data = []

    for i in range(len(doc)):
        page = doc.load_page(i)
        text_dict = page.get_text("dict")

        clean_blocks = []
        for block in text_dict["blocks"]:
            if block["type"] == 0: # text
                clean_blocks.append(json.loads(json.dumps(block, default=str)))
            elif block["type"] == 1: # image
                img_ext = block["ext"]
                img_filename = f"page_{i+1}_block_{block['number']}.{img_ext}"
                if "image" in block:
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

    # Save data.json
    with open(os.path.join(output_dir, "data.json"), "w") as f:
        json.dump(pages_data, f)

    # Extract TOC from page 5 (index 4)
    toc = extract_toc_from_dict(pages_data[4])
    with open(os.path.join(output_dir, "toc.json"), "w") as f:
        json.dump(toc, f, indent=2)

def extract_toc_from_dict(toc_page_data):
    blocks = toc_page_data['blocks']
    lines = []
    for block in blocks:
        if block['type'] == 0:
            for line in block['lines']:
                y = (line['bbox'][1] + line['bbox'][3]) / 2
                x = line['bbox'][0]
                text = "".join(span['text'] for span in line['spans']).strip()
                font = line['spans'][0]['font']
                lines.append({'y': y, 'x': x, 'text': text, 'font': font})

    mid = toc_page_data['width'] / 2
    left_column_lines = sorted([l for l in lines if l['x'] < mid], key=lambda l: l['y'])
    right_column_lines = sorted([l for l in lines if l['x'] >= mid], key=lambda l: l['y'])

    def group_by_y(column_lines):
        grouped = []
        if not column_lines: return []
        sorted_lines = sorted(column_lines, key=lambda l: l['y'])
        curr = [sorted_lines[0]]
        for i in range(1, len(sorted_lines)):
            if abs(sorted_lines[i]['y'] - curr[0]['y']) < 5:
                curr.append(sorted_lines[i])
            else:
                grouped.append(curr)
                curr = [sorted_lines[i]]
        grouped.append(curr)
        return grouped

    left_groups = group_by_y(left_column_lines)
    right_groups = group_by_y(right_column_lines)

    all_items = []
    current_chapter = None

    for groups in [left_groups, right_groups]:
        for group in groups:
            group.sort(key=lambda l: l['x'])
            full_text = " ".join(l['text'] for l in group).replace('\t', ' ').strip()

            # Check if it's a chapter header
            is_chapter_num = any(l['font'] == 'Arial-Black' for l in group)
            is_chapter_title = any(l['font'] == 'VAGRounded-Bold' for l in group)

            # Regex to find title and page at the end
            match = re.search(r'(.*?)\s+(\d+)$', full_text)
            if match:
                title = match.group(1).strip()
                page = int(match.group(2)) + 1
            else:
                title = full_text
                page = None

            if is_chapter_num:
                # New chapter
                current_chapter = {"title": "", "page": page, "subsections": []}
                all_items.append(current_chapter)
                # If it also has title on same line
                if title and not title.isdigit():
                    current_chapter['title'] = title
            elif is_chapter_title:
                if current_chapter and not current_chapter['title']:
                    current_chapter['title'] = title
                    if page: current_chapter['page'] = page
                else:
                    # New chapter without number?
                    current_chapter = {"title": title, "page": page, "subsections": []}
                    all_items.append(current_chapter)
            elif current_chapter and title:
                # Subsection
                current_chapter['subsections'].append({"title": title, "page": page})

    # Cleanup: remove chapters without title
    all_items = [c for c in all_items if c['title']]
    return all_items

if __name__ == "__main__":
    extract_book("Basic-English-Grammar Book.pdf")
