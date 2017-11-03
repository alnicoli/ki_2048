import random
import game
import sys
import math
from heuristicai import *
# Author:      chrn (original by nneonneo)
# Date:        11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.
R = [[20,5,4,1],[5,4,1,0],[4,1,0,-1],[1,0,-1,-2]] # Tile weight

def find_best_move(board):
    """
    find the best move for the next turn.
    It will split the workload in 4 process for each move.
    """
    bestmove = -1
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    move_args = [UP,DOWN,LEFT,RIGHT]

    result = [score_toplevel_move(i, board) for i in range(len(move_args))]

    print("RESULTS: " + str(result))

    bestmove = result.index(max(result))

    #input("PRESS ANY KEY")

    return bestmove

def score_toplevel_move(move, board):
    """
    Entry Point to score the first move.
    """
    newboard = execute_move(move, board)

    if board_equals(board, newboard):
        print("OLD BOARD")
        return 0

    if empty_tiles_count(newboard) > 5:
        score = expectimax(newboard, 3, 1)  #1
    else:
        score = expectimax(newboard, 4, 1)  #1

    return score

def expectimax(board, depth, step):
    if depth == 0:
        return calc_score(board)

    elif step == 1:
        score = 0

        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    board[i][j] = 4
                    newscore = expectimax(board, depth-1, 2) #2

                    if newscore == -99999999:
                        score += 0
                    else:
                        score += 1/empty_tiles_count(board) if empty_tiles_count(board) != 0 else 1 * 0.1 * newscore

                    board[i][j] = 2
                    newscore = expectimax(board, depth-1, 2)

                    if newscore == -99999999:
                        score += 0
                    else:
                        score += 1/empty_tiles_count(board) if empty_tiles_count(board) != 0 else 1 * 0.9 * newscore

        return score

    elif step == 2:
        score = -99999999

        for i in range(4):
            newboard = execute_move(i, board)
            newscore = expectimax(newboard, depth-1, 1) #3

            if newscore > score:
                score = newscore

        return score

def calc_score(board):
    snake = []
    for i, col in enumerate(zip(*board)):
        snake.extend(reversed(col) if i % 2 == 0 else col)

    m = max(snake)

    empty = empty_tiles_count(board)

    summ = sum((x / 10 ** n) for n, x in enumerate(snake))
    pen = math.pow(max(snake) * abs(board[3][0] - m), 2)

    print("SUM: " + str(summ))
    print("PEN: " + str(pen))

    return summ - pen if summ - pen > 0 else 0


def calc_score_old(board):
    positionRanking = 0

    for i in range(4):
        for j in range(4):
            positionRanking += abs(R[i][j] * board[i][j] * board[i][j])

    penalty = 0
    multiplikator = 2

    points = 0

    for i in range(4):
        for j in range(4):
            if j - 1 >= 0 and board[i][j] != 0 and board[i][j-1] != 0:
                penalty += abs(board[i][j] - board[i][j - 1]) * multiplikator
            if j + 1 < 4 and board[i][j] != 0 and board[i][j+1] != 0:
                penalty += abs(board[i][j] - board[i][j + 1]) * multiplikator

                if board[i][j] == board[i][j + 1] and board[i][j] != 0:
                    points += 2 * board[i][j]
            if i - 1 >= 0 and board[i][j] != 0 and board[i-1][j] != 0:
                penalty += abs(board[i][j] - board[i - 1][j]) * multiplikator
            if i + 1 < 4 and board[i][j] != 0 and board[i+1][j] != 0:
                penalty += abs(board[i][j] - board[i + 1][j]) * multiplikator

                if board[i][j] == board[i + 1][j] and board[i][j] != 0:
                    points += 2 * board[i][j]

    returning_position_ranking = positionRanking / math.log(2)
    returning_points = points / math.log(2) * points
    returning_penalty = penalty / math.log(2)
    empty = math.pow(highest_tile(board)+empty_tiles_count(board), 2)

    return returning_position_ranking + returning_points - returning_penalty + empty

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

def empty_tiles_count(board):
    count = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                count += 1
    return count

def highest_tile(board):
    highest = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                if board[i][j] > highest:
                    highest = board[i][j]
    return highest