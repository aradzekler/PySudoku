import pygame


class GuiSquare:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

        def draw(self, win):
            fnt = pygame.font.SysFont("comicsans", 40)

            gap = self.width / 9
            x = self.col * gap
            y = self.row * gap

            if self.temp != 0 and self.value == 0:
                text = fnt.render(str(self.temp), 1, (128, 128, 128))
                win.blit(text, (x + 5, y + 5))
            elif not (self.value == 0):
                text = fnt.render(str(self.value), 1, (0, 0, 0))
                win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

            if self.selected:
                pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)
