import pygame
import time
import sudoku_gui
import static_helpers

pygame.font.init()


class SudokuGrid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        # gui_square is a
        self.gui_squares = [[sudoku_gui.GuiSquare(self.board[i][j], i, j, width, height) for j in range(cols)] for i in
                            range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None
        self.win = win


    # updating the current state of the model.
    def update_model(self):
        self.model = [[self.gui_squares[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # function to place a value in certain square.
    def place(self, val):
        row, col = self.selected
        if self.gui_squares[row][col].value == 0:
            self.gui_squares[row][col].set_val(val)
            self.update_model()

            if static_helpers.valid(self.model, val, (row, col)) and self.solve():  # if the board is valid, solve
                return True
            else:
                self.gui_squares[row][col].set_val(0)
                self.gui_squares[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.gui_squares[row][col].set_temp(val)

    # actually drawing the board using pygame drawline method.
    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.gui_squares[i][j].draw(self.win)

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.gui_squares[i][j].selected = False

        self.gui_squares[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.gui_squares[row][col].value == 0:
            self.gui_squares[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.gui_squares[i][j].value == 0:
                    return False
        return True

    def solve(self):
        find = static_helpers.find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if static_helpers.valid(self.model, i, (row, col)):
                self.model[row][col] = i

                if self.solve():
                    return True

                self.model[row][col] = 0

        return False

    def solve_gui(self):
        self.update_model()
        find = static_helpers.find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if static_helpers.valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.gui_squares[row][col].set_val(i)
                self.gui_squares[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.gui_squares[row][col].set_val(0)
                self.update_model()
                self.gui_squares[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False
