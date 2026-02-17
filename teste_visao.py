import os
import PIL.Image
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Carrega a chave
load_dotenv()
chave = os.getenv("GOOGLE_API_KEY")

if not chave:
    print("❌ ERRO: Chave não encontrada no .env")
    exit()

genai.configure(api_key=chave)

# 2. O TRUQUE DE ENGENHEIRO (Arruma o GPS)
# Pega o endereço exato onde este script está salvo no computador
pasta_do_script = os.path.dirname(os.path.abspath(__file__))

# Monta o caminho completo da imagem (Script + Nome do Arquivo)
# ATENÇÃO: Se sua foto se chama 'maquina.jfif', deixe assim.
caminho_imagem = os.path.join(pasta_do_script, 'maquina.jfif')

print(f"📂 Procurando imagem em: {caminho_imagem}")

try:
    img = PIL.Image.open(caminho_imagem)
    print("✅ Imagem carregada com sucesso!")
except FileNotFoundError:
    print("\n❌ ERRO FATAL: O Python foi até a pasta certa, mas não achou o arquivo.")
    print("👉 Verifique se o nome é 'maquina.jfif' ou 'maquina.jpg' e renomeie o código na linha 22.")
    exit()

# 3. Prepara o modelo 
model = genai.GenerativeModel('gemini-2.5-flash')

# 4. O Prompt 
prompt = """
Você é um Perito em Engenharia de Segurança.
Analise esta imagem.
1. Liste os riscos iminentes.
2. Cite a NR violada.
Seja breve.
"""

print("🔍 IA Analisando... aguarde...")
response = model.generate_content([prompt, img])

print("\n📋 LAUDO TÉCNICO:")
print("-" * 40)
print(response.text)
print("-" * 40)