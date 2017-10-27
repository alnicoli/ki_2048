import random
import game
import sys
import numpy as np
import math

# Author:			chrn (original by nneonneo)
# Date:				11.11.2016
# Description:		The logic of the AI to beat the game.

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

R = [[6,5,4,1],[5,4,1,0],[4,3,2,1],[3,2,1,0]] # Tile weight

def find_best_move(board):
    bestmove = 0

    #[0][0] for horizontal points
    #[0][1] for horizontal merges count
    #[0][0] for vertical points
    #[0][0] for vertical merges count

    possiblePointsAndMerges = np.array([[0,0],[0,0]])

    # horizonal check
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j+1] and board[i][j] != 0 and board[i][j+1] != 0:
                possiblePointsAndMerges[0][0] += 2*board[i][j]
                possiblePointsAndMerges[0][1] += 1

    # vertical check
    for i in range(4):
        for j in range(3):
            if board[j][i] == board[j+1][i] and board[j][i] != 0 and board[j+1][i] != 0:
                possiblePointsAndMerges[1][0] += 2*board[j][i]
                possiblePointsAndMerges[1][1] += 1

    zeroCount = getZeroCount(board)

    # Force decision based on possible merges
    if zeroCount < 8:
        if possiblePointsAndMerges[0][1] > possiblePointsAndMerges[1][1]:
            bestmove = random.choice([LEFT,RIGHT])
        elif possiblePointsAndMerges[0][1] == possiblePointsAndMerges[1][1]:
            bestmove = random.choice([UP,DOWN,LEFT,RIGHT])
        else:
            bestmove = random.choice([UP,DOWN])
    # Use way of most points
    else:
        if possiblePointsAndMerges[0][0] > possiblePointsAndMerges[1][0]:
            bestmove = random.choice([LEFT,RIGHT])
        elif possiblePointsAndMerges[0][0] == possiblePointsAndMerges[1][0]:
            bestmove = random.choice([UP,DOWN,LEFT,RIGHT])
        else:
            bestmove = random.choice([UP,DOWN])

	# TODO:
	# Build a heuristic agent on your own that is much better than the random agent.
	# Your own agent don't have to beat the game.
    #bestmove = find_best_move_random_agent()
    return bestmove

def find_best_move_v2(board):
    bestmove = 0

    #[0][0] for horizontal points
    #[0][1] for horizontal merges count
    #[0][0] for vertical points
    #[0][0] for vertical merges count

    possiblePointsAndMerges = np.array([[0,0],[0,0]])

    tileCounter = 0

    # horizonal check
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j+1]:
                possiblePointsAndMerges[0][0] += 2*board[i][j]
                possiblePointsAndMerges[0][1] += 1

    # vertical check
    for i in range(4):
        for j in range(3):
            if board[j][i] == board[j+1][i]:
                possiblePointsAndMerges[1][0] += 2*board[j][i]
                possiblePointsAndMerges[1][1] += 1

    # count not empty tiles
    for j in range(4):
        for i in range(4):
            if board[j][i] != 0:
                tileCounter += tileCounter

    # Force decision based on possible merges
        if possiblePointsAndMerges[0][1] > possiblePointsAndMerges[1][1]:
            bestmove = random.choice([LEFT,RIGHT])
        elif possiblePointsAndMerges[0][1] == possiblePointsAndMerges[1][1]:
            if possiblePointsAndMerges[0][0] > possiblePointsAndMerges[1][0]:
                bestmove = random.choice([LEFT,RIGHT])
            elif possiblePointsAndMerges[0][0] == possiblePointsAndMerges[1][0]:
                bestmove = random.choice([UP,DOWN,LEFT,RIGHT])
            else:
                bestmove = random.choice([UP,DOWN])
        else:
            bestmove = random.choice([UP,DOWN])


	# TODO:
	# Build a heuristic agent on your own that is much better than the random agent.
	# Your own agent don't have to beat the game.
    #bestmove = find_best_move_random_agent()
    return bestmove

def find_best_move_v3(board):
    ranks = [0,0,0,0]

    newboard = execute_move(UP, board)
    ranks[0] = boardRanking(newboard)

    if board_equals(board, newboard):
        ranks[0] = 0

    newboard = execute_move(DOWN, board)
    ranks[1] = boardRanking(newboard)

    if board_equals(board, newboard):
        ranks[1] = 0

    newboard = execute_move(LEFT, board)
    ranks[2] = boardRanking(newboard)

    if board_equals(board, newboard):
        ranks[2] = 0

    newboard = execute_move(RIGHT, board)
    ranks[3] = boardRanking(newboard)

    if board_equals(board, newboard):
        ranks[3] = 0

    bestmove = ranks.index(max(ranks))

    #input("Press ANY KEY to continue")

    return bestmove

def find_best_move_random_agent():
    return random.choice([UP,DOWN,LEFT,RIGHT])

def logger(value):
    if value == 0:
        return 0
    else:
        return math.log(value) / math.log(2)

def boardRanking_testing(board):

    positionRanking = 0

    for i in range(4):
        for j in range(4):
            positionRanking += abs(R[i][j] * board[i][j] * board[i][j])

    penalty = 0
    multiplikator = 2

    points = 0

    for i in range(4):
        for j in range(4):
            current = logger(board[i][j])

            if j-1 >= 0:
                penalty += abs(current - logger(board[i][j-1])) * multiplikator
            if j+1 < 4:
                penalty += abs(current - logger(board[i][j+1])) * multiplikator

                if current == board[i][j+1] and board[i][j] != 0:
                    points += 2*board[i][j]
            if i-1 >= 0:
                penalty += abs(current - logger(board[i-1][j])) * multiplikator
            if i+1 < 4:
                penalty += abs(current - logger(board[i+1][j])) * multiplikator

                if current == board[i+1][j] and current != 0:
                    points += 2*current

    pr = positionRanking/math.log(2)
    po = points * logger(maxTile(board)) * 3
    pe = penalty * logger(maxTile(board))

    print("Position ranking: " + str(pr))
    print("Points: " + str(po))
    print("Penalty: " + str(pe))

    return pr + getEmptyTiles(board) * getEmptyTiles(board)

def maxTile(board):
    res = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] > res:
                res = board[i][j]
    return res

def boardRanking(board):

    positionRanking = 0

    for i in range(4):
        for j in range(4):
            positionRanking += abs(R[i][j] * pow(board[i][j], 2))

    penalty = 0
    multiplikator = 2

    points = 0

    for i in range(4):
        for j in range(4):
            if j-1 >= 0:
                penalty += abs(board[i][j] - board[i][j-1]) * multiplikator
            if j+1 < 4:
                penalty += abs(board[i][j] - board[i][j+1]) * multiplikator

                if board[i][j] == board[i][j+1] and board[i][j] != 0:
                    points += 2*board[i][j]
            if i-1 >= 0:
                penalty += abs(board[i][j] - board[i-1][j]) * multiplikator
            if i+1 < 4:
                penalty += abs(board[i][j] - board[i+1][j]) * multiplikator

                if board[i][j] == board[i+1][j] and board[i][j] != 0:
                    points += 2*board[i][j]

    print("Position ranking: " + str(positionRanking/math.log(2)))
    print("Points: " + str(points/math.log(2)*points))
    print("Penalty: " + str(penalty/math.log(2)))

    return (positionRanking/math.log(2) + points/math.log(2)*points - penalty/math.log(2))

def execute_move(move, board):
    """
    move and return the grid without a new random tile
	It won't affect the state of the game in the browser.
    """

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

def getPossibleMerges(board):
    possibleMerges = [0,0]

    for i in range(4):
        lastX = 0
        lastY = 0

        for j in range(4):
            if board[i][j] != 0:
                if lastX == board[i][j]:
                    possibleMerges[0] += 1
                    lastX = 0
                elif board[i][j]:
                    lastX = board[i][j]


            if board[j][i] != 0:
                if lastY == board[j][i]:
                    possibleMerges[1] += 1
                    lastY = 0
                elif board[j][i]:
                    lastY = board[j][i]

    return possibleMerges



def getHeuristic(board):
    return getEmpty(board) * 3 + boardRanking(board)

def getTiles(board):
    zeros = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                zeros += 1

    return zeros

def getEmptyTiles(board):
    empty = 0

    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                empty += 1

    return empty