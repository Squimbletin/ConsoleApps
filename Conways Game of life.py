import random
import time
import os

GREEN = '\033[32m' # ascii for Dark Green colour
RESET = '\033[90m' # ascii for Gray / Dead Colour


def generate_board(rows, cols, alive_prob): #initialize board of defined size 
    board = [] 
    for _ in range(rows):
        row = []
        for _ in range(cols):
            cell = 'O' if random.random() < alive_prob else 'X'
            row.append(cell)
        board.append(row)
    return board

def printBoard(board): # print board with colours for alive cells
    for row in board:
        line = ''
        for cell in row:
            if cell == 'O':
                line += GREEN + 'O' + RESET + ' '
            else:
                line += cell + ' '
        print(line)


def count_neighbors(board, row, col): # counts the amount of alive cells surrounding a cell
    directions = [(-1, -1), (-1, 0), (-1, 1),#
                  ( 0, -1),          ( 0, 1), # each possible direction you can move around a cell
                  ( 1, -1), ( 1, 0), ( 1, 1)]#
    count = 0
    for dr, dc in directions: # check each direction around a cell and see if there are any alive cells
        r, c = row + dr, col + dc
        if 0 <= r < len(board) and 0 <= c < len(board[0]):
            if board[r][c] == 'O':
                count += 1
    return count

def IsAlive(board):
    rows = len(board)
    cols = len(board[0])
    new_board = [row[:] for row in board]

    # check to see if the board follows the rules and update it if nessisary

    #1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    #2. Any live cell with two or three live neighbours lives on to the next generation.
    #3. Any live cell with more than three live neighbours dies, as if by overpopulation.
    #4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    for x in range(rows):
        for y in range(cols):
            count = count_neighbors(board, x, y)
            if board[x][y] == 'O':
                new_board[x][y] = 'O' if 2 <= count <= 3 else 'X'
            else:
                new_board[x][y] = 'O' if count == 3 else 'X'
    return new_board

# --- Main Loop ---
board = generate_board(25, 25, 0.25) # Generate Board

while True:
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
    printBoard(board) # print board
    board = IsAlive(board) # update board with alive cells
    time.sleep(1) # wait one second to avoid way to fast flickering

