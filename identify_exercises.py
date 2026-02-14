import json
import os

def identify():
    with open('app/data.json', 'r') as f:
        data = json.load(f)

    exercise_pages = []
    for page in data:
        page_num = page['page_num']
        text = ""
        for block in page['blocks']:
            if block['type'] == 0:
                for line in block['lines']:
                    text += "".join(span['text'] for span in line['spans']) + " "

        has_blanks = '____' in text
        has_circle = 'circle' in text.lower() or 'underline' in text.lower()

        if has_blanks or has_circle:
            exercise_pages.append({
                'page': page_num,
                'has_blanks': has_blanks,
                'has_circle': has_circle
            })

    print(f"Found {len(exercise_pages)} potential exercise pages.")
    for ep in exercise_pages[:20]: # Show first 20
        print(ep)

if __name__ == "__main__":
    identify()
