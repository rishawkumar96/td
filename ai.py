import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Set up API keys
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token"
OPENAI_API_KEY = "your_openai_api_key"
openai.api_key = OPENAI_API_KEY

async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}]
    )
    reply = response["choices"][0]["message"]["content"]
    await update.message.reply_text(reply)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I'm an AI bot. Ask me anything!")

app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
