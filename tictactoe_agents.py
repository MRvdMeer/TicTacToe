"""
This is a testing ground to develop agents for tic tac toe
"""

import tictactoe_engine as te
import copy
import random
import math


class Agent:
    """Base class for agents that play tic tac toe"""
    def __init__(self, name=''):
        self.name = name

    def score_move(self, move, board):
        """computes the score of a move on a board; uses compute_heuristic"""
        player = board.active_player
        temp_board = copy.deepcopy(board)
        move_row, move_col = move
        temp_board.place_piece(row=move_row, col=move_col, player=player)
        final_score = self.compute_heuristic(temp_board, player)
        # print('Final score of move ({0}) is: {1}'.format(', '.join([str(comp + 1) for comp in move]), final_score))
        return final_score

    @staticmethod
    def compute_heuristic(board, player):
        """compute 'score' of a board from the perspective of the player selected
        this heuristic works as follows:
        get 1e6 if you win
        get -1e5 if you lose
        get -1e3 if the opponent controls two squares in one direction and the third is empty
        get 1e2 if you control two squares in one direction and the third is empty
        get 0 for a drawn game

        previously the agent would get a bonus point for controlling the center, to force it to play there
        if no other moves were more urgent, but we have removed this behavior."""

        outcome = board.game_end()
        if outcome:
            if board.winner == player:
                return 1e6
            elif board.winner != player:
                return -1e5
            else:
                # in this case the game ended in a draw
                return 0

        # initiate counters
        num_twos = 0
        num_twos_opp = 0
        player_piece = board.pieces[player]
        opponent_piece = board.pieces[1 - player]

        # check the rows
        row_player = [row.count(player_piece) for row in board.board]
        row_opponent = [row.count(opponent_piece) for row in board.board]
        for row in range(0, 3):  # two rows
            if row_player[row] == 2 and row_opponent[row] == 0:
                num_twos += 1
            elif row_player[row] == 0 and row_opponent[row] == 2:
                num_twos_opp += 1

        # check the columns
        cols = [[row[i] for row in board.board] for i in range(0, 3)]
        col_player = [col.count(player_piece) for col in cols]
        col_opponent = [col.count(opponent_piece) for col in cols]
        for col in range(0, 3):  # three columns
            if col_player[col] == 2 and col_opponent[col] == 0:
                num_twos += 1
            elif col_player[col] == 0 and col_opponent[col] == 2:
                num_twos_opp += 1

        # check for diagonals
        diags = [[board.board[i][i] for i in range(0, 3)], [board.board[j][2 - j] for j in range(0, 3)]]
        diag_player = [diag.count(player_piece) for diag in diags]
        diag_opponent = [diag.count(opponent_piece) for diag in diags]
        for diag in range(0, 2):  # two diagonals
            if diag_player[diag] == 2 and diag_opponent[diag] == 0:
                num_twos += 1
            elif diag_player[diag] == 0 and diag_opponent[diag] == 2:
                num_twos_opp += 1

        control_center = int(board.board[1][1] == player_piece)  # this is removed for now
        control_center = 0

        final_score = 1e2 * num_twos - 1e3 * num_twos_opp + control_center
        return final_score


class HumanAgent(Agent):
    """This is a human-controlled agent"""
    def __init__(self, name='Human'):
        super().__init__(name)
        self.player = 'human'

    def make_move(self, board):
        move_string = input(
            # 'Player {0} please make a move (row, col in the range 1-3)\n'.format(str(board.active_player + 1)))
            '{0}, please make a move (row, col in the range 1-3)\n'.format(self.name))
        while ',' not in move_string:
            print('Please separate row and column by a comma\n')
            move_string = input(
                # 'Player {0} please make a move (row, col in the range 1-3)\n'.format(str(board.active_player + 1)))
                '{0}, please make a move (row, col in the range 1-3)\n'.format(self.name))
        print('')

        move_decomposed = [int(item.strip()) for item in move_string.split(",")]
        return move_decomposed[0] - 1, move_decomposed[1] - 1


class RandomAgent(Agent):
    """This is an agent that randomly makes (legal) moves"""
    def __init__(self, name='Random AI'):
        super().__init__(name=name)
        self.player = 'computer'

    def make_move(self, board):
        legal_moves = board.get_legal_moves()
        move = random.choice(legal_moves)
        print("{0} made the move ({1})\n".format(self.name, ', '.join([str(comp + 1) for comp in move])))
        return move


class OneStepAgent(Agent):
    """This agent uses one-move-ahead heuristics to determine its next move"""
    def __init__(self, name='1-move AI'):
        super().__init__(name=name)
        self.player = 'computer'

    def make_move(self, board):
        legal_moves = board.get_legal_moves()
        move_scores = [self.score_move(move, board) for move in legal_moves]
        move_score_dict = dict(zip(legal_moves, move_scores))
        best_score = max(move_scores)
        best_moves = [move for move in legal_moves if move_score_dict[move] == best_score]
        move = random.choice(best_moves)
        print("{0} made the move ({1})\n".format(self.name, ', '.join([str(comp + 1) for comp in move])))
        return move


class NStepAgent(Agent):
    """This agent looks ahead N steps and picks the best move based on what it can foresee"""

    def __init__(self, name='Minimax AI', nsteps=9, verbose=False):
        super().__init__(name=name)
        self.player = 'computer'
        self.nsteps = nsteps
        self.verbose = verbose

    def make_move(self, board):
        legal_moves = board.get_legal_moves()
        move_scores = [self.score_move(move, board) for move in legal_moves]
        move_score_dict = dict(zip(legal_moves, move_scores))
        best_score = max(move_scores)
        best_moves = [move for move in legal_moves if move_score_dict[move] == best_score]
        move = random.choice(best_moves)
        print("{0} made the move ({1})\n".format(self.name, ', '.join([str(comp + 1) for comp in move])))
        return move

    @staticmethod
    def compute_heuristic(board, player):
        """compute 'score' of a board from the perspective of the player selected
        this heuristic works as follows:
        get 10 if you win
        get -10 if you lose
        get 0 in all other cases"""

        outcome = board.game_end()
        if outcome:
            if board.winner == player:
                return 100 - len(board.moves)
            elif board.winner == 1 - player:
                return -100 + len(board.moves)
        return 0

    def score_move(self, move, board):
        """this version of score_move uses minimax to look n steps ahead"""
        player = board.active_player
        temp_board = copy.deepcopy(board)
        move_row, move_col = move
        temp_board.place_piece(row=move_row, col=move_col, player=player)
        alpha_beta_score = self.alpha_beta_minimax(board=temp_board,
                                              depth=self.nsteps,
                                              alpha=-math.inf,
                                              beta=math.inf,
                                              maximizing_player=False,
                                              player=player)
        if self.verbose:
            print('score of move ({0}) is: {1}'.format(', '.join([str(comp + 1) for comp in move]), alpha_beta_score))

        # simple_score = self.simple_minimax(board=temp_board,
        #                                   depth=self.nsteps,
        #                                   maximizing_player=False,
        #                                   player=player)
        # print('Simple score of move ({0}) is: {1}'.format(', '.join([str(comp + 1) for comp in move]), simple_score))
        return alpha_beta_score

    def simple_minimax(self, board, depth, maximizing_player, player):
        """
        uses simple minimax to find solution to the n-step lookahead optimization

        Pseudocode:
        function minimax(node, depth, maximizingPlayer) is
            if depth = 0 or node is a terminal node then
                return the heuristic value of node
            if maximizingPlayer then
                value := −∞
                for each child of node do
                    value := max(value, minimax(child, depth − 1, FALSE))
                return value
            else (* minimizing player *)
                value := +∞
                for each child of node do
                    value := min(value, minimax(child, depth − 1, TRUE))
                return value
        (* Initial call *)
        minimax(origin, depth, TRUE)
        """
        if depth == 0 or board.game_end():
            return self.compute_heuristic(board, player)

        if maximizing_player:
            value = -math.inf
            legal_moves = board.get_legal_moves()

            for move in legal_moves:
                temp_board = copy.deepcopy(board)
                move_row, move_col = move
                temp_board.place_piece(row=move_row, col=move_col, player=temp_board.active_player)
                value = max(value, self.simple_minimax(temp_board,
                                                       depth=depth - 1,
                                                       maximizing_player=False,
                                                       player=player))
            return value

        else:
            value = math.inf
            legal_moves = board.get_legal_moves()

            for move in legal_moves:
                temp_board = copy.deepcopy(board)
                move_row, move_col = move
                temp_board.place_piece(row=move_row, col=move_col, player=temp_board.active_player)
                value = min(value, self.simple_minimax(temp_board,
                                                       depth=depth - 1,
                                                       maximizing_player=True,
                                                       player=player))
            return value

    def alpha_beta_minimax(self, board, depth, alpha, beta, maximizing_player, player):
        """uses the alpha-beta minimax algorithm to find the minimax solution for the n-step lookahead optimization
        see: https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

        Pseudocode:
        function alphabeta(node, depth, α, β, maximizingPlayer) is
            if depth = 0 or node is a terminal node then
                return the heuristic value of node
            if maximizingPlayer then
                value := −∞
                for each child of node do
                    value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
                    α := max(α, value)
                    if α ≥ β then
                        break (* β cut-off *)
                return value
            else
                value := +∞
                for each child of node do
                    value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
                    β := min(β, value)
                    if β ≤ α then
                        break (* α cut-off *)
                return value

        (* Initial call *)
        alphabeta(origin, depth, −∞, +∞, TRUE)
        """

        if depth == 0 or board.game_end():
            return self.compute_heuristic(board, player)

        if maximizing_player:
            value = -math.inf
            legal_moves = board.get_legal_moves()

            for move in legal_moves:
                temp_board = copy.deepcopy(board)
                move_row, move_col = move
                temp_board.place_piece(row=move_row, col=move_col, player=temp_board.active_player)
                value = max(value, self.alpha_beta_minimax(board=temp_board,
                                                           depth=depth - 1,
                                                           alpha=alpha,
                                                           beta=beta,
                                                           maximizing_player=False,
                                                           player=player))
                alpha = max(alpha, value)

                if alpha >= beta:
                    break
            return value

        else:
            value = math.inf
            legal_moves = board.get_legal_moves()

            for move in legal_moves:
                temp_board = copy.deepcopy(board)
                move_row, move_col = move
                temp_board.place_piece(row=move_row, col=move_col, player=temp_board.active_player)
                value = min(value, self.alpha_beta_minimax(board=temp_board,
                                                           depth=(depth - 1),
                                                           alpha=alpha,
                                                           beta=beta,
                                                           maximizing_player=True,
                                                           player=player))
                beta = min(beta, value)

                if beta <= alpha:
                    break
            return value


# Purely for testing purposes - this should be called from tictactoe game
if __name__ == '__main__':
    print('The game has begun!')
    player_1_agent = NStepAgent(nsteps=9)
    player_2_agent = HumanAgent()
    ttt = te.TicTacToe(agent_1=player_1_agent, agent_2=player_2_agent)
    ttt.play_game()
