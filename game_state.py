# game_state.py - stores game logic and QuoridorState Class

import copy
import random
from constants import GRID_SIZE

class QuoridorState:
    def __init__(self, player1_pos, player2_pos, barriers, player_turn):
        self.player1_pos = player1_pos
        self.player2_pos = player2_pos
        self.barriers = barriers
        self.player_turn = player_turn
    
    def getLegalMoves(self):
        legal_moves = []
        row, col = self.player1_pos if self.player_turn == 1 else self.player2_pos
        for move_dir, (dr, dc) in [('up', (-1, 0)), ('down', (1, 0)),
                                   ('left', (0, -1)), ('right', (0, 1))]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                if not self.isMoveBlocked((row, col), (new_row, new_col)):
                    legal_moves.append((new_row, new_col, move_dir))
        return legal_moves

    def isMoveBlocked(self, start_pos, end_pos):
        startRow, startCol = start_pos
        endRow, endCol = end_pos

        # Check vertical movement (up or down)
        if startCol == endCol:
            # Moving down: check if there's a horizontal barrier right below the start cell.
            if endRow == startRow + 1:
                for barrier in self.barriers:
                    if barrier[2] == 'horizontal':
                        # A horizontal barrier placed at (row, col) blocks moving from row-1 to row.
                        # Here, if the barrier's row equals endRow and covers the pawn's column, block it.
                        if barrier[0] == endRow and barrier[1] <= startCol < barrier[1] + 2:
                            return True
            # Moving up: check if there's a horizontal barrier right above the start cell.
            elif endRow == startRow - 1:
                for barrier in self.barriers:
                    if barrier[2] == 'horizontal':
                        if barrier[0] == startRow and barrier[1] <= startCol < barrier[1] + 2:
                            return True

        # Check horizontal movement (left or right)
        if startRow == endRow:
            # Moving right: check if there's a vertical barrier immediately to the right.
            if endCol == startCol + 1:
                for barrier in self.barriers:
                    if barrier[2] == 'vertical':
                        if barrier[1] == endCol and barrier[0] <= startRow < barrier[0] + 2:
                            return True
            # Moving left: check if there's a vertical barrier immediately to the left.
            elif endCol == startCol - 1:
                for barrier in self.barriers:
                    if barrier[2] == 'vertical':
                        if barrier[1] == startCol and barrier[0] <= startRow < barrier[0] + 2:
                            return True

        return False


    def move_player(self, direction):
        current_pos = self.player1_pos if self.player_turn == 1 else self.player2_pos
        row, col = current_pos
        new_row, new_col = row, col

        if direction == 'up' and row > 0:
            new_row -= 1
        elif direction == 'down' and row < GRID_SIZE - 1:
            new_row += 1
        elif direction == 'left' and col > 0:
            new_col -= 1
        elif direction == 'right' and col < GRID_SIZE - 1:
            new_col += 1

        if not self.isMoveBlocked((row, col), (new_row, new_col)):
            if self.player_turn == 1:
                self.player1_pos = (new_row, new_col)
            else:
                self.player2_pos = (new_row, new_col)
            self.player_turn = 3 - self.player_turn

    def applyMoves(self, move):
    # Use the same barrier list (do not copy)
        new_state = QuoridorState(self.player1_pos, self.player2_pos, self.barriers, self.player_turn)
        if new_state.player_turn == 1:
            new_state.player1_pos = move
        else:
            new_state.player2_pos = move
        new_state.player_turn = 3 - new_state.player_turn
        return new_state


    def isTerminal(self):
        # Game ends if Player 1 reaches the top row or Player 2 reaches the bottom row.
        return self.player1_pos[0] == 0 or self.player2_pos[0] == GRID_SIZE - 1

    def getWinner(self):
        if self.player1_pos[0] == 0:
            return 1
        elif self.player2_pos[0] == GRID_SIZE - 1:
            return 2
        return None
