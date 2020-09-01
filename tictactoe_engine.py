"""
Back-end for playing tic-tac-toe

First create simple data structures that hold the game state, then encapsulate these into classes
print out the game state after every move
"""

import tictactoe_agents as ta

"""
This is what we want to accomplish eventually:

while True:
    check_victory_conditions()
    next_player_make_move()
"""


class GameBoard:
    """
    This class represents the game board of a game of Tic Tac Toe.
    It allows players to make moves and to check whether the game is over.
    """

    def __init__(self):
        self.board = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]  # a list of rows
        self.pieces = ['X', 'O']
        self.moves = []
        self.active_player = 0
        self.winner = -1

    def print_board(self):
        """prints the current state of the game"""
        for row in self.board:
            print('|'.join(row))

        print('')

    def place_piece(self, row, col, player):
        """places a piece for player on row, col"""
        if player < 0 or player > 1:
            raise ValueError('player must be 0 or 1')

        if row < 0 or row > 2 or col < 0 or col > 2:
            print('\nWarning: the proposed move is illegal - please specify row and column in the range 1-3.\n')
        elif self.board[row][col] == '.':
            self.board[row][col] = self.pieces[player]
            self.moves.append((row, col, player))
            self.active_player = 1 - self.active_player
        else:
            print('\nWarning: the proposed move is illegal - that field is already occupied. No move has been made.\n')

    def get_legal_moves(self):
        """
        Returns a list of legal moves. Those moves are precisely the board entries that have a '.'
        """
        empty_space_loc = []
        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[i][j] == '.':
                    empty_space_loc.append((i, j))

        return empty_space_loc

    def game_end(self):
        """
        checks to see if any player has won or if the game is drawn
        # check for rows
        """
        row_player_1 = [row.count('X') for row in self.board]
        if row_player_1.count(3) > 0:
            self.winner = 0
            return True
        row_player_2 = [row.count('O') for row in self.board]
        if row_player_2.count(3) > 0:
            self.winner = 1
            return True

        # check for columns
        cols = [[row[i] for row in self.board] for i in range(0, 3)]
        col_player_1 = [col.count('X') for col in cols]
        if col_player_1.count(3) > 0:
            self.winner = 0
            return True
        col_player_2 = [col.count('O') for col in cols]
        if col_player_2.count(3) > 0:
            self.winner = 1
            return True

        # check for diagonals
        diags = [[self.board[i][i] for i in range(0, 3)], [self.board[j][2 - j] for j in range(0, 3)]]
        diag_player_1 = [diag.count('X') for diag in diags]
        if diag_player_1.count(3) > 0:
            self.winner = 0
            return True
        diag_player_2 = [diag.count('O') for diag in diags]
        if diag_player_2.count(3) > 0:
            self.winner = 1
            return True

        # At this point, there is no winner - now check if any valid moves can still be made
        if len(self.moves) >= 9:
            return True
        # If we reached this point then none of the game-end conditions have been met
        return False


class TicTacToe:
    """
    This class represents the interface to playing a game of tic tac toe.
    It contains options for using Agents or for players to play against one another.
    """

    def __init__(self, agent_1, agent_2):
        self.game_board = GameBoard()
        self.agents = [agent_1, agent_2]

    def play_game(self):
        while not self.game_board.game_end():
            print('Current board position:\n')
            self.game_board.print_board()
            move_row, move_col = self.agents[self.game_board.active_player].make_move(self.game_board)
            self.game_board.place_piece(row=move_row, col=move_col, player=self.game_board.active_player)

        print('===========')
        print('Game over!')
        print('===========\n')
        if self.game_board.winner == -1:
            print('The game ended in a draw\n')
        else:
            print('Congratulations, {0}!\n'.format(self.agents[self.game_board.winner].name))
        print('Final board position:')
        self.game_board.print_board()


if __name__ == '__main__':
    print('The game has begun!')
    player_1_agent = ta.HumanAgent('Human Player')
    player_2_agent = ta.NStepAgent()
    ttt = TicTacToe(agent_1=player_1_agent, agent_2=player_2_agent)
    ttt.play_game()
