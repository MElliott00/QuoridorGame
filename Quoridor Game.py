import pygame
import sys
import math
import random
import copy

pygame.init()

# Constants for game
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BARRIER_COLOR = (0, 0, 0)

# Initialize game Board
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quoridor Game")

class QuoridorState:
    def __init__(self, player1_pos, player2_pos, barriers, player_turn):
        self.player1_pos = player1_pos
        self.player2_pos = player2_pos
        self.barriers = barriers
        self.player_turn = player_turn
    
    # Returns the legal moves for the current player
    def getLegalMoves(self):
        legal_moves = []
        row, col = self.player1_pos if self.player_turn == 1 else self.player2_pos

        for move_dir, (dr, dc) in [('up', (-1, 0)), ('down', (1, 0)), ('left', (0, -1)), ('right', (0, 1))]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                if not self.isMoveBlocked((row, col), (new_row, new_col)):
                    legal_moves.append((new_row, new_col, move_dir))
        return legal_moves

    def isMoveBlocked(self, start_pos, end_pos):
        startRow, startCol = start_pos
        endRow, endCol = end_pos
        for barrier in self.barriers:
            barrierRow, barrierCol, orientation = barrier
            if orientation == 'horizontal':
                if startRow == endRow and (startCol >= barrierCol and startCol <= barrierCol + 1) and (endCol >= barrierCol + 1):
                    return True
            elif orientation == 'vertical':
                if startCol == endCol and (startRow >= barrierRow and startRow <= barrierRow + 1) and (endRow >= barrierRow and endRow <= barrierRow + 1):
                    return True 
        return False

    def move_player(self, direction):
        current_pos = self.player1_pos if self.player_turn == 1 else self.player2_pos
        row, col = current_pos
        new_row, new_col = row, col

        if direction == 'up' and row > 0:
            new_row -= 1
        elif direction == 'down' and row < 8:
            new_row += 1
        elif direction == 'left' and col > 0:
            new_col -= 1
        elif direction == 'right' and col < 8:
            new_col += 1
    
        if not self.isMoveBlocked((row, col), (new_row, new_col)):
            if self.player_turn == 1:
                self.player1_pos = (new_row, new_col)
            else:
                self.player2_pos = (new_row, new_col)
            self.player_turn = 3 - self.player_turn  # Switch turn

    # Returns a new game state after applying the move
    def applyMoves(self, move):
        new_state = QuoridorState(self.player1_pos, self.player2_pos, list(self.barriers), self.player_turn)
        if new_state.player_turn == 1:
            new_state.player1_pos = move
        else:
            new_state.player2_pos = move
        new_state.player_turn = 3 - new_state.player_turn  # Switch turn
        return new_state

    def isTerminal(self):
        # Checks if player has won
        return self.player1_pos[0] == 0 or self.player2_pos[0] == 8

    def getWinner(self):
        # Returns the winning player
        if self.player1_pos[0] == 0:
            return 1
        elif self.player2_pos[0] == 8:
            return 2
        return None

# Monte Carlo Tree Search
class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def isFullyExpanded(self):
        # Checks if all legal moves have been expanded
        return len(self.children) == len(self.state.getLegalMoves())

    def bestChild(self, explorationWeight=1.0):
        # Selects the best child using UCB1 formula (Exploitation + Exploration)
        return max(self.children, key=lambda child: (child.wins / (child.visits + 1e-6)) +
                   explorationWeight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6)))

    def expand(self):
        # Expands the current node by applying all legal moves to create child nodes
        availableMoves = self.state.getLegalMoves()
        for move in availableMoves:
            newState = self.state.applyMoves(move[:2])  # Apply move to create new state
            childNode = MCTSNode(newState, parent=self)
            self.children.append(childNode)

    def simulate(self):
        # Simulates a random game from the current state until a terminal state is reached
        currentState = copy.deepcopy(self.state)  # Deep copy to avoid modifying the original state
        while not currentState.isTerminal():
            move = random.choice(currentState.getLegalMoves())  # Random move selection
            currentState = currentState.applyMoves(move[:2])
        return currentState.getWinner()  # Return the winner of the simulation

    def backpropagate(self, result):
        # Backpropagates the result up the tree, updating the visit and win counts
        self.visits += 1
        if result == self.state.player_turn:
            self.wins += 1  # Increment win count if current node's player wins
        if self.parent:
            self.parent.backpropagate(result)  # Propagate the result to the parent node

