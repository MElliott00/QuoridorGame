import time
import random
from game_state import QuoridorState
from mcts import best_ai_move


def random_agent_move(state):
    moves = state.getLegalMoves()
    return random.choice(moves)[:2] if moves else None


def run_single_game():
    #AI is player 2
    state = QuoridorState(player1_pos=(8, 4), player2_pos=(0, 4), barriers=[], player_turn=1)
    ai_turn = True  
    move_times = []
    moves_count = 0

    # Track move efficiency
    while not state.isTerminal():
        start_time = time.time()
        if ai_turn:
            move = best_ai_move(state)
        else:
            move = random_agent_move(state)

        elapsed = time.time() - start_time
        if ai_turn:
            move_times.append(elapsed)

        if move is None:
            break

        state = state.applyMoves(move)
        ai_turn = not ai_turn
        moves_count += 1

    winner = state.getWinner()
    ai_won = winner == 2
    avg_move_time = sum(move_times) / len(move_times) if move_times else 0

    return ai_won, moves_count, avg_move_time


# TEST
def evaluate_ai(num_games=1000):
    ai_wins = 0
    total_moves = 0
    total_time = 0

    for i in range(num_games):
        ai_won, moves, avg_time = run_single_game()
        ai_wins += ai_won
        total_moves += moves
        total_time += avg_time
        print(f"Game {i+1}: AI {'won' if ai_won else 'lost'} in {moves} moves (avg AI move time: {avg_time:.4f}s)")

    win_rate = (ai_wins / num_games) * 100
    avg_moves = total_moves / num_games
    avg_move_time = total_time / num_games

    print("\nAI Evaluation Results:")
    print(f"AI Win Rate: {win_rate}%")
    print(f"Average moves per game: {avg_moves:.2f}")
    print(f"Average AI decision time per move: {avg_move_time:.4f}s")


if __name__ == "__main__":
    evaluate_ai(num_games=1000)