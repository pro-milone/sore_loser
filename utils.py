from typing import Dict, Tuple

class Board:
    def __init__(self, board_string: str):
        self.board_string = board_string.lower()
        self.mapping = self.create_grid()

    def create_grid(self) -> Dict[Tuple[int, int], str]:
        """Maps board_string to a square grid (row, col)."""
        n = int(len(self.board_string) ** 0.5)
        grid = {}
        for idx, letter in enumerate(self.board_string):
            i = idx // n
            j = idx % n
            grid[(i, j)] = letter
        return grid
