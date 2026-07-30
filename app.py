import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="Trilha Matemática - Função Afim", page_icon="🎲", layout="centered")

TAMANHO_TRILHA = 20
CASAS_SORTE = [3, 8, 14]
CASAS_AZAR = [5, 11, 17]
CASAS_BONUS = [7, 13]

# Inicialização do Estado do Jogo
if "jogo_iniciado" not in st.session_state:
    st.session_state.jogo_iniciado = False
    st.session_state.posicoes = [0, 0]
    st.session_state.turno = 0
    st.session_state.nomes = ["Jogador 1", "Jogador 2"]
    st.session_state.desafio_atual = None
    st.session_state.mensagem = ""
    st.session_state.fase = "pergunta"

def gerar_desafio():
    tipo = random.choice(["valor_funcao", "coeficiente_a", "zero_funcao", "interpretacao_crescente"])
    a = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
    b = random.randint(-10, 10)
    sinal_b = f"+ {b}" if b >= 0 else f"- {abs(b)}"

    if tipo == "valor_funcao":
        x = random.randint(-5, 5)
        resp = a * x + b
        perg = f"Dada a função $f(x) = {a}x {sinal_b}$, qual é o valor de $f({x})$?"
        exp = f"Calculando: $f({x}) = {a} \\cdot ({x}) {sinal_b} = {resp}$"
    elif tipo == "zero_funcao":
        x_exato = random.randint(-5, 5)
        a = random.choice([-3, -2, -1, 1, 2, 3])
        b = -a * x_exato
        sinal_b = f"+ {b}" if b >= 0 else f"- {abs(b)}"
        resp = x_exato
        perg = f"Qual é a raiz (zero da função) de $f(x) = {a}x {sinal_b}$?"
        exp = f"Para $f(x) = 0$: ${a}x {sinal_b} = 0 \\implies x = {resp}$"
    elif tipo == "coeficiente_a":
        resp = a
        perg = f"Na função $f(x) = {a}x {sinal_b}$, qual é o coeficiente angular ($a$)?"
        exp = f"O coeficiente angular é o número que acompanha $x$, portanto $a = {a}$."
    else:
        resp = "crescente" if a > 0 else "decrescente"
        perg = f"A função $f(x) = {a}x {sinal_b}$ é 'crescente' ou 'decrescente'?"
        exp = f"Como $a = {a}$ ({'a > 0' if a > 0 else 'a < 0'}), a função é {resp}."

    return {"pergunta": perg, "resposta": str(resp).lower().strip(), "explicacao": exp}

st.title("🎲 Trilha Matemática: Função Afim")

if not st.session_state.jogo_iniciado:
    st.subheader("Configuração da Partida")
    nome1 = st.text_input("Nome do Jogador 1 (Verde)", value="Jogador 1")
    nome2 = st.text_input("Nome do Jogador 2 (Amarelo)", value="Jogador 2")
    
    if st.button("🚀 Iniciar Jogo"):
        st.session_state.nomes = [nome1, nome2]
        st.session_state.jogo_iniciado = True
        st.session_state.desafio_atual = gerar_desafio()
        st.rerun()

else:
    jogador_atual_idx = st.session_state.turno % 2
    nome_atual = st.session_state.nomes[jogador_atual_idx]

    st.write("### 📌 Tabuleiro")
    tabuleiro_vis = ""
    for i in range(TAMANHO_TRILHA + 1):
        p1 = "🟢" if st.session_state.posicoes[0] == i else ""
        p2 = "🟡" if st.session_state.posicoes[1] == i else ""
        
        if p1 or p2:
            tabuleiro_vis += f"|{p1}{p2}| "
        elif i in CASAS_SORTE:
            tabuleiro_vis += "[🍀] "
        elif i in CASAS_AZAR:
            tabuleiro_vis += "[💥] "
        elif i in CASAS_BONUS:
            tabuleiro_vis += "[⭐] "
        else:
            tabuleiro_vis += f"[{i}] "
            
    st.info(tabuleiro_vis)
    st.caption("Legenda: 🟢 P1 | 🟡 P2 | 🍀 Sorte (+1) | 💥 Azar (-2) | ⭐ Bônus")
    
    st.write(f"**Posição atual:** {st.session_state.nomes[0]}: Casa {st.session_state.posicoes[0]} | {st.session_state.nomes[1]}: Casa {st.session_state.posicoes[1]}")
    st.divider()

    if max(st.session_state.posicoes) >= TAMANHO_TRILHA:
        vencedor_idx = st.session_state.posicoes.index(max(st.session_state.posicoes))
        st.balloons()
        st.success(f"🎉 PARABÉNS! **{st.session_state.nomes[vencedor_idx]}** VENCEU O JOGO!")
        if st.button("🔄 Jogar Novamente"):
            st.session_state.jogo_iniciado = False
            st.session_state.posicoes = [0, 0]
            st.session_state.turno = 0
            st.rerun()
    else:
        cor_jogador = "🟢" if jogador_atual_idx == 0 else "🟡"
        st.subheader(f"Vez de {cor_jogador} **{nome_atual}**")

        if st.session_state.fase == "pergunta":
            desafio = st.session_state.desafio_atual
            st.write(f"**Desafio:** {desafio['pergunta']}")
            
            resposta_user = st.text_input("Sua resposta:", key="input_resposta")
            
            if st.button("Enviar Resposta"):
                res_limpa = resposta_user.strip().lower()
                if res_limpa == desafio['resposta']:
                    dado = random.randint(1, 3)
                    nova_pos = st.session_state.posicoes[jogador_atual_idx] + dado
                    
                    msg = f"✅ **Correto!** {desafio['explicacao']}\n\n🎲 Você tirou **{dado}** no dado!"
                    
                    if nova_pos in CASAS_SORTE:
                        nova_pos += 1
                        msg += "\n\n🍀 **CASA SORTE!** Avança mais +1 casa!"
                    elif nova_pos in CASAS_AZAR:
                        nova_pos -= 2
                        msg += "\n\n💥 **CASA AZAR!** Recua -2 casas!"
                        
                    st.session_state.posicoes[jogador_atual_idx] = max(0, min(nova_pos, TAMANHO_TRILHA))
                    st.session_state.mensagem = ("sucesso", msg)
                else:
                    msg = f"❌ **Incorreto!** A resposta era **{desafio['resposta']}**.\n\n*Explicação:* {desafio['explicacao']}"
                    st.session_state.mensagem = ("erro", msg)
                
                st.session_state.fase = "resultado"
                st.rerun()

        elif st.session_state.fase == "resultado":
            tipo_msg, texto = st.session_state.mensagem
            if tipo_msg == "sucesso":
                st.success(texto)
            else:
                st.error(texto)

            if st.button("Próxima Jogada ➡️"):
                st.session_state.turno += 1
                st.session_state.desafio_atual = gerar_desafio()
                st.session_state.fase = "pergunta"
                st.rerun()