def MCTS_Search(rootState, iterations=500):
    if rootState.isTerminal():
        return rootState.player2_pos
    rootNode = MCTSNode(rootState)

    for _ in range(iterations):
        node = rootNode

        # Selection: Traverse the tree to select a leaf node for expansion
        while not node.isFullyExpanded() and node.children:  # Traverse until we find an unexpanded child
            node = node.bestChild()  # Select the best child using the UCB formula

        # Expansion: Expand the node by adding all legal moves if the state is not terminal
        if not node.state.isTerminal():
            node.expand()  # Expand and add children nodes based on legal moves

        # Simulation: Simulate a random game from the current node until terminal state
        result = node.simulate()  # Run simulation and get the result (winner)

        # Backpropagation: Propagate the result back up the tree to update visit/win counts
        node.backpropagate(result)

    # After all iterations, select the best move (best child node without exploration weight)
    bestMove = rootNode.bestChild(explorationWeight=0)  # Choose the child with the highest win ratio
    return bestMove.state.player2_pos  # Assuming the bestMove corresponds to the state after player 2's move

# Player positions
player1_pos = (8, 4)  # Player 1 bottom
player2_pos = (0, 4)  # Player 2 top

# Barrier placement
barriers = []

def draw_board():
    # Draw grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, LIGHT_GRAY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

    # Draw barriers as thick lines along the grid lines
    barrier_thickness = 10  # Set the thickness for the barriers
    for barrier in barriers:
        if barrier[2] == 'horizontal':
            # Draw a horizontal barrier across two tiles, extending above and below the line
            pygame.draw.rect(screen, BARRIER_COLOR, (barrier[1] * CELL_SIZE, barrier[0] * CELL_SIZE - barrier_thickness // 2, CELL_SIZE * 2, barrier_thickness))
        elif barrier[2] == 'vertical':
            # Draw a vertical barrier across two tiles, extending left and right of the line
            pygame.draw.rect(screen, BARRIER_COLOR, (barrier[1] * CELL_SIZE - barrier_thickness // 2, barrier[0] * CELL_SIZE, barrier_thickness, CELL_SIZE * 2))

    # Draw players' positions
    pygame.draw.circle(screen, BLUE, (player1_pos[1] * CELL_SIZE + CELL_SIZE // 2, player1_pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    pygame.draw.circle(screen, RED, (player2_pos[1] * CELL_SIZE + CELL_SIZE // 2, player2_pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

def getGridPos(mousePos):
    x, y = mousePos
    return (y // CELL_SIZE, x // CELL_SIZE)

def placeBarrierAtClick(mousePos, orientation):
    row, col = getGridPos(mousePos)
    # Place barriers only on grid lines
    if orientation == 'horizontal' and 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE - 1:
        if not any((barrier[0] == row and barrier[1] == col and barrier[2] == 'horizontal') for barrier in barriers):
            barriers.append((row, col, 'horizontal'))
    elif orientation == 'vertical' and 0 <= row < GRID_SIZE - 1 and 0 <= col < GRID_SIZE:
        if not any((barrier[0] == row and barrier[1] == col and barrier[2] == 'vertical') for barrier in barriers):
            barriers.append((row, col, 'vertical'))

# AI Move Feedback: Simple message to show it's the AI's turn
font = pygame.font.SysFont(None, 40)
def show_message(message, color, position):
    text = font.render(message, True, color)
    screen.blit(text, position)

def main():
    global player1_pos, player2_pos, barriers
    clock = pygame.time.Clock()
    game_running = True
    aiTurn = False
    barrierOrientation = 'horizontal'

    currentState = QuoridorState(player1_pos, player2_pos, barriers, player_turn=1)

    while game_running:
        screen.fill(WHITE)
        draw_board()

        if aiTurn:
            show_message("AI is thinking...", (255, 0, 0), (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            # Barrier placement
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click to place barriers
                    placeBarrierAtClick(event.pos, barrierOrientation)

            elif event.type == pygame.KEYDOWN and not aiTurn:
                # Player 1 Controls (Movement)
                if event.key in {pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT}:
                    direction = {pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}[event.key]
                    currentState.move_player(direction)
                    aiTurn = True

                # Player 1 barrier placement (Switching orientation)
                elif event.key == pygame.K_q:
                    barrierOrientation = 'horizontal'
                elif event.key == pygame.K_e:
                    barrierOrientation = 'vertical'

        # AI turn logic
        if aiTurn:
            bestMove = MCTS_Search(currentState, iterations=500)
            currentState = currentState.applyMoves(bestMove)  # Apply AI's best move
            player2_pos = currentState.player2_pos  # Update player2_pos
            player1_pos = currentState.player1_pos  # Update player1_pos
            currentState.player_turn = 1  # Switch turn back to Player 1 after AI's move
            aiTurn = False

            # Check if the game is won after the AI's move
            if currentState.isTerminal():
                winner = currentState.getWinner()
                show_message(f"Player {winner} wins!", (0, 255, 0), (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
                pygame.display.flip()
                pygame.time.wait(2000)  # Display winner for 2 seconds
                game_running = False  # End game after a winner is determined

        pygame.display.flip()
        clock.tick(30)  # Control the frame rate to make the game smoother

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

