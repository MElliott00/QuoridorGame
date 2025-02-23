# main.py

import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, CELL_SIZE, GRID_SIZE
from board import draw_board, placeBarrierAtClick, show_message
from game_state import QuoridorState
from mcts import MCTS_Search

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quoridor Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Initial positions and state
player1_pos = (8, 4)
player2_pos = (0, 4)
barriers = []
currentState = QuoridorState(player1_pos, player2_pos, barriers, player_turn=1)

def main():
    global player1_pos, player2_pos, barriers, currentState
    game_running = True
    aiTurn = False
    barrierOrientation = 'horizontal'

    while game_running:
        screen.fill(WHITE)
        draw_board(screen, barriers, currentState.player1_pos, currentState.player2_pos)
        if aiTurn:
            show_message(screen, "AI is thinking...", (255, 0, 0),
                         (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3), font)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                placeBarrierAtClick(event.pos, barrierOrientation, barriers)

            elif event.type == pygame.KEYDOWN and not aiTurn:
                if event.key in {pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT}:
                    direction = {pygame.K_UP: 'up', pygame.K_DOWN: 'down',
                                 pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}[event.key]
                    currentState.move_player(direction)
                    aiTurn = True
                elif event.key == pygame.K_q:
                    barrierOrientation = 'horizontal'
                elif event.key == pygame.K_e:
                    barrierOrientation = 'vertical'
        
        if aiTurn:
            bestMove = MCTS_Search(currentState, iterations=500)
            currentState = currentState.applyMoves(bestMove)
            player2_pos = currentState.player2_pos
            player1_pos = currentState.player1_pos
            currentState.player_turn = 1  # Switch back to player's turn
            aiTurn = False
            if currentState.isTerminal():
                winner = currentState.getWinner()
                show_message(screen, f"Player {winner} wins!", (0, 255, 0),
                             (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3), font)
                pygame.display.flip()
                pygame.time.wait(2000)
                game_running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
