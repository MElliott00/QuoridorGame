# board.py
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, CELL_SIZE, TEXT_COLOR, BOARD_COLOR, GRID_COLOR, PLAYER1_COLOR, PLAYER2_COLOR, BARRIER_COLOR
from game_state import QuoridorState

def draw_board(screen, barriers, player1_pos, player2_pos, player1_barriers, player2_barriers, font):
    # Clear screen
    screen.fill(BOARD_COLOR)

    # Draw UI bar (above the board)
    ui_bar_height = 50
    pygame.draw.rect(screen, GRID_COLOR, (0, 0, SCREEN_WIDTH, ui_bar_height))

    # Draw text inside UI bar
    p1_text = font.render(f"P1 Barriers: {player1_barriers}", True, TEXT_COLOR)
    p2_text = font.render(f"P2 Barriers: {player2_barriers}", True, TEXT_COLOR)

    screen.blit(p1_text, (20, 15))  # Left side
    screen.blit(p2_text, (SCREEN_WIDTH - 200, 15))  # Right side

    # Draw the grid starting below the UI bar
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, BOARD_COLOR,
                             (col * CELL_SIZE, row * CELL_SIZE + ui_bar_height, CELL_SIZE, CELL_SIZE), 1)
            pygame.draw.rect(screen, GRID_COLOR,
                             (col * CELL_SIZE, row * CELL_SIZE + ui_bar_height, CELL_SIZE, CELL_SIZE), 2)

    # Draw barriers
    barrier_thickness = 10
    for wall in barriers:
        row, col, orientation = wall
        if orientation == 'horizontal':
            pygame.draw.rect(screen, BARRIER_COLOR,
                             (col * CELL_SIZE,
                              row * CELL_SIZE + ui_bar_height - barrier_thickness // 2,
                              CELL_SIZE * 2,
                              barrier_thickness))
        elif orientation == 'vertical':
            pygame.draw.rect(screen, BARRIER_COLOR,
                             (col * CELL_SIZE - barrier_thickness // 2,
                              row * CELL_SIZE + ui_bar_height,
                              barrier_thickness,
                              CELL_SIZE * 2))

    # Draw players
    pygame.draw.circle(screen, PLAYER1_COLOR, (player1_pos[1] * CELL_SIZE + CELL_SIZE // 2,
                                      player1_pos[0] * CELL_SIZE + CELL_SIZE // 2 + ui_bar_height),
                       CELL_SIZE // 3)
    pygame.draw.circle(screen, PLAYER2_COLOR, (player2_pos[1] * CELL_SIZE + CELL_SIZE // 2,
                                       player2_pos[0] * CELL_SIZE + CELL_SIZE // 2 + ui_bar_height),
                       CELL_SIZE // 3)

def getGridPos(mousePos):
    x, y = mousePos
    if y < 50:  # Clicked in the status bar area
        return None
    return ( (y - 50) // CELL_SIZE, x // CELL_SIZE )  # Adjust for the bar height

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
    
def barriers_remainig(screen, font, player1_barriers, player2_barriers):
    
    p1_text_pos = (20, 20) #player 1
    p2_text_pos = (20, SCREEN_HEIGHT - 40) #player 2

    p1_text = font.render(f"Player 1 Barriers: {player1_barriers}", True, (255, 255, 255))
    p2_text = font.render(f"Player 2 Barriers: {player2_barriers}", True, (255, 255, 255))

    screen.blit(p1_text, p1_text_pos)
    screen.blit(p2_text, p2_text_pos)

def show_message(screen, message, color, position, font):
    text = font.render(message, True, color)
    screen.blit(text, position)