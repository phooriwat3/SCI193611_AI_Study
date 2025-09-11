from pacman_module.game import Agent, Directions
import math

class PacmanAgent(Agent):
    def __init__(self, depth=3):
        super().__init__()
        self.depth = depth
        self.last = Directions.STOP

    # ---------- Public API ----------
    def get_action(self, state):
        # ใช้ bulk successors ของ Pacman (เอนจินจะนับ expanded เอง)
        succs = state.generatePacmanSuccessors()
        if not succs:
            return Directions.STOP

        alpha, beta = -math.inf, math.inf
        best_val, best_act = -math.inf, Directions.STOP

        # heuristic ordering (optional, H-Minimax)
        scored = []
        for succ, act in succs:
            scored.append((self._evaluate(succ), act, succ))
        scored.sort(reverse=True, key=lambda x: x[0])

        for _, act, succ in scored:
            val = self._min_value(succ, self.depth, 1, alpha, beta)
            if val > best_val or (val == best_val and act == self.last):
                best_val, best_act = val, act
            alpha = max(alpha, best_val)

        self.last = best_act
        return best_act

    # ---------- Minimax with Alpha-Beta ----------
    def _max_value(self, state, depth, alpha, beta):
        if self._cutoff(state, depth):
            return self._evaluate(state)

        v = -math.inf
        succs = state.generatePacmanSuccessors()  # << สำคัญ
        if not succs:
            return self._evaluate(state)

        # heuristic ordering (optional)
        scored = [(self._evaluate(s), a, s) for (s, a) in succs]
        scored.sort(reverse=True, key=lambda x: x[0])

        for _, _act, succ in scored:
            v = max(v, self._min_value(succ, depth, 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def _min_value(self, state, depth, agent_index, alpha, beta):
        if self._cutoff(state, depth):
            return self._evaluate(state)

        v = math.inf
        succs = state.generateGhostSuccessors(agent_index)  # << สำคัญ
        if not succs:
            return self._evaluate(state)

        # heuristic ordering (optional)
        scored = [(self._evaluate(s), a, s) for (s, a) in succs]
        scored.sort(key=lambda x: x[0])  # MIN: แย่ -> ดี

        # คำนวณ agent ถัดไปและ depth
        next_agent = agent_index + 1
        next_depth = depth
        if next_agent >= state.getNumAgents():
            next_agent = 0
            next_depth = depth - 1

        for _, _act, succ in scored:
            if next_agent == 0:
                score = self._max_value(succ, next_depth, alpha, beta)
            else:
                score = self._min_value(succ, next_depth, next_agent, alpha, beta)
            v = min(v, score)
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # ---------- Helpers ----------
    def _cutoff(self, state, depth):
        return state.isWin() or state.isLose() or depth == 0

    def _evaluate(self, state):
        score = state.getScore()
        try:
            pos = state.getPacmanPosition()
            food = state.getFood().asList()
            f_left = len(food)

            d_food = min((abs(pos[0] - fx) + abs(pos[1] - fy) for (fx, fy) in food), default=0)
            ghosts = getattr(state, "getGhostPositions", lambda: [])()
            d_ghost = min((abs(pos[0] - gx) + abs(pos[1] - gy) for (gx, gy) in ghosts), default=6)

            # ปรับน้ำหนัก
            return score - 0.15 * d_food - 0.5 * f_left + 0.1 * min(d_ghost, 7)
        except Exception:
            return score


