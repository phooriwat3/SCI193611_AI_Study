from pacman_module.game import Agent, Directions
import heapq
import itertools

class PacmanAgent(Agent):
    def __init__(self, args=None):
        super().__init__()
        self.actions = []
        self.counter = itertools.count()
        self.args = args

    def heuristic(self, position, food):
        if not food:
            return 0
        return min(abs(position[0] - fx) + abs(position[1] - fy) for fx, fy in food)

    def astar(self, state):
        start = state.getPacmanPosition()
        food = state.getFood().asList()

        frontier = []
        start_h = self.heuristic(start, food)
        heapq.heappush(frontier, (start_h, 0, next(self.counter), state, []))

        explored = {}

        while frontier:
            f, g, _, current_state, path = heapq.heappop(frontier)
            pos = current_state.getPacmanPosition()

            if pos in food:
                return path

            if pos in explored and explored[pos] <= g:
                continue
            explored[pos] = g

            for action in current_state.getLegalActions():
                if action == Directions.STOP:
                    continue

                successor = current_state.generatePacmanSuccessor(action)
                if successor is None:
                    continue

                next_pos = successor.getPacmanPosition()
                cost = g + 1
                h = self.heuristic(next_pos, food)
                f_new = cost + h

                heapq.heappush(frontier,
                               (f_new, cost, next(self.counter), successor, path + [action]))

        return []

    def get_action(self, state):
        if not self.actions:
            self.actions = self.astar(state)

        if self.actions:
            return self.actions.pop(0)

        return Directions.STOP
