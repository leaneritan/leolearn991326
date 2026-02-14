import fitz
import json
import re

def extract_toc(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[4] # Page 5
    text_dict = page.get_text("dict")

    lines = []
    for block in text_dict["blocks"]:
        if block["type"] == 0:
            for line in block["lines"]:
                y = (line["bbox"][1] + line["bbox"][3]) / 2
                x = line["bbox"][0]
                text = "".join(span["text"] for span in line["spans"]).strip()
                font = line["spans"][0]["font"]
                lines.append({"y": y, "x": x, "text": text, "font": font})

    # Split into two columns
    mid = page.rect.width / 2
    left_column_lines = sorted([l for l in lines if l["x"] < mid], key=lambda l: l["y"])
    right_column_lines = sorted([l for l in lines if l["x"] >= mid], key=lambda l: l["y"])

    def group_by_y(column_lines):
        grouped = []
        if not column_lines: return []
        # Sort by Y first
        sorted_lines = sorted(column_lines, key=lambda l: l['y'])
        curr = [sorted_lines[0]]
        for i in range(1, len(sorted_lines)):
            if abs(sorted_lines[i]['y'] - curr[0]['y']) < 3: # Tight threshold for same line
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

    # Process both columns in order
    for groups in [left_groups, right_groups]:
        for group in groups:
            group.sort(key=lambda l: l['x'])
            text = " ".join(l['text'] for l in group).strip()
            font = group[0]['font']

            # Heuristics based on observed debug output
            if font == 'Arial-Black':
                # Chapter number
                if current_chapter and not current_chapter['title']:
                    # Should not happen if structured
                    pass
                current_chapter = {"title": "", "page": None, "subsections": []}
                all_items.append(current_chapter)
            elif font == 'VAGRounded-Bold':
                # Chapter title (sometimes includes number like "13 Sentences")
                if not current_chapter:
                    current_chapter = {"title": text, "page": None, "subsections": []}
                    all_items.append(current_chapter)
                else:
                    if not current_chapter['title']:
                        current_chapter['title'] = text
                    else:
                        # Maybe a new chapter without Arial-Black number?
                        current_chapter = {"title": text, "page": None, "subsections": []}
                        all_items.append(current_chapter)
            elif font == 'VAGRounded-Light':
                if text.isdigit():
                    pg = int(text) + 1 # App page offset
                    if current_chapter:
                        if current_chapter['subsections']:
                            if current_chapter['subsections'][-1]['page'] is None:
                                current_chapter['subsections'][-1]['page'] = pg
                            else:
                                # Page for the chapter itself?
                                current_chapter['page'] = pg
                        elif current_chapter['page'] is None:
                            current_chapter['page'] = pg
                else:
                    # Subsection title
                    if current_chapter:
                        current_chapter['subsections'].append({"title": text, "page": None})

    return all_items

if __name__ == "__main__":
    toc = extract_toc("Basic-English-Grammar Book.pdf")
    print(json.dumps(toc, indent=2))
