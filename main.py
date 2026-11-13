
from vision import (
    capture_screen,
    select_board,
    split_squares
)

def main():

    print("=== CHESS AGENT ===")

    image, monitor = capture_screen()

    board = select_board(image, monitor)

    squares = split_squares(board)

    print("\nSistema de visão inicializado.")
    print("Casas detectadas:", len(squares))

    for square in ["a8", "e4", "d1", "h1"]:
        print(square, squares[square].shape)


if __name__ == "__main__":
    main()
