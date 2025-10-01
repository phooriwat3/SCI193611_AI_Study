# Complete this class for all parts of the project

from pacman_module.game import Agent
from pacman_module.pacman import Directions


class PacmanAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

    def get_action(self, state, belief_state):
        """
        Given a pacman game state and a belief state,
                returns a legal move.

        Arguments:
        ----------
        - `state`: the current game state. See FAQ and class
                   `pacman.GameState`.
        - `belief_state`: a list of probability matrices.

        Return:
        -------
        - A legal move as defined in `game.Directions`.
        """

        # XXX: Your code here to obtain bonus
         # 1) legal actions
        try:
            legal = [a for a in state.getLegalActions() if a != Directions.STOP]
        except TypeError:
            legal = [a for a in state.getLegalActions(0) if a != Directions.STOP]
        if not legal:
            return Directions.STOP

        # 2) ฟังก์ชันช่วย: next position + expected Manhattan distance (แบบเร็ว)
        import numpy as np

        def next_pos(pos, action):
            x, y = pos
            if action == Directions.NORTH: return (x, y + 1)
            if action == Directions.SOUTH: return (x, y - 1)
            if action == Directions.EAST:  return (x + 1, y)
            if action == Directions.WEST:  return (x - 1, y)
            return (x, y)  # เผื่อกรณี STOP

        def expected_l1_to_all_ghosts_fast(p_after, belief_state):
            nx, ny = p_after
            total = 0.0
            for B in belief_state:
                # B.shape = (W, H); Bx[x] = sum_y B[x,y], By[y] = sum_x B[x,y]
                Bx = B.sum(axis=1)  # ความน่าจะเป็นมาร์จินัลตามแกน x (ยาว W)
                By = B.sum(axis=0)  # ความน่าจะเป็นมาร์จินัลตามแกน y (ยาว H)
                xs = np.arange(B.shape[0])
                ys = np.arange(B.shape[1])
                total += np.abs(xs - nx) @ Bx + np.abs(ys - ny) @ By
            return float(total)

        # 3) เลือกแอ็กชันที่ทำให้ "ผลรวมระยะแมนฮัตตันที่คาดหมายถึงผีทุกตัว" ต่ำสุด
        pac_pos = state.getPacmanPosition()
        best_action, best_score = None, float("inf")

        for a in legal:
            pos_after = next_pos(pac_pos, a)
            score = expected_l1_to_all_ghosts_fast(pos_after, belief_state)

            # tie-break เล็กน้อย เพื่อไม่ให้แกว่งในกรณีคะแนนเท่ากัน
            if a == Directions.NORTH: score -= 1e-6
            elif a == Directions.EAST: score -= 2e-6
            elif a == Directions.SOUTH: score -= 3e-6
            elif a == Directions.WEST: score -= 4e-6

            if score < best_score:
                best_score, best_action = score, a

        return best_action if best_action is not None else Directions.STOP

        # XXX: End of your code here to obtain bonus


