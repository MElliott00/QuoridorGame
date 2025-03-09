# game_state.py - stores game logic and QuoridorState Class

import copy
import random
from constants import GRID_SIZE
from collections import deque

class QuoridorState:
    def __init__(self, player1_pos, player2_pos, barriers=None, player_turn=1):
        self.player1_pos = player1_pos
        self.player2_pos = player2_pos
        self.barriers = barriers
        self.player_turn = player_turn
        # Initialize barriers available for each player.
        self.player1_barriers = 10
        self.player2_barriers = 10

    def isMoveBlocked(self, start_pos, end_pos):
        r, c = start_pos
        r2, c2 = end_pos

        # Moving up: crossing from row r to r-1.
        if r2 == r - 1 and c2 == c:
            # For a horizontal wall stored as (r, col, 'horizontal'),
            # the wall sits along the edge between row r and r-1.
            return any(w[2] == 'horizontal' and w[0] == r and (c == w[1] or c == w[1] + 1) for w in self.barriers)

        # Moving down: crossing from row r to r+1.
        elif r2 == r + 1 and c2 == c:
            return any(w[2] == 'horizontal' and w[0] == r2 and (c == w[1] or c == w[1] + 1) for w in self.barriers)

        # Moving right: crossing from column c to c+1.
        elif r2 == r and c2 == c + 1:
            return any(w[2] == 'vertical' and w[1] == c2 and (r == w[0] or r == w[0] + 1) for w in self.barriers)

        # Moving left: crossing from column c to c-1.
        elif r2 == r and c2 == c - 1:
            return any(w[2] == 'vertical' and w[1] == c and (r == w[0] or r == w[0] + 1) for w in self.barriers)

        return False



    
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

    def is_path_blocked(self):
        def bfs(start, goal_row):
            from collections import deque
            queue = deque([start])
            visited = set()
            while queue:
                row, col = queue.popleft()
                if row == goal_row:
                    return False
                if (row, col) in visited:
                    continue
                visited.add((row, col))
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    new_pos = (row + dr, col + dc)
                    if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE:
                        if not self.isMoveBlocked((row, col), new_pos):
                            queue.append(new_pos)
            return True

        return bfs(self.player1_pos, 0) or bfs(self.player2_pos, GRID_SIZE - 1)
    
    def move_player(self, direction):
        row, col = self.player1_pos if self.player_turn == 1 else self.player2_pos
        new_row, new_col = row, col

        if direction == 'up' and row > 0:
            new_row -= 1
        elif direction == 'down' and row < GRID_SIZE - 1:
            new_row += 1
        elif direction == 'left' and col > 0:
            new_col -= 1
        elif direction == 'right' and col < GRID_SIZE - 1:
            new_col += 1

        if self.isMoveBlocked((row, col), (new_row, new_col)):
            print(f"Move blocked! Player {self.player_turn} cannot move {direction}")
            return

        if self.player_turn == 1:
            self.player1_pos = (new_row, new_col)
        else:
            self.player2_pos = (new_row, new_col)

        print(f"Player {self.player_turn} moved {direction} to ({new_row}, {new_col})")
        print(f"Current Barriers: {self.barriers}")

        # Switch turns after a valid move.
        self.player_turn = 3 - self.player_turn

    def applyMoves(self, move):
        new_state = QuoridorState(
            player1_pos=self.player1_pos,
            player2_pos=self.player2_pos,
            barriers=copy.deepcopy(self.barriers),
            player_turn=3 - self.player_turn
        )

        if self.player_turn == 1:
            new_state.player1_pos = move
        else:
            new_state.player2_pos = move

        new_state.player1_barriers = self.player1_barriers
        new_state.player2_barriers = self.player2_barriers

        return new_state


    def isTerminal(self):
        return self.player1_pos[0] == 0 or self.player2_pos[0] == GRID_SIZE - 1

    def getWinner(self):
        if self.player1_pos[0] == 0:
            return 1
        elif self.player2_pos[0] == GRID_SIZE - 1:
            return 2
        return None
