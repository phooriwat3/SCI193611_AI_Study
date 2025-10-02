from pacman_module.game import Agent, Directions

class PacmanAgent(Agent):
    def __init__(self, depth=5):
        super().__init__()
        self.depth = depth
        self.expanded_nodes = 0
        self.last = Directions.STOP  # จำทิศล่าสุดไว้กัน oscillation
        
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
            
        v = float("inf")
        for succ, action in successors:
            score = self.minimax(succ, next_depth, next_agent)
            v = min(v, score)
        return v
    
    def max_value(self, state, depth):
        # นับ node expansion ที่นี่
        self.expanded_nodes += 1
        
        # Base case
        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluation_function(state)
        
        v = float("-inf") 
        successors = state.generatePacmanSuccessors()
        if not successors:
            return self.evaluation_function(state)
        
        # จัดลำดับแบบเดียวกับ root เพื่อเสริมความเสถียรในต้นไม้
        successors.sort(key=lambda sa: sa[0].getScore(), reverse=True)
        
        for succ, action in successors:
            score = self.min_value(succ, depth, 1)
            v = max(v, score)
        return v

    
    def minimax(self, state, depth, agent_index):
        if agent_index == 0:  # Pacman's turn (MAX)
            if depth == self.depth:  # Root level - return action
                best_score = float("-inf")
                best_action = Directions.STOP

                # ใช้ generatePacmanSuccessors เพื่อให้ engine นับ expanded ได้ + เอา "คะแนนจริงของ successor" มาเป็นตัวจัดลำดับ
                successors = state.generatePacmanSuccessors()
                if not successors:
                    return Directions.STOP
            
                # จัดลำดับ: เอาสถานะที่ "ได้คะแนนมากกว่า" (เช่น กินเม็ดได้ทันที) มาก่อน
                successors.sort(key=lambda sa: sa[0].getScore(), reverse=True)
            
                for succ, action in successors:
                    score = self.min_value(succ, depth, 1)
            
                    # 1) เกณฑ์หลัก: เอาคะแนนมากสุด
                    take = score > best_score
            
                    # 2) tie-break: คะแนนเท่ากัน → ชอบ "คงทิศเดิม" มากกว่า
                    if score == best_score and action == self.last:
                        take = True
            
                    # 3) tie-break เพิ่มเติม: คะแนนเท่ากัน → เลี่ยง "ย้อนทิศ" ถ้ามีตัวเลือกอื่น
                    if score == best_score and action == self._reverse_of(self.last):
                        # ถ้าเจอทางอื่นเท่ากันที่ไม่ย้อน ให้ข้ามอันนี้
                        continue
            
                    if take:
                        best_score, best_action = score, action
            
                self.last = best_action
                return best_action

            else:
                return self.max_value(state, depth)
        else:
            return self.min_value(state, depth, agent_index)
    
    def _reverse_of(self, a):
        rev = {Directions.NORTH: Directions.SOUTH,
           Directions.SOUTH: Directions.NORTH,
           Directions.EAST:  Directions.WEST,
           Directions.WEST:  Directions.EAST}
        return rev.get(a, Directions.STOP)

    
    def evaluation_function(self, state):
        return state.getScore()
    
    def get_and_reset_expanded(self):
        """เมธอดที่ engine เรียกเพื่อดึงจำนวนโหนดและรีเซ็ต"""
        n = self.expanded_nodes
        self.expanded_nodes = 0
        return n