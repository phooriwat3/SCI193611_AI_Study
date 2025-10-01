#!/usr/bin/env python3
"""
Q-Learning Assignment - Grid World Challenge
แบบฝึกหัด Q-learning สำหรับนักเรียน

นักเรียนสามารถดัดแปลงไฟล์นี้เพื่อทำ assignment ต่างๆ
"""

from simple_q_learning import SimpleGridWorld, SimpleQLearning

def assignment_1_basic():
    """
    Assignment 1: Basic Q-Learning
    ให้รัน Q-learning ใน Grid World 4x4 และตอบคำถาม
    """
    print("=== Assignment 1: Basic Q-Learning ===")
    print()
    
    # TODO: สร้าง environment และ agent
    env = SimpleGridWorld(size=4)
    agent = SimpleQLearning(
        n_states=16,
        n_actions=4,
        learning_rate=0.01,
        discount=0.9,
        epsilon=0.1
    )
    
    print("Grid World Setup:")
    env.print_grid()
    
    # TODO: ฝึก agent
    print("Training...")
    agent.train(env, episodes=500)
    
    # TODO: ทดสอบและวิเคราะห์ผล
    print("\nTesting trained agent:")
    reward, steps, path = agent.test(env, show_path=False)
    print(f"Total reward: {reward}")
    print(f"Steps taken: {steps}")
    
    # แสดง Q-table บางส่วน
    print("\nQ-Table (first 8 states):")
    print("State |   ↑   |   ↓   |   ←   |   →   ")
    print("-" * 40)
    for state in range(8):
        q_vals = agent.q_table[state]
        print(f"{state:5d} | {q_vals[0]:5.2f} | {q_vals[1]:5.2f} | {q_vals[2]:5.2f} | {q_vals[3]:5.2f}")
    
    print("\n--- Questions for Assignment 1 ---")
    print("1. อธิบายทำไม Q-value ของ state ที่ใกล้ goal มีค่าสูงกว่า")
    print("2. ทำไม epsilon-greedy policy สำคัญในการเรียนรู้")
    print("3. ลองเปลี่ยน learning rate เป็น 0.01 และ 0.5 แล้วเปรียบเทียบผล")
    print("-"*20)
    print("1. Ans: เพราะรางวัลจาก goal จะถูกส่งย้อนกลับมายัง state ก่อนหน้า ทำให้ state ที่อยู่ใกล้ goal มีค่าสูงตามไปด้วย เช่น state 8 คือ goal เเละ agents กำลังอยู่ state 7 มันจะตัดสินใจว่าถ้าเดินไป sate 8 จะได้รับ goal ดังนั้นค่า Q-value ของ sate 7 จึงสูงขึ้น")
    print("2. Ans: เพื่อสร้างสมดุลระหว่าง การใช้ทางที่ดีที่สุดที่รู้ (Exploit) กับ การลองเส้นทางใหม่ๆ (Explore) ป้องกันไม่ให้ agent ติดอยู่กับเส้นทางที่ไม่ดีที่สุด")
    print("3. Ans: Learning Rate = 0.01 จะเชื่อข้อมูลเก่ามากกว่าข้อมูลใหม่ที่เพิ่งเจอ ทำให้ Q-table เปลี่ยนแปลงทีละน้อย  Agent ยังหาทางไปถึง goal ได้ไม่ดีนัก ได้ reward ต่ำ\n        Learning Rate = 0.5 Agent ให้น้ำหนักกับข้อมูลใหม่มากๆ ทำให้ Q-table เปลี่ยนแปลงอย่างรวดเร็ว แต่ผลลัพธ์ที่ได้อาจไม่สม่ำเสมอ หรืออาจจะได้ค่า reward ที่ไม่สูงที่สุด เพราะการอัปเดตที่รุนแรงเกินไป")
    
