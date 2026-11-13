
import cv2
import csv
import shutil

from pathlib import Path

RAW_DIR = Path("dataset/raw")
LABELED_DIR = Path("dataset/labeled")
METADATA_DIR = Path("dataset/metadata")
CSV_FILE = METADATA_DIR / "labels.csv"

# Teclas de classificação
KEYS = {
    ord("1"): "light_pawn",
    ord("2"): "light_knight",
    ord("3"): "light_bishop",
    ord("4"): "light_rook",
    ord("5"): "light_queen",
    ord("6"): "light_king",

    ord("a"): "dark_pawn",
    ord("s"): "dark_knight",
    ord("d"): "dark_bishop",
    ord("f"): "dark_rook",
    ord("g"): "dark_queen",
    ord("h"): "dark_king",

    ord("0"): "empty"
}


def load_labels():
    if not CSV_FILE.exists():
        return []

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def save_labels(labels):
    METADATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["square", "class", "filename"]
        )

        writer.writeheader()
        writer.writerows(labels)


def show_instructions(image, square, current, total):
    display = cv2.resize(image, (400, 400))

    cv2.putText(
        display,
        f"Square: {square} ({current}/{total})",
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 0),
        2
    )

    return display


def main():
    images = sorted(RAW_DIR.glob("*.png"))

    if not images:
        print("Nenhuma imagem encontrada em dataset/raw/")
        return

    labels = load_labels()

    labeled_squares = {
        item["square"] for item in labels
    }

    pending = [
        image for image in images
        if image.stem not in labeled_squares
    ]

    if not pending:
        print("Todas as casas já foram classificadas!")
        return

    print("\n=== CHESS AGENT LABELER ===")
    print("1-6: Peças claras")
    print("A/H: Peças escuras")
    print("0: Casa vazia")
    print("X: Pular")
    print("Z: Desfazer última classificação")
    print("ESC: Sair")

    index = 0

    while index < len(pending):
        image_path = pending[index]

        image = cv2.imread(str(image_path))

        if image is None:
            print("Erro ao carregar:", image_path)
            index += 1
            continue

        display = show_instructions(
            image,
            image_path.stem,
            index + 1,
            len(pending)
        )

        cv2.imshow("Chess Agent - Labeler", display)

        key = cv2.waitKey(0) & 0xFF

        if key == 27:
            break

        elif key == ord("x"):
            index += 1

        elif key == ord("z"):
            if labels:
                last = labels.pop()

                output = (
                    LABELED_DIR
                    / last["class"]
                    / last["filename"]
                )

                if output.exists():
                    output.unlink()

                save_labels(labels)
                index = 0

                labeled_squares = {
                    item["square"] for item in labels
                }

                pending = [
                    img for img in images
                    if img.stem not in labeled_squares
                ]

                print("Última classificação desfeita.")

        elif key in KEYS:
            class_name = KEYS[key]

            destination = LABELED_DIR / class_name
            destination.mkdir(parents=True, exist_ok=True)

            filename = image_path.name

            shutil.copy2(
                image_path,
                destination / filename
            )

            labels.append({
                "square": image_path.stem,
                "class": class_name,
                "filename": filename
            })

            save_labels(labels)

            print(image_path.stem, "->", class_name)

            index += 1

    cv2.destroyAllWindows()

    print("\nClassificações salvas:", len(labels))
    print("Arquivo:", CSV_FILE)


if __name__ == "__main__":
    main()
