# Stephen Wang
# Revised: 12/5/20
# Dots and Boxes; 2 Player

import pygame
from math import floor, ceil
from edges import Boxes

def build_board(): # building board matrix | k = square | j = a row of squares | i = all rows
    return [[[0 for k in range(5)] for j in range(DIM)] for i in range(DIM)]

def draw_edges(): # draw edges, squares, and dots
    edges = {}
    for key in ["left_edges", "upper_edges", "lower_edges", "right_edges", "squares", "dots"]:
        edges[key] = Boxes(screen, board)

    edges["squares"].draw(XSLOT, YSLOT, 4, DIM, CELL, LINE)
    edges["left_edges"].draw(XSLOT, YSLOT, 0, DIM, CELL, LINE)
    edges["upper_edges"].draw(XSLOT, YSLOT, 1, DIM, CELL, LINE)
    edges["lower_edges"].draw(XSLOT, YSLOT + CELL + LINE, 2, DIM, CELL, LINE)
    edges["right_edges"].draw(XSLOT + CELL + LINE, YSLOT, 3, DIM, CELL, LINE)
    edges["dots"].dots(XSLOT, YSLOT, DIM, CELL, LINE)

def update_board(a, b, num, player, p1, p2, sq_t): 
    # -- update edge -- #
    if board[a][b][num] == 0:
        board[a][b][num] = player

    # -- update square -- #
    # are all edges clicked?
    for i in range(4):
        if board[a][b][i] == 0:
            return p1, p2, player, sq_t

    # if so, change square and score
    if player == 1 and board[a][b][4] == 0:
        board[a][b][4] = 1
        p1 += 1
    elif player == 2 and board[a][b][4] == 0:
        board[a][b][4] = 2
        p2 += 1
    sq_t += 1

    return p1, p2, player, sq_t

def game_status(p1, p2): # Is the game over?
    if p1 + p2 >= (DIM ** 2):
        if p1 > p2:
            return "P1 (Red) Wins!"
        if p2 > p1:
            return "P2 (Blue) Wins!"
        return "Tie Game!"
    return False

def select_edge(mouse_x, mouse_y, p1, p2, player, sq_t):
    exact_x, exact_y = (mouse_x - XSLOT) / (CELL + LINE), (mouse_y - YSLOT) / (CELL + LINE)
    floor_x, floor_y = floor(exact_x), floor(exact_y)
    round_x, round_y = round(exact_x), round(exact_y)

    # if Case 1, 2, or 3 -> do not select an edge
    # Case 1: Click outside of board
    if (mouse_x < XSLOT - LINE) or (mouse_x > XSLOT + LINE + DIM * (CELL + LINE)) \
    or (mouse_y < YSLOT - LINE) or (mouse_y > YSLOT + LINE + DIM * (CELL + LINE)):
        return p1, p2, player

    # Case 2: Click inside board
    if (abs(exact_x - round_x) > TOLERANCE and abs(exact_y - round_y) > TOLERANCE):
        return p1, p2, player

    # Case 3: Click on a dot or on an edge already taken
    if (screen.get_at(pygame.mouse.get_pos()) == (83, 83, 83)) \
    or (screen.get_at(pygame.mouse.get_pos()) == (214, 48, 49)) \
    or (screen.get_at(pygame.mouse.get_pos()) == (9, 132, 227)): 
        return p1, p2, player

    # vertical edges
    elif abs(exact_x - round_x) < TOLERANCE: 
        if 0 < round_x < DIM: # overlapping left/right edges
            p1, p2, player, sq_t = update_board(round_x, floor_y, 0, player, p1, p2, sq_t)
            p1, p2, player, sq_t = update_board(round_x - 1, floor_y, 3, player, p1, p2, sq_t)
        elif round_x == 0: # leftmost edge
            p1, p2, player, sq_t = update_board(round_x, floor_y, 0, player, p1, p2, sq_t)
        else: # rightmost edge
            p1, p2, player, sq_t = update_board(round_x - 1, floor_y, 3, player, p1, p2, sq_t)

    # horizontal edges
    elif abs(exact_y - round_y) < TOLERANCE: 
        if 0 < round_y < DIM: # overlapping upper/lower edges
            p1, p2, player, sq_t = update_board(floor_x, round_y, 1, player, p1, p2, sq_t)
            p1, p2, player, sq_t = update_board(floor_x, round_y - 1, 2, player, p1, p2, sq_t)
        elif round_y == 0: # uppermost edge
            p1, p2, player, sq_t = update_board(floor_x, round_y, 1, player, p1, p2, sq_t)
        else: # lowermost edge
            p1, p2, player, sq_t = update_board(floor_x, round_y - 1, 2, player, p1, p2, sq_t)

    player = check_turn(player) # if no square turned, flip turn
    if sq_t != 0: # if at least one square turned, flip turn again
        player = check_turn(player)

    return p1, p2, player

def draw_score(p1, p2, player, screen):
    # storing text objects
    text = {}
    for key in ["p1", "p2", "win", "turn", "restart"]:
        text[key] = Boxes(screen, board)

    # storing font styles
    font = {}
    for key in ["70", "50", "25", "0"]:
        font[key] = pygame.font.SysFont("freesansbold.ttf", int(key))

    # draw current score
    text["p1"].display_txt(font["70"], str(p1), (255, 118, 117), (30, 20))
    text["p2"].display_txt(font["70"], str(p2), (116, 185, 255), (WINDOW_X - 60, 20))

    # if game is not over, display whose turn it is
    if player == 1:
        text["turn"].display_txt(font["50"], "P1 Turn", (255, 118, 117), (WINDOW_X/2.25, 30))
    elif player == 2:
        text["turn"].display_txt(font["50"], "P2 Turn", (116, 185, 255), (WINDOW_X/2.25, 30))

    # otherwise, display winner and restart message
    if game_status(p1, p2) != False:
        text["turn"].display_txt(font["0"], "P2 Turn", (116, 185, 255), (WINDOW_X/2.25, 30))
        screen.fill((255, 255, 255), (WINDOW_X/2.25, 30, 150, 40))
        text["win"].display_txt(font["50"], game_status(p1, p2), (0, 184, 148), (WINDOW_X/3, 30))
        text["restart"].display_txt(font["25"], "Press R to restart", (0, 184, 148), (WINDOW_X/3, 70))

def check_turn(player):
    return 2 if player == 1 else 1

if __name__ == '__main__': 
    DIM = 3 # dimension
    CELL = 85
    LINE = 6
    TOLERANCE = 0.1 # how off click can be
    WINDOW_X, WINDOW_Y = 700, 700 # window size
    XSLOT = (WINDOW_X / 2) - (DIM / 2) * CELL # x-origin
    YSLOT = (WINDOW_Y / 2) - (DIM / 2) * CELL # y-origin

    # game mechanics
    board = build_board()
    player = 1
    p1_score, p2_score = 0, 0
    sq_t = 0 # has a square been made?

    # set up window
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_X, WINDOW_Y))
    pygame.display.set_caption("Dots and Boxes")
    icon = pygame.image.load("square.png")
    pygame.display.set_icon(icon)

    # game loop
    finished = False
    while finished != True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN: # mouse click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                p1_score, p2_score, player = select_edge(mouse_x, mouse_y, p1_score, p2_score, player, sq_t)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_status(p1_score, p2_score) != False: # restart
                board = build_board()
                player = 1
                p1_score, p2_score = 0, 0
                sq_t = 0
            elif event.type == pygame.QUIT: # quit
                finished = True

        screen.fill((255, 255, 255))
        draw_edges()
        draw_score(p1_score, p2_score, player, screen)
        pygame.display.update()
