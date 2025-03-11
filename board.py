# board.py
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, CELL_SIZE, WHITE, BLACK, LIGHT_GRAY, PINK, GREEN, BARRIER_COLOR
from game_state import QuoridorState

# board.py
def draw_board(screen, barriers, player1_pos, player2_pos):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, LIGHT_GRAY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

    barrier_thickness = 10
    for wall in barriers:
        row, col, orientation = wall
        if orientation == 'horizontal':
            # Draw a horizontal wall along the top edge of row 'row'
            pygame.draw.rect(screen, BARRIER_COLOR,
                             (col * CELL_SIZE,
                              row * CELL_SIZE - barrier_thickness // 2,
                              CELL_SIZE * 2,
                              barrier_thickness))
        elif orientation == 'vertical':
            # Draw a vertical wall along the left edge of column 'col'
            pygame.draw.rect(screen, BARRIER_COLOR,
                             (col * CELL_SIZE - barrier_thickness // 2,
                              row * CELL_SIZE,
                              barrier_thickness,
                              CELL_SIZE * 2))
    pygame.draw.circle(screen, PINK, (player1_pos[1] * CELL_SIZE + CELL_SIZE // 2, player1_pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    pygame.draw.circle(screen, GREEN, (player2_pos[1] * CELL_SIZE + CELL_SIZE // 2, player2_pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)


def getGridPos(mousePos):
    x, y = mousePos
    return (y // CELL_SIZE, x // CELL_SIZE)

def placeBarrierAtClick(mousePos, orientation, state):
    row, col = getGridPos(mousePos)
    
    # Check barrier count for the current player.
    if state.player_turn == 1 and state.player1_barriers <= 0:
        print("Player 1 has no barriers left!")
        return False
    elif state.player_turn == 2 and state.player2_barriers <= 0:
        print("Player 2 has no barriers left!")
        return False

    # Create a single-tuple wall representation.
    if orientation == 'horizontal' and col < GRID_SIZE - 1:
        new_wall = (row, col, 'horizontal')
    elif orientation == 'vertical' and row < GRID_SIZE - 1:
        new_wall = (row, col, 'vertical')
    else:
        # Invalid placement (e.g. out of bounds)
        return False

    # Prevent overlapping: check if any wall already occupies that cell.
    if any(b[:2] == new_wall[:2] for b in state.barriers):
        print("Invalid wall placement! Walls cannot overlap.")
        return False

    # Backup the current barriers.
    original_barriers = state.barriers.copy()

    # Add the new wall.
    state.barriers.append(new_wall)
    print(f"Wall placed at {new_wall}")

    # Check for path blockage.
    if not state.is_path_blocked():
        # Successful placement: deduct a barrier from the current player.
        if state.player_turn == 1:
            state.player1_barriers -= 1
        else:
            state.player2_barriers -= 1
        return True
    else:
        # Revert if the placement blocks a path.
        state.barriers = original_barriers
        print("Wall placement blocked! Path must remain open.")
        return False
    
def show_message(screen, message, color, position, font):
    text = font.render(message, True, color)
    screen.blit(text, position)
