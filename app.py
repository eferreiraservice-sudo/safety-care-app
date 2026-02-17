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
def gerar_pdf(texto_laudo, nome_arquivo="laudo_tecnico.pdf"):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho Safety&Care
    pdf.set_font("Arial", 'B', 16)
    pdf.set_text_color(0, 51, 102) # Azul Marinho
    pdf.cell(0, 10, "Safety&Care - Inteligência em Segurança", ln=True, align='C')
    
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(100, 100, 100)
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pdf.cell(0, 10, f"Relatório Gerado em: {data_atual}", ln=True, align='C')
    pdf.ln(10)
    
    # Título do Laudo
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, "LAUDO TÉCNICO PRELIMINAR DE INSPEÇÃO", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Conteúdo (Texto da IA)
    pdf.set_font("Arial", size=11)
    # O multi_cell cuida das quebras de linha automáticas
    pdf.multi_cell(0, 8, texto_laudo.encode('latin-1', 'replace').decode('latin-1'))
    
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
    if "laudo" in st.session_state:
        st.markdown("---")
        st.markdown("### 📋 Relatório Gerado")
        st.write(st.session_state.laudo)
        
        # Botão de Download
        pdf_bytes = gerar_pdf(st.session_state.laudo)
        st.download_button(
            label="📥 Baixar Laudo em PDF",
            data=pdf_bytes,
            file_name=f"Laudo_SafetyCare_{datetime.now().strftime('%d%m%Y')}.pdf",
            mime="application/pdf"
        )