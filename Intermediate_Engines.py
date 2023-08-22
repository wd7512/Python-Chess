import chess
from Simple_Display import main, main_one_agent, main_two_agent
from Recording_Display import save_main_two_agent
from copy import deepcopy
import random
import time
import chess.polyglot



'''
The main issues with this simple min max are as follows
 - It has no sense of what the actual win condition is (checkmate)
 - Therefore it does not have an ability to handle a scenario
 - where there are no legal moves
#COMPLETED

 - Also it always picks the first move from the list when
 - there are multiple moves with the same evaulation.
 - We could simply pick a random one or have a secondary
 - evaluation function.
#COMPLETED

 - Perhaps this evaluation function could be the total number
 - of possible moves as a simple concept in chess is to activate
 - pieces onto much more mobile squares
#COMPLETED

 - Openings are terrible for this ai and it will always for a min max
 - function as it can never look deep enough ahead. Therefore we can
 - try to implement an opening book.
#COMPLETED
'''


#opening book
reader = chess.polyglot.open_reader('baron30.bin')

def random_agent(BOARD):

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

def eval_space(BOARD):
    no_moves = len(list(BOARD.legal_moves))

    #this function is always between 0 and 1 so we will never evaluate
    #this as being greater than a pawns value. The 20 value is arbitrary
    #but this number is chosen as it centers value around 0.5
    value = (no_moves/(20+no_moves))
    
    if BOARD.turn == True:
        return value
    else:
        return -value

def min_maxN(BOARD,N):

    opening_move = reader.get(BOARD)

    if opening_move == None:
        pass
    else:
        return opening_move.move


    #generate list of possible moves
    moves = list(BOARD.legal_moves)
    scores = []

    #score each move
    for move in moves:
        #temp allows us to leave the original game state unchanged
        temp = deepcopy(BOARD)
        temp.push(move)

        #here we must check that the game is not over
        outcome = temp.outcome()
        
        #if checkmate
        if outcome == None:
            #if we have not got to the final depth
            #we search more moves ahead
            if N>1:
                temp_best_move = min_maxN(temp,N-1)
                temp.push(temp_best_move)

            scores.append(eval_board(temp))

            
            
        #if checkmate
        elif temp.is_checkmate():

            # we return this as best move as it is checkmate
            return move

        # if stalemate
        else:
            #value to disencourage a draw
            #the higher the less likely to draw
            #default value should be 0
            #we often pick 0.1 to get the bot out of loops in bot vs bot
            val = 1000
            if BOARD.turn == True:
                scores.append(-val)
            else:
                scores.append(val)

        #this is the secondary eval function
        scores[-1] = scores[-1] + eval_space(temp)


    if BOARD.turn == True:
        
        best_move = moves[scores.index(max(scores))]

    else:
        best_move = moves[scores.index(min(scores))]



    return best_move
        
# a simple wrapper function as the display only gives one imput , BOARD

def min_max1(BOARD):
    return min_maxN(BOARD,1)

def min_max2(BOARD):

    return min_maxN(BOARD,2)

def min_max3(BOARD):
    return min_maxN(BOARD,3)

def min_max4(BOARD):
    return min_maxN(BOARD,4)

main_one_agent(chess.Board(),min_max2,False)
