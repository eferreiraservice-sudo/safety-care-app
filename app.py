import streamlit as st
import os
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Safety&Care AI", page_icon="🛡️")

# --- CARREGA CHAVE ---
load_dotenv()
chave = os.getenv("GOOGLE_API_KEY")

# --- FUNÇÃO PARA GERAR PDF ---
def gerar_pdf(texto_laudo, imagem_pil):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho Safety&Care
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, "Safety&Care - Inteligência em Segurança", ln=True, align='C')
    pdf.ln(5)

    # Inserir a Foto (Salvando uma cópia temporária para o PDF ler)
    temp_path = "temp_evidencia.png"
    imagem_pil.save(temp_path)
    # x=55 centraliza a imagem no A4
    pdf.image(temp_path, x=55, w=100) 
    pdf.ln(10)

    # Conteúdo do Laudo
    pdf.set_font("Arial", size=11)
    pdf.set_text_color(0, 0, 0)
    # Limpa caracteres especiais para não dar erro no PDF
    texto_limpo = texto_laudo.encode('latin-1', 'ignore').decode('latin-1')
    pdf.multi_cell(0, 8, texto_limpo)
    
    return bytes(pdf.output())

# --- INTERFACE ---
st.title("🛡️ Safety&Care AI")
st.subheader("Sistema de Auditoria de NRs")

arquivo = st.file_uploader("Suba a foto para análise", type=['jpg', 'jpeg', 'png', 'jfif'])

if arquivo:
    img = Image.open(arquivo)
    st.image(img, use_container_width=True)
    
    if st.button("🚀 EXECUTAR AUDITORIA"):
        try:
            with st.spinner("Analisando..."):
                genai.configure(api_key=chave)
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = "Aja como engenheiro de segurança. Analise os riscos desta foto e cite as NRs violadas de forma estruturada."
                response = model.generate_content([prompt, img])
                
                # Guarda o resultado na "memória" da página (session_state)
                st.session_state.laudo = response.text
                st.success("Análise Concluída!")

        except Exception as e:
            st.error(f"Erro: {e}")

    # Se o laudo já existe, mostra o botão de PDF
    # Verificamos se já existe um laudo gerado na memória do site
if "laudo" in st.session_state:
    st.markdown("---")
    st.subheader("📄 Relatório Técnico")
    st.write(st.session_state.laudo)

    # BOTÃO ATUALIZADO: Ele gera o PDF usando o texto E a imagem
    if st.button("Gerar PDF do Laudo"):
        # Aqui passamos o texto (session_state.laudo) e a foto (img)
        pdf_bytes = gerar_pdf(st.session_state.laudo, img)
        
        st.download_button(
            label="📥 Baixar Laudo com Evidência",
            data=pdf_bytes,
            file_name="laudo_safety_care.pdf",
            mime="application/pdf"
        
        )