# board.py

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE, CELL_SIZE, WHITE, BLACK, LIGHT_GRAY, BLUE, RED, BARRIER_COLOR

def draw_board(screen, barriers, player1_pos, player2_pos):
    # Draw grid cells
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, LIGHT_GRAY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
    
    # Draw barriers (using thick lines)
    barrier_thickness = 10
    for barrier in barriers:
        if barrier[2] == 'horizontal':
            pygame.draw.rect(screen, BARRIER_COLOR,
                             (barrier[1] * CELL_SIZE,
                              barrier[0] * CELL_SIZE - barrier_thickness // 2,
                              CELL_SIZE * 2,
                              barrier_thickness))
        elif barrier[2] == 'vertical':
            pygame.draw.rect(screen, BARRIER_COLOR,
                             (barrier[1] * CELL_SIZE - barrier_thickness // 2,
                              barrier[0] * CELL_SIZE,
                              barrier_thickness,
                              CELL_SIZE * 2))
    
    # Draw players
    pygame.draw.circle(screen, PINK,
                       (player1_pos[1] * CELL_SIZE + CELL_SIZE // 2,
                        player1_pos[0] * CELL_SIZE + CELL_SIZE // 2),
                       CELL_SIZE // 3)
    pygame.draw.circle(screen, GREEN,
                       (player2_pos[1] * CELL_SIZE + CELL_SIZE // 2,
                        player2_pos[0] * CELL_SIZE + CELL_SIZE // 2),
                       CELL_SIZE // 3)

def getGridPos(mousePos):
    x, y = mousePos
    return (y // CELL_SIZE, x // CELL_SIZE)

def placeBarrierAtClick(mousePos, orientation, barriers):
    row, col = getGridPos(mousePos)
    if orientation == 'horizontal' and 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE - 1:
        if not any((barrier[0] == row and barrier[1] == col and barrier[2] == 'horizontal') for barrier in barriers):
            barriers.append((row, col, 'horizontal'))
    elif orientation == 'vertical' and 0 <= row < GRID_SIZE - 1 and 0 <= col < GRID_SIZE:
        if not any((barrier[0] == row and barrier[1] == col and barrier[2] == 'vertical') for barrier in barriers):
            barriers.append((row, col, 'vertical'))

def show_message(screen, message, color, position, font):
    text = font.render(message, True, color)
    screen.blit(text, position)
