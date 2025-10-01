# minimax.py

from pacman_module.game import Agent
from pacman_module.pacman import GameState

class PacmanAgent(Agent):
    """
    Pacman Agent ที่ใช้อัลกอริทึม Minimax
    """

    def __init__(self, depth='2'):
        super().__init__()
        self.depth = int(depth)

    def get_action(self, state: GameState):
        """
        หา Action ที่ดีที่สุดสำหรับ Pacman โดยใช้อัลกอริทึม Minimax
        """
        # เริ่มต้นค้นหาจาก Pacman (agent 0) ที่ความลึก 0
        _, best_action = self.minimax_value(state, 0, 0)
        return best_action

    def minimax_value(self, state: GameState, current_depth, agent_index):
        """
        ฟังก์ชัน Minimax แบบ Recursive หลัก
        """
        num_agents = state.getNumAgents()
        
        # กำหนด Agent และ Depth ถัดไป
        next_agent_index = (agent_index + 1) % num_agents
        next_depth = current_depth
        if next_agent_index == 0:
            next_depth += 1

        # Base Case: ถ้าถึงความลึกสูงสุด หรือเกมจบแล้ว ให้คืนค่า evaluation
        if next_depth > self.depth or state.isWin() or state.isLose():
            return state.getScore(), None

        # ถ้าเป็นตาของ Pacman (Maximizer)
        if agent_index == 0:
            return self.max_value(state, next_depth, next_agent_index)
        # ถ้าเป็นตาของผี (Minimizer)
        else:
            return self.min_value(state, next_depth, next_agent_index, agent_index)

    def max_value(self, state: GameState, current_depth, agent_index):
        """
        คำนวณค่าที่ดีที่สุดสำหรับ Maximizer (Pacman)
        """
        max_val = -float('inf')
        best_action = None
        
        # ใช้ generatePacmanSuccessors เพื่อให้มีการนับ Expanded Nodes
        successors = state.generatePacmanSuccessors()
        if not successors:
            return state.getScore(), None

        for successor_state, action in successors:
            val, _ = self.minimax_value(successor_state, current_depth, agent_index)
            if val > max_val:
                max_val = val
                best_action = action
        return max_val, best_action

    def min_value(self, state: GameState, current_depth, agent_index, ghost_index):
        """
        คำนวณค่าที่ดีที่สุดสำหรับ Minimizer (Ghost)
        """
        min_val = float('inf')
        
        # ใช้ generateGhostSuccessors เพื่อให้มีการนับ Expanded Nodes
        successors = state.generateGhostSuccessors(ghost_index)
        if not successors:
            return state.getScore(), None

        for successor_state, action in successors:
            val, _ = self.minimax_value(successor_state, current_depth, agent_index)
            min_val = min(min_val, val)
        
        # ในตาของผี เราไม่จำเป็นต้องคืน Action
        return min_val, None