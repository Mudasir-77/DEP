import math
import argparse

class NimGame:
    def __init__(self, num_red, num_blue, version, first_player, depth=None):
        self.num_red = num_red
        self.num_blue = num_blue
        self.version = version
        self.first_player = first_player
        self.depth = depth
        self.current_player = first_player

    def is_game_over(self):
        if self.version == "standard":
            return self.num_red == 0 or self.num_blue == 0
        else:  # Misere version
            return self.num_red == 0 and self.num_blue == 0

    def calculate_score(self):
        return self.num_red * 2 + self.num_blue * 3

    def play_turn(self, red_to_remove, blue_to_remove):
        self.num_red -= red_to_remove
        self.num_blue -= blue_to_remove
        self.current_player = "computer" if self.current_player == "human" else "human"

    def get_human_move(self):
        while True:
            try:
                red_to_remove = int(input(f"Enter the number of red marbles to remove (0 to {self.num_red}): "))
                blue_to_remove = int(input(f"Enter the number of blue marbles to remove (0 to {self.num_blue}): "))
                if 0 <= red_to_remove <= self.num_red and 0 <= blue_to_remove <= self.num_blue:
                    return red_to_remove, blue_to_remove
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter integers only.")

    def get_computer_move(self):
        best_move = self.minmax(self.depth, True, -math.inf, math.inf)[0]  # Get the best move
        print(f"Computer picked {best_move[0]} red and {best_move[1]} blue marble.")
        return best_move

    def play_game(self):
        while not self.is_game_over():
            print(f"Current state: Red marbles: {self.num_red}, Blue marbles: {self.num_blue}")
            if self.current_player == "human":
                red_to_remove, blue_to_remove = self.get_human_move()
            else:
                red_to_remove, blue_to_remove = self.get_computer_move()
            self.play_turn(red_to_remove, blue_to_remove)

        print(f"Game Over! Final score: {self.calculate_score()}")

    def minmax(self, depth, is_maximizing_player, alpha, beta):
        if self.is_game_over() or depth == 0:
            return (0, 0), self.calculate_score()  # Return a default move and the score

        if is_maximizing_player:
            max_eval = -math.inf
            best_move = (0, 0)
            for move in self.get_possible_moves():
                self.play_turn(*move)
                eval = self.minmax(depth - 1, False, alpha, beta)[1]  # Get the score from the recursive call
                self.undo_turn(*move)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return best_move, max_eval  # Return the best move and the max evaluation
        else:
            min_eval = math.inf
            best_move = (0, 0)
            for move in self.get_possible_moves():
                self.play_turn(*move)
                eval = self.minmax(depth - 1, True, alpha, beta)[1]  # Get the score from the recursive call
                self.undo_turn(*move)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return best_move, min_eval  # Return the best move and the min evaluation

    def get_possible_moves(self):
        possible_moves = []
        for r in range(self.num_red + 1):
            for b in range(self.num_blue + 1):
                if r + b > 0:  # At least one marble must be removed
                    possible_moves.append((r, b))
        return possible_moves

    def undo_turn(self, red_to_remove, blue_to_remove):
        self.num_red += red_to_remove
        self.num_blue += blue_to_remove
        self.current_player = "computer" if self.current_player == "human" else "human"

def parse_arguments():
    parser = argparse.ArgumentParser(description="Play the Red-Blue Nim Game.")
    parser.add_argument("--num-red", type=int, default=10, help="Number of red marbles.")
    parser.add_argument("--num-blue", type=int, default=10, help="Number of blue marbles.")
    parser.add_argument("--version", type=str, choices=["standard", "misere"], default="standard",
                        help="Game version.")
    parser.add_argument("--first-player", type=str, choices=["computer", "human"], default="computer",
                        help="First player.")
    parser.add_argument("--depth", type=int, help="Search depth for AI (optional).")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    game = NimGame(args.num_red, args.num_blue, args.version, args.first_player, args.depth)
    game.play_game()