import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
from datetime import datetime
from duckduckgo_search import DDGS

# --- Configurações ---
TOKEN = os.environ['TELEGRAM_TOKEN']
GEMINI_KEY = os.environ['GEMINI_KEY']

# --- Integração Gemini ---
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- Função para buscar na web (DuckDuckGo) ---
def buscar_duckduckgo(query, max_resultados=5):
    resultados = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_resultados):
            resultados.append(f"{r['title']}\n{r['href']}\n{r['body']}")
    return "\n\n".join(resultados)

# --- Geração de resposta com Gemini ---
def gerar_resposta(user_input, contexto):
    try:
        web_contexto = buscar_duckduckgo(user_input)

        prompt = f"""Você é o assistente oficial da FURIA Esports (CS2). 
Contexto interno: {contexto}
Contexto da web: {web_contexto}

Regras:
- Seja preciso e empolgado
- Use emojis relevantes
- Responda em português (1-2 frases)
- Nunca invente informações
Pergunta: {user_input}"""

        response = model.generate_content(
            prompt,
            generation_config={"temperature": 0.7, "max_output_tokens": 150},
            safety_settings={
                'HARASSMENT': 'BLOCK_NONE',
                'HATE_SPEECH': 'BLOCK_NONE'
            }
        )
        return response.text
    except Exception as e:
        print(f"Erro Gemini: {str(e)}")
        return "Desculpe, não consegui processar sua solicitação."

# --- Dados Simulados da FURIA ---
def get_elenco_atual():
    return [
        "yuurih (Yuri Santos) - 🇧🇷 Brasil - Rifler",
        "KSCERATO (Kaike Cerato) - 🇧🇷 Brasil - Rifler",
        "FalleN (Capitão) (Gabriel Toledo) - 🇧🇷 Brasil - Rifler",
        "molodoy (Danil Golubenko) - 🇰🇿 Cazaquistão - AWPer",
        "YEKINDAR (Mareks Gaļinskis) - 🇱🇻 Letônia - Rifler",
        "sidde (Sid Macedo) - 🇧🇷 Brasil - Treinador",
        "Hepa (Juan Borges) - 🇪🇸 Espanha - Treinador Assistente"
    ]

def get_proximo_jogo():
    return {
        "data": "10/05/2025",
        "hora": "05:00",
        "adversario": "The MongolZ",
        "campeonato": "PGL Astana 2025"
    }

def get_ultimo_jogo():
    return {
        "data": "02/05/2025",
        "adversario": "The MongolZ",
        "resultado": "0-2"
    }

# --- Estatísticas de Jogadores ---
def get_estatisticas_jogador(jogador):
    estatisticas = {
        "FalleN": {"K/D": "1.20", "MVPs": 10},
        "molodoy": {"K/D": "1.05", "MVPs": 8},
        "YEKINDAR": {"K/D": "1.50", "MVPs": 12},
        "sidde": {"K/D": "1.10", "MVPs": 6},
        "Jogador 5": {"K/D": "1.15", "MVPs": 5}
    }
    if jogador in estatisticas:
        return f"{jogador}: K/D Ratio = {estatisticas[jogador]['K/D']}, MVPs = {estatisticas[jogador]['MVPs']}"
    else:
        return "Jogador não encontrado."

# --- Pergunta de Preferência de Jogo ---
async def perguntar_preferencia(update: Update, context: CallbackContext):
    resposta = "Qual jogo você acompanha mais? (CS:GO ou Valorant)"
    await update.message.reply_text(resposta)

def responder_com_base_na_preferencia(preferencia):
    if preferencia == "CS:GO":
        return "Aqui estão as últimas informações sobre CS:GO!"
    else:
        return "Aqui estão as últimas informações sobre Valorant!"


from telegram import InputMediaPhoto

def enviar_imagem(update, url_imagem):
    update.message.reply_photo(photo=url_imagem)

# --- Handler principal ---
async def handle_message(update: Update, context: CallbackContext):
    user_input = update.message.text.lower()

    elenco = get_elenco_atual()
    proximo_jogo = get_proximo_jogo()
    ultimo_jogo = get_ultimo_jogo()

    contexto = f"""
Elenco: {', '.join(elenco)}
Último jogo: {ultimo_jogo['resultado']} vs {ultimo_jogo['adversario']}
Próximo jogo: FURIA vs {proximo_jogo['adversario']} dia {proximo_jogo['data']} às {proximo_jogo['hora']} ({proximo_jogo['campeonato']})
"""

    if "elenco" in user_input or "jogadores" in user_input:
        resposta = "👥 Elenco Atual:\n" + "\n".join(elenco)

    elif "próximo jogo" in user_input or "quando joga" in user_input:
        resposta = (f"⚔️ Próximo jogo: FURIA vs {proximo_jogo['adversario']}\n"
                    f"📅 {proximo_jogo['data']} às {proximo_jogo['hora']}\n"
                    f"🏆 {proximo_jogo['campeonato']}")

    elif "último jogo" in user_input or "resultado" in user_input:
        resposta = (f"⏮️ Último jogo: FURIA {ultimo_jogo['resultado']} "
                    f"{ultimo_jogo['adversario']} ({ultimo_jogo['data']})")

    elif "contato" in user_input:
        resposta = "📩 Contato oficial:\n- Site: https://furia.gg\n- Email: contato@furia.gg"

    elif "notícias" in user_input or "últimas notícias" in user_input:
       
        resposta = buscar_duckduckgo("últimas notícias FURIA Esports")

    elif "estatísticas" in user_input or "k/d" in user_input:
        jogador = "FalleN"  
        resposta = get_estatisticas_jogador(jogador)

    elif "preferência" in user_input:
        await perguntar_preferencia(update, context)
        return  

    elif "imagem" in user_input or "vídeo" in user_input:
        enviar_imagem(update, "URL_DO_GIF_AQUI")
        resposta = "Aqui está uma imagem épica da FURIA!"

    else:
        
        resposta = gerar_resposta(user_input, contexto)

    await update.message.reply_text(resposta)

# --- Inicialização ---
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot FURIA Pro Ativado com DuckDuckGo + Gemini!")
    application.run_polling()

if __name__ == "__main__":
    main()
