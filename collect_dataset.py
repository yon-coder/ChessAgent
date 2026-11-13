
import time
import cv2
import keyboard

from pathlib import Path
from vision import capture_board, split_squares

OUTPUT_DIR = Path("dataset/extra_raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

existing = list(OUTPUT_DIR.glob("p*_*.png"))
position_id = len(existing) // 64 + 1

print("=== CHESS AGENT: DATASET COLLECTOR ===")
print("F8 = Capturar posição")
print("ESC = Encerrar coleta")
print("\nDeixe o Duolingo em primeiro plano.")

try:
    while True:
        if keyboard.is_pressed("esc"):
            break

        if keyboard.is_pressed("f8"):
            time.sleep(0.3)

            board_image = capture_board()
            squares = split_squares(board_image)

            for square_name, image in squares.items():
                filename = f"p{position_id:03d}_{square_name}.png"
                cv2.imwrite(
                    str(OUTPUT_DIR / filename),
                    image
                )

            print(f"Posição {position_id:03d}: 64 imagens salvas.")
            position_id += 1

            time.sleep(0.7)

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

print("\nColeta encerrada.")
