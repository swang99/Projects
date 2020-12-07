# Stephen Wang
# Edited: 12/5/20, Original: 5/23/18
# Final project - Dots and boxes

import pygame
from math import floor, ceil
from edges import Boxes, Dots, Text

def buildBoard(): # building board matrix
    board = []
    for i in range(DIM):
        board.append([])
        for j in range(DIM):
            board[i].append([0,0,0,0,0])
    return board

def drawEdges(): 
    left_edges = Boxes(XSLOT, YSLOT, screen, board)
    upper_edges = Boxes(XSLOT, YSLOT, screen, board)
    lower_edges = Boxes(XSLOT, YSLOT + CELL_SIZE + LINE_THICKNESS, screen, board)
    right_edges = Boxes(XSLOT+ CELL_SIZE + LINE_THICKNESS, YSLOT, screen, board)
    squares = Boxes(XSLOT, YSLOT, screen, board)
    dots = Dots(XSLOT, YSLOT, screen, board)

    squares.draw(4, DIM, CELL_SIZE, LINE_THICKNESS)
    left_edges.draw(0, DIM, CELL_SIZE, LINE_THICKNESS)
    upper_edges.draw(1, DIM, CELL_SIZE, LINE_THICKNESS)
    lower_edges.draw(2, DIM, CELL_SIZE, LINE_THICKNESS)
    right_edges.draw(3, DIM, CELL_SIZE, LINE_THICKNESS)
    dots.draw(DIM, CELL_SIZE, LINE_THICKNESS)

def UpdateEdges(a, b, num, player): 
    if player == 1 and board[a][b][num] == 0:
        board[a][b][num] = 1
    elif player == 2 and board[a][b][num] == 0:
        board[a][b][num] = 2

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
            return "Player 1 Wins!"
        elif p2 > p1:
            return "Player 2 Wins!"
        else:
            return "Tie Game!"
    else:
        return False

def selectEdge(mouse_x, mouse_y, p1, p2, player, squareTurned):
    exact_x = (mouse_x - XSLOT) / (CELL_SIZE + LINE_THICKNESS) 
    exact_y = (mouse_y - YSLOT) / (CELL_SIZE + LINE_THICKNESS)
    floor_x = floor(exact_x)
    floor_y = floor(exact_y)
    round_x = round(exact_x)
    round_y = round(exact_y)

    if mouse_x < XSLOT - LINE_THICKNESS or mouse_x > XSLOT + DIM * (CELL_SIZE + LINE_THICKNESS) \
    or mouse_y < YSLOT - LINE_THICKNESS or mouse_y > YSLOT + DIM * (CELL_SIZE + LINE_THICKNESS) \
    or screen.get_at(pygame.mouse.get_pos()) == (83, 83, 83) \
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
    text = {"p1": Text(screen), "p2": Text(screen), "win": Text(screen), "turn": Text(screen)}

    text["p1"].display(pygame.font.SysFont("freesansbold.ttf", 70), str(p1), (255, 118, 117), (30, 20))
    text["p2"].display(pygame.font.SysFont("freesansbold.ttf", 70), str(p2), (116, 185, 255), (WINDOW_X - 60, 20))
    
    if player == 1:
        text["turn"].display(pygame.font.SysFont("freesansbold.ttf", 50), "Turn ■", (255, 118, 117), (WINDOW_X/2.25, 30))
    else:
        text["turn"].display(pygame.font.SysFont("freesansbold.ttf", 50), "Turn ■", (116, 185, 255), (WINDOW_X/2.25, 30))
    
    if GameStatus(p1, p2) != False:
        text["win"].display(pygame.font.SysFont("freesansbold.ttf", 50), GameStatus(p1, p2), (0, 184, 148), (WINDOW_X/2.25, 30))
    
def checkTurn(player):
    return 2 if player == 1 else 1

if __name__ == '__main__': 
    DIM = 5 # dimension
    CELL_SIZE = 85
    LINE_THICKNESS = 6
    TOLERANCE = 0.1 # how off click can be
    WINDOW_X = 700
    WINDOW_Y = 700
    XSLOT = (WINDOW_X / 2) - (DIM / 2) * CELL_SIZE # x-origin 
    YSLOT = (WINDOW_Y / 2) - (DIM / 2) * CELL_SIZE # y-origin

    # game mechanics
    board = buildBoard()
    player = 1
    p1_score, p2_score = 0, 0
    squareTurned = 0

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                p1_score, p2_score, player = selectEdge(mouse_x, mouse_y, p1_score, p2_score, player, squareTurned)
            elif event.type == pygame.QUIT:
                finished = True
        
        screen.fill((255, 255, 255))
        drawEdges()
        drawScore(p1_score, p2_score, player, screen)
        pygame.display.update()
