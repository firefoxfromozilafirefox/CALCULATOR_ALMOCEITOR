import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuração da página
st.set_page_config(page_title="Racha Conta Restaurante", page_icon="🍴")



# 1. Base de Dados do Cardápio
cardapio = {
    "Entradas": {"Proteinas": 31.0, "Baião Grande": 30.0, "Salada Caesar": 28.0},
    "Pratos Principais": {"Risoto de Cogumelos": 55.0, "Filé com Fritas": 65.0, "Pasta Carbonara": 48.0},
    "Bebidas": {"Suco Natural": 12.0, "Refrigerante": 8.0, "Cerveja Artesanal": 18.0},
    "Sobremesas": {"Pudim": 15.0, "Brownie com Sorvete": 22.0}
}

st.title("🍴 PicNic Calculator")

# 2. Seleção de Itens
st.header("1. Escolha os itens do cardápio")
itens_selecionados = []

cols = st.columns(2)
for i, (categoria, produtos) in enumerate(cardapio.items()):
    with cols[i % 2]:
        st.subheader(categoria)
        for produto, preco in produtos.items():
            if st.checkbox(f"{produto} - R$ {preco:.2f}", key=produto):
                itens_selecionados.append({"nome": produto, "preco": preco})

st.divider()

# 3. Resumo e Rateio
if itens_selecionados:
    st.header("2. Resumo do Pedido")
    total_conta = sum(item["preco"] for item in itens_selecionados)
    
    for item in itens_selecionados:
        st.write(f"✅ {item['nome']}: R$ {item['preco']:.2f}")
    
    st.info(f"**Total da Conta: R$ {total_conta:.2f}**")

    st.header("3. Divisão")
    num_pessoas = st.number_input("Dividir por quantas pessoas?", min_value=1, value=2, step=1)
    
    valor_por_pessoa = total_conta / num_pessoas
    
    st.success(f"💰 **Valor por pessoa: R$ {valor_por_pessoa:.2f}**")

    st.divider()

    # 4. Pagamento (O Homi)
    st.header("4. Pagamento para o Homi")
    chave_pix = st.text_input("Insira sua Chave PIX (E-mail, CPF ou Celular):")
    nome_titular = st.text_input("Nome do Titular da conta:")

    if chave_pix:
        st.warning(f"Atenção pessoal! Paguem **R$ {valor_por_pessoa:.2f}** para:")
        st.code(f"Chave PIX: {chave_pix}\nTitular: {nome_titular}", language="text")
        st.caption("Dica: Copie a chave acima para o seu app do banco.")
else:
    st.info("Selecione itens do cardápio para começar o cálculo.")

destinatario = st.text_input("E-mail do destinatário para enviar a cobrança:")

def enviar_email(destinatario, valor, chave, titular):
    # Configurações do Servidor (Exemplo Gmail)
    meu_email = "adiel.silva@unimedfortaleza.com.br"
    minha_senha = "uwjz rxab kkem zjbw" 

    # Estrutura da Mensagem
    msg = MIMEMultipart()
    msg['From'] = meu_email
    msg['To'] = destinatario
    msg['Subject'] = f"Conta do Restaurante - R$ {valor:.2f}"

    corpo = f"""
    Olá! Aqui estão os dados para o pagamento da conta:
    
    💰 Valor devido: R$ {valor:.2f}
    🔑 Chave PIX: {chave}
    👤 Titular: {titular}
    
    Obrigado!
    """
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(meu_email, minha_senha)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Erro ao enviar: {e}")
        return False

# --- Interface Streamlit (abaixo do que já tínhamos) ---
st.divider()
st.header("📩 Enviar Cobrança por E-mail")

with st.form("form_email"):
    emails_input = st.text_area("Digite os e-mails (separados por vírgula):")
    botao_enviar = st.form_submit_button("Enviar para todos")

    if botao_enviar:
        if not chave_pix or not emails_input:
            st.warning("Preencha a chave PIX e os e-mails primeiro!")
        else:
            lista_emails = [e.strip() for e in emails_input.split(",")]
            sucesso_total = True
            
            for email in lista_emails:
                if enviar_email(email, valor_por_pessoa, chave_pix, nome_titular):
                    st.toast(f"E-mail enviado para {email}!")
                else:
                    sucesso_total = False
            
            if sucesso_total:
                st.success("🎉 Todos os e-mails foram enviados com sucesso!")