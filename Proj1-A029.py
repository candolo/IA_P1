"""
Projecto 1 - Inteligencia Artificial

Implementacao de um agente capaz de solucionar tabuleiros do jogo Solitaire


Grupo 29:
- Hugo Miguel Neves do Vale n 75834
- Joao Goncalo da Luz Rodrigues n 76154

"""
from search import *

import copy
import time

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

def run_searchs(game):
    dfs_problem = InstrumentedProblem(game)
    greedy_problem = InstrumentedProblem(game)
    astar_problem = InstrumentedProblem(game)
    
    #DFS Test
    t0_dfs = time.clock()
    depth_first_tree_search(dfs_problem)
    t1_dfs = time.clock()
    t_dfs = t1_dfs - t0_dfs
    
    #Greedy Test
    t0_greedy = time.clock()
    greedy_search(greedy_problem)
    t1_greedy = time.clock()
    t_greedy = t1_greedy - t0_greedy    
    
    #Astar Test
    t0_astar = time.clock()
    astar_search(astar_problem)
    t1_astar = time.clock()
    t_astar = t1_astar - t0_astar
    
    dfs_word = "### DFS ###\nTime: " + repr(t_dfs) + "\nSucessors: " + repr(dfs_problem.succs) + "\nGoal Tests: " + repr(dfs_problem.goal_tests) + "\nStates: " + repr(dfs_problem.states)
    print(dfs_word)
    
    greedy_word = "### Greedy ###\nTime: " + repr(t_greedy) + "\nSucessors: " + repr(greedy_problem.succs) + "\nGoal Tests: " + repr(greedy_problem.goal_tests) + "\nStates: " + repr(greedy_problem.states)
    print(greedy_word)
    
    astar_word = "### Astar ###\nTime: " + repr(t_astar) + "\nSucessors: " + repr(astar_problem.succs) + "\nGoal Tests: " + repr(astar_problem.goal_tests) + "\nStates: " + repr(astar_problem.states)
    print(astar_word)
    
    return dfs_word + "\n" + greedy_word + "\n" + astar_word
    
print("Running Searches in Board1\n")
file = open("Board1.txt","w+")
result = run_searchs(game1)
file.write(result)
file.close
print("\nBoard1 Searches Done\n")

print("Running Searches in Board2\n")
file = open("Board2.txt","w+")
result = run_searchs(game2)
file.write(result)
file.close
print("\nBoard2 Searches Done\n")

print("Running Searches in Board3\n")
file = open("Board3.txt","w+")
result = run_searchs(game3)
file.write(result)
file.close
print("\nBoard3 Searches Done\n")

print("Running Searches in Board4\n")
file = open("Board4.txt","w+")
result = run_searchs(game4)
file.write(result)
file.close
print("\nBoard4 Searches Done\n")