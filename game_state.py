# game_state.py - stores game logic and QuoridorState Class

import copy
import random
import heapq
from constants import GRID_SIZE
from collections import deque

def a_star(start, goal_row, state):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (priority, position)
    cost_so_far = {start: 0}

    while priority_queue:
        _, (row, col) = heapq.heappop(priority_queue)

        if row == goal_row:
            return cost_so_far[(row, col)]  # Return path length

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = (row + dr, col + dc)

            if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE:
                if not state.isMoveBlocked((row, col), new_pos):
                    new_cost = cost_so_far[(row, col)] + 1  # Uniform cost
                    if new_pos not in cost_so_far or new_cost < cost_so_far[new_pos]:
                        cost_so_far[new_pos] = new_cost
                        priority = new_cost + abs(goal_row - new_pos[0])  # Manhattan heuristic
                        heapq.heappush(priority_queue, (priority, new_pos))

    return float('inf')  # No valid path


class QuoridorState:
    def __init__(self, player1_pos, player2_pos, barriers, player_turn, lastMoveTaken=None):
        self.player1_pos = player1_pos
        self.player2_pos = player2_pos
        self.barriers = barriers
        self.player_turn = player_turn
        self.lastMoveTaken = lastMoveTaken
        # Initialize barriers available for each player.
        self.player1_barriers = 10
        self.player2_barriers = 10

    def __eq__(self, other):
        if not isinstance(other, QuoridorState):
            return False
        return (self.player1_pos == other.player1_pos and
                self.player2_pos == other.player2_pos and
                set(self.barriers) == set(other.barriers) and
                self.player1_barriers == other.player1_barriers and
                self.player2_barriers == other.player2_barriers and
                self.player_turn == other.player_turn)

    def __hash__(self):
        #good for set/dict use
        return hash((self.player1_pos, self.player2_pos, frozenset(self.barriers),
                     self.player1_barriers, self.player2_barriers, self.player_turn))

    def isMoveBlocked(self, start_pos, end_pos):
        r, c = start_pos
        r2, c2 = end_pos

        # Moving up: crossing from row r to r-1.
        if r2 == r - 1 and c2 == c:
            # For a horizontal wall stored as (r, col, 'horizontal'),
            # the wall sits along the edge between row r and r-1.
            return any(len(w) == 3 and w[2] == 'horizontal' and w[0] == r and (c == w[1] or c == w[1] + 1) for w in self.barriers)

        # Moving down: crossing from row r to r+1.
        elif r2 == r + 1 and c2 == c:
            return any(len(w) == 3 and w[2] == 'horizontal' and w[0] == r2 and (c == w[1] or c == w[1] + 1) for w in self.barriers)

        # Moving right: crossing from column c to c+1.
        elif r2 == r and c2 == c + 1:
            return any(len(w) == 3 and w[2] == 'vertical' and w[1] == c2 and (r == w[0] or r == w[0] + 1) for w in self.barriers)

        # Moving left: crossing from column c to c-1.
        elif r2 == r and c2 == c - 1:
            return any(len(w) == 3 and w[2] == 'vertical' and w[1] == c and (r == w[0] or r == w[0] + 1) for w in self.barriers)

        return False

    # def getShortestPathLength(self, player):
    #     def bfs(start, goal_row):
    #         from collections import deque
    #         queue = deque([start])
    #         visited = set([start])
    #         distance = 0
    #         while queue:
    #             #distance += 1
    #             for _ in range(len(queue)):
    #                 row, col = queue.popleft()
    #                 if row == goal_row:
    #                     return distance
    #                 #Explores neighbors
    #                 for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    #                     new_pos = (row + dr, col + dc)
    #                     if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE:
    #                         if not self.isMoveBlocked((row, col), new_pos):
    #                             visited.add(new_pos)
    #                             queue.append(new_pos)
                                
    #             distance += 1
    #         return float('inf')

    #     if player == 1:
    #         return bfs(self.player1_pos, 0)
    #     else:
    #         return bfs(self.player2_pos, GRID_SIZE - 1)

    def getShortestPathLength(self, player):
        return a_star(self.player1_pos, 0, self) if player == 1 else a_star(self.player2_pos, GRID_SIZE - 1, self)


    def wallsRemaining(self, player):
        return self.player1_barriers if player == 1 else self.player2_barriers


    def getLegalMoves(self):
        print(f"Checking legal moves. Current barriers: {self.barriers}")
        legal_moves = []
        row, col = self.player1_pos if self.player_turn == 1 else self.player2_pos
        for move_dir, (dr, dc) in [('up', (-1, 0)), ('down', (1, 0)),
                               ('left', (0, -1)), ('right', (0, 1))]:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                if not self.isMoveBlocked((row, col), (new_row, new_col)):
                    legal_moves.append(("move", (row, col), (new_row, new_col))) 

        # Add barrier placements if barriers are remaining
        if self.wallsRemaining(self.player_turn) > 0:
            for r in range(GRID_SIZE - 1):  # Barriers are placed between cells, so limit by GRID_SIZE-1
                for c in range(GRID_SIZE - 1):
                    for orientation in ['horizontal', 'vertical']:
                        if self.isBarrierPlacementValid((r, c), orientation):
                            # Temporarily add the barrier to test if paths remain unblocked
                            temp_barriers = self.barriers + [((r, c), orientation)]
                            temp_state = copy.deepcopy(self)
                            temp_state.barriers = temp_barriers
                            if not temp_state.is_path_blocked():
                                legal_moves.append(("barrier", (r, c), orientation))

        return legal_moves

    def isBarrierPlacementValid(self, pos, orientation):
        for barrier in self.barriers:
            if barrier == (pos, orientation):
                return False
        return True

    def is_path_blocked(self):
        print(f"Checking path blockage with barriers: {self.barriers}")
        return a_star(self.player1_pos, 0, self) == float('inf') or a_star(self.player2_pos, GRID_SIZE - 1, self) == float('inf')

    # def is_path_blocked(self):
    #     print(f"Checking path blockage with barriers: {self.barriers}")
    #     def bfs(start, goal_row):
    #         from collections import deque
    #         queue = deque([start])
    #         visited = set()
    #         while queue:
    #             row, col = queue.popleft()
    #             if row == goal_row:
    #                 return False
    #             if (row, col) in visited:
    #                 continue
    #             visited.add((row, col))
    #             for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
    #                 new_pos = (row + dr, col + dc)
    #                 if 0 <= new_pos[0] < GRID_SIZE and 0 <= new_pos[1] < GRID_SIZE:
    #                     if not self.isMoveBlocked((row, col), new_pos):
    #                         queue.append(new_pos)
    #         return True

    #     return bfs(self.player1_pos, 0) or bfs(self.player2_pos, GRID_SIZE - 1)
    
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
        new_state = copy.deepcopy(self)
        if move[0] == "move":
            _, from_pos, to_pos = move
            if self.player_turn == 1:
                new_state.player1_pos = to_pos
            else:
                new_state.player2_pos = to_pos
        elif move[0] == "barrier":
            _, (row, col), orientation = move
            new_state.barriers.append((row, col, orientation))
            # Decrement barrier count
            if self.player_turn == 1:
                new_state.player1_barriers -= 1
            else:
                new_state.player2_barriers -= 1

        # Switch turns
        new_state.player_turn = 3 - self.player_turn
        # Store last move
        new_state.lastMoveTaken = move
        return new_state

    def isTerminal(self):
        return self.player1_pos[0] == 0 or self.player2_pos[0] == GRID_SIZE - 1

    def getWinner(self):
        if self.player1_pos[0] == 0:
            return 1
        elif self.player2_pos[0] == GRID_SIZE - 1:
            return 2
        return None
