import google.generativeai as genai
import os
from dotenv import load_dotenv

# 1. Carrega a chave
load_dotenv()
chave = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=chave)

print("🔍 CONSULTANDO O GOOGLE SOBRE MODELOS DISPONÍVEIS...")
print("-" * 40)

try:
    # 2. Pede a lista de todos os modelos
    for m in genai.list_models():
        # Filtra só os que servem para gerar texto (chat)
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ MODELO ENCONTRADO: {m.name}")
            
except Exception as e:
    print(f"❌ ERRO AO LISTAR: {e}")

print("-" * 40)