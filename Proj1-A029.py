"""
Projecto 1 - Inteligencia Artificial

Implementacao de um agente capaz de solucionar tabuleiros do jogo Solitaire


Grupo 29:
- Hugo Miguel Neves do Vale n 75834
- Joao Goncalo da Luz Rodrigues n 76154

"""
from search import *

import copy

# TAI content
def c_peg ():
    return "O"
def c_empty ():
    return "_"
def c_blocked ():
    return "X"
def is_empty (e):
    return e == c_empty()
def is_peg (e):
    return e == c_peg()
def is_blocked (e):
    return e == c_blocked()


# TAI pos
# Tuplo (l, c)
def make_pos (l, c):
    return (l, c)
def pos_l (pos):
    return pos[0]
def pos_c (pos):
    return pos[1]


# TAI move
# List [p_initial, p_final]
def make_move (i, f):
    return [i, f]
def move_initial (move):
    return move[0]
def move_final (move):
    return move[1]


# TAI board
# Board [[line1], [line2], ..., [linen]] len(board) = num_lines , len(line) = num_collumns
# Move [p_initial, p_final]
def board_moves (board):
    num_lines = len(board)
    num_collumns = len(board[0])
    moves = []
    
    for i in range(num_lines):
        for j in range(num_collumns):
            if is_peg(board[i][j]):
                if (i-2) >= 0 and is_peg(board[i-1][j]) and is_empty(board[i-2][j]):
                    moves.append(make_move(make_pos(i,j),make_pos(i-2,j)))
                if (i+2) <= (num_lines-1) and is_peg(board[i+1][j]) and is_empty(board[i+2][j]):
                    moves.append(make_move(make_pos(i,j),make_pos(i+2,j)))
                if (j-2) >= 0 and is_peg(board[i][j-1]) and is_empty(board[i][j-2]):
                    moves.append(make_move(make_pos(i,j),make_pos(i,j-2)))
                if (j+2) <= (num_collumns-1) and is_peg(board[i][j+1]) and is_empty(board[i][j+2]):
                    moves.append(make_move(make_pos(i,j),make_pos(i,j+2)))               
    
    return moves

def board_perform_move (board, move):
    final_board = copy.deepcopy(board)
    
    final_board[(pos_l(move_initial(move)) + pos_l(move_final(move)))//2][(pos_c(move_initial(move)) + pos_c(move_final(move)))//2] = c_empty()
    final_board[pos_l(move_initial(move))][pos_c(move_initial(move))] = c_empty()
    final_board[pos_l(move_final(move))][pos_c(move_final(move))] = c_peg()
    
    return final_board


# Class sol_state
class sol_state:
    def __init__(self, board):
        self.board = board
        
    def __lt__(self, other_sol_state):
        return self.board < other_sol_state.board
    
    def __le__(self, other_sol_state):
        return self.board <= other_sol_state.board
    
    def __eq__(self, other_sol_state):
        return self.board == other_sol_state.board
    
    def __ne__(self, other_sol_state):
        return self.board != other_sol_state.board
    
    def __ge__(self, other_sol_state):
        return self.board > other_sol_state.board
    
    def __gt__(self, other_sol_state):
        return self.board >= other_sol_state.board
    
    def __hash__(self):
        return hash(tuple([tuple(line) for line in self.board]))
    

# Class solitaire
# The agent main operations are defined here
class solitaire(Problem):
    """Models a Solitaire problem as a satisfaction problem. 
       A solution cannot have more than 1 peg left on the board."""
    
    def __init__(self, board):
        Problem.__init__(self, sol_state(board))
        
    def actions(self, state):        
        return board_moves(state.board)
    
    def result(self, state, action):
        return sol_state(board_perform_move(state.board, action))
        
    def goal_test(self, state):      
        count_peg = 0
        for line in state.board:
            count_peg += line.count(c_peg())
        return count_peg == 1
    
    def path_cost(self, c, state1, action, state2):
        return len(board_moves(state2.board))
    
    def h(self, node):
        """Needed for informed search."""
        count_peg = -1
        for line in node.state.board:
            count_peg += line.count(c_peg())
        return count_peg

game1 = solitaire([["_","O","O","O","_"],["O","_","O","_","O"],["_","O","_","O","_"],["O","_","O","_","_"],["_","O","_","_","_"]])
game2 = solitaire([["O","O","O","X"],["O","O","O","O"],["O","_","O","O"],["O","O","O","O"]])
game3 = solitaire([["O","O","O","X","X"],["O","O","O","O","O"],["O","_","O","_","O"],["O","O","O","O","O"]])
game4 = solitaire([["O","O","O","X","X","X"],["O","_","O","O","O","O"],["O","O","O","O","O","O"],["O","O","O","O","O","O"]])

compare_searchers([game1,game2,game3,game4],['Searcher','Board1','Board2','Board3','Board4'],[depth_first_tree_search, greedy_search, astar_search])

