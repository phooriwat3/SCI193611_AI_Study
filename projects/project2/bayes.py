# Complete this class for all parts of the project

from pacman_module.game import Agent
import numpy as np
from pacman_module import util
from scipy.stats import binom
from pacman_module.pacman import Directions
from pacman_module.game import Actions


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
        """

        self.beliefGhostStates = None
        self.walls = None
        self.ghost_type = self.args.ghostagent
        self.sensor_variance = self.args.sensorvariance

        # พารามิเตอร์สำหรับ Binomial Distribution ที่ใช้สร้าง Noise
        self.p = 0.5
        self.n = int(self.sensor_variance / (self.p * (1 - self.p)))

        # พารามิเตอร์สำหรับ Transition Model
        # ค่านี้จะถูกตั้งค่าตามประเภทของผีใน `_get_transition_model`
        self.fear_factor = 1.0


    def _get_sensor_model(self, pacman_position, evidence):
        """
        คำนวณ Sensor Model P(E_t | X_t)
        
        Return:
        -------
        2D numpy array ขนาด [width, height] ที่แต่ละช่อง (w, h)
        คือค่าความน่าจะเป็น P(E_t=evidence | X_t=(w, h))
        """
        width, height = self.walls.width, self.walls.height
        sensor_model = np.zeros((width, height))

        # วนลูปทุกตำแหน่งที่เป็นไปได้ของผี
        for w in range(width):
            for h in range(height):
                if not self.walls[w][h]:
                    # คำนวณระยะห่างจริง (Manhattan distance)
                    true_distance = util.manhattanDistance((w, h), pacman_position)
                    
                    # คำนวณค่า k สำหรับ PMF ของ Binomial distribution
                    # จาก noisy_dist = true_dist + k' - n*p
                    # --> k' = noisy_dist - true_dist + n*p
                    k = evidence - true_distance + self.n * self.p

                    # คำนวณความน่าจะเป็นที่จะได้ evidence นี้ ถ้าผีอยู่ที่ (w, h)
                    prob = binom.pmf(k, self.n, self.p)
                    sensor_model[w, h] = prob
        
        return sensor_model


    def _get_transition_model(self, pacman_position):
        """
        คำนวณ Transition Model P(X_t+1 | X_t)
        
        Return:
        -------
        4D numpy array ขนาด [width, height, width, height] ที่แต่ละช่อง
        (w1, h1, w2, h2) คือ P(X_t+1=(w1, h1) | X_t=(w2, h2))
        """
        width, height = self.walls.width, self.walls.height
        transition_model = np.zeros((width, height, width, height))

        # กำหนดค่า fear_factor ตามประเภทของผี
        if self.ghost_type == 'scared':
            self.fear_factor = 2**3
        elif self.ghost_type == 'afraid':
            self.fear_factor = 2
        else: # confused
            self.fear_factor = 1
        
        # วนลูปทุกตำแหน่งเริ่มต้นที่เป็นไปได้ (X_t)
        for w2 in range(width):
            for h2 in range(height):
                if not self.walls[w2][h2]:
                    pos_t = (w2, h2)
                    possible_actions = Actions.getLegalNeighbors(pos_t, self.walls)
                    
                    # ถ้าไม่มีทางไปต่อ ผีจะอยู่ที่เดิม
                    if not possible_actions:
                         transition_model[w2, h2, w2, h2] = 1.0
                         continue

                    dist = util.Counter()
                    current_distance = util.manhattanDistance(pos_t, pacman_position)

                    for action_pos in possible_actions:
                        succ_distance = util.manhattanDistance(action_pos, pacman_position)
                        # ให้คะแนนสูงขึ้นกับการกระทำที่ทำให้ระยะห่างจาก Pacman เพิ่มขึ้น
                        dist[action_pos] = self.fear_factor if succ_distance >= current_distance else 1
                    
                    dist.normalize()

                    # กำหนดค่าความน่าจะเป็นในการเปลี่ยนตำแหน่ง
                    for next_pos, prob in dist.items():
                        w1, h1 = next_pos
                        transition_model[w1, h1, w2, h2] = prob

        return transition_model


    def _get_updated_belief(self, belief, evidences, pacman_position, ghosts_eaten):
        """
        อัปเดต Belief State โดยใช้ Bayes Filter
        """
        updated_beliefs = []
        transition_model = self._get_transition_model(pacman_position)

        for i, (prev_belief, evidence, eaten) in enumerate(zip(belief, evidences, ghosts_eaten)):
            # ถ้าผีกินไปแล้ว belief state จะเป็นศูนย์
            if eaten:
                updated_beliefs.append(np.zeros_like(prev_belief))
                continue
            
            # 1. Prediction Step
            # P(X_t) = Σ [ P(X_t | X_{t-1}) * P(X_{t-1}) ]
            predicted_belief = np.tensordot(transition_model, prev_belief, axes=([2, 3], [0, 1]))

            # 2. Update Step
            # P(X_t | E_t) ∝ P(E_t | X_t) * P(X_t)
            sensor_model = self._get_sensor_model(pacman_position, evidence)
            unnormalized_belief = sensor_model * predicted_belief
            
            # 3. Normalization
            total_prob = np.sum(unnormalized_belief)
            if total_prob > 0:
                updated_belief = unnormalized_belief / total_prob
            else:
                # ถ้าไม่มีความน่าจะเป็นเหลืออยู่เลย ให้กลับไปเป็น uniform
                width, height = self.walls.width, self.walls.height
                num_positions = width * height - self.walls.count()
                updated_belief = np.ones_like(prev_belief) / num_positions
                updated_belief[self.walls.data] = 0

            updated_beliefs.append(updated_belief)

        return updated_beliefs


    def update_belief_state(self, evidences, pacman_position, ghosts_eaten):
        belief = self._get_updated_belief(self.beliefGhostStates, evidences,
                                          pacman_position, ghosts_eaten)
        self.beliefGhostStates = belief
        return belief

    def _get_evidence(self, state):
        positions = state.getGhostPositions()
        pacman_position = state.getPacmanPosition()
        noisy_distances = []

        for pos in positions:
            true_distance = util.manhattanDistance(pos, pacman_position)
            noise = binom.rvs(self.n, self.p) - self.n*self.p
            noisy_distances.append(true_distance + noise)

        return noisy_distances

    def _record_metrics(self, belief_states, state):
        pass

    def get_action(self, state):
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