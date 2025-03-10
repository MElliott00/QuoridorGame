import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, CELL_SIZE, GRID_SIZE
from board import draw_board, placeBarrierAtClick, show_message
from game_state import QuoridorState
from mcts import best_ai_move

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quoridor Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

player1_pos = (8, 4)
player2_pos = (0, 4)
barriers = []
currentState = QuoridorState(player1_pos, player2_pos, barriers, player_turn=1)

def main():
    global currentState
    game_running = True
    aiTurn = False
    barrierOrientation = 'horizontal'

    while game_running:
        screen.fill(WHITE)
        draw_board(screen, currentState.barriers, currentState.player1_pos, currentState.player2_pos)

        if aiTurn:
            show_message(screen, "AI is thinking...", (255, 0, 0),
                         (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3), font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                success = placeBarrierAtClick(event.pos, barrierOrientation, currentState)
                if success:
                    currentState.player_turn = 3 - currentState.player_turn
                    if not currentState.isTerminal():
                        aiTurn = (currentState.player_turn == 2)
                    print("Barrier placed!")
                else:
                    print("Invalid barrier placement!")

            elif event.type == pygame.KEYDOWN and not aiTurn:
                if event.key in {pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT}:
                    direction = {pygame.K_UP: 'up', pygame.K_DOWN: 'down',
                                 pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}[event.key]
                    currentState.move_player(direction)

                    if currentState.isTerminal():
                        winner = currentState.getWinner()
                        show_message(screen, f"Player {winner} wins!", (0, 255, 0),
                                     (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3), font)
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        game_running = False
                        continue  

                    aiTurn = (currentState.player_turn == 2)
                elif event.key == pygame.K_q:
                    barrierOrientation = 'horizontal'
                elif event.key == pygame.K_e:
                    barrierOrientation = 'vertical'

        if aiTurn:
            bestMove = best_ai_move(currentState)
            if bestMove:
                currentState = currentState.applyMoves(bestMove)

            if currentState.isTerminal():
                winner = currentState.getWinner()
                show_message(screen, f"Player {winner} wins!", (0, 255, 0),
                            (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3), font)
                pygame.display.flip()
                pygame.time.wait(2000)
                game_running = False
            else:
                aiTurn = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
