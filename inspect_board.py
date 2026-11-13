
import cv2
import os

from vision import split_squares

def main():

    print("Carregando imagem calibrada...")

    # Utiliza a imagem salva anteriormente
    image = cv2.imread("screenshots/board.png")

    if image is None:
        raise FileNotFoundError(
            "screenshots/board.png não encontrado!"
        )

    squares = split_squares(image)

    os.makedirs("dataset/raw", exist_ok=True)

    tile_size = 100
    rows = []

    for row in range(8):

        tiles = []

        for col in range(8):

            square_name = f"{'abcdefgh'[col]}{8-row}"
            square = squares[square_name]

            filename = f"{square_name}.png"

            cv2.imwrite(
                f"dataset/raw/{filename}",
                square
            )

            resized = cv2.resize(
                square,
                (tile_size, tile_size)
            )

            cv2.putText(
                resized,
                square_name,
                (5, 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                1
            )

            tiles.append(resized)

        rows.append(cv2.hconcat(tiles))

    sheet = cv2.vconcat(rows)

    cv2.imwrite(
        "screenshots/squares_grid.png",
        sheet
    )

    print("64 casas extraídas!")
    print("Resultado: screenshots/squares_grid.png")


if __name__ == "__main__":
    main()
