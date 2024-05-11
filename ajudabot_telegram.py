import telebot
import requests
import json
import google.generativeai as genai

bot = telebot.TeleBot("", parse_mode=None)

GOOGLE_API_KEY = ""
genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

generation_config = {
    "candidate_count": 1,
    "temperature": 0.5,
}

safety_settings = {
    "HARASSMENT": "BLOCK_NONE",
    "HATE": "BLOCK_NONE",
    "SEXUAL": "BLOCK_NONE",
    "DANGEROUS": "BLOCK_NONE",
}

model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config,
                               safety_settings=safety_settings)

chat = model.start_chat(history=[])

@bot.message_handler(func=lambda m: True)
def respond_with_gemini(message):
    prompt = message.text
    response = chat.send_message(prompt)
    bot.reply_to(message, response.text)

def get_entidades():
    """
    Obtém a lista de entidades do endpoint da API de doações.

    Retorna:
        Lista de dicionários contendo as informações das entidades.
    """
    response = requests.get(API_DOACOES_URL)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        print(f"Erro ao obter entidades: {response.status_code}")
        return []

def enviar_opcoes(mensagem):
    """
    Envia mensagem ao usuário com as opções disponíveis.

    Args:
        mensagem: Objeto Message do Telebot.
    """
    opcoes = [
        "1. Preciso de ajuda",
        "2. Doar",
        "3. Últimas notícias",
        "4. Pontos de doações"
    ]
    texto_opcoes = "\n".join(opcoes)
    bot.reply_to(mensagem, texto_opcoes)

def processar_escolha(mensagem):
    """
    Processa a escolha do usuário e direciona para a funcionalidade correspondente.

    Args:
        mensagem: Objeto Message do Telebot.
    """
    texto_escolha = mensagem.text
    if texto_escolha == "1. Preciso de ajuda":
        # Implementar funcionalidade de solicitação de ajuda
        pass
    elif texto_escolha == "2. Doar":
        mostrar_entidades(mensagem)
    elif texto_escolha == "3. Últimas notícias":
        # Implementar funcionalidade de notícias
        pass
    elif texto_escolha == "4. Pontos de doações":
        # Implementar funcionalidade de pontos de doação
        pass
    else:
        bot.reply_to(mensagem, "Opção inválida. Tente novamente.")

def mostrar_entidades(mensagem):
    """
    Mostra ao usuário a lista de entidades com opções para doação.

    Args:
        mensagem: Objeto Message do Telebot.
    """
    entidades = get_entidades()
    if entidades:
        texto_entidades = "\n".join(f"{i+1}. {entidade['nome']}" for i, entidade in enumerate(entidades))
        bot.reply_to(mensagem, texto_entidades)
        bot.send_message(mensagem.chat.id, "Digite o número da entidade para doar:")
    else:
        bot.reply_to(mensagem, "Ainda não há entidades cadastradas.")

def processar_escolha_entidade(mensagem):
    """
    Processa a escolha da entidade pelo usuário e mostra as informações de doação.

    Args:
        mensagem: Objeto Message do Telebot.
    """
    try:
        numero_entidade = int(mensagem.text) - 1
        entidades = get_entidades()
        entidade_escolhida = entidades[numero_entidade]
        if entidade_escolhida:
            texto_doacao = f"**Doar para {entidade_escolhida['nome']}**\n"
            texto_doacao += f"QR Code Pix: {entidade_escolhida['qr_code_pix']}\n"
            texto_doacao += f"Pix Copia e Cola: {entidade_escolhida['pix_copia_cola']}\n"
            bot.reply_to(mensagem, texto_doacao)
        else:
            bot.reply_to(mensagem, "Entidade inválida. Tente novamente.")
    except ValueError:  # Corrected exception name
        bot.reply_to(mensagem, "Entidade inválida. Tente novamente.")
