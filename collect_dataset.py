
import time
import re
import cv2
import keyboard

from pathlib import Path
from vision import capture_board, split_squares, calibrate_board

OUTPUT_DIR = Path("dataset/extra_raw")
CONFIG_FILE = Path("board_config.json")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def next_position_id():
    ids = []

    for file in OUTPUT_DIR.glob("p*_*.png"):
        match = re.match(r"p(\d+)_", file.name)
        if match:
            ids.append(int(match.group(1)))

    return max(ids, default=0) + 1


position_id = next_position_id()


def calibrate():
    print("\nIniciando calibração...")
    calibrate_board()
    print("Calibração concluída!\n")


print("=== CHESS AGENT: DATASET COLLECTOR ===")
print("F8 = Capturar posição")
print("F9 = Recalibrar tabuleiro")
print("ESC = Encerrar coleta")

if not CONFIG_FILE.exists():
    print("\nNenhuma calibração encontrada.")
    calibrate()
else:
    print("\nConfiguração existente encontrada.")
    print("Se o tabuleiro estiver fora da região, pressione F9.")

print("\nDeixe o Duolingo em primeiro plano.")
print("Coletor iniciado!\n")

try:
    while True:

        if keyboard.is_pressed("esc"):
            break

        elif keyboard.is_pressed("f9"):
            time.sleep(0.3)
            calibrate()
            time.sleep(0.5)

        elif keyboard.is_pressed("f8"):
            time.sleep(0.3)

            board_image = capture_board()
            squares = split_squares(board_image)

            if len(squares) != 64:
                print("Erro: não foram identificadas 64 casas.")
                continue

            for square_name, image in squares.items():
                filename = f"p{position_id:03d}_{square_name}.png"

                cv2.imwrite(
                    str(OUTPUT_DIR / filename),
                    image
                )

            print(
                f"Posição {position_id:03d}: "
                f"{len(squares)} imagens salvas."
            )

            position_id += 1
            time.sleep(0.7)

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

print("\nColeta encerrada.")
print(f"Próximo ID disponível: {position_id:03d}")
