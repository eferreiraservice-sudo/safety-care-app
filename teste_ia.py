import os
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Carrega a chave do cofre (.env)
load_dotenv()
chave = os.getenv("GOOGLE_API_KEY")

if not chave:
    print("ERRO: Não achei a chave no arquivo .env!")
else:
    print("Chave encontrada! Conectando...")

    # 2. Configura a IA
    genai.configure(api_key=chave)

    # 3. Chama o modelo (Gemini 1.5 Flash - Rápido e Barato)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # 4. Pergunta de Engenharia
    print("Perguntando para a IA sobre NR-12...")
    response = model.generate_content("Resuma em 1 frase o objetivo principal da NR-12 para um leigo.")

    # 5. Mostra a resposta
    print("\nRESPOSTA DA IA:")
    print("-" * 30)
    print(response.text)
    print("-" * 30)