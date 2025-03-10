import math
import random
import copy
from game_state import QuoridorState
from collections import deque

# Utility function: Find the shortest path to the goal using BFS
def shortest_path_length(state, start, goal_row):
    """Returns the shortest path length from 'start' to the goal row using BFS."""
    queue = deque([(start, 0)])  # (position, steps)
    visited = set()

    while queue:
        (row, col), steps = queue.popleft()

        if row == goal_row:
            return steps

        if (row, col) in visited:
            continue
        visited.add((row, col))

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = (row + dr, col + dc)
            if 0 <= new_pos[0] < 9 and 0 <= new_pos[1] < 9 and not state.isMoveBlocked((row, col), new_pos):
                queue.append((new_pos, steps + 1))

    return float('inf')  # No valid path found (shouldn't happen in valid games)

# Heuristic function
def heuristic_evaluation(state):
    """Evaluates the state based on shortest path calculations and strategic positioning."""
    player1_path = shortest_path_length(state, state.player1_pos, 0)
    player2_path = shortest_path_length(state, state.player2_pos, 8)

    # Barrier consideration
    barrier_advantage = state.player2_barriers - state.player1_barriers  # AI should manage barriers well

    # Higher score = better for AI
    return (player1_path - player2_path) * 10 + barrier_advantage * 3

# Minimax with α-β pruning and heuristic evaluation
def minimax(state, depth, alpha, beta, maximizingPlayer):
    """Minimax with Alpha-Beta Pruning and improved strategic evaluation."""
    if depth == 0 or state.isTerminal():
        return heuristic_evaluation(state), None

    legal_moves = state.getLegalMoves()
    if maximizingPlayer:
        max_eval = -math.inf
        best_move = None
        for move in legal_moves:
            new_state = state.applyMoves(move[:2])
            eval_score, _ = minimax(new_state, depth - 1, alpha, beta, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move[:2]
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break  # Alpha-beta pruning
        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = None
        for move in legal_moves:
            new_state = state.applyMoves(move[:2])
            eval_score, _ = minimax(new_state, depth - 1, alpha, beta, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move[:2]
            beta = min(beta, eval_score)
            if beta <= alpha:
                break  # Alpha-beta pruning
        return min_eval, best_move

# AI Move Decision
def best_ai_move(state):
    """Determines the AI move using Minimax."""
    depth = 3  # Adjust for performance
    _, move = minimax(state, depth, -math.inf, math.inf, True)
    return move
