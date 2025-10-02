# Complete this class for all parts of the project

from pacman_module.game import Agent
import numpy as np
from pacman_module import util
from scipy.stats import binom
import math

class BeliefStateAgent(Agent):
    def __init__(self, args):
        """
        Arguments:
        ----------
        - `args`: Namespace of arguments from command-line prompt.
        """
        self.args = args

        """
            Variables to use in 'update_belief_state' method.
            Initialization occurs in 'get_action' method.

            XXX: DO NOT MODIFY THE DEFINITION OF THESE VARIABLES  
            # Doing so will result in a 0 grade.
        """

        # Current list of belief states over ghost positions
        self.beliefGhostStates = None

        # Grid of walls (assigned with 'state.getWalls()' method)
        self.walls = None

        # Hyper-parameters
        self.ghost_type = self.args.ghostagent           # ประเภทผี: scared/afraid/confused
        self.sensor_variance = self.args.sensorvariance  # ความแปรปรวนของเซนเซอร์
        
        # โมเดลสัญญาณรบกวนเป็น Binomial(n, p) โดย p=0.5 และเราชิฟต์ให้อยู่รอบศูนย์
        self.p = 0.5
        # เลือก n ให้สอดคล้องกับ variance ของ Binomial: Var = n p (1-p) = n * 0.5 * 0.5
        # => n = variance / (p*(1-p))
        self.n = int(self.sensor_variance/(self.p*(1-self.p)))
         
        self.layout_name = getattr(self.args, "layout", "unknown")
        self.runid = getattr(self.args, "seed", -1)
        # XXX: Your code here
    def _shape(self):
        # ขนาดกระดาน (กว้าง, สูง)
        return self.walls.width, self.walls.height

    def _is_legal(self, x, y):
        # ช่อง (x,y) เดินได้หรือไม่ (อยู่นอกเขตหรือเป็นกำแพง = false)
        if x < 0 or x >= self.walls.width or y < 0 or y >= self.walls.height:
            return False
        return not self.walls[x][y]

    def _legal_neighbors(self, x, y):
        # เพื่อนบ้าน 4 ทิศ (Von Neumann) ที่ "เดินได้"
        cand = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [(nx, ny) for (nx, ny) in cand if self._is_legal(nx, ny)]

    def _normalize_matrix(self, matrix):
        # ทำให้ผลรวมของความน่าจะเป็น = 1 (ถ้าทั้งหมดเป็น 0 ให้กระจายเท่ากันทุกช่อง)
        s = matrix.sum()
        if s > 0.0:
            matrix /= s
        else:
            matrix[:] = 1.0 / matrix.size
        return matrix
        # XXX: End of your code


    def _get_sensor_model(self, pacman_position, evidence):
        """
        Arguments:
        ----------
        - `pacman_position`: 2D coordinates position
          of pacman at state x_{t}
          where 't' is the current time step

        Return:
        -------
        The sensor model represented as a 2D numpy array of
        size [width, height].
        The element at position (w, h) is the probability
        P(E_t=evidence | X_t=(w, h))
        """
        W, H = self._shape()
        likelihood = np.zeros((W, H), dtype=float)
        z = evidence        # ค่าที่เซนเซอร์วัดได้ (มี noise)
        n = self.n
        p = self.p
        np_half = n * p     # = n*0.5 (ค่าเฉลี่ยของ Binomial)
        px, py = pacman_position

        for x in range(W):
            for y in range(H):
                if not self._is_legal(x, y):
                    continue
                # ระยะจริงแบบแมนฮัตตันจากตำแหน่งผู้สมัคร (x,y) ไปยังแพคแมน
                d = util.manhattanDistance((x, y), (px, py))
                k_real = z - d + np_half
                # k คือค่าที่ต้องได้จากตัวแปรสุ่ม Binomial (หลังชิฟต์กลับ)
                k = int(round(k_real))
                # ต้องเป็นจำนวนเต็มในช่วง [0, n] เท่านั้นจึงมีความน่าจะเป็น > 0
                if 0 <= k <= n and abs(k - k_real) < 1e-9:
                    likelihood[x, y] = binom.pmf(k, n, p)
                else:
                    likelihood[x, y] = 0.0
        return likelihood

    def _get_transition_model(self, pacman_position, prev_pos):
        """
        Arguments:
        ----------
        - `pacman_position`: 2D coordinates position
          of pacman at state x_{t}
          where 't' is the current time step

        Return:
        -------
        The transition model represented as a 4D numpy array of
        size [width, height, width, height].
        The element at position (w1, h1, w2, h2) is the probability
        P(X_t+1=(w1, h1) | X_t=(w2, h2))
        """
        W, H = self._shape()
        T_next = np.zeros((W, H), dtype=float)
    

        x0, y0 = prev_pos
        if not self._is_legal(x0, y0):
            return T_next  # จุดเดิมผิดกฎ

        # คำนวณ alpha แบบ local (ไม่แตะ __init__)
        gt = self.ghost_type if hasattr(self, "ghost_type") else "confused"
        alpha = 2.0 if gt == "scared" else 1.0 if gt == "afraid" else 0.0

        px, py = pacman_position
        # ระยะปัจจุบันจากจุดเดิมไปยังแพคแมน
        cur_d = abs(x0 - px) + abs(y0 - py)
        
         # เพื่อนบ้านที่เดินได้จากจุดเดิม
        nbrs = self._legal_neighbors(x0, y0)
        if not nbrs:
            # ถ้าไม่มีทางไป ให้คงอยู่ที่เดิม
            T_next[x0, y0] = 1.0
            return T_next

        # คะแนน softmax: exp(alpha * Δ) โดย Δ = dist(next,P) - dist(cur,P)
        scores = []
        for (x1, y1) in nbrs:
            delta = (abs(x1 - px) + abs(y1 - py)) - cur_d   # Δ = dist(next) - dist(cur)
            scores.append(math.exp(alpha * delta))

        total = sum(scores)
        if total <= 0.0:
            # safety: ถ้าทั้งหมดเป็น 0 แบ่งเท่ากัน
            prob = 1.0 / len(nbrs)
            for (x1, y1) in nbrs:
                T_next[x1, y1] = prob
        else:
            # eps=0.0 (ตั้งค่าได้ถ้าต้องการให้กระจายขึ้นเล็กน้อย)
            eps = 0.0
            for j, (x1, y1) in enumerate(nbrs):
                base = scores[j] / total
                prob = (1 - eps) * base + eps * (1.0 / len(nbrs))
                T_next[x1, y1] = prob

        return T_next

    def _get_updated_belief(self, belief, evidences, pacman_position,
            ghosts_eaten):
        """
        Given a list of (noised) distances from pacman to ghosts,
        and the previous belief states before receiving the evidences,
        returns the updated list of belief states about ghosts positions

        Arguments:
        ----------
        - `belief`: A list of Z belief states at state x_{t-1}
          as N*M numpy mass probability matrices
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.
        - `evidences`: list of distances between
          pacman and ghosts at state x_{t}
          where 't' is the current time step
        - `pacman_position`: 2D coordinates position
          of pacman at state x_{t}
          where 't' is the current time step
        - `ghosts_eaten`: list of booleans indicating
          whether ghosts have been eaten or not

        Return:
        -------
        - A list of Z belief states at state x_{t}
          as N*M numpy mass probability matrices
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.

        N.B. : [0,0] is the bottom left corner of the maze.
               Matrices filled with zeros must be returned for eaten ghosts.
        """

        # XXX: Your code here
        W, H = self._shape()
        Z = len(belief)        # จำนวนผี
        new_belief_states = []

        for i in range(Z):
            # ถ้าผีตัวนี้โดนกินแล้ว ให้คืนเมทริกซ์ศูนย์
            if ghosts_eaten[i]:
                new_belief_states.append(np.zeros((W, H), dtype=float))
                continue

            # === 1. Prediction Step ===
            prior_belief = belief[i]
            predicted_belief = np.zeros((W, H), dtype=float)

             # สำหรับตำแหน่งก่อนหน้าแต่ละจุด (ที่มีความน่าจะเป็น > 0)
            for x0 in range(W):
                for y0 in range(H):
                    if prior_belief[x0, y0] > 0:
                         # คำนวณทรานซิชันจากจุด (x0,y0) ไปทุกเพื่อนบ้าน (2D)
                        transition = self._get_transition_model(
                            pacman_position, (x0, y0)
                        )
                        # กระจายมวล prior ไปยังปลายทาง
                        predicted_belief += prior_belief[x0, y0] * transition

            # === 2) Update step ===
            # คูณด้วย likelihood จากเซนเซอร์ของเฟรมปัจจุบัน
            likelihood = self._get_sensor_model(pacman_position, evidences[i])
            posterior_belief = predicted_belief * likelihood

             # === 3) Normalize ===
            self._normalize_matrix(posterior_belief)
            new_belief_states.append(posterior_belief)

        return new_belief_states

        # XXX: End of your code

    def update_belief_state(self, evidences, pacman_position, ghosts_eaten):
        """
        Given a list of (noised) distances from pacman to ghosts,
        returns a list of belief states about ghosts positions

        Arguments:
        ----------
        - `evidences`: list of distances between
          pacman and ghosts at state x_{t}
          where 't' is the current time step
        - `pacman_position`: 2D coordinates position
          of pacman at state x_{t}
          where 't' is the current time step
        - `ghosts_eaten`: list of booleans indicating
          whether ghosts have been eaten or not

        Return:
        -------
        - A list of Z belief states at state x_{t}
          as N*M numpy mass probability matrices
          where N and M are respectively width and height
          of the maze layout and Z is the number of ghosts.

        XXX: DO NOT MODIFY THIS FUNCTION !!!
        Doing so will result in a 0 grade.
        """
        belief = self._get_updated_belief(self.beliefGhostStates, evidences,
                                          pacman_position, ghosts_eaten)
        self.beliefGhostStates = belief
        return belief

    def _get_evidence(self, state):
        """
        Computes noisy distances between pacman and ghosts.

        Arguments:
        ----------
        - `state`: The current game state s_t
                   where 't' is the current time step.
                   See FAQ and class `pacman.GameState`.


        Return:
        -------
        - A list of Z noised distances in real numbers
          where Z is the number of ghosts.

        XXX: DO NOT MODIFY THIS FUNCTION !!!
        Doing so will result in a 0 grade.
        """
        positions = state.getGhostPositions()
        pacman_position = state.getPacmanPosition()
        noisy_distances = []

        for pos in positions:
            true_distance = util.manhattanDistance(pos, pacman_position)
            noise = binom.rvs(self.n, self.p) - self.n*self.p
            noisy_distances.append(true_distance + noise)

        return noisy_distances

    def _record_metrics(self, belief_states, state):
        """
        Use this function to record your metrics
        related to true and belief states.
        Won't be part of specification grading.

        Arguments:
        ----------
        - `state`: The current game state s_t
                   where 't' is the current time step.
                   See FAQ and class `pacman.GameState`.
        - `belief_states`: A list of Z
           N*M numpy matrices of probabilities
           where N and M are respectively width and height
           of the maze layout and Z is the number of ghosts.

        N.B. : [0,0] is the bottom left corner of the maze
        """
        import csv, os
        if not hasattr(self, "_t"): self._t = 0

        os.makedirs("results", exist_ok=True)
        fpath = f"results/metrics_{self.ghost_type}.csv"
        newfile = not os.path.exists(fpath)
    
        true_positions = state.getGhostPositions()
    
        with open(fpath, "a", newline="") as f:
            w = csv.writer(f)
            if newfile:
                w.writerow(["runid","t","ghost_idx","entropy","pat","expected_L1",
                            "layout","ghost_type","sensor_var"])
            for gi, B in enumerate(belief_states):
                flat = B.flatten()
                entropy = float(-np.sum(flat[flat>0] * np.log(flat[flat>0] + 1e-12)))
                tx, ty = true_positions[gi]
                tx, ty = int(round(tx)), int(round(ty))
                pat = float(B[tx, ty]) if (0 <= tx < B.shape[0] and 0 <= ty < B.shape[1]) else 0.0
                W, H = B.shape
                xs = np.arange(W)[:, None]
                ys = np.arange(H)[None, :]
                exp_L1 = float(np.sum(B * (np.abs(xs - tx) + np.abs(ys - ty))))
                w.writerow([self.runid, self._t, gi, entropy, pat, exp_L1,
                            self.layout_name, self.ghost_type, self.sensor_variance])
        self._t += 1
    
    def get_action(self, state):
        """
        Given a pacman game state, returns a belief state.

        Arguments:
        ----------
        - `state`: the current game state.
                   See FAQ and class `pacman.GameState`.

        Return:
        -------
        - A belief state.
        """

        """
           XXX: DO NOT MODIFY THAT FUNCTION !!!
                Doing so will result in a 0 grade.
        """
        # Variables are specified in constructor.
        if self.beliefGhostStates is None:
            self.beliefGhostStates = state.getGhostBeliefStates()
        if self.walls is None:
            self.walls = state.getWalls()

        evidence = self._get_evidence(state)
        newBeliefStates = self.update_belief_state(evidence,
                                                   state.getPacmanPosition(),
                                                   state.data._eaten[1:])
        self._record_metrics(self.beliefGhostStates, state)

        return newBeliefStates, evidence
