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
        n_states=36, # ขนาด: 6x6
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
    """class DoubleQLearning(SimpleQLearning):
if v > best:
best, b_star = v, a
target = reward + (0.0 if done else self.gamma * self.q_a[next_state][b_star])
td = target - self.q_b[state][action]
self.q_b[state][action] += self.lr * td


state = next_state
if done:
break
episode_rewards.append(total)
# สร้าง q_table รวมเพื่อความเข้ากันได้ตอน test()
self.q_table = [[self.q_a[s][a] + self.q_b[s][a] for a in range(self.n_actions)]
for s in range(self.n_states)]
return episode_rewards if return_rewards else None

    """
    print("\nExample: Simple SARSA Implementation")
    
    class SARSAAgent(SimpleQLearning):
        """SARSA Agent - On-policy learning"""
        
        def train_episode(self, env, max_steps=100):
            state = env.reset()
            action = self.get_action(state)  # เลือก action แรก
            total_reward = 0
            
            for _ in range(max_steps):
                next_state, reward, done = env.step(action)
                next_action = self.get_action(next_state) if not done else 0
                
                # SARSA update: ใช้ actual next action แทน max
                target = reward + self.gamma * self.q_table[next_state][next_action]
                error = target - self.q_table[state][action]
                self.q_table[state][action] += self.lr * error
                
                total_reward += reward
                state, action = next_state, next_action
                
                if done:
                    break
            
            return total_reward, 0
    
    print("SARSA vs Q-Learning comparison example implemented above.")

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
    """ try:
import matplotlib.pyplot as plt
import numpy as np
has_mpl = True
except Exception:
has_mpl = False


# สร้าง/ฝึกโมเดลสั้น ๆ เพื่อดึง Q-table มาแสดง
env = SimpleGridWorld(size=5)
agent = SimpleQLearning(n_states=25, n_actions=4, learning_rate=0.1, discount=0.9, epsilon=0.2)
rewards = agent.train(env, episodes=400) # ถ้า train() ไม่คืน rewards ก็จะเป็น None


# 1) Learning curve
if has_mpl and rewards is not None:
plt.figure(figsize=(9, 4))
plt.plot(rewards)
plt.title('Learning Curve (Total Reward per Episode)')
plt.xlabel('Episode')
plt.ylabel('Total Reward')
plt.grid(True)
plt.tight_layout()
try:
plt.show()
except Exception:
print("(แสดงกราฟไม่สำเร็จบนสภาพแวดล้อมนี้)")
else:
print("(ไม่มี matplotlib หรือ train() ไม่คืน rewards — ข้ามกราฟ learning curve)")


# 2) Heatmap ของค่า V(s) = max_a Q(s,a)
q = agent.q_table
v = [max(row) for row in q]
size = int(math.sqrt(len(v)))
if has_mpl:
data = [[v[r*size+c] for c in range(size)] for r in range(size)]
plt.figure(figsize=(4.5, 4))
plt.imshow(data, interpolation='nearest')
plt.title('State Value Heatmap (max Q)')
plt.colorbar(label='Value')
plt.xticks(range(size))
plt.yticks(range(size))
plt.tight_layout()
try:
plt.show()
except Exception:
print("(แสดง heatmap ไม่สำเร็จบนสภาพแวดล้อมนี้)")
else:
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
print(row)"""
    print("Ideas for enhanced visualization:")
    print("1. Plot learning curves with matplotlib")
    print("2. Create heatmap of Q-values")
    print("3. Animate the learning process")
    print("4. Show value function as 3D surface")
    print("5. Create policy visualization with arrows")
    
    print("\nSample code for learning curve:")
    print("""
import matplotlib.pyplot as plt

def plot_learning_curve(episode_rewards):
    plt.figure(figsize=(10, 6))
    plt.plot(episode_rewards)
    plt.title('Q-Learning Performance')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.grid(True)
    plt.show()
    """)

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
