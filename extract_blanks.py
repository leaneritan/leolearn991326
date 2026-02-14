import json
import re

def extract_blanks_context(data_path):
    with open(data_path, 'r') as f:
        pages = json.load(f)

    blanks = []
    for page in pages:
        page_num = page['page_num']
        for block in page['blocks']:
            if block['type'] == 0:
                for line_idx, line in enumerate(block['lines']):
                    line_text = "".join(span['text'] for span in line['spans'])
                    if '____' in line_text:
                        # Get some context
                        context = line_text

                        # Find all blanks in this line
                        # We need to match what processInteractiveSpan in index.html does
                        parts = re.split(r'_{2,}', line_text)

                        # We'll use the same key generation logic as in index.html
                        # key = `ans_${pageNum}_${Math.round(x)}_${Math.round(y)}_${i}`;
                        # Note: origin is [x, y]

                        for i, span in enumerate(line['spans']):
                            if '____' in span['text']:
                                x = round((span['origin'][0] / page['width']) * 100)
                                y = round((span['origin'][1] / page['height']) * 100)

                                # Since a span might have multiple blanks (unlikely but possible)
                                span_parts = re.split(r'_{2,}', span['text'])
                                for j in range(len(span_parts) - 1):
                                    blanks.append({
                                        "page": page_num,
                                        "x": x,
                                        "y": y,
                                        "span_index": i,
                                        "blank_index": j,
                                        "text": line_text,
                                        "key": f"ans_{page_num}_{x}_{y}_{j}"
                                    })

    return blanks

if __name__ == "__main__":
    blanks = extract_blanks_context('app/data.json')
    with open('blanks_context.json', 'w') as f:
        json.dump(blanks, f, indent=2)
    print(f"Extracted {len(blanks)} blanks.")
