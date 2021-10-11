import tictactoe_engine as te
import tictactoe_agents as ta


def select_agent(input_player):
    """Gathers input to select agent type"""
    helper = [str(num) for num in range(0, 10)]
    player_agent = None

    incorrect_choice = True
    while incorrect_choice:
        print('Please pick Player {0} from the following choices:'.format(input_player))
        player_choice = input('1: Human player\n'
                              '2: Easy Computer\n'
                              '3: Medium Computer\n'
                              '4: Hard Computer\n'
                              '5: Hard Computer with move explanation\n')
        incorrect_choice = False
        player = 0

        try:
            player = int(player_choice.strip())
        except ValueError:
            print('Please enter a number to represent your choice')
            incorrect_choice = True

        if player == 1:
            player_agent = ta.HumanAgent('Human')
        elif player == 2:
            player_agent = ta.RandomAgent('Easy Computer')
        elif player == 3:
            player_agent = ta.OneStepAgent('Medium Computer')
        elif player == 4:
            player_agent = ta.NStepAgent('Hard Computer')
        elif player == 5:
            player_agent = ta.NStepAgent('Hard Computer', verbose=True)
        else:
            incorrect_choice = True
            print('I don\'t understand your choice, please try again')

    return player_agent


if __name__ == '__main__':
    print('The game has begun!')

    player_1_agent = select_agent(1)
    player_2_agent = select_agent(2)

    ttt = te.TicTacToe(agent_1=player_1_agent, agent_2=player_2_agent)
    ttt.play_game()