def assignment_2_parameter_study():
    """1
    
    Assignment 2: Parameter Study
    ศึกษาผลของพารามิเตอร์ต่างๆ ต่อการเรียนรู้
    """
    print("=== Assignment 2: Parameter Study ===")
    print()
    
    # ทดลองกับ learning rates ต่างๆ
    learning_rates = [0.01, 0.1, 0.3, 0.7]
    print("Testing different learning rates:")
    
    for lr in learning_rates:
        env = SimpleGridWorld(size=4)
        agent = SimpleQLearning(
            n_states=16,
            n_actions=4,
            learning_rate=lr,
            discount=0.9,
            epsilon=0.1
        )
        
        agent.train(env, episodes=500)
        reward, steps, _ = agent.test(env, show_path=False)
        
        print(f"Learning Rate {lr}: Final reward = {reward:.2f}, Steps = {steps}")
    
    print("\n--- Questions for Assignment 2 ---")
    print("1. Learning rate ไหนให้ผลดีที่สุด? ทำไม?")
    print("2. ลองทดลองกับ epsilon values: 0.01, 0.1, 0.3, 0.7")
    print("3. ลองทดลองกับ discount factor: 0.5, 0.7, 0.9, 0.99")
    print("-"*20)
    print("1. Ans: ประมาณ 0.1 ถึง 0.3 เพราะสมดุล ไม่ช้าและไม่เร็วเกินไป")
    print("2. Ans: Epsilon น้อยไป: ไม่กล้าลองทางใหม่ อาจติดอยู่กับเส้นทางที่ไม่ดี\n        Epsilon มากไป: เดินสุ่มมั่วเกินไป ทำให้เรียนรู้ช้า")
    print("3. Ans: Gamma สูง (0.9, 0.99): เหมาะกับปัญหานี้ เพราะทำให้ Agent มองการณ์ไกล ไปถึงรางวัลที่ Goal")

def assignment_3_environment_design():
    """
    Assignment 3: Environment Design
    ออกแบบ environment ใหม่และทดสอบ
    """
    print("=== Assignment 3: Environment Design ===")
    print()
    
    # TODO: ให้นักเรียนสร้าง environment ใหม่
    # ตัวอย่าง: Grid World ขนาดใหญ่กว่า หรือมีอุปสรรคมากกว่า
        
    class CustomGridWorld(SimpleGridWorld):
        def __init__(self):
            super().__init__(size=5)
            # เพิ่มอุปสรรคใหม่
            self.obstacles = [(2, 1), (2, 2), (2, 3), (2, 4)] #  เพิ่มกำแพงตรงกลางบังคับให้ Agent ต้องเดินอ้อม
            # เปลี่ยน reward structure
            self.goal_reward = 50 # เพิ่มรางวัล goal ให้สูงขึ้น
            self.obstacle_penalty = -10
    
    env = CustomGridWorld()
    print("Custom Grid World:")
    env.print_grid()
    
    agent = SimpleQLearning(
    n_states=25,  # 5x5 = 25
    n_actions=4,
    learning_rate=0.1,
    discount=0.9,
    epsilon=0.2
)
    
    agent.train(env, episodes=1000)
    reward, steps, _ = agent.test(env, show_path=False)
    print(f"Custom environment result: Reward = {reward:.2f}, Steps = {steps}")
    
    print("\n--- Tasks for Assignment 3 ---")
    print("1. ออกแบบ Grid World ของคุณเอง (ขนาด, อุปสรรค, rewards)")
    print("2. เปรียบเทียบผลการเรียนรู้กับ standard environment")
    print("3. วิเคราะห์ว่า environment design ส่งผลต่อ learning อย่างไร")
    print("-"*20)
    print("1. Ans: ขนาด: 6x6, อุปสรรค: เพิ่มกำแพงตรงกลาง, rewards: 50")
    print("2. Ans: world ใหญ่ขึ้น, อุปสรรคเยอะขึ้น  Agent เรียนรู้ได้ช้าลง และต้องใช้จำนวน episodes ในการฝึกมากกว่าเดิม")
    print("3. Ans: Grid World ใหญ่ จำนวน states ก็จะยิ่งเพิ่มขึ้น ทำให้ Q-table ใหญ่ตามไปด้วย Agent ต้องใช้เวลาสำรวจนานขึ้นมากกว่าจะเก็บข้อมูลได้ครบถ้วน")


