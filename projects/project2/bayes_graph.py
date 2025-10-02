import matplotlib
matplotlib.use('Agg')
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import glob # Library สำหรับค้นหาไฟล์

# --- 1. โหลดและรวมข้อมูล ---
# ระบุโฟลเดอร์ที่เก็บไฟล์ CSV
results_dir = "results"
# ค้นหาไฟล์ CSV ทั้งหมดในโฟลเดอร์
csv_files = glob.glob(os.path.join(results_dir, "*.csv"))

# อ่านและรวมไฟล์ทั้งหมดเป็น DataFrame เดียว
df_list = []
for f in csv_files:
    df_list.append(pd.read_csv(f))

# รวม DataFrame ทั้งหมด
df = pd.concat(df_list, ignore_index=True)

# (แนะนำ) สร้างคอลัมน์ใหม่สำหรับใช้เป็น 'hue' เพื่อให้ legend อ่านง่ายขึ้น
df['condition'] = "ghost=" + df['ghost_type'] + ", var=" + df['sensor_var'].astype(str)

print("ข้อมูลตัวอย่าง:")
print(df.head())
print(f"\nโหลดข้อมูลทั้งหมด {len(df)} แถว จาก {len(csv_files)} ไฟล์")

# --- 2. สร้างกราฟ ---
# กำหนดสไตล์ของกราฟ
sns.set_theme(style="whitegrid")

# รายการของ Metrics ที่เราต้องการจะพล็อต
metrics_to_plot = {
    'expected_L1': 'Expected L1 Error (Lower is Better)',
    'pat': 'Probability at Truth (Higher is Better)',
    'entropy': 'Belief State Entropy (Lower is Better)'
}

# วนลูปเพื่อสร้างกราฟสำหรับแต่ละ Metric
for metric_col, title in metrics_to_plot.items():
    plt.figure(figsize=(12, 7)) # สร้าง Figure ใหม่สำหรับแต่ละกราฟ

    # ใช้ seaborn.lineplot เพื่อสร้างกราฟเส้น
    # - x: แกน X คือเวลา (t)
    # - y: แกน Y คือ Metric ที่เราสนใจ
    # - hue: แยกสีของเส้นตามเงื่อนไขการทดลอง (condition)
    # - ci='sd': ให้แถบ Error Bar แสดงค่าเบี่ยงเบนมาตรฐาน (Standard Deviation)
    # - estimator='mean': เส้นกราฟคือค่าเฉลี่ยของทุก runid ณ เวลานั้นๆ
    ax = sns.lineplot(
        data=df,
        x='t',
        y=metric_col,
        hue='condition', # ใช้คอลัมน์ที่สร้างขึ้นมาใหม่
        style='ghost_type', # อาจจะใช้ style ช่วยแยกเส้น 'scared' vs 'confused'
        errorbar='sd' # แสดง standard deviation เป็น error band
    )

    # --- 3. ตกแต่งกราฟ ---
    ax.set_title(title, fontsize=16)
    ax.set_xlabel("Time Step (t)", fontsize=12)
    ax.set_ylabel(metric_col, fontsize=12)
    plt.legend(title='Experiment Condition')
    plt.tight_layout() # จัด layout ให้สวยงาม

    # --- 4. บันทึกและแสดงผล ---
    output_filename = f"plot_{metric_col}.png"
    plt.savefig(output_filename)
    print(f"บันทึกกราฟ '{output_filename}' เรียบร้อยแล้ว")
    
    plt.show() # แสดงกราฟขึ้นมา