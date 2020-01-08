import numpy as np
import pygame as py
import sys


def createBoard():
    return np.zeros((6,8))


def dropPiece(board, row, col, piece):
    board[row][col] = piece

def valid_loc(board, col):

    return col >= 0 and col <= 6 and board[0][col] == 0 

def get_next_row(board, col):
    for r in range(1,7):
        if board[6-r][col] == 0:
            return 6-r


def seq_check(the_seq, col, piece):
    count = 1
    curr_col = col + 1
    while count < 4 and curr_col < the_seq.size:
        if the_seq[curr_col] == piece:
            count += 1
            curr_col += 1
        else:
            break
    curr_col = col - 1
    while count < 4 and curr_col >= 0:
        if the_seq[curr_col] == piece:
            count += 1
            curr_col -= 1
        else:
            break

    if count >= 4:
        return True

def winning_move(board, piece, row, col):
    
    #check col
    the_col = board[:,col]

    if seq_check(the_col, row, piece):
        return True

    #check row
    the_row = board[row,:]

    if seq_check(the_row, col, piece):
        return True

    #leading diag
    count = 1
    offset = col - row
    if offset < 4 and offset > -3:
        lead_diag = np.diagonal(board, offset)
        if offset > 0 and seq_check(lead_diag, row, piece):
            return True
        elif offset < 0 and seq_check(lead_diag, col, piece):
            return True

    #other diag
    board = np.flip(board, 1)
    col = 6-col
    count = 1
    offset = col - row
    if offset < 4 and offset > -3:
        lead_diag = np.diagonal(board, offset)
        if offset > 0 and seq_check(lead_diag, row, piece):
            return True
        elif offset < 0 and seq_check(lead_diag, col, piece):
            return True

    return False

def draw_baord(screen, board):

    for c in range(7):
        for r in range(1,7):

            py.draw.rect(screen, (0,0,255), (c*100, r*100, 100, 100))
            if board[r-1,c] == 0:
                co = (0,0,0)
            elif board[r-1,c] == 1:
                co = (255,0,0)
            else:
                co = (255,255,0)
            py.draw.circle(screen, co, (c*100+50, r*100+50), 45) 

    py.display.update()



board = createBoard()
gameO = False
turn = 0

py.init()
screen = py.display.set_mode((700, 700))
myfont = py.font.SysFont("monospace", 75)
draw_baord(screen, board)

while not gameO:

    for event in py.event.get():
        if event.type == py.QUIT:
            gameO = True
            sys.exit

        if event.type == py.MOUSEMOTION:
            py.draw.rect(screen, (0,0,0), (0,0,700,100))
            posx = event.pos[0]
            if turn == 0:
                co = (255,0,0)
            else:
                co = (255,255,0)

            py.draw.circle(screen, co, (posx, 50), 45)

            py.display.update()
        if event.type == py.MOUSEBUTTONDOWN:
            py.draw.rect(screen, (0,0,0), (0,0,700,100))
            posx = event.pos[0]
            if turn == 1:
                co = (255,0,0)
            else:
                co = (255,255,0)

            py.draw.circle(screen, co, (posx, 50), 45)

            py.display.update()
            col = event.pos[0]//100

            if valid_loc(board, col):
                row = get_next_row(board, col)
                dropPiece(board, row, col, turn + 1)
            else:
                continue

            draw_baord(screen, board)

            if winning_move(board, turn+1, row, col):
                py.draw.rect(screen, (0,0,0), (0,0,700,100))
                label = myfont.render("Player {} won".format(turn+1), 1, (255, 255, 255))
                screen.blit(label, (80, 10))
                gameO = True

            draw_baord(screen, board)
            turn = (turn + 1) % 2

            if gameO:
                py.time.wait(1000)




