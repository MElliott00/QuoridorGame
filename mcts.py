# mcts.py - Monte Carlo Tree Search
import math
import random
import copy
from game_state import QuoridorState

def heuristic(state, player):
    player_path = state.getShortestPathLength(player)
    opponent_path = state.getShortestPathLength(3 - player)
    walls_left = state.wallsRemaining(player)
    
    return (opponent_path - player_path) + 0.1 * walls_left


class MCTSNode:
    def __init__(self, state, parent=None, player=None, lastMoveTaken=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.lastMoveTaken = lastMoveTaken
        if parent is None:
            if player is None:
                raise ValueError("Root node must have a player value.")
            self.player = player  # AI player's perspective
        else:
            # The move that led to this state was made by the opponent of the current turn.
            self.player = 3 - state.player_turn

    def isFullyExpanded(self):
        return len(self.children) == len(self.state.getLegalMoves())

    def bestChild(self, explorationWeight=1.0):
        return max(self.children, key=lambda child: (child.wins / (child.visits + 1e-6)) +
                   explorationWeight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6)))

    def expand(self):
        legal_moves = self.state.getLegalMoves()
        existing_states = [child.state for child in self.children]

        unvisited_moves = []
        for move in legal_moves:
            new_state = self.state.applyMoves(move)
            if new_state not in existing_states:
                unvisited_moves.append((move, new_state))

        if not unvisited_moves:
            print("All moves already expanded. Returning random child.")
            return random.choice(self.children)  # Fallback if all moves visited

        # Pick best unvisited move based on heuristic (optional)
        best_score = -float('inf')
        best_move = None
        best_state = None
        current_player = self.state.player_turn

        for move, new_state in unvisited_moves:
            score = heuristic(new_state, current_player)
            if score > best_score:
                best_score = score
                best_move = move
                best_state = new_state

        # Add child
        child_node = MCTSNode(best_state, parent=self, lastMoveTaken=best_move)
        self.children.append(child_node)
        print(f"Expanding node with barriers: {best_state.barriers}")  # NEW barriers checked
        return child_node

    def simulate(self):
        currentState = copy.deepcopy(self.state)
        print(f"Simulating from state with barriers: {currentState.barriers}")
        while not currentState.isTerminal():
            legal_moves = currentState.getLegalMoves()
            if not legal_moves:
                break
            
            best_score = -float('inf')
            best_move = None
            current_player = currentState.player_turn

            for move in legal_moves:
                if move[0] == "move":
                    next_state = currentState.applyMoves(move)
                    score = heuristic(next_state, current_player)
                elif move[0] == "barrier":
                    next_state = currentState.applyMoves(move)
                    score = heuristic(next_state, current_player)
                if score > best_score:
                    best_score = score
                    best_move = move

            if best_move:
                currentState = currentState.applyMoves(best_move)
            else:
                break
        
        return currentState.getWinner()

    def backpropagate(self, result):
        self.visits += 1
        if self.player is not None and result == self.player:
            self.wins += 1
        if self.parent:
            self.parent.backpropagate(result)


def MCTS_Search(rootState, iterations=1, ai_player=2):
    if rootState.isTerminal():
        return rootState.player2_pos
    
    rootNode = MCTSNode(rootState, player=ai_player)
    for i in range(iterations):
        print(f"Starting iteration: {i}")
        node = rootNode
        # Selection
        while node.isFullyExpanded() and not node.state.isTerminal():
            node = node.bestChild()
        # Expansion
        if not node.state.isTerminal():
            node = node.expand()
        #simulate
        result = node.simulate()
        #backpropogate
        node.backpropagate(result)
    #chooses best move
    bestMoveNode = rootNode.bestChild(explorationWeight=0)
    return bestMoveNode.lastMoveTaken


