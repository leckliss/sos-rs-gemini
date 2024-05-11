import telebot
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

bot.infinity_polling()