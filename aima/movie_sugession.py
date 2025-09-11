# 🏆 Challenge: ลองเขียนโค้ดแก้ปัญหาระบบแนะนำหนังด้วยตัวเอง!

# สร้าง symbols (ให้นักเรียนเติมเอง)
# เช่น: ActionJohn, SciFiJohn, MatrixJohn, ComedyMary, etc.
ActionJohn, SciFiJohn, MatrixJohn = expr('ActionJohn, SciFiJohn, MatrixJohn') # John 
ComedyMary, HangoverMary = expr('ComedyMary, HangoverMary')                   # Mary
HorrorTom, ComedyTom, HangoverTom = expr('HorrorTom, ComedyTom, HangoverTom') # Tom

# สร้าง KB
movie_kb = PropKB()

# เพิ่มกฎและข้อเท็จจริงต่างๆ (ให้นักเรียนเติมเอง)
# movie_kb.tell(...)
# 1.ถ้าคนชอบ Action และชอบ Sci-Fi แล้วแนะนำหนัง "Matrix"
movie_kb.tell(expr("(ActionJohn & SciFiJohn) ==> MatrixJohn"))

# 2.ถ้าคนชอบ Comedy แล้วแนะนำหนัง "The Hangover"
movie_kb.tell(expr("ComedyMary ==> HangoverMary")) 
movie_kb.tell(expr("(ComedyTom & ~HorrorTom) ==> HangoverTom")) # Tom ใส่เงื่อนไข ~Horror เพื่อกัน conflict (กันไม่ให้กฎคอมเมดี้ยิง)

# 3.ถ้าคนชอบ Horror แล้วไม่แนะนำหนัง Comedy (ในที่นี้คือ The Hangover)
movie_kb.tell(expr("HorrorTom ==> ~HangoverTom"))

# ข้อเท็จจริง
# 4.จอห์นชอบ Action และ Sci-Fi
movie_kb.tell(ActionJohn)
movie_kb.tell(SciFiJohn)

# 5.แมรี่ชอบ Comedy
movie_kb.tell(ComedyMary)

# 6.ทอมชอบ Horror และ Comedy
movie_kb.tell(HorrorTom)
movie_kb.tell(ComedyTom)

# ทดสอบคำตอบ
# ใช้ tt_entails หรือ pl_resolution ในการทดสอบ
def check(kb, q):
    qe = expr(q) if isinstance(q, str) else q
    return {
        "tt_entails": tt_entails(kb.clauses, qe),
        "pl_resolution": pl_resolution(kb.clauses, qe)
    }

# print("John ควรดู Matrix หรือไม่:", movie_kb.ask_if_true(...))
print("... ผลการเเนะนำหนัง ...")
print(f"John ควรดู Matrix หรือไม่: {movie_kb.ask_if_true(MatrixJohn)}")
print(f"Mary ควรดู The Hangover หรือไม่: {movie_kb.ask_if_true(HangoverMary)}")
print(f"Tom ควรดู The Hangover หรือไม่: {movie_kb.ask_if_true(HangoverTom)}")
print(f"สรุปได้ว่า 'ไม่ควร' เเนะนำ The Hangover ให้ Tom หรือไม่: {movie_kb.ask_if_true(~HangoverTom)}")