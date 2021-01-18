# Stephen Wang
# Revised: 12/5/20
# Dots and Boxes; 2 Player

import pygame
from math import floor, ceil
from edges import Boxes

def buildBoard(): # building board matrix | k = square | j = a row of squares | i = all rows
    return [[[0 for k in range(5)] for j in range(DIM)] for i in range(DIM)]

def drawEdges(): # draw edges, squares, and dots
    edges = {}

    for key in ["left_edges", "upper_edges", "lower_edges", "right_edges", "squares", "dots"]:
        edges[key] = Boxes(screen, board)

    edges["squares"].draw(XSLOT, YSLOT, 4, DIM, CELL_SIZE, LINE_THICKNESS)
    edges["left_edges"].draw(XSLOT, YSLOT, 0, DIM, CELL_SIZE, LINE_THICKNESS)
    edges["upper_edges"].draw(XSLOT, YSLOT, 1, DIM, CELL_SIZE, LINE_THICKNESS)
    edges["lower_edges"].draw(XSLOT, YSLOT + CELL_SIZE + LINE_THICKNESS, 2, DIM, CELL_SIZE, LINE_THICKNESS)
    edges["right_edges"].draw(XSLOT + CELL_SIZE + LINE_THICKNESS, YSLOT, 3, DIM, CELL_SIZE, LINE_THICKNESS)
    edges["dots"].dots(XSLOT, YSLOT, DIM, CELL_SIZE, LINE_THICKNESS)

def UpdateEdges(a, b, num, player): 
    if board[a][b][num] == 0:
        board[a][b][num] = player

def UpdateSq(a, b, p1, p2, player, squareTurned):
    # are all edges clicked?
    for i in range(4):
        if board[a][b][i] == 0:
            return p1, p2, player, squareTurned

    # if so, change square
    if player == 1 and board[a][b][4] == 0:
        board[a][b][4] = 1
        p1 += 1
    elif player == 2 and board[a][b][4] == 0:
        board[a][b][4] = 2
        p2 += 1
    squareTurned += 1

    return p1, p2, player, squareTurned
        
def GameStatus(p1, p2): # Is the game over?
    if p1 + p2 == (DIM ** 2):
        if p1 > p2:
            return "P1 (Red) Wins!"
        elif p2 > p1:
            return "P2 (Blue) Wins!"
        else:
            return "Tie Game!"
    else:
        return False

def selectEdge(mouse_x, mouse_y, p1, p2, player, squareTurned):
    exact_x, exact_y = (mouse_x - XSLOT) / (CELL_SIZE + LINE_THICKNESS), (mouse_y - YSLOT) / (CELL_SIZE + LINE_THICKNESS)
    floor_x, floor_y = floor(exact_x), floor(exact_y)
    round_x, round_y = round(exact_x), round(exact_y)

    if mouse_x < XSLOT - LINE_THICKNESS or mouse_x > XSLOT + LINE_THICKNESS + DIM * (CELL_SIZE + LINE_THICKNESS) \
    or mouse_y < YSLOT - LINE_THICKNESS or mouse_y > YSLOT + LINE_THICKNESS + DIM * (CELL_SIZE + LINE_THICKNESS) \
    or screen.get_at(pygame.mouse.get_pos()) == (83, 83, 83) \
    or screen.get_at(pygame.mouse.get_pos()) == (214, 48, 49) \
    or screen.get_at(pygame.mouse.get_pos()) == (9, 132, 227) \
    or abs(exact_x - round_x) > TOLERANCE and abs(exact_y - round_y) > TOLERANCE: # if click outside of edges
        return p1, p2, player

    # vertical edges
    elif abs(exact_x - round_x) < TOLERANCE: 
        if 0 < round_x < DIM: # overlapping left/right edges
            UpdateEdges(round_x, floor_y, 0, player)
            p1, p2, player, squareTurned = UpdateSq(round_x, floor_y, p1, p2, player, squareTurned)
            UpdateEdges(round_x - 1, floor_y, 3, player)
            p1, p2, player, squareTurned = UpdateSq(round_x - 1, floor_y, p1, p2, player, squareTurned)
        elif round_x == 0: # leftmost edge
            UpdateEdges(round_x, floor_y, 0, player) 
            p1, p2, player, squareTurned = UpdateSq(round_x, floor_y, p1, p2, player, squareTurned)
        else: # rightmost edge - only working when cursor is on left side
            UpdateEdges(round_x - 1, floor_y, 3, player) 
            p1, p2, player, squareTurned = UpdateSq(round_x - 1, floor_y, p1, p2, player, squareTurned)
    
    # horizontal edges
    elif abs(exact_y - round_y) < TOLERANCE: 
        if 0 < round_y < DIM: # overlapping upper/lower edges
            UpdateEdges(floor_x, round_y, 1, player)
            p1, p2, player, squareTurned = UpdateSq(floor_x, round_y, p1, p2, player, squareTurned)
            UpdateEdges(floor_x, round_y - 1, 2, player)
            p1, p2, player, squareTurned = UpdateSq(floor_x, round_y - 1, p1, p2, player, squareTurned)
        elif round_y == 0: # uppermost edge - NOT WORKING
            UpdateEdges(floor_x, round_y, 1, player) 
            p1, p2, player, squareTurned = UpdateSq(floor_x, round_y, p1, p2, player, squareTurned) 
        else: # lowermost edge
            UpdateEdges(floor_x, round_y - 1, 2, player)
            p1, p2, player, squareTurned = UpdateSq(floor_x, round_y - 1, p1, p2, player, squareTurned) 

    player = checkTurn(player) # if no square turned, flip turn
    if squareTurned != 0: # if at least one square turned, flip turn again
        player = checkTurn(player)
    
    return p1, p2, player
    
