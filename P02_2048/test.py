import random
import game
import sys
from multiprocessing import Pool
import itertools

import time


# Author:   chrn (original by nneonneo)
# Date: 11.11.2016
# Copyright:   Algorithm from https://github.com/nneonneo/2048-ai
# Description: The logic to beat the game. Based on expectimax algorithm.

def find_best_move(board):
    """
    find the best move for the next turn.
    It will split the workload in 4 process for each move.
    """


bestmove = -1
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
move_args = [UP, DOWN, LEFT, RIGHT]
result = [score_toplevel_move(i, board) for i in range(len(move_args))]
bestmove = result.index(max(result))
for m in move_args:
    print(m)
print(result[m])
return bestmove


def score_toplevel_move(move, board):
    """
    Entry Point to score the first move.
    """


newboard = execute_move(move, board)

if board_equals(board, newboard):
    return 0
    # TODO:
    # Implement the Expectimax Algorithm.
    # 1.) Start the recursion until it reach a certain depth
    # 2.) When you don't reach the last depth, get all possible board states and
    # calculate their scores dependence of the probability this will occur. (recursively)
    # 3.) When you reach the leaf calculate the board score with your heuristic.
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3
    score = 0
    DEPTH = 2
    score = max(score, score_move(UP, newboard, DEPTH))
    score = max(score, score_move(DOWN, newboard, DEPTH))
    score = max(score, score_move(LEFT, newboard, DEPTH))
    score = max(score, score_move(RIGHT, newboard, DEPTH))

    for x in range(4):
        for y in range(4):
            if newboard[x, y] == 0:
            newboard[x, y] = 2

    score += 0.9 * calc_score(newboard, UP)
    score += 0.9 * calc_score(newboard, DOWN)
    score += 0.9 * calc_score(newboard, LEFT)
    score += 0.9 * calc_score(newboard, RIGHT)
    newboard[x, y] = 4
    score += 0.1 * calc_score(newboard, UP)
    score += 0.1 * calc_score(newboard, DOWN)
    score += 0.1 * calc_score(newboard, LEFT)
    score += 0.1 * calc_score(newboard, RIGHT)

    return score


# return random.randint(0,1000)

def score_move(move, board, depth):
    """
    Entry Point to score the first move.
    """


newboard = execute_move(move, board)
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

if board_equals(board, newboard):
    return 0
score = 0
if depth > 0:
    score = max(score, score_move(UP, newboard, depth - 1))
score = max(score, score_move(DOWN, newboard, depth - 1))
score = max(score, score_move(LEFT, newboard, depth - 1))
score = max(score, score_move(RIGHT, newboard, depth - 1))
for x in range(4):
    for y in range(4):
        if newboard[x, y] == 0:
        newboard[x, y] = 2
score += 0.9 * calc_score(newboard, UP)
score += 0.9 * calc_score(newboard, DOWN)
score += 0.9 * calc_score(newboard, LEFT)
score += 0.9 * calc_score(newboard, RIGHT)
newboard[x, y] = 4
score += 0.1 * calc_score(newboard, UP)
score += 0.1 * calc_score(newboard, DOWN)
score += 0.1 * calc_score(newboard, LEFT)
score += 0.1 * calc_score(newboard, RIGHT)

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


return (newboard == board).all()


def func_star(a_b):
    """
    Helper Method to split the programm in more processes.
    Needed to handle more than one parameter.
    """


return score_toplevel_move(*a_b)


def calc_score(board, move):
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


highest_match = [0, 0]
match_count = [0, 0]
# Calculate Score for Horizontal Move
for x in range(4):
    last_element = 0
for y in range(4):
    if board[x, y] != 0:
        if last_element == board[x, y]:
        highest_match[0] += board[x, y] * 2
match_count[0] += 1
last_element = board[x, y]
# Calculate Score for Vertical Move
for y in range(4):
    last_element = 0
for x in range(4):
    if board[x, y] != 0:
        if last_element == board[x, y]:
        highest_match[1] += board[x, y] * 2
match_count[1] += 1
last_element = board[x, y]

max_merges = match_count[0] + match_count[1]
weight_vert = 0
weight_hor = 0
if max_merges > 0:
    weight_hor = match_count[0] / max_merges
weight_vert = match_count[1] / max_merges
score_horizontal = highest_match[0] * weight_hor
score_vertcal = highest_match[1] * weight_vert
score_left = 0
score_right = 0
score_up = 0
score_down = 0
if score_horizontal > score_vertcal:
    score_left = calc_board_score(execute_move(LEFT, board))
score_right = calc_board_score(execute_move(RIGHT, board))
elif score_horizontal < score_vertcal:
score_up = calc_board_score(execute_move(UP, board))
score_down = calc_board_score(execute_move(DOWN, board))
else:
score_left = calc_board_score(execute_move(LEFT, board))
score_right = calc_board_score(execute_move(RIGHT, board))
score_up = calc_board_score(execute_move(UP, board))
score_down = calc_board_score(execute_move(DOWN, board))
return max(score_down, score_left, score_right, score_up)


def calc_board_score(board):
    board_score = 0


zeroes = 0
for x in range(4):
    for y in range(4):
        board_score += board[x, y] * (0.1 * x + 1 * y);
if board[x, y] == 0:
    zeroes += 1
return board_score * (zeroes / 16)
