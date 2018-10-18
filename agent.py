from search import (Problem, Node)

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
                    moves.append([make_pos(i,j),make_pos(i-2,j)])
                if (i+2) <= (num_lines-1) and is_peg(board[i+1][j]) and is_empty(board[i+2][j]):
                    moves.append([make_pos(i,j),make_pos(i+2,j)])
                if (j-2) >= 0 and is_peg(board[i][j-1]) and is_empty(board[i][j-2]):
                    moves.append([make_pos(i,j),make_pos(i,j-2)])
                if (j+2) <= (num_collumns-1) and is_peg(board[i][j+1]) and is_empty(board[i][j+2]):
                    moves.append([make_pos(i,j),make_pos(i,j+2)])            
    
    return moves

def board_perform_move (board, move):
    initial = move_initial(move)
    final = move_final(move)
    final_board = copy.deepcopy(board)
    
    middle_pos_l = (pos_l(initial) + pos_l(final))//2
    middle_pos_c = (pos_c(initial) + pos_c(final))//2
    
    final_board[middle_pos_l][middle_pos_c] = c_empty()
    final_board[pos_l(initial)][pos_c(initial)] = c_empty()
    final_board[pos_l(final)][pos_c(final)] = c_peg()
    
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
        hashable_matrix = []
        for i in range(len(self.board)):
            hashable_matrix.append(tuple(self.board[1]))
        return hash(tuple(hashable_matrix))
    

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
        for i in range(len(state.board)):
            count_peg += state.board[i].count(c_peg())
        return count_peg == 1
    
    def path_cost(self, c, state1, action, state2):
        return c + 1
    
    def h(self, node):
        """Needed for informed search."""
        state_node = copy.deepcopy(node.state)
        count_peg = -1
        for i in range(len(state_node.board)):
            count_peg += state_node.board[i].count(c_peg())
        return count_peg
