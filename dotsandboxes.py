# Stephen Wang
# Edited: 12/5/20, Original: 5/23/18
# Final project - Dots and boxes

import pygame
from math import floor, ceil
from edges import Boxes, Dots

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

    # vertical edges
    if abs(exact_x - round_x) < TOLERANCE: 
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
    
    else: # if click outside board
        return p1, p2, player

    player = checkTurn(player) # if no square turned, flip turn
    if squareTurned != 0: # if at least one square turned, flip turn again
        player = checkTurn(player)
    
    return p1, p2, player
    
def drawScore(p1, p2): 
    font = pygame.font.SysFont("Cambria", 25)
    p1_text = font.render("Player 1: " + str(p1), False, (255, 118, 117))
    p2_text = font.render("Player 2: " + str(p2), False, (116, 185, 255))
    screen.blit(p1_text, (20, 20))
    screen.blit(p2_text, (20, 55))
    if GameStatus(p1, p2) != False:
        win_text = font.render(GameStatus(p1, p2), False, (0, 184, 148))
        screen.blit(win_text, (20, 90))
    
def checkTurn(player):
    return 2 if player == 1 else 1

if __name__ == '__main__': 
    DIM = 3 # dimension
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
                drawScore(p1_score, p2_score)
            elif event.type == pygame.QUIT:
                finished = True
        
        screen.fill((255, 255, 255))
        drawEdges()
        drawScore(p1_score, p2_score)
        pygame.display.update()
