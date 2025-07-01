---
marp: true
math: mathjax
---

<!-- .slide: class="middle,center,title-slide" -->

# Introduction to Artificial Intelligence

Lecture 1: Intelligent agents

<br><br>
Ittipon Fongkaew  


---

<!-- .slide: class="middle" -->

# Intelligent agents

---

# Agents and environments

<br><br><br>

<div style="display: flex; align-items: center; justify-content: center;">
  <div style="flex:1; text-align: center;"><br><br><br>Percepts $s$</div>
  <div style="flex:2; text-align: center;"><img src="figures/lec8/loop.png" style="width:95%;" /></div>
  <div style="flex:1; text-align: center;"><br><br><br>Actions $a$</div>
</div>

<!--  
ตัวอย่าง Roomba  
-->

---

<!-- .slide: class="middle" -->

## Agents

- **Agent** คือสิ่งที่ *รับรู้* สภาพแวดล้อมของมันผ่านทาง sensor และ  
  ทำ *action* ผ่านทาง actuator

- พฤติกรรมของ agent อธิบายได้ด้วย **policy** ซึ่งเป็นฟังก์ชัน

$$
\pi : \mathcal{P}^* \to \mathcal{A}
$$

ที่แมปลำดับ percept ไปยัง action

---

<!-- .slide: class="middle" -->

## Simplified Pacman world

<div align="center"><img src="figures/lec1/pacman.png" style="width:20%;" /></div>

ลองพิจารณาโลก 2 ช่อง ที่มี agent Pacman  
- Percept: ตำแหน่งและเนื้อหา เช่น $(\text{left cell}, \text{no food})$
- Action: $\text{go left}$, $\text{go right}$, $\text{eat}$, $\text{do nothing}$

<!--  
อธิบายให้ชัดเจนว่าเกมนี้แตกต่างจาก Pacman จริง  
-->

---

<!-- .slide: class="middle" -->

## Pacman agent

Policy ของ Pacman agent คือฟังก์ชันที่แมปลำดับ percept ไปยัง action ซึ่งสามารถสร้างเป็นตารางได้

| Percept sequence                                              | Action            |
|---------------------------------------------------------------|-------------------|
| $(\text{left cell}, \text{no food})$                         | $\text{go right}$ |
| $(\text{left cell}, \text{food})$                            | $\text{eat}$      |
| $(\text{right cell}, \text{no food})$                        | $\text{go left}$  |
| $(\text{left cell}, \text{food})$                            | $\text{eat}$      |
| $(\text{left cell}, \text{no food}), (\text{left cell}, \text{no food})$ | $\text{go right}$ |
| $(\text{left cell}, \text{no food}), (\text{left cell}, \text{food})$    | $\text{eat}$      |
| (...)                                                        | (...)             |

---

<!-- .slide: class="middle,center,black-slide" -->

<img src="figures/lec1/pacman-world.jpg" style="width:100%;" />

แล้ว Pacman จริงล่ะ?

<!--  
ลองรันโปรแกรม!  
-->

---

<!-- .slide: class="middle" -->

## The optimal policy?

policy ที่เหมาะสมที่สุดของ agent คืออะไร?

จะนิยามเป้าหมายของ Pacman อย่างไร?
- ได้ 1 แต้มต่อการกิน food dot แต่ละอันจนถึงเวลา $t$?
- ได้ 1 แต้มต่อ food dot ที่กิน, ลบ 1 แต้มต่อ move?
- ลงโทษหากเหลือ food dot ไม่ถูกกินมากเกินไป?

สามารถ implement ใน agent program ขนาดเล็กและมีประสิทธิภาพได้หรือไม่?

---

# Rational agents

- performance measure ประเมินลำดับสถานะของสภาพแวดล้อมที่เกิดจากพฤติกรรม agent
- rational agent คือ agent ที่เลือก action ที่ **maximize**  
  *expected* value ของ performance measure ตาม percept sequence ที่ได้รับมาจนถึงตอนนี้

> Rationality สนใจแค่ **what** ตัดสินใจอะไร (ไม่ใช่ขั้นตอนความคิดแบบมนุษย์)

