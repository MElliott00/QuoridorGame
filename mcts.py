# mcts.py monte carlo tree search

import math
import random
import copy
from game_state import QuoridorState

class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def isFullyExpanded(self):
        return len(self.children) == len(self.state.getLegalMoves())

    def bestChild(self, explorationWeight=1.0):
        return max(self.children, key=lambda child: (child.wins / (child.visits + 1e-6)) +
                   explorationWeight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6)))

    def expand(self):
        availableMoves = self.state.getLegalMoves()
        for move in availableMoves:
            newState = self.state.applyMoves(move[:2])
            childNode = MCTSNode(newState, parent=self)
            self.children.append(childNode)

    def simulate(self):
        currentState = copy.deepcopy(self.state)
        while not currentState.isTerminal():
            move = random.choice(currentState.getLegalMoves())
            currentState = currentState.applyMoves(move[:2])
        return currentState.getWinner()

    def backpropagate(self, result):
        self.visits += 1
        if result == self.state.player_turn:
            self.wins += 1
        if self.parent:
            self.parent.backpropagate(result)

def MCTS_Search(rootState, iterations=500):
    if rootState.isTerminal():
        return rootState.player2_pos
    rootNode = MCTSNode(rootState)
    for _ in range(iterations):
        node = rootNode
        while not node.isFullyExpanded() and node.children:
            node = node.bestChild()
        if not node.state.isTerminal():
            node.expand()
        result = node.simulate()
        node.backpropagate(result)
    bestMove = rootNode.bestChild(explorationWeight=0)
    return bestMove.state.player2_pos
