"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    no_x = 0
    no_o = 0
    for row in board:
        for col in row:
            if col == X:
                no_x += 1
            if col == O:
                no_o += 1
    if no_x > no_o:
        return O
    else:
        return X

  


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == EMPTY:
                possible_moves.add((row,col))
    return possible_moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    possible_actions = actions(board)

    if action not in possible_actions:
        raise Exception("Invalid Action")
    
    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]
    
    for row in range(len(board)):
        if board[0][row] == board[1][row] == board[2][row] and board[0][row] is not EMPTY:
            return board[0][row]
    
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board [0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    for row in board:
        for col in row:
            if col == EMPTY:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def min_value(board):
    """
    Returns the minimum value of the board
    """
    v = math.inf

    # runs when game is over
    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = min(v, max_value(result(board,action)))
    return v

def max_value(board):
    """
    Returns the maximum value of the board
    """
    v = -math.inf

    # runs when game is over
    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = max(v, min_value(result(board,action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # returns true if game is over
    if terminal(board): 
        return None
    
    # X is max player
    elif player(board) == X:
        plays =[]

        for action in actions(board):
            plays.append([min_value(result(board,action)),action])

        # shorting and getting the maximum value
        return sorted(plays, key =lambda x:x[0], reverse= True)[0][1]
    # O is min player
    elif player(board) == O:
        plays =[]

        for action in actions(board):
            plays.append([max_value(result(board,action)),action])
        # shorting and getting the minimum value
        return sorted(plays, key =lambda x:x[0])[0][1]