<sub>Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.</sub>

---

<!-- .slide: class="middle" -->

<div align="center"><img src="figures/lec0/max-utility.png" /></div>

ในคอร์สนี้ Artificial intelligence = **Maximizing expected performance**

<sub>Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.</sub>

<!--  
เน้นความสำคัญของ expected  
-->

---

<!-- .slide: class="middle" -->

- Rationality $\neq$ omniscience  
    - percept อาจจะไม่บอกข้อมูลที่จำเป็นทั้งหมด
- Rationality $\neq$ clairvoyance  
    - ผลลัพธ์ของ action อาจไม่เป็นตามที่คาด
- ดังนั้น rational $\neq$ สำเร็จเสมอ
- แต่ rationality นำไปสู่ *exploration*, *learning* และ *autonomy*

---

# Performance, environment, actuators, sensors

ลักษณะของ performance measure, environment, action space และ percept  
กำหนดแนวทางในการเลือก rational action  
ทั้งหมดนี้รวมเรียกว่า **task environment**

## ตัวอย่าง 1: agent เล่นหมากรุก
- performance measure: ชนะ, เสมอ, แพ้, ...
- environment: กระดาน, คู่ต่อสู้, ...
- actuator: ขยับตัวหมาก, ...
- sensor: สถานะกระดาน, การเดินของคู่ต่อสู้, ...

---

<!-- .slide: class="middle" -->

## ตัวอย่าง 2: รถยนต์ไร้คนขับ
- performance measure: ความปลอดภัย, ถึงจุดหมาย, ความถูกต้องตามกฎหมาย, ความสบาย, ...
- environment: ถนน, ทางหลวง, การจราจร, คนเดินถนน, สภาพอากาศ, ...
- actuator: พวงมาลัย, คันเร่ง, เบรก, แตร, ลำโพง, จอแสดงผล, ...
- sensor: กล้อง, accelerometer, gauge, เซนเซอร์เครื่องยนต์, GPS, ...

## ตัวอย่าง 3: ระบบวินิจฉัยทางการแพทย์
- performance measure: สุขภาพผู้ป่วย, ค่าใช้จ่าย, เวลา, ...
- environment: ผู้ป่วย, โรงพยาบาล, ประวัติแพทย์, ...
- actuator: วินิจฉัย, รักษา, ส่งต่อ, ...
- sensor: ประวัติแพทย์, ผลแลป, ...

---

# Environment types

*Fully observable* vs. **partially observable**  
> sensor ของ agent ให้ข้อมูลครบถ้วนของสถานะ environment ณ เวลานั้นหรือไม่

*Deterministic* vs. **stochastic**  
> สถานะถัดไปถูกกำหนดโดยสถานะปัจจุบันและ action ของ agent หรือไม่

*Episodic* vs. **sequential**  
> ประสบการณ์ของ agent แบ่งเป็น episode อิสระหรือไม่

*Static* vs. **dynamic**  
> environment เปลี่ยนแปลงได้หรือไม่ หรือ performance measure เปลี่ยนตามเวลา

---

<!-- .slide: class="middle" -->

*Discrete* vs. **continuous**  
> สถานะ environment, เวลา, percept หรือ action เป็นค่าต่อเนื่องหรือไม่

*Single agent* vs. **multi-agent**  
> environment มี agent หลายตัวที่มีปฏิสัมพันธ์กันหรือไม่

*Known* vs **unknown**  
> agent มีความรู้เกี่ยวกับ "กฎฟิสิกส์" ของ environment หรือไม่

---

<!-- .slide: class="middle" -->

Task environment ต่อไปนี้ fully observable หรือไม่? deterministic? episodic?  
static? discrete? single agent? known?

- Crossword puzzle
- Chess พร้อมนาฬิกา
- Poker
- Backgammon
- ขับรถแท็กซี่
- การวินิจฉัยโรค
- วิเคราะห์ภาพ
- หุ่นยนต์หยิบชิ้นส่วน
- refinery controller
- โลกจริง

---