def assignment_4_advanced():
    """
    Assignment 4: Advanced Modifications
    การปรับปรุง algorithm หรือเพิ่มฟีเจอร์ใหม่
    """
    print("=== Assignment 4: Advanced Modifications ===")
    print()
    
    # TODO: ให้นักเรียนเลือกหัวข้อที่สนใจ
    
    print("Choose one of the following topics:")
    print("1. Implement SARSA algorithm และเปรียบเทียบกับ Q-Learning")
    print("2. Add epsilon decay strategy ที่ซับซ้อนกว่า")
    print("3. Implement Double Q-Learning")
    print("4. Add experience replay")
    print("5. Create multi-goal environment")
    print("6. Implement priority sweeping")
    
    print("=== Topic 5: Create multi-goal environment ===")
    print()

    # --- Step 1: ออกแบบ Environment ที่มีหลายเป้าหมาย ---
    # เราจะสร้าง Grid World ขนาด 5x5 ที่มีเป้าหมาย 2 แห่ง
    # Goal 1: อยู่ใกล้ แต่ให้รางวัลน้อย (+20)
    # Goal 2: อยู่ไกลกว่า และมีอุปสรรคขวาง แต่ให้รางวัลสูง (+100)
    
    # Import SimpleGridWorld มาเพื่อสืบทอดคุณสมบัติ
    from simple_q_learning import SimpleGridWorld

    class MultiGoalGridWorld(SimpleGridWorld):
     """
     Grid World หลายเป้าหมาย (รางวัลต่างกัน)
     - G1: (2,4) +20
     - G2: (4,4) +100
     - สิ่งกีดขวาง: (3,2), (3,3), (3,4)
     """
    def __init__(self, size=5):
        super().__init__(size=size)

        # ตำแหน่งเริ่มต้น agent
        self.start_pos = (0, 0)
        self.agent_pos = self.start_pos

        # เป้าหมายและรางวัล
        self.goals = {
            (2, 4): 20,   # ใกล้กว่ารางวัลน้อย
            (4, 4): 100   # ไกลกว่าแต่รางวัลสูง
        }

        # สิ่งกีดขวาง
        self.obstacles = [(3, 2), (3, 3), (3, 4)]

        # กำหนด penalty/step reward ให้ชัดเจน (กันพลาดชื่อไม่ตรงกับคลาสฐาน)
        self.step_penalty = -1        # รางวัลสำหรับการเดินปกติแต่ละก้าว
        self.obstacle_penalty = -10   # ชนกำแพงโดนปรับ
        # บาง implementation ใช้ชื่ออื่น ลองแมปให้ด้วยเผื่อไว้
        if not hasattr(self, "move_penalty"):
            self.move_penalty = self.step_penalty

        # ปิดการใช้ goal_state เดิมของคลาสฐาน (เรามีหลาย goal)
        self.goal_state = None

    def reset(self):
        """รีเซ็ต episode แล้วคืนค่า state เริ่มต้น"""
        self.agent_pos = self.start_pos
        return self.pos_to_state(self.agent_pos)

    def pos_to_state(self, pos):
        """map (row, col) -> state index [0..size*size-1]"""
        return pos[0] * self.size + pos[1]

    def step(self, action):
        """
        รับ action -> (next_state, reward, done)
        0:↑ 1:↓ 2:← 3:→
        """
        row, col = self.agent_pos

        # คำนวณตำแหน่งใหม่ตามขอบเขต
        if action == 0:      # Up
            row = max(0, row - 1)
        elif action == 1:    # Down
            row = min(self.size - 1, row + 1)
        elif action == 2:    # Left
            col = max(0, col - 1)
        elif action == 3:    # Right
            col = min(self.size - 1, col + 1)

        new_pos = (row, col)

        # ถ้าชนสิ่งกีดขวาง: อยู่ที่เดิม + โทษ
        if new_pos in self.obstacles:
            next_state = self.pos_to_state(self.agent_pos)
            return next_state, self.obstacle_penalty, False

        # อัปเดตตำแหน่ง
        self.agent_pos = new_pos
        next_state = self.pos_to_state(self.agent_pos)

        # ถ้าไปถึงเป้าหมายใดเป้าหมายหนึ่ง -> จบ episode
        if self.agent_pos in self.goals:
            reward = self.goals[self.agent_pos]
            return next_state, reward, True

        # เดินปกติ
        return next_state, self.step_penalty, False

    def print_grid(self):
        """พิมพ์กริด แสดง A/G/X/."""
        for r in range(self.size):
            row_str = ""
            for c in range(self.size):
                pos = (r, c)
                if pos == self.agent_pos:
                    row_str += " A "
                elif pos in self.goals:
                    row_str += " G "
                elif pos in self.obstacles:
                    row_str += " X "
                else:
                    row_str += " . "
            print(row_str)
             
        
    # --- Step 2: สร้าง Environment และ Agent ---
    env = MultiGoalGridWorld(size=5)
    agent = SimpleQLearning(
        n_states=25,       # 5x5 grid
        n_actions=4,
        learning_rate=0.1,
        discount=0.95,     # gamma สูงเพื่อให้มองการณ์ไกล
        epsilon=0.1
    )

    print("Multi-Goal Grid World Setup:")
    print("A = Agent, G = Goal, X = Obstacle")
    print("Goal at (2, 4) gives +20 reward.")
    print("Goal at (4, 4) gives +100 reward.")
    env.print_grid()
    print("-" * 20)

    # --- Step 3: ฝึก Agent ---
    # ต้องการจำนวน episode ที่มากขึ้นเพื่อให้ Agent เรียนรู้สถานการณ์ที่ซับซ้อน
    print("Training agent in the multi-goal environment...")
    agent.train(env, episodes=3000)
    print("Training complete.")

    # --- Step 4: ทดสอบและวิเคราะห์ผล ---
    print("\nTesting trained agent:")
    # เราจะเริ่ม agent ที่ (0,0) เพื่อดูว่ามันเลือกเส้นทางไหน
    env.agent_pos = (0,0) 
    reward, steps, path = agent.test(env, show_path=True)
    
    print(f"\nPath taken: {path}")
    print(f"Total reward: {reward}")
    print(f"Steps taken: {steps}")

    print("\n--- Analysis for Multi-Goal Environment ---")
    print("1. ผลลัพธ์ที่คาดหวังคืออะไร?")
    print("   - Agent ควรจะเรียนรู้ที่จะเพิกเฉยต่อเป้าหมายที่ให้รางวัลน้อย (+20) แม้จะอยู่ใกล้กว่า")
    print("   - และควรเลือกเดินทางอ้อมอุปสรรคเพื่อไปยังเป้าหมายที่ให้รางวัลสูงสุด (+100) แทน")
    print("\n2. ทำไม Agent ถึงเลือกเส้นทางนั้น?")
    print("   - เพราะ Q-Learning มี Discount Factor (gamma) ซึ่งทำให้รางวัลในอนาคตมีค่า")
    print("   - แม้ว่าการเดินทางไปเป้าหมายไกลจะใช้หลาย step (โดน step_penalty หลายครั้ง) แต่รางวัลตอนท้าย (+100) เมื่อถูกคิดลดทอนกลับมาแล้ว ก็ยังคงมีค่า (Value) สูงกว่าเส้นทางที่ไปสู่รางวัล +20")
    print("   - Agent จึงไม่ได้เลือกทางที่ให้รางวัลทันที แต่เลือกทางที่ให้ 'ผลตอบแทนรวมสูงสุดในระยะยาว' (Maximum Expected Future Reward)")
    print("\n3. ผลการทดลองสอดคล้องกับที่คาดหวังหรือไม่?")
    if reward > 50:
         print("   - 'ใช่' Agent ได้รางวัลสูง แสดงว่ามันเลือกไปที่เป้าหมาย +100 สำเร็จ ซึ่งพิสูจน์ว่ามันสามารถตัดสินใจเลือกเป้าหมายที่ให้ผลตอบแทนดีที่สุดได้")
    else:
         print("   - 'อาจจะไม่' Agent ได้รางวัลน้อย แสดงว่ามันอาจจะยังเรียนรู้ไม่ดีพอ หรือติดอยู่ที่เป้าหมายแรก อาจต้องเพิ่มจำนวน episodes ในการฝึก หรือปรับ learning rate/epsilon")


