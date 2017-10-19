import random
import game
import sys

# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.

def find_best_move(board):
    """
    find the best move for the next turn.
    It will split the workload in 4 process for each move.
    """
    bestmove = -1
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    move_args = [UP,DOWN,LEFT,RIGHT]
    
    result = [score_toplevel_move(i, board) for i in range(len(move_args))]
    
    bestmove = result.index(max(result))
    for m in move_args:
        print(m)
        print(result[m])
    
    return bestmove
    
def score_toplevel_move(move, board, depth = 0):
    """
    Entry Point to score the first move.
    """
    newboard = execute_move(move, board)
    emptyTiles = getEmptyTiles(newboard)
    
    if board_equals(board,newboard):
        return 0
       
    if depth < 2:
        score = 0
        
        for i in range(4): 
                for j in range(3):
                    if newboard[i][j] == 0:
                        newboard[i][j] = 2
                        score += 0.9 * score_toplevel_move(0, newboard, depth+1)
                        score += 0.9 * score_toplevel_move(1, newboard, depth+1)
                        score += 0.9 * score_toplevel_move(2, newboard, depth+1)
                        score += 0.9 * score_toplevel_move(3, newboard, depth+1)
                        
                        newboard[i][j] = 4
                        score += 0.1 * score_toplevel_move(0, newboard, depth+1)
                        score += 0.1 * score_toplevel_move(1, newboard, depth+1)
                        score += 0.1 * score_toplevel_move(2, newboard, depth+1)
                        score += 0.1 * score_toplevel_move(3, newboard, depth+1)
        return score
        
    else: 
        return calcScore(move, board)

def getHeuristic(scores2, scores4, board):
    Rank = [[6,5,4,3], [5,4,3,2], [4,3,2,1], [3,2,1,0]]
    
    scoreHeuristic = 0
    for j in range(len(scores2)):
        scoreHeuristic += scores2[j] * 0.9
    for j in range(len(scores4)):
        scoreHeuristic += scores4[j] * 0.1
              
        """
    positionHeuristic = 0  
    for i in range(0, 4):  
        for j in range(0, 4):
            positionHeuristic += Rank[i][j] * board[i][j]
         """   
    return scoreHeuristic
            
def calcScore(move, board):
    score = 0;
    # horizonal check
    if move == 2 or move == 3:
        for i in range(4): 
            for j in range(3):
                if board[i][j] == board[i][j+1]:
                    score += 2*board[i][j]

    # vertical check
    if move == 0 or move == 1:
        for i in range(4): 
            for j in range(3):
                if board[j][i] == board[j+1][i]:
                    score += 2*board[j][i]
                    
    return score

def execute_move(move, board):
    """
    move and return the grid without a new random tile 
	It won't affect the state of the game in the browser.
    """

    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

    if move == UP:
        return game.merge_up(board)
    elif move == DOWN:
        return game.merge_down(board)
    elif move == LEFT:
        return game.merge_left(board)
    elif move == RIGHT:
        return game.merge_right(board)
    else:
        sys.exit("No valid move")
        
def board_equals(board, newboard):
    """
    Check if two boards are equal
    """
    return  (newboard == board).all()  

def getEmptyTiles(board):
    tiles = [];
    
    for i in range(4): 
        for j in range(4):
            if board[i][j] == 0:
                tiles.append([i, j])
                
    return tiles