<!-- .slide: class="middle,center,black-slide" -->

<img src="figures/lec1/pacman-world.jpg" style="width:100%;" />

Pacman ล่ะ?

---

# Agent programs

เป้าหมายของเราคือออกแบบ **agent program** ที่ implement agent policy

agent program สามารถออกแบบและ implement ได้หลายแบบ เช่น

- ตาราง
- กฎ (rules)
- อัลกอริทึมค้นหา (search algorithm)
- อัลกอริทึมเรียนรู้ (learning algorithm)

---

# Reflex agents

Reflex agent ...
- เลือก action จาก percept ปัจจุบัน (อาจจะใช้ memory ด้วย);
- อาจจะมี memory หรือแบบจำลอง world state;
- ไม่พิจารณาผลในอนาคตของ action ที่เลือก

<br>
<div align="center" style="width:50%"><img src="figures/lec1/reflex-agent-cartoon.png" /></div>

<sub>Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.</sub>

---

<!-- .slide: class="middle" -->

## Simple reflex agents

<div align="center" style="width:80%"><img src="figures/lec1/simple-reflex-agent.svg" /></div>

<!--  
วิธีแก้ปัญหาตารางขนาดใหญ่: ลืมอดีตไปเลย!  
ใช้กฎ condition-action ในการบีบอัดตาราง  
-->

---

<!-- .slide: class="middle" -->

- *Simple reflex agent* เลือก action จาก percept ปัจจุบัน  
  โดยไม่สนใจประวัติ percept ที่ผ่านมา
- พวกเขาใช้ **condition-action rules** แมทช์ percept ปัจจุบันกับ action  
  กฎช่วยให้ย่อขนาดฟังก์ชันลงได้
- ทำงานได้ดีเฉพาะใน *Markovian* environment คือ ตัดสินใจได้จาก percept ปัจจุบันเพียงอย่างเดียว  
  หมายถึง environment ต้อง fully observable

<!--  
ตัวอย่าง (รถยนต์อัตโนมัติ): ถ้ารถข้างหน้าชะลอ ให้เบรก  
สีรถ, ยี่ห้อ, เพลงที่เปิด, หรือสภาพอากาศไม่เกี่ยวข้อง  
-->

---

<!-- .slide: class="middle" -->

## Model-based reflex agents

<div align="center" style="width:80%"><img src="figures/lec1/model-based-reflex-agent.svg" /></div>

<!--  
วิธีแก้: ไม่ต้องลืมอดีต เก็บ internal representation (belief state)  
จากสิ่งที่เห็นในอดีต แล้วใช้ state นี้ map ไปยัง action  
-->

---

<!-- .slide: class="middle" -->

- *Model-based agent* รับมือกับ partial observability โดยเก็บ internal state  
  เพื่อติดตามส่วนที่มองไม่เห็นใน environment
- internal state จะถูกอัปเดตตาม **model** ที่บอกว่า  
  - environment เปลี่ยนแปลงอย่างไรหากไม่มี agent  
  - agent ทำ action ใดมีผลต่อโลกอย่างไร

---

# Planning agents

Planning agent ...
- ถามว่า "what if?"
- ตัดสินใจโดยพิจารณาผล (ที่คาดการณ์) ของ action;
- ต้องมี model ของ environment ว่าเปลี่ยนแปลงอย่างไรเมื่อลงมือทำ action
- ต้องนิยามเป้าหมาย (goal)

<br>
<div align="center" style="width:50%"><img src="figures/lec1/plan-agent-cartoon.png" /></div>