def bonus_visualization():
    """
    Bonus: Enhanced Visualization
    การแสดงผลที่สวยงามขึ้น (สำหรับนักเรียนที่สนใจ)
    """
    print("=== Bonus: Enhanced Visualization ===")
    print()
    
    # TODO: ใช้ matplotlib สร้างกราฟ learning curve
    # TODO: สร้าง animation ของการเรียนรู้
    # TODO: แสดง heatmap ของ Q-values
    import math
    print("=== Bonus: Enhanced Visualization ===\n")

    # ฝึกสั้น ๆ เพื่อให้มี Q-table ใช้งาน
    env = SimpleGridWorld(size=5)
    agent = SimpleQLearning(n_states=25, n_actions=4, learning_rate=0.1, discount=0.9, epsilon=0.2)
    rewards = agent.train(env, episodes=400)

    # 1) Learning curve
    try:
        import matplotlib.pyplot as plt
        if rewards is not None:
            plt.figure(figsize=(9, 4))
            plt.plot(rewards)
            plt.title('Learning Curve (Total Reward per Episode)')
            plt.xlabel('Episode')
            plt.ylabel('Total Reward')
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        else:
            print("(train() ไม่คืน rewards — ข้ามกราฟ learning curve)")
    except Exception:
        print("(ไม่มี matplotlib — ข้ามกราฟ learning curve)")

    # 2) Heatmap ของค่า V(s) = max_a Q(s,a)
    q = agent.q_table
    v = [max(row) for row in q]
    size = int(math.sqrt(len(v)))
    try:
        import matplotlib.pyplot as plt
        data = [[v[r*size+c] for c in range(size)] for r in range(size)]
        plt.figure(figsize=(4.5, 4))
        plt.imshow(data, interpolation='nearest')
        plt.title('State Value Heatmap (max Q)')
        plt.colorbar(label='Value')
        plt.xticks(range(size))
        plt.yticks(range(size))
        plt.tight_layout()
        plt.show()
    except Exception:
        print("ASCII Heatmap (approx.):")
        chars = " .:-=+*#%@"
        mx, mn = max(v), min(v)
        span = (mx - mn) if mx != mn else 1.0
        for r in range(size):
            row = ''
            for c in range(size):
                val = v[r*size+c]
                idx = int((val - mn) / span * (len(chars) - 1))
                row += chars[idx]
            print(row)

    # 3) Policy visualization
    arrows = {0: '↑', 1: '↓', 2: '←', 3: '→'}
    policy = [max(range(4), key=lambda a: agent.q_table[s][a]) for s in range(agent.n_states)]
    print("\nPolicy (greedy argmax Q):")
    for r in range(size):
        line = ' '.join(arrows[policy[r*size + c]] for c in range(size))
        print(line)

    print("\n(เสร็จสิ้น Bonus Visualization)")

def main():
    """เลือก assignment ที่จะทำ"""
    print("🎓 Q-Learning Assignments")
    print("=========================")
    print()
    
    assignments = {
        '1': assignment_1_basic,
        '2': assignment_2_parameter_study,
        '3': assignment_3_environment_design,
        '4': assignment_4_advanced,
        '5': bonus_visualization
    }
    
    while True:
        print("Available assignments:")
        print("1. Basic Q-Learning (เริ่มต้น)")
        print("2. Parameter Study (ศึกษาพารามิเตอร์)")
        print("3. Environment Design (ออกแบบ environment)")
        print("4. Advanced Modifications (ขั้นสูง)")
        print("5. Bonus: Visualization (เสริม)")
        print("6. Exit")
        print()
        
        choice = input("เลือก assignment (1-6): ").strip()
        
        if choice in assignments:
            print()
            assignments[choice]()
            print("\n" + "="*50 + "\n")
        elif choice == '6':
            print("Good luck with your assignments! 🚀")
            break
        else:
            print("กรุณาเลือก 1-6")

if __name__ == "__main__":
    main()
