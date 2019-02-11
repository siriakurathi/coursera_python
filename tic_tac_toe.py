"""
Monte Carlo Tic-Tac-Toe Player
"""

from collections import defaultdict
from random import choice
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 2.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def alternate_player(current_player):
    """
    retuerns constant value (provided from proc_ttt_provided) for alternate player.
    """
    if (current_player == provided.PLAYERX):
        return provided.PLAYERO
    else:
        return provided.PLAYERX

def mc_trial(board, player):
    """
    This function takes a current board and the next player to move. 
    The function should play a game starting with the given player by 
    making random moves, alternating between players. The function 
    should return when the game is over. The modified board will 
    contain the state of the game, so the function does not return anything. 
    In other words, the function should modify the board input.
    """
    current_player = player
    while(board.check_win() == None):
        empty_squares = board.get_empty_squares()
        move_square = choice(empty_squares)
        board.move(move_square[0],move_square[1],current_player)
        current_player = alternate_player(current_player)

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) with the same dimensions 
    as the Tic-Tac-Toe board, a board from a completed game, and which player the 
    machine player is. The function should score the completed board and update the 
    scores grid. As the function updates the scores grid directly, it does not return anything,
    """
    if board.check_win() == player:
        current_offset = SCORE_CURRENT * 1
        other_offset = SCORE_OTHER * -1
    elif board.check_win() == alternate_player(player):
        current_offset = SCORE_CURRENT * -1
        other_offset = SCORE_OTHER * 1
    else:
        return None

    for row_index in range(board.get_dim()):
        for col_index in range(board.get_dim()):
            if board.square(row_index,col_index) == player:
                scores[row_index][col_index] += current_offset
            elif board.square(row_index, col_index) == alternate_player(player):
                scores[row_index][col_index] += other_offset

def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores. The function should find all 
    of the empty squares with the maximum score and randomly return one of them as a (row, column) 
    tuple. It is an error to call this function with a board that has no empty squares 
    (there is no possible next move), so your function may do whatever it wants in that case. 
    The case where the board is full will not be tested.
    """
    dictionary = defaultdict(list)
    empty_squares = board.get_empty_squares()
    
    if len(empty_squares) == 0:
        return None
    
    for square in empty_squares:
        dictionary[scores[ square[0] ][ square[1] ]].append(square)

    max_values = dictionary[max(dictionary.keys())]
    best_move = choice(max_values)

    return best_move

def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is, and the number of trials 
    to run. The function should use the Monte Carlo simulation described above to return a move for 
    the machine player in the form of a (row, column) tuple. Be sure to use the other functions you have written!
    """
    scores = [[0 for dummy_y in range(board.get_dim())] for dummy_x in range(board.get_dim())]

    for dummy_trial in range(trials):
        game = board.clone()
        mc_trial(game, player)
        mc_update_scores(scores, game, player)

    return get_best_move(board, scores)