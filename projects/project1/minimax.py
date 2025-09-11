from pacman_module.game import Agent, Directions

class PacmanAgent(Agent):
    def __init__(self, depth=2):
        super().__init__()
        self.depth = depth
        self.expanded_nodes = 0
        
    def get_action(self, gameState):
        # เรียกใช้ minimax และ return action
        return self.minimax(gameState, self.depth, 0)
    
    def min_value(self, state, depth, agent_index):
        # นับ node expansion ที่นี่
        self.expanded_nodes += 1
        
        # Base case
        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluation_function(state)
        
        next_agent = agent_index + 1
        if next_agent >= state.getNumAgents():
            next_agent = 0  # กลับไป Pacman
            next_depth = depth - 1  # ลด depth
        else:
            next_depth = depth  # ยังอยู่ระดับเดียวกัน
            
        # Call generateGhostSuccessors() to get successors and count node expansion
        successors = state.generateGhostSuccessors(agent_index)
        if not successors:
            return self.evaluation_function(state)
            
        best_score = float('inf')
        for successor, action in successors:
            score = self.minimax(successor, next_depth, next_agent)
            best_score = min(best_score, score)
        return best_score
    
    def max_value(self, state, depth):
        # นับ node expansion ที่นี่
        self.expanded_nodes += 1
        
        # Base case
        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluation_function(state)
        
        best_score = float('-inf')
        for action in state.getLegalActions(0):  # Pacman is agent 0
            if action == Directions.STOP:
                continue
            successor = state.generateSuccessor(0, action)
            score = self.min_value(successor, depth, 1)  # Ghost starts at index 1
            best_score = max(best_score, score)
        return best_score
    
    def minimax(self, state, depth, agent_index):
        if agent_index == 0:  # Pacman's turn (MAX)
            if depth == self.depth:  # Root level - return action
                best_score = float('-inf')
                best_action = Directions.STOP
                for action in state.getLegalActions(0):
                    if action == Directions.STOP:
                        continue
                    successor = state.generateSuccessor(0, action)
                    score = self.min_value(successor, depth, 1)
                    if score > best_score:
                        best_score = score
                        best_action = action
                return best_action
            else:
                return self.max_value(state, depth)
        else:  # Ghost's turn (MIN)
            return self.min_value(state, depth, agent_index)
    
    def evaluation_function(self, state):
        return state.getScore()
    
    def get_and_reset_expanded(self):
        """เมธอดที่ engine เรียกเพื่อดึงจำนวนโหนดและรีเซ็ต"""
        n = self.expanded_nodes
        self.expanded_nodes = 0
        return n