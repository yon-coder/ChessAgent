
import cv2
import csv
from pathlib import Path

CSV_FILE = Path("dataset/metadata/labels.csv")
OUTPUT = Path("screenshots/dataset_review.png")

with open(CSV_FILE, newline="", encoding="utf-8") as file:
    labels = list(csv.DictReader(file))

cells = []

for item in sorted(labels, key=lambda x: x["square"]):
    path = Path("dataset/raw") / f'{item["square"]}.png'
    image = cv2.imread(str(path))

    if image is None:
        continue

    image = cv2.resize(image, (100, 100))
    label = item["class"]

    cv2.rectangle(image, (0, 75), (100, 100), (0, 0, 0), -1)
    cv2.putText(
        image,
        f'{item["square"]}: {label}',
        (2, 92),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.32,
        (255, 255, 255),
        1
    )

    cells.append(image)

rows = []

for i in range(0, len(cells), 8):
    rows.append(cv2.hconcat(cells[i:i + 8]))

grid = cv2.vconcat(rows)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
cv2.imwrite(str(OUTPUT), grid)

print(f"Grade salva em: {OUTPUT}")
