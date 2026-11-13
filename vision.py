
import cv2
import mss
import numpy as np
import json
import os
import time
os.makedirs("screenshots", exist_ok=True)


def capture_screen():

    print("\nPreparando captura...")

    for i in range(5, 0, -1):
        print(f"Capturando em {i} segundos...")
        time.sleep(1)

    with mss.mss() as sct:

        monitor = sct.monitors[1]

        screenshot = np.array(
            sct.grab(monitor)
        )

        image = cv2.cvtColor(
            screenshot,
            cv2.COLOR_BGRA2BGR
        )

        return image, monitor



def select_board(image, monitor):
    """Permite selecionar manualmente o tabuleiro."""

    print("Selecione a área do tabuleiro.")
    print("Pressione ENTER ou SPACE para confirmar.")

    x, y, w, h = cv2.selectROI(
        "Chess Agent - Board Selection",
        image,
        showCrosshair=True,
        fromCenter=False
    )

    cv2.destroyAllWindows()

    if w == 0 or h == 0:
        raise ValueError("Nenhum tabuleiro selecionado.")

    # Coordenadas absolutas da tela
    config = {
        "left": int(monitor["left"] + x),
        "top": int(monitor["top"] + y),
        "width": int(w),
        "height": int(h)
    }

    board_image = image[y:y+h, x:x+w]

    cv2.imwrite(
        "screenshots/board.png",
        board_image
    )

    with open("board_config.json", "w") as file:
        json.dump(config, file, indent=4)

    print("Tabuleiro calibrado!")
    print(config)

    return board_image


def split_squares(board_image):

    height, width = board_image.shape[:2]

    squares = {}

    for row in range(8):
        for col in range(8):

            x1 = round(col * width / 8)
            x2 = round((col + 1) * width / 8)

            y1 = round(row * height / 8)
            y2 = round((row + 1) * height / 8)

            name = f"{'abcdefgh'[col]}{8-row}"

            squares[name] = board_image[y1:y2, x1:x2]

    return squares

def capture_board():

    with open("board_config.json", "r") as file:
        config = json.load(file)

    with mss.mss() as sct:
        screenshot = np.array(sct.grab(config))

    image = cv2.cvtColor(
        screenshot,
        cv2.COLOR_BGRA2BGR
    )

    return image


if __name__ == "__main__":

    image, monitor = capture_screen()

    board = select_board(image, monitor)

    squares = split_squares(board)

    print(f"Casas identificadas: {len(squares)}")
    print("Exemplo:", squares["e4"].shape)
