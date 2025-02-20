import pygame
import sys

pygame.init()

#Constants for game
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

#Initialize game Board
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quoridor Game")

#Player postitions
player1_pos = (8,4) #Player 1 bottom
player2_pos = (0,4) #Player 2 top

#barrier plaacement
barriers = []

def draw_board():
    #draw grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pygame.draw.rect(screen, LIGHT_GRAY, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
            pygame.draw.rect(screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
    
    # Draw barriers
    for barrier in barriers:
        if barrier[2] == 'horizontal':
            pygame.draw.rect(screen, BARRIER_COLOR, (barrier[1] * CELL_SIZE, barrier[0] * CELL_SIZE, CELL_SIZE * 2, CELL_SIZE))
        elif barrier[2] == 'vertical':
            pygame.draw.rect(screen, BARRIER_COLOR, (barrier[1] * CELL_SIZE, barrier[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE * 2))

    # Draw players' positions
    pygame.draw.circle(screen, BLUE, (player1_pos[1] * CELL_SIZE + CELL_SIZE // 2, player1_pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    pygame.draw.circle(screen, RED, (player2_pos[1] * CELL_SIZE + CELL_SIZE // 2, player2_pos[0] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)

def move_player(player, direction):
    global player1_pos, player2_pos
    if player == 1: 
        current_postition = player1_pos
    else:
        current_postition = player2_pos

    row, col = current_postition
    new_row, new_col = row, col

    if direction == 'up' and row > 0:
        new_row -=1
    elif direction == 'down' and row < 8:
        new_row += 1
    elif direction == 'left' and col > 0:
        new_col -= 1
    elif direction == 'right' and col < 8:
        new_col += 1
    
    if (new_row, new_col) != player1_pos and (new_row, new_col) != player2_pos:
        if player == 1:
            player1_pos = (new_row, new_col)
        else:
            player2_pos = (new_row, new_col)

def place_barrier(player, position, orientation):
    barriers.append((position[0], position[1], orientation))

def main():
    global player1_pos, player2_pos, barriers
    clock = pygame.time.Clock()
    game_running = True

    while game_running:
        screen.fill(WHITE)
        draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                #player 1 Controls
                if event.key == pygame.K_UP:
                    move_player(1, 'up')
                elif event.key == pygame.K_DOWN:
                    move_player(1, 'down')
                elif event.key == pygame.K_LEFT:
                    move_player(1, 'left')
                elif event.key == pygame.K_RIGHT:
                    move_player(1, 'right')
                
                #Player 2 controls
                elif event.key == pygame.K_w:
                    move_player(2, 'up')
                elif event.key == pygame.K_s:
                    move_player(2, 'down')
                elif event.key == pygame.K_a:
                    move_player(2, 'left')
                elif event.key == pygame.K_d:
                    move_player(2, 'right')
                
                #Barrier placement P1 (Q and E)
                elif event.key == pygame.K_q:
                    place_barrier(1, (player1_pos[0], player1_pos[1]), 'horizontal')
                elif event.key == pygame.K_e:
                    place_barrier(1, (player1_pos[0], player1_pos[1]), 'vertical')

                #Barrier placement P2 (Z and X
                elif event.key == pygame.K_z:
                    place_barrier(2, (player2_pos[0], player2_pos[1]), 'horizontal')
                elif event.key == pygame.K_x:
                    place_barrier(2, (player2_pos[0], player2_pos[1]), 'vertical')
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
                