<sub>Credits: [CS188](https://inst.eecs.berkeley.edu/~cs188/), UC Berkeley.</sub>

---

<!-- .slide: class="middle" -->

## Goal-based agents

<div align="center" style="width:80%"><img src="figures/lec1/goal-based-agent.svg" /></div>

<!--  
ไม่ง่ายที่จะ map state ไปยัง action เพราะ goal ไม่ได้แสดงเป็นกฎ condition-action  
-->

---

<!-- .slide: class="middle" -->

- กระบวนการตัดสินใจ:
    1. สร้างลำดับ action ที่เป็นไปได้
    2. ทำนาย state ที่จะตามมา
    3. ประเมิน **goal** ของแต่ละ state
- *Goal-based agent* เลือก action ที่จะทำให้บรรลุ goal
    - ทั่วไปกว่ากฎ (rules) เพราะ goal มักไม่แสดงในกฎ
    - การหาลำดับ action ที่จะบรรลุเป้าหมายทำได้ยาก  
      ต้องใช้ *search* หรือ *planning*

---

<!-- .slide: class="middle" -->

## Utility-based agents

<div align="center" style="width:80%"><img src="figures/lec1/utility-based-agent.svg" /></div>

<!--  
หลายครั้ง มี action sequence หลายแบบที่บรรลุเป้าหมาย  
เราควรเลือกสิ่งที่ "ดีที่สุด"  
-->

---

<!-- .slide: class="middle" -->

- *Goal* มักไม่เพียงพอที่จะสร้างพฤติกรรมที่มีคุณภาพสูง  
  goal ให้การประเมินเป็นแค่ binary (สำเร็จ/ไม่สำเร็จ)
- **Utility function** ให้คะแนนลำดับสถานะ environment  
    - utility function คือการ internalize performance measure
- rational utility-based agent เลือก action ที่ **maximize expected utility** ของผลลัพธ์

<!--  
ตัวอย่าง (รถยนต์อัตโนมัติ): เส้นทางไปถึงที่หมายมีหลายเส้น แต่บางเส้นเร็วกว่า/ปลอดภัยกว่า  
-->

---

# Learning agents

<br>
<div align="center" style="width:80%"><img src="figures/lec1/learning-agent.svg" /></div>

---

<!-- .slide: class="middle" -->

- *Learning agent* มีความสามารถในการ **self-improvement**  
  สามารถเก่งขึ้นกว่าความรู้เริ่มต้นของตนเอง
- ปรับเปลี่ยน knowledge component ได้โดย:
    - เรียนรู้ว่า *โลก* เปลี่ยนแปลงอย่างไร
    - เรียนรู้ผลของ action
    - เรียนรู้ utility ของ action ผ่าน *reward*

---

<!-- .slide: class="middle" -->

## A learning autonomous car

- *Performance element*:  
    - ระบบปัจจุบันที่เลือก action และขับรถ
- *Critic* สังเกตสภาพแวดล้อมแล้วส่งข้อมูลไปยัง *learning element*
    - เช่น รถเลี้ยวซ้ายเร็วข้าม 3 เลน critic ได้ยินคำสบถจากผู้ขับอื่นและแจ้งว่าเป็น bad action
    - learning element พยายามปรับปรุง performance element เพื่อไม่ให้เกิดเหตุการณ์นี้อีก
- *Problem generator* ชี้จุดพฤติกรรมที่ควรปรับปรุง และเสนอให้ทดลอง
    - เช่น ทดลองเบรกบนถนนหลากหลายสภาพอากาศ

---

# Summary

- **Agent** คือสิ่งที่รับรู้และกระทำใน environment
- *Performance measure* ประเมินพฤติกรรมของ agent  
  **Rational agent** เลือก action เพื่อ maximize expected value ของ performance measure
- *Task environment* ประกอบด้วย performance measure, environment, actuator, sensor  
  มีมิติสำคัญที่หลากหลาย
- **Agent program** คือสิ่งที่ implement agent function การออกแบบขึ้นกับ task environment
- *Simple reflex agent* ตอบสนองโดยตรงต่อ percept  
  *Model-based reflex agent* มี internal state เพื่อติดตามโลก  
  *Goal-based agent* กระทำเพื่อบรรลุเป้าหมาย  
  **Utility-based agent** maximize expected performance
- ทุก agent สามารถพัฒนาตนเองได้ผ่าน **learning**

<!--  
สัปดาห์หน้าเราจะได้เห็นวิธีสร้าง agent ตัวแรก: goal-based agent ด้วย search algorithm  
-->

---

<!-- .slide: class="end-slide,center" -->
<!-- count: false -->

The end. 