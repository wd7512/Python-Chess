import chess
from Simple_Display import main, main_one_agent, main_two_agent
from Recording_Display import save_main_two_agent
import random
import time
from copy import deepcopy

def random_agent(BOARD):
    time.sleep(0)
    return random.choice(list(BOARD.legal_moves))

scoring= {'p': -1,
          'n': -3,
          'b': -3,
          'r': -5,
          'q': -9,
          'k': 0,
          'P': 1,
          'N': 3,
          'B': 3,
          'R': 5,
          'Q': 9,
          'K': 0,
          
          }




def eval_board(BOARD):
    score = 0
    pieces = BOARD.piece_map()
    for key in pieces:
        score += scoring[str(pieces[key])]

    return score

#this is min_max at one level
def most_value_agent(BOARD):



    moves = list(BOARD.legal_moves)
    scores = []
    for move in moves:
        temp = deepcopy(BOARD)
        temp.push(move)
        

        scores.append(eval_board(temp))


    if BOARD.turn == True:
        
        best_move = moves[scores.index(max(scores))]

    else:
        best_move = moves[scores.index(min(scores))]

    return best_move

def min_max2(BOARD):

    moves = list(BOARD.legal_moves)
    scores = []

    for move in moves:
        temp = deepcopy(BOARD)
        temp.push(move)

        temp_best_move = most_value_agent(temp)

        temp.push(temp_best_move)

        scores.append(eval_board(temp))

    if BOARD.turn == True:
        
        best_move = moves[scores.index(max(scores))]

    else:
        best_move = moves[scores.index(min(scores))]

    return best_move


def min_maxN(BOARD,N):


    moves = list(BOARD.legal_moves)
    scores = []

    for move in moves:
        temp = deepcopy(BOARD)
        temp.push(move)

        if N>1:
            temp_best_move = min_maxN(temp,N-1)
            temp.push(temp_best_move)

        scores.append(eval_board(temp))

    if BOARD.turn == True:
        
        best_move = moves[scores.index(max(scores))]

    else:
        best_move = moves[scores.index(min(scores))]

    return best_move
        
# a simple wrapper function as the display only gives one imput , BOARD
def play_min_maxN(BOARD):
    N=3
    return min_maxN(BOARD,N)

save_main_two_agent(chess.Board(),play_min_maxN,True,random_agent)
