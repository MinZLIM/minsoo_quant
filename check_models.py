# check_models.py
import google.generativeai as genai
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)

print("사용 가능한 모델 목록:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)