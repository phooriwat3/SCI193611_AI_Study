import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("สวัสดี! ลองตอบข้อความนี้ดูหน่อย")
print(response.text)
