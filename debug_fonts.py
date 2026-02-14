import json
with open('app/data.json') as f:
    data = json.load(f)
    page = data[0]
    for block in page['blocks']:
        if block['type'] == 0:
            for line in block['lines']:
                for span in line['spans']:
                    print(f"Text: {span['text']}, Size: {span['size']}, Font: {span['font']}")
