# mcts.py - Monte Carlo Tree Search

import math
import random
import copy
from game_state import QuoridorState

class MCTSNode:
    def __init__(self, state, parent=None, player=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.player = player if parent is None else 3 - state.player_turn

    def isFullyExpanded(self):
        return len(self.children) == len(self.state.getLegalMoves())

    def bestChild(self, explorationWeight=1.0):
        return max(self.children, key=lambda child: (child.wins / (child.visits + 1e-6)) +
                   explorationWeight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6)))

    def expand(self):
        legal_moves = self.state.getLegalMoves()
        for move in legal_moves:
            new_state = self.state.applyMoves(move[:2])
            if not any(child.state == new_state for child in self.children):
                childNode = MCTSNode(new_state, parent=self)
                self.children.append(childNode)
                return childNode
        return random.choice(self.children)

    def simulate(self):
        currentState = copy.deepcopy(self.state)
        while not currentState.isTerminal():
            moves = currentState.getLegalMoves()
            if not moves:
                break
            move = random.choice(moves)
            currentState = currentState.applyMoves(move[:2])
        return currentState.getWinner()

    def backpropagate(self, result):
        self.visits += 1
        if self.player is not None and result == self.player:
            self.wins += 1
        if self.parent:
            self.parent.backpropagate(result)

def MCTS_Search(rootState, iterations=500, ai_player=2):
    """Monte Carlo Tree Search algorithm for AI decision-making."""
    
    if rootState.isTerminal():
        return rootState.player2_pos  # ✅ Ensure it returns a valid position
    
    rootNode = MCTSNode(rootState, player=ai_player)
    
    for _ in range(iterations):
        node = rootNode
        while node.isFullyExpanded() and not node.state.isTerminal():
            node = node.bestChild()

        if not node.state.isTerminal():
            node = node.expand()

        result = node.simulate()
        node.backpropagate(result)

    bestMoveNode = rootNode.bestChild(explorationWeight=0)

    # ✅ Ensure AI move is a valid (row, col) tuple
    if not isinstance(bestMoveNode.state.player2_pos, tuple) or len(bestMoveNode.state.player2_pos) != 2:
        raise ValueError(f"Invalid AI move: {bestMoveNode.state.player2_pos}")

    return bestMoveNode.state.player2_pos
