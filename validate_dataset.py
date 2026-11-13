
import csv
from pathlib import Path
from collections import Counter

RAW_DIR = Path("dataset/raw")
LABELED_DIR = Path("dataset/labeled")
CSV_FILE = Path("dataset/metadata/labels.csv")

CLASSES = [
    "light_pawn", "light_knight", "light_bishop",
    "light_rook", "light_queen", "light_king",
    "dark_pawn", "dark_knight", "dark_bishop",
    "dark_rook", "dark_queen", "dark_king",
    "empty"
]


def main():
    if not CSV_FILE.exists():
        print("ERRO: labels.csv não encontrado.")
        return

    with open(CSV_FILE, newline="", encoding="utf-8") as file:
        labels = list(csv.DictReader(file))

    squares = [item["square"] for item in labels]
    counts = Counter(item["class"] for item in labels)

    print("\n=== CHESS AGENT: DATASET AUDIT ===\n")

    print("Total de registros:", len(labels))
    print("Casas únicas:", len(set(squares)))
    print("Imagens brutas:", len(list(RAW_DIR.glob("*.png"))))

    print("\n=== DISTRIBUIÇÃO DAS CLASSES ===")

    for class_name in CLASSES:
        count = counts[class_name]
        print(f"{class_name:15} : {count:2}")

    print("\n=== VERIFICAÇÃO DE INTEGRIDADE ===")

    errors = []

    if len(squares) != len(set(squares)):
        errors.append("Existem casas duplicadas no CSV.")

    if len(labels) != 64:
        errors.append("O dataset não possui exatamente 64 registros.")

    if len(set(squares)) != 64:
        errors.append("O dataset não possui 64 casas únicas.")

    for item in labels:
        square = item["square"]
        class_name = item["class"]
        filename = item["filename"]

        if class_name not in CLASSES:
            errors.append(f"Classe inválida: {class_name}")

        if not (RAW_DIR / f"{square}.png").exists():
            errors.append(f"Imagem bruta ausente: {square}")

        if not (LABELED_DIR / class_name / filename).exists():
            errors.append(f"Imagem classificada ausente: {filename}")

    for class_name in CLASSES:
        if counts[class_name] == 0:
            print(f"AVISO: classe sem exemplos: {class_name}")

    if errors:
        print("\nPROBLEMAS ENCONTRADOS:")
        for error in errors:
            print("-", error)
    else:
        print("\nIntegridade estrutural: OK")

    print("\nAuditoria concluída.")


if __name__ == "__main__":
    main()