def drawScore(p1, p2, player, screen): 
    # storing all text objects
    text = {"p1": Boxes(screen, board), "p2": Boxes(screen, board), "win": Boxes(screen, board), \
            "turn": Boxes(screen, board), "restart": Boxes(screen, board)}

    # draw current score
    text["p1"].display_txt(pygame.font.SysFont("freesansbold.ttf", 70), str(p1), (255, 118, 117), (30, 20))
    text["p2"].display_txt(pygame.font.SysFont("freesansbold.ttf", 70), str(p2), (116, 185, 255), (WINDOW_X - 60, 20))
    
    # if game is not over, display whose turn it is
    if player == 1:
        text["turn"].display_txt(pygame.font.SysFont("freesansbold.ttf", 50), "P1 Turn", (255, 118, 117), (WINDOW_X/2.25, 30))
    elif player == 2:
        text["turn"].display_txt(pygame.font.SysFont("freesansbold.ttf", 50), "P2 Turn", (116, 185, 255), (WINDOW_X/2.25, 30))
   
    # otherwise, display winner and restart message
    if GameStatus(p1, p2) != False:
        text["turn"].display_txt(pygame.font.SysFont("freesansbold.ttf", 0), "P2 Turn", (116, 185, 255), (WINDOW_X/2.25, 30))
        screen.fill((255, 255, 255), (WINDOW_X/2.25, 30, 150, 40))
        text["win"].display_txt(pygame.font.SysFont("freesansbold.ttf", 50), GameStatus(p1, p2), (0, 184, 148), (WINDOW_X/3, 30))
        text["restart"].display_txt(pygame.font.SysFont("freesansbold.ttf", 25), "Press R to restart", (0, 184, 148), (WINDOW_X/3, 70))
    
def checkTurn(player):
    return 2 if player == 1 else 1

if __name__ == '__main__': 
    DIM = 3 # dimension
    CELL_SIZE = 85
    LINE_THICKNESS = 6
    TOLERANCE = 0.1 # how off click can be
    WINDOW_X, WINDOW_Y = 700, 700 # window size
    XSLOT = (WINDOW_X / 2) - (DIM / 2) * CELL_SIZE # x-origin 
    YSLOT = (WINDOW_Y / 2) - (DIM / 2) * CELL_SIZE # y-origin

    # game mechanics
    board = buildBoard()
    player = 1
    p1_score, p2_score = 0, 0
    squareTurned = 0 # has a square been made?

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
                p1_score, p2_score, player = selectEdge(mouse_x, mouse_y, p1_score, p2_score, player, squareTurned)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and GameStatus(p1_score, p2_score) != False: # restart
                board = buildBoard()
                player = 1
                p1_score, p2_score = 0, 0
                squareTurned = 0
            elif event.type == pygame.QUIT: # quit
                finished = True

        screen.fill((255, 255, 255))
        drawEdges()
        drawScore(p1_score, p2_score, player, screen)
        pygame.display.update()