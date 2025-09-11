from pacman_module.game import Agent
from pacman_module.pacman import GameState
from pacman_module.util import manhattanDistance


def score_evaluation_function(current_game_state: GameState):
    """
    This default evaluation function just returns the score of the state.
    """
    return current_game_state.getScore()


class PacmanAgent(Agent):
    """
    An agent that uses H-Minimax with Alpha-Beta Pruning.
    The evaluation function is the score of the state.
    """

    def __init__(self, depth='2', eval_fn=score_evaluation_function):
        """
        Initializes the agent with a search depth and an evaluation function.
        """
        super().__init__()
        self.depth = int(depth)
        self.evaluation_function = eval_fn
        self.action = None

    def get_action(self, game_state: GameState):
        """
        Returns the best action using H-Minimax with Alpha-Beta Pruning.
        """
        self.alpha_beta_search(game_state)
        return self.action

    def alpha_beta_search(self, game_state: GameState):
        """
        The main function for Alpha-Beta search.
        """
        alpha = -float('inf')
        beta = float('inf')
        self.action = self.max_value(game_state, 0, 0, alpha, beta)[1]

    def max_value(self, game_state: GameState, current_depth, agent_index, alpha, beta):
        """
        Calculates the max value for Pacman's turn in Alpha-Beta Pruning.
        """
        if self.is_terminal_state(game_state, current_depth):
            return self.evaluation_function(game_state), None

        v = -float('inf')
        best_action = None

        for action in game_state.getLegalActions(agent_index):
            successor_state = game_state.generateSuccessor(agent_index, action)
            new_val = self.min_value(successor_state, current_depth, agent_index + 1, alpha, beta)[0]

            if new_val > v:
                v = new_val
                best_action = action
            if v > beta:
                return v, best_action
            alpha = max(alpha, v)

        return v, best_action

    def min_value(self, game_state: GameState, current_depth, agent_index, alpha, beta):
        """
        Calculates the min value for the ghost's turn in Alpha-Beta Pruning.
        """
        if self.is_terminal_state(game_state, current_depth):
            return self.evaluation_function(game_state), None

        v = float('inf')
        best_action = None
        num_agents = game_state.getNumAgents()
        next_agent_index = agent_index + 1

        for action in game_state.getLegalActions(agent_index):
            successor_state = game_state.generateSuccessor(agent_index, action)

            if next_agent_index == num_agents:
                new_val = self.max_value(successor_state, current_depth + 1, 0, alpha, beta)[0]
            else:
                new_val = self.min_value(successor_state, current_depth, next_agent_index, alpha, beta)[0]

            if new_val < v:
                v = new_val
                best_action = action
            if v < alpha:
                return v, best_action
            beta = min(beta, v)

        return v, best_action

    def is_terminal_state(self, game_state: GameState, current_depth):
        """
        Checks if the current state is a terminal state (win, lose, or max depth reached).
        """
        return game_state.isWin() or game_state.isLose() or current_depth == self.depth