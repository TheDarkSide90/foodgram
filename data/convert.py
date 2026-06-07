import csv
import json

INPUT_CSV = 'ingredients.csv'
OUTPUT_JSON = 'ingredients.json'

data = []

with open(INPUT_CSV, encoding='utf-8') as f:
    reader = csv.reader(f)

    for i, row in enumerate(reader, start=1):
        name, unit = row

        data.append({
            "model": "recipes.ingredient",
            "pk": i,
            "fields": {
                "name": name.strip(),
                "measurement_unit": unit.strip()
            }
        })

with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('DONE → ingredients.json created')
