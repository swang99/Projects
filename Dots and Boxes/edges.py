import pygame

class Boxes:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board

    def draw(self, x, y, num, dim, size, thickness):
        new_y = y
        for i in range(dim):
            for j in range(dim):
                # update color
                if num != 4:
                    if self.board[i][j][num] == 0:
                        color = (178, 190, 195)
                    elif self.board[i][j][num] == 1:
                        color = (214, 48, 49)
                    elif self.board[i][j][num] == 2:
                        color = (9, 132, 227)
                else:
                    if self.board[i][j][4] == 0:
                        color = (255, 255, 255)
                    elif self.board[i][j][4] == 1:
                        color = (255, 118, 117)
                    elif self.board[i][j][4] == 2:
                        color = (116, 185, 255)

                # draw edges/squares
                if num == 0 or num == 3:
                    pygame.draw.line(self.screen, color, (x, new_y), (x, new_y + size + thickness), thickness)
                elif num == 1 or num == 2:
                    pygame.draw.line(self.screen, color, (x, new_y), (x + size + thickness, new_y), thickness)
                else:
                    pygame.draw.rect(self.screen, color, (x + (thickness/2), new_y + (thickness/2), size + 1, size + 1))
                new_y += size + thickness
            x += size + thickness
            new_y = y

    def dots(self, x, y, dim, size, thickness):
        RADIUS = 8
        new_y = y

        # draw the dots
        for i in range(dim + 1):
            for j in range(dim + 1):
                pygame.draw.circle(self.screen, (83, 83, 83), (x, new_y), RADIUS)
                new_y += size + thickness
            x += size + thickness
            new_y = y

    def display_txt(self, font, text, color, pos):
        # simplified method to blit pygame text
        t = font.render(text, True, color)
        self.screen.blit(t, pos)