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
        existingMove = {child.state.player1_pos if self.state.player_turn == 1 else child.state.player2_pos for child in self.children}
        
        for move in availableMoves:
            newPos = move[:2]
            if newPos not in existingMove:
                newState = self.state.applyMoves(move[:2])
                childNode = MCTSNode(newState, parent=self)
                self.children.append(childNode)
                return

    def simulate(self):
        currentState = copy.deepcopy(self.state)
        while not currentState.isTerminal():
            legalMoves = currentState.getLegalMoves()
            if not legalMoves:
                break  # Avoids infinite loop

            if currentState.player_turn == 1:
                legalMoves.sort(key=lambda move: move[0]) #lower row is better
            else:
                legalMoves.sort(key=lambda move: -move[0]) #higher row is better
            
            move = random.choice(legalMoves[:3]) #pick from the best 3 moves)
            currentState = currentState.applyMoves(move[:2])
        return currentState.getWinner()  # Ensure getWinner returns the correct result

    def backpropagate(self, result):
        self.visits += 1
        if result == self.state.player_turn:  # Ensure player_turn is correctly defined
            self.wins += 1
        if self.parent:
            self.parent.backpropagate(result)

def MCTS_Search(rootState, iterations=500):
    if rootState.isTerminal():
        return rootState.player2_pos  # Ensure player2_pos is correctly defined
    
    rootNode = MCTSNode(rootState)

    for _ in range(iterations):
        node = rootNode

        # Selection
        while node.children:
            node = node.bestChild()
            if not node.isFullyExpanded():
                break

        # Expansion
        if not node.state.isTerminal():
            node.expand()

        # Simulation
        result = node.simulate()
        
        # Backpropagation
        node.backpropagate(result)

    # Choose best move
    bestMove = rootNode.bestChild(explorationWeight=0)
    return bestMove.state.player2_pos  # Ensure player2_pos is correctly defined